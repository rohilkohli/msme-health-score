from enum import Enum


class ScoreCategory(str, Enum):
    VERY_STRONG = "Very Strong"
    STRONG = "Strong"
    MODERATE = "Moderate"
    WEAK = "Weak"
    HIGH_RISK = "High Risk"

    @classmethod
    def from_score(cls, score: float) -> "ScoreCategory":
        if score >= 800:
            return cls.VERY_STRONG
        elif score >= 700:
            return cls.STRONG
        elif score >= 600:
            return cls.MODERATE
        elif score >= 500:
            return cls.WEAK
        else:
            return cls.HIGH_RISK


class ScoreCategoryColor(str, Enum):
    VERY_STRONG = "Green"
    STRONG = "Blue"
    MODERATE = "Yellow"
    WEAK = "Orange"
    HIGH_RISK = "Red"

    @classmethod
    def from_category(cls, category: ScoreCategory) -> str:
        mapping = {
            ScoreCategory.VERY_STRONG: cls.VERY_STRONG.value,
            ScoreCategory.STRONG: cls.STRONG.value,
            ScoreCategory.MODERATE: cls.MODERATE.value,
            ScoreCategory.WEAK: cls.WEAK.value,
            ScoreCategory.HIGH_RISK: cls.HIGH_RISK.value,
        }
        return mapping.get(category, "Gray")


class RiskLevel(str, Enum):
    VERY_LOW = "Very Low"
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


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
