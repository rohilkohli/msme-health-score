from enum import Enum


class ScoreCategory(str, Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    FAIR = "Fair"
    NEEDS_IMPROVEMENT = "Needs Improvement"
    CRITICAL = "Critical"

    @classmethod
    def from_score(cls, score: float) -> "ScoreCategory":
        if score >= 800:
            return cls.EXCELLENT
        elif score >= 600:
            return cls.GOOD
        elif score >= 400:
            return cls.FAIR
        elif score >= 200:
            return cls.NEEDS_IMPROVEMENT
        else:
            return cls.CRITICAL


class ScoreCategoryColor(str, Enum):
    EXCELLENT = "Green"
    GOOD = "Blue"
    FAIR = "Yellow"
    NEEDS_IMPROVEMENT = "Orange"
    CRITICAL = "Red"

    @classmethod
    def from_category(cls, category: ScoreCategory) -> str:
        mapping = {
            ScoreCategory.EXCELLENT: cls.EXCELLENT.value,
            ScoreCategory.GOOD: cls.GOOD.value,
            ScoreCategory.FAIR: cls.FAIR.value,
            ScoreCategory.NEEDS_IMPROVEMENT: cls.NEEDS_IMPROVEMENT.value,
            ScoreCategory.CRITICAL: cls.CRITICAL.value,
        }
        return mapping.get(category, "Gray")


class RiskLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    VERY_HIGH = "Very High"


class DataSourceType(str, Enum):
    GST = "GST"
    UPI = "UPI"
    EPFO = "EPFO"
    ACCOUNT_AGGREGATOR = "Account Aggregator"


class DataSourceStatus(str, Enum):
    PENDING = "pending"
    CONNECTED = "connected"
    FETCHING = "fetching"
    COMPLETED = "completed"
    FAILED = "failed"


class MSMEBusinessType(str, Enum):
    MICRO = "Micro"
    SMALL = "Small"
    MEDIUM = "Medium"


class IndustryType(str, Enum):
    MANUFACTURING = "Manufacturing"
    SERVICES = "Services"
    TRADING = "Trading"
    AGRICULTURE = "Agriculture"
    CONSTRUCTION = "Construction"
    TECHNOLOGY = "Technology"
    FOOD_PROCESSING = "Food Processing"
    TEXTILES = "Textiles"
    HEALTHCARE = "Healthcare"
    LOGISTICS = "Logistics"
