from enum import Enum


# -------- Phase 2: Competitive Signals --------

class EventType(str, Enum):
    NEW_PRODUCT_LAUNCH = "new_product_launch"
    PRICE_CHANGE = "price_change"
    NONE = "none"


class Sentiment(str, Enum):
    POSITIVE = "positive"
    MIXED_POSITIVE = "mixed_positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    UNKNOWN = "unknown"


class Clarity(str, Enum):
    CLEAR = "clear"
    CONFUSING = "confusing"
    UNKNOWN = "unknown"


class PriceInfo(str, Enum):
    LOWER = "lower"
    HIGHER = "higher"
    SAME = "same"
    UNKNOWN = "unknown"


# 🔥 NEW — competitive edge enums (used once rules depend on them)

class ExecutionQuality(str, Enum):
    STRONG = "strong"
    AVERAGE = "average"
    WEAK = "weak"
    UNKNOWN = "unknown"


class MessagingStrength(str, Enum):
    CLEAR = "clear"
    GENERIC = "generic"
    CONFUSING = "confusing"
    UNKNOWN = "unknown"


class MarketConfusion(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


# -------- Phase 1: Strategy Output --------

class StrategyType(str, Enum):
    POSITIONING = "positioning_response"
    PRICING = "pricing_response"
    WAIT = "wait_and_observe"


class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
