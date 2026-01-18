from pydantic import BaseModel
from typing import Literal


class AdvisorInputSchema(BaseModel):
    strategy_type: str
    focus: str
    urgency: Literal["low", "medium", "high"]
    signals: list[str]


class AdvisorOutputSchema(BaseModel):
    advice: str
    reason: str
    confidence: Literal["low", "medium", "high"]
