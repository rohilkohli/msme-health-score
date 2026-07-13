# MSME Financial Health Score

> AI-Powered Credit Assessment Platform for India's MSMEs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://reactjs.org/)

## Problem Statement

Bank's MSME credit evaluation relies on traditional financial documents, which many New-to-Credit (NTC) and New-to-Bank (NTB) enterprises lack or maintain inadequately. Despite availability of rich alternate data (GST, UPI, AA, EPFO, etc.), absence of a unified assessment framework leads to high rejection rates, missed viable borrowers, limited portfolio diversification, and slower financial inclusion progress.

## Solution

An AI/ML-driven **MSME Financial Health Card** that:
- Aggregates alternate data from GST, UPI, Account Aggregator, and EPFO
- Computes a **multidimensional financial health score** (0-1000) across 6 key dimensions
- Visualizes strengths and risks through an intuitive Health Card interface
- Integrates with ULI/OCEN/AA ecosystems for seamless data flow
- Enables near real-time credit assessment
- Expands onboarding of credit-invisible MSMEs while improving portfolio quality

## Scoring Dimensions

| Dimension | Data Source | Weight |
|-----------|------------|--------|
| Cashflow Strength & Stability | UPI + AA + GST | 25% |
| Repayment Capacity & Leverage Proxy | AA Bank Statements | 20% |
| Business Activity & Growth Momentum | GST + UPI + EPFO | 15% |
| Transaction Quality & Conduct | UPI + GST + Risk Signals | 15% |
| Compliance & Formalization | GST + EPFO + Business Vintage | 15% |
| Resilience & Risk Buffers | AA + Cross-source Risk Signals | 10% |

## Score Categories

| Score Range | Category | Risk Level |
|-------------|----------|------------|
| 800-1000 | Very Strong | Very Low |
| 700-799 | Strong | Low |
| 600-699 | Moderate | Moderate |
| 500-599 | Weak | High |
| 0-499 | High Risk | High |

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: SQLite (demo) / PostgreSQL (production)
- **ML**: scikit-learn, pandas, numpy
- **Auth**: JWT (python-jose)

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: TailwindCSS
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Icons**: Lucide React

### Deployment
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Hosting**: Vercel (frontend) + Railway/Render (backend)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                       │
│  Landing │ Dashboard │ Health Card │ Credit Assessment    │
└────────────────────────┬────────────────────────────────┘
                         │ REST API
┌────────────────────────┴────────────────────────────────┐
│                  Backend (FastAPI)                        │
├──────────────────────────────────────────────────────────┤
│  Auth │ MSME Mgmt │ Data Ingestion │ Scoring │ ML Model  │
├──────────────────────────────────────────────────────────┤
│              Data Source Adapters                         │
│  GST API │ UPI Analytics │ EPFO │ Account Aggregator     │
├──────────────────────────────────────────────────────────┤
│     Scoring Engine (6-Dimension Weighted Model)          │
├──────────────────────────────────────────────────────────┤
│          ML Layer (Random Forest + XGBoost)               │
├──────────────────────────────────────────────────────────┤
│              Database (SQLite/PostgreSQL)                 │
└──────────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────┴────┐   ┌──────┴──────┐  ┌────┴────┐
    │ULI/OCEN │   │    AA (RBI) │  │  EPFO   │
    │Ecosystem│   │  Framework  │  │  Portal │
    └─────────┘   └─────────────┘  └─────────┘
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python data/seed_data.py  # Generate synthetic data
uvicorn main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker (Recommended)
```bash
docker-compose up --build
```

The app will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for the interactive Swagger UI.

### Key Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login and get JWT |
| POST | /api/msme/register | Register MSME profile |
| POST | /api/data-sources/connect | Initiate AA consent |
| POST | /api/health-score/compute/{id} | Compute health score |
| GET | /api/health-score/{id} | Get score breakdown |
| GET | /api/credit-assessment/{id} | Credit readiness |
| GET | /api/dashboard/stats | Platform statistics |

## Ecosystem Integration

### Account Aggregator (AA)
- Implements RBI's Account Aggregator framework
- Consent-based data sharing
- Supports FIP (Financial Information Provider) data fetch

### ULI (Unified Lending Interface)
- Standardized lending API integration
- Real-time score sharing with lenders

### OCEN (Open Credit Enablement Network)
- Loan marketplace integration
- Standardized credit assessment sharing

## Team

- **Team Name**: [Your Team Name]
- **Problem Statement**: PS3 - Financial Health Score

## License

MIT License - see [LICENSE](LICENSE) for details.
