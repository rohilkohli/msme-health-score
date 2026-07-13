import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from sqlalchemy.orm import Session

from models.database import (
    MSME,
    DataSourceConnection,
    IngestionRun,
    RawPayload,
    NormalizedFact,
    FeatureSnapshot,
    QualityIssue,
    GSTFiling,
    UPITransaction,
    EPFOContribution,
    BankStatement,
    GSTFilingFact,
    UPITxnFact,
    AABankStatementFact,
    EPFOContributionFact,
)


class IngestionPipelineService:
    """Ingestion pipeline for consented GST/UPI/AA/EPFO data."""

    def __init__(self, db: Session):
        self.db = db

    def run_ingestion(
        self,
        msme_id: int,
        source: str,
        window_start: Optional[datetime] = None,
        window_end: Optional[datetime] = None,
        trigger_type: str = "manual",
    ) -> IngestionRun:
        msme = self.db.query(MSME).filter(MSME.id == msme_id).first()
        if not msme:
            raise ValueError("MSME not found")

        source_name = self._normalize_source(source)
        connection = (
            self.db.query(DataSourceConnection)
            .filter(
                DataSourceConnection.msme_id == msme_id,
                DataSourceConnection.source_type == source_name,
            )
            .first()
        )
        if not connection:
            raise ValueError(f"Data source connection missing for {source_name}")
        if connection.consent_expires_at and connection.consent_expires_at < datetime.utcnow():
            raise ValueError(f"Consent expired for {source_name}")

        run = IngestionRun(
            source=source_name,
            msme_id=msme_id,
            data_source_connection_id=connection.id,
            status="fetching",
            window_start=window_start,
            window_end=window_end,
            run_version=self._next_run_version(msme_id, source_name),
            records_received=0,
            records_valid=0,
            started_at=datetime.utcnow(),
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        try:
            records = self._extract_records(msme_id, source_name, window_start, window_end)
            run.records_received = len(records)

            valid_records: List[Tuple[str, Dict[str, Any]]] = []
            issues_count = 0

            for source_record_id, record in records:
                self._store_raw_payload(run.id, msme_id, source_name, source_record_id, record)
                issues = self._validate_record(source_name, source_record_id, record)
                if issues:
                    issues_count += len(issues)
                    for issue in issues:
                        self.db.add(issue)
                    continue
                valid_records.append((source_record_id, record))

            for source_record_id, record in valid_records:
                self._normalize_record(run.id, msme_id, source_name, source_record_id, record)

            run.records_valid = len(valid_records)
            coverage, recency, reliability = self._compute_quality_metrics(
                source_name,
                valid_records,
                issues_count,
            )
            run.coverage_score = coverage
            run.recency_score = recency
            run.reliability_score = reliability
            run.status = "completed"
            run.finished_at = datetime.utcnow()

            snapshot = self._build_feature_snapshot(run)
            self.db.add(snapshot)

            connection.status = "completed"
            connection.last_fetched_at = datetime.utcnow()
            connection.last_sync_at = datetime.utcnow()
            self.db.commit()
        except Exception as exc:  # noqa: BLE001
            run.status = "failed"
            run.error_summary = str(exc)
            run.finished_at = datetime.utcnow()
            connection.status = "failed"
            self.db.commit()
            raise

        self.db.refresh(run)
        return run

    def _next_run_version(self, msme_id: int, source: str) -> int:
        last = (
            self.db.query(IngestionRun)
            .filter(IngestionRun.msme_id == msme_id, IngestionRun.source == source)
            .order_by(IngestionRun.id.desc())
            .first()
        )
        return (last.run_version if last else 0) + 1

    def _normalize_source(self, source: str) -> str:
        source_value = (source or "").strip().lower()
        mapping = {
            "gst": "GST",
            "upi": "UPI",
            "epfo": "EPFO",
            "aa": "Account Aggregator",
            "account_aggregator": "Account Aggregator",
            "account aggregator": "Account Aggregator",
        }
        normalized = mapping.get(source_value)
        if not normalized:
            raise ValueError("Unsupported source")
        return normalized

    def _extract_records(
        self,
        msme_id: int,
        source: str,
        window_start: Optional[datetime],
        window_end: Optional[datetime],
    ) -> List[Tuple[str, Dict[str, Any]]]:
        window_end = window_end or datetime.utcnow()

        if source == "GST":
            query = self.db.query(GSTFiling).filter(GSTFiling.msme_id == msme_id)
            if window_start:
                query = query.filter(GSTFiling.filing_date >= window_start)
            query = query.filter(GSTFiling.filing_date <= window_end)
            filings = query.all()
            return [
                (
                    f"GST-{msme_id}-{filing.filing_period}-{filing.return_type}-{filing.id}",
                    {
                        "filing_period": filing.filing_period,
                        "filing_date": filing.filing_date.isoformat() if filing.filing_date else None,
                        "due_date": filing.due_date.isoformat() if filing.due_date else None,
                        "return_type": filing.return_type,
                        "taxable_turnover": filing.taxable_turnover,
                        "tax_paid": filing.tax_paid,
                        "itc_claimed": filing.itc_claimed,
                        "is_on_time": filing.is_on_time,
                    },
                )
                for filing in filings
            ]

        if source == "UPI":
            query = self.db.query(UPITransaction).filter(UPITransaction.msme_id == msme_id)
            if window_start:
                query = query.filter(UPITransaction.transaction_date >= window_start)
            query = query.filter(UPITransaction.transaction_date <= window_end)
            txns = query.all()
            return [
                (
                    txn.reference_id or f"UPI-{msme_id}-{txn.id}",
                    {
                        "transaction_time": txn.transaction_date.isoformat(),
                        "amount": txn.amount,
                        "direction": "CREDIT" if txn.is_credit else "DEBIT",
                        "counterparty_vpa": txn.counterparty_vpa,
                        "merchant_category": txn.category,
                        "reference_id": txn.reference_id,
                        "is_success": True,
                    },
                )
                for txn in txns
            ]

        if source == "EPFO":
            query = self.db.query(EPFOContribution).filter(EPFOContribution.msme_id == msme_id)
            if window_start:
                query = query.filter(EPFOContribution.payment_date >= window_start)
            query = query.filter(EPFOContribution.payment_date <= window_end)
            contributions = query.all()
            return [
                (
                    c.challan_number or f"EPFO-{msme_id}-{c.id}",
                    {
                        "contribution_month": c.contribution_month,
                        "due_date": c.due_date.isoformat() if c.due_date else None,
                        "payment_date": c.payment_date.isoformat() if c.payment_date else None,
                        "employee_contribution": c.employee_contribution,
                        "employer_contribution": c.employer_contribution,
                        "total_contribution": c.total_contribution,
                        "employee_count": c.num_employees,
                        "is_on_time": c.is_on_time,
                        "challan_id": c.challan_number,
                    },
                )
                for c in contributions
            ]

        query = self.db.query(BankStatement).filter(BankStatement.msme_id == msme_id)
        if window_start:
            query = query.filter(BankStatement.month >= window_start.strftime("%Y-%m"))
        query = query.filter(BankStatement.month <= window_end.strftime("%Y-%m"))
        statements = query.all()
        return [
            (
                f"AA-{msme_id}-{s.month}-{s.id}",
                {
                    "month": s.month,
                    "opening_balance": s.opening_balance,
                    "closing_balance": s.closing_balance,
                    "total_credits": s.total_credits,
                    "total_debits": s.total_debits,
                    "num_credit_transactions": s.num_credit_transactions,
                    "num_debit_transactions": s.num_debit_transactions,
                    "avg_daily_balance": s.avg_daily_balance,
                    "min_balance": s.min_balance,
                    "max_balance": s.max_balance,
                    "emi_outflows": s.emi_outflows,
                    "salary_outflows": s.salary_outflows,
                    "tax_outflows": s.tax_outflows,
                },
            )
            for s in statements
        ]

    def _store_raw_payload(
        self,
        run_id: int,
        msme_id: int,
        source: str,
        source_record_id: str,
        payload: Dict[str, Any],
    ) -> None:
        payload_json = json.dumps(payload, sort_keys=True, default=str)
        checksum = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()

        existing = (
            self.db.query(RawPayload)
            .filter(
                RawPayload.msme_id == msme_id,
                RawPayload.source == source,
                RawPayload.source_record_id == source_record_id,
            )
            .first()
        )
        if existing:
            return

        self.db.add(
            RawPayload(
                ingestion_run_id=run_id,
                msme_id=msme_id,
                source=source,
                source_record_id=source_record_id,
                payload_json=payload_json,
                checksum=checksum,
                received_at=datetime.utcnow(),
            )
        )

    def _validate_record(
        self,
        source: str,
        source_record_id: str,
        record: Dict[str, Any],
    ) -> List[QualityIssue]:
        required_fields = {
            "GST": ["filing_period", "return_type"],
            "UPI": ["transaction_time", "amount", "direction"],
            "EPFO": ["contribution_month", "challan_id"],
            "Account Aggregator": ["month"],
        }

        issues: List[QualityIssue] = []
        for field in required_fields.get(source, []):
            if record.get(field) in (None, ""):
                issues.append(
                    QualityIssue(
                        msme_id=record.get("msme_id") or 0,
                        source=source,
                        source_record_id=source_record_id,
                        issue_type="mandatory_field_missing",
                        severity="high",
                        field_name=field,
                        message=f"Missing required field: {field}",
                    )
                )

        if source == "UPI" and record.get("direction") not in {"CREDIT", "DEBIT"}:
            issues.append(
                QualityIssue(
                    msme_id=record.get("msme_id") or 0,
                    source=source,
                    source_record_id=source_record_id,
                    issue_type="enum_validation_failed",
                    severity="medium",
                    field_name="direction",
                    message="UPI direction must be CREDIT or DEBIT",
                )
            )

        return issues

    def _normalize_record(
        self,
        run_id: int,
        msme_id: int,
        source: str,
        source_record_id: str,
        record: Dict[str, Any],
    ) -> None:
        event_time = self._event_time_for_source(source, record)

        self._upsert_normalized_fact(
            run_id=run_id,
            msme_id=msme_id,
            source=source,
            source_record_id=source_record_id,
            event_time=event_time,
            amount=self._amount_for_source(source, record),
            direction=self._direction_for_source(source, record),
            counterparty_id=self._counterparty_for_source(source, record),
            compliance_flag=self._compliance_for_source(source, record),
            metadata_json=json.dumps(record, sort_keys=True, default=str),
        )

        if source == "GST":
            self._upsert_gst_fact(run_id, msme_id, source_record_id, record)
        elif source == "UPI":
            self._upsert_upi_fact(run_id, msme_id, source_record_id, record)
        elif source == "EPFO":
            self._upsert_epfo_fact(run_id, msme_id, source_record_id, record)
        else:
            self._upsert_aa_fact(run_id, msme_id, source_record_id, record)

    def _upsert_normalized_fact(
        self,
        run_id: int,
        msme_id: int,
        source: str,
        source_record_id: str,
        event_time: datetime,
        amount: Optional[float],
        direction: Optional[str],
        counterparty_id: Optional[str],
        compliance_flag: Optional[bool],
        metadata_json: str,
    ) -> None:
        existing = (
            self.db.query(NormalizedFact)
            .filter(
                NormalizedFact.msme_id == msme_id,
                NormalizedFact.source == source,
                NormalizedFact.source_record_id == source_record_id,
            )
            .first()
        )
        if existing:
            if event_time and existing.event_time and event_time < existing.event_time:
                return
            existing.ingestion_run_id = run_id
            existing.event_time = event_time
            existing.amount = amount
            existing.direction = direction
            existing.counterparty_id = counterparty_id
            existing.compliance_flag = compliance_flag
            existing.metadata_json = metadata_json
            return

        self.db.add(
            NormalizedFact(
                ingestion_run_id=run_id,
                msme_id=msme_id,
                source=source,
                source_record_id=source_record_id,
                event_time=event_time,
                amount=amount,
                direction=direction,
                counterparty_id=counterparty_id,
                compliance_flag=compliance_flag,
                metadata_json=metadata_json,
            )
        )

    def _upsert_gst_fact(self, run_id: int, msme_id: int, source_record_id: str, record: Dict[str, Any]) -> None:
        existing = (
            self.db.query(GSTFilingFact)
            .filter(GSTFilingFact.msme_id == msme_id, GSTFilingFact.source_record_id == source_record_id)
            .first()
        )
        filing_date = self._parse_dt(record.get("filing_date"))
        due_date = self._parse_dt(record.get("due_date"))

        if existing:
            existing.ingestion_run_id = run_id
            existing.filing_period = record.get("filing_period")
            existing.filing_date = filing_date
            existing.due_date = due_date
            existing.return_type = record.get("return_type")
            existing.taxable_turnover = record.get("taxable_turnover")
            existing.tax_paid = record.get("tax_paid")
            existing.itc_claimed = record.get("itc_claimed")
            existing.is_on_time = record.get("is_on_time")
            return

        self.db.add(
            GSTFilingFact(
                ingestion_run_id=run_id,
                msme_id=msme_id,
                source_record_id=source_record_id,
                filing_period=record.get("filing_period"),
                filing_date=filing_date,
                due_date=due_date,
                return_type=record.get("return_type") or "UNKNOWN",
                taxable_turnover=record.get("taxable_turnover"),
                tax_paid=record.get("tax_paid"),
                itc_claimed=record.get("itc_claimed"),
                is_on_time=record.get("is_on_time"),
            )
        )

    def _upsert_upi_fact(self, run_id: int, msme_id: int, source_record_id: str, record: Dict[str, Any]) -> None:
        existing = (
            self.db.query(UPITxnFact)
            .filter(UPITxnFact.msme_id == msme_id, UPITxnFact.source_record_id == source_record_id)
            .first()
        )
        txn_time = self._parse_dt(record.get("transaction_time")) or datetime.utcnow()
        direction = record.get("direction")
        counterparty_vpa = (record.get("counterparty_vpa") or "").strip().lower()
        vpa_hash = self._hash(counterparty_vpa) if counterparty_vpa else None

        if existing:
            existing.ingestion_run_id = run_id
            existing.transaction_time = txn_time
            existing.amount = record.get("amount") or 0
            existing.direction = direction or "DEBIT"
            existing.payer_vpa_hash = vpa_hash if direction == "DEBIT" else None
            existing.payee_vpa_hash = vpa_hash if direction == "CREDIT" else None
            existing.merchant_category = record.get("merchant_category")
            existing.reference_id = record.get("reference_id")
            existing.is_success = bool(record.get("is_success", True))
            return

        self.db.add(
            UPITxnFact(
                ingestion_run_id=run_id,
                msme_id=msme_id,
                source_record_id=source_record_id,
                transaction_time=txn_time,
                amount=record.get("amount") or 0,
                direction=direction or "DEBIT",
                payer_vpa_hash=vpa_hash if direction == "DEBIT" else None,
                payee_vpa_hash=vpa_hash if direction == "CREDIT" else None,
                merchant_category=record.get("merchant_category"),
                reference_id=record.get("reference_id"),
                is_success=bool(record.get("is_success", True)),
            )
        )

    def _upsert_epfo_fact(self, run_id: int, msme_id: int, source_record_id: str, record: Dict[str, Any]) -> None:
        existing = (
            self.db.query(EPFOContributionFact)
            .filter(EPFOContributionFact.msme_id == msme_id, EPFOContributionFact.source_record_id == source_record_id)
            .first()
        )

        if existing:
            existing.ingestion_run_id = run_id
            existing.contribution_month = record.get("contribution_month")
            existing.due_date = self._parse_dt(record.get("due_date"))
            existing.payment_date = self._parse_dt(record.get("payment_date"))
            existing.employee_contribution = record.get("employee_contribution")
            existing.employer_contribution = record.get("employer_contribution")
            existing.total_contribution = record.get("total_contribution")
            existing.employee_count = record.get("employee_count")
            existing.is_on_time = record.get("is_on_time")
            existing.challan_id = record.get("challan_id") or source_record_id
            return

        self.db.add(
            EPFOContributionFact(
                ingestion_run_id=run_id,
                msme_id=msme_id,
                source_record_id=source_record_id,
                contribution_month=record.get("contribution_month"),
                due_date=self._parse_dt(record.get("due_date")),
                payment_date=self._parse_dt(record.get("payment_date")),
                employee_contribution=record.get("employee_contribution"),
                employer_contribution=record.get("employer_contribution"),
                total_contribution=record.get("total_contribution"),
                employee_count=record.get("employee_count"),
                is_on_time=record.get("is_on_time"),
                challan_id=record.get("challan_id") or source_record_id,
            )
        )

    def _upsert_aa_fact(self, run_id: int, msme_id: int, source_record_id: str, record: Dict[str, Any]) -> None:
        existing = (
            self.db.query(AABankStatementFact)
            .filter(AABankStatementFact.msme_id == msme_id, AABankStatementFact.source_record_id == source_record_id)
            .first()
        )

        if existing:
            existing.ingestion_run_id = run_id
            existing.month = record.get("month")
            existing.opening_balance = record.get("opening_balance")
            existing.closing_balance = record.get("closing_balance")
            existing.total_credits = record.get("total_credits")
            existing.total_debits = record.get("total_debits")
            existing.num_credit_transactions = record.get("num_credit_transactions")
            existing.num_debit_transactions = record.get("num_debit_transactions")
            existing.avg_daily_balance = record.get("avg_daily_balance")
            existing.min_balance = record.get("min_balance")
            existing.max_balance = record.get("max_balance")
            existing.emi_outflows = record.get("emi_outflows")
            existing.salary_outflows = record.get("salary_outflows")
            existing.tax_outflows = record.get("tax_outflows")
            return

        self.db.add(
            AABankStatementFact(
                ingestion_run_id=run_id,
                msme_id=msme_id,
                source_record_id=source_record_id,
                month=record.get("month"),
                opening_balance=record.get("opening_balance"),
                closing_balance=record.get("closing_balance"),
                total_credits=record.get("total_credits"),
                total_debits=record.get("total_debits"),
                num_credit_transactions=record.get("num_credit_transactions"),
                num_debit_transactions=record.get("num_debit_transactions"),
                avg_daily_balance=record.get("avg_daily_balance"),
                min_balance=record.get("min_balance"),
                max_balance=record.get("max_balance"),
                emi_outflows=record.get("emi_outflows"),
                salary_outflows=record.get("salary_outflows"),
                tax_outflows=record.get("tax_outflows"),
            )
        )

    def _build_feature_snapshot(self, run: IngestionRun) -> FeatureSnapshot:
        period = (run.window_end or datetime.utcnow()).strftime("%Y-%m")

        gst = self.db.query(GSTFilingFact).filter(GSTFilingFact.msme_id == run.msme_id).all()
        upi = self.db.query(UPITxnFact).filter(UPITxnFact.msme_id == run.msme_id).all()
        epfo = self.db.query(EPFOContributionFact).filter(EPFOContributionFact.msme_id == run.msme_id).all()
        aa = self.db.query(AABankStatementFact).filter(AABankStatementFact.msme_id == run.msme_id).all()

        window_3m = self._window_metrics(gst, upi, epfo, aa, 3)
        window_6m = self._window_metrics(gst, upi, epfo, aa, 6)
        window_12m = self._window_metrics(gst, upi, epfo, aa, 12)

        metrics = {
            "coverage": run.coverage_score,
            "recency": run.recency_score,
            "reliability": run.reliability_score,
            "records_received": float(run.records_received or 0),
            "records_valid": float(run.records_valid or 0),
            "run_version": float(run.run_version or 1),
        }

        return FeatureSnapshot(
            ingestion_run_id=run.id,
            msme_id=run.msme_id,
            snapshot_period=period,
            snapshot_granularity="monthly",
            window_3m_json=json.dumps(window_3m, sort_keys=True),
            window_6m_json=json.dumps(window_6m, sort_keys=True),
            window_12m_json=json.dumps(window_12m, sort_keys=True),
            metrics_json=json.dumps(metrics, sort_keys=True),
            created_at=datetime.utcnow(),
        )

    def _window_metrics(
        self,
        gst: List[GSTFilingFact],
        upi: List[UPITxnFact],
        epfo: List[EPFOContributionFact],
        aa: List[AABankStatementFact],
        months: int,
    ) -> Dict[str, float]:
        gst_sorted = sorted(gst, key=lambda x: x.filing_period)[-months:]
        upi_sorted = sorted(upi, key=lambda x: x.transaction_time)[-months * 30 :]
        epfo_sorted = sorted(epfo, key=lambda x: x.contribution_month)[-months:]
        aa_sorted = sorted(aa, key=lambda x: x.month)[-months:]

        gst_turnover = float(np.sum([x.taxable_turnover or 0 for x in gst_sorted])) if gst_sorted else 0.0
        upi_credits = float(np.sum([x.amount for x in upi_sorted if x.direction == "CREDIT"])) if upi_sorted else 0.0
        upi_debits = float(np.sum([x.amount for x in upi_sorted if x.direction == "DEBIT"])) if upi_sorted else 0.0
        epfo_on_time = (
            float(np.mean([1.0 if x.is_on_time else 0.0 for x in epfo_sorted]) * 100) if epfo_sorted else 0.0
        )
        avg_balance = float(np.mean([x.avg_daily_balance or 0 for x in aa_sorted])) if aa_sorted else 0.0

        return {
            "gst_turnover_sum": round(gst_turnover, 2),
            "upi_net_flow": round(upi_credits - upi_debits, 2),
            "upi_txn_count": float(len(upi_sorted)),
            "epfo_on_time_ratio": round(epfo_on_time, 2),
            "aa_avg_daily_balance": round(avg_balance, 2),
        }

    def _compute_quality_metrics(
        self,
        source: str,
        valid_records: List[Tuple[str, Dict[str, Any]]],
        issues_count: int,
    ) -> Tuple[float, float, float]:
        total = len(valid_records) + issues_count
        coverage = round((len(valid_records) / total) * 100, 2) if total else 0.0

        event_times = [self._event_time_for_source(source, r) for _, r in valid_records]
        if event_times:
            latest = max(event_times)
            age_days = max((datetime.utcnow() - latest).days, 0)
            recency = round(max(0.0, 100 - age_days * 1.5), 2)
        else:
            recency = 0.0

        reliability = round(max(0.0, 100 - (issues_count / max(total, 1)) * 100), 2)
        return coverage, recency, reliability

    def _event_time_for_source(self, source: str, record: Dict[str, Any]) -> datetime:
        if source == "GST":
            return self._parse_dt(record.get("filing_date")) or datetime.utcnow()
        if source == "UPI":
            return self._parse_dt(record.get("transaction_time")) or datetime.utcnow()
        if source == "EPFO":
            return self._parse_dt(record.get("payment_date")) or datetime.utcnow()
        month = record.get("month")
        if month:
            return datetime.strptime(f"{month}-01", "%Y-%m-%d")
        return datetime.utcnow()

    def _amount_for_source(self, source: str, record: Dict[str, Any]) -> Optional[float]:
        if source == "GST":
            return record.get("taxable_turnover")
        if source == "UPI":
            return record.get("amount")
        if source == "EPFO":
            return record.get("total_contribution")
        return record.get("total_credits")

    def _direction_for_source(self, source: str, record: Dict[str, Any]) -> Optional[str]:
        if source == "UPI":
            return record.get("direction")
        return None

    def _counterparty_for_source(self, source: str, record: Dict[str, Any]) -> Optional[str]:
        if source != "UPI":
            return None
        counterparty = (record.get("counterparty_vpa") or "").strip().lower()
        return self._hash(counterparty) if counterparty else None

    def _compliance_for_source(self, source: str, record: Dict[str, Any]) -> Optional[bool]:
        if source == "GST":
            return record.get("is_on_time")
        if source == "EPFO":
            return record.get("is_on_time")
        return None

    def _parse_dt(self, value: Optional[str]) -> Optional[datetime]:
        if not value:
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    def _hash(self, value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()
