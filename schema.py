from pydantic import BaseModel
from typing import Literal

class BusinessIntent(BaseModel):
    task: Literal["analysis", "decision", "summary"]
    domain: Literal["customer", "finance", "operations", "risk"]
    urgency: Literal["low", "high"]
    customer_id: str | None