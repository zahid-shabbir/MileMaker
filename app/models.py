# models.py
from typing import Any, List, Optional
from pydantic import BaseModel
from datetime import datetime


class ActivityLog(BaseModel):
    route_id: str
    attempt_date_time: datetime  # ISO 8601 datetime string
    success: bool


class LineItem(BaseModel):
    name: str
    rate: float
    conditions: List[str]


class LineItemResponse(BaseModel):
    name: str
    quantity: float
    rate: float
    total: float


class RateCard(BaseModel):
    tier: str
    line_items: Optional[List[LineItem]] = []
    minimum_earnings: float


class EarningsStatement(BaseModel):
    line_items: List[LineItemResponse]
    line_items_subtotal: float
    hours_worked: float
    minimum_earnings: float
    final_earnings: float
