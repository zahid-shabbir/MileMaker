from typing import Any, List
from app.models import ActivityLog, RateCard, EarningsStatement, LineItemResponse
from app.utils.line_item_utils import calculate_quantity
from app.utils.activity_log_utils import calculate_hours_worked


def calculate_line_items(rate_card: RateCard, activity_logs: List[ActivityLog]) -> List[LineItemResponse]:
    line_items: List[LineItemResponse] = []

    for line_item in rate_card.line_items:
        quantity = calculate_quantity(line_item.name, activity_logs)
        total = line_item.rate * quantity
        line_items.append(LineItemResponse(
            name=line_item.name,
            quantity=quantity,
            rate=line_item.rate,
            total=total
        ))
    return line_items


def calculate_subtotal(line_items: List[LineItemResponse]) -> float:
    return sum(item.total for item in line_items)


def calculate_minimum_earnings(rate_card: RateCard, line_items_subtotal: float) -> float:
    return min(rate_card.minimum_earnings, line_items_subtotal)


def calculate_final_earnings(minimum_earnings: float, line_items_subtotal: float) -> float:
    return max(minimum_earnings, line_items_subtotal)


def apply_rate_card(activity_logs: List[ActivityLog], rate_card: RateCard) -> EarningsStatement:
    line_items = calculate_line_items(rate_card, activity_logs)
    line_items_subtotal = calculate_subtotal(line_items)
    hours_worked = calculate_hours_worked(activity_logs)
    minimum_earnings = calculate_minimum_earnings(
        rate_card, line_items_subtotal)
    final_earnings = calculate_final_earnings(
        minimum_earnings, line_items_subtotal)

    return EarningsStatement(
        line_items=line_items,
        line_items_subtotal=line_items_subtotal,
        hours_worked=hours_worked,
        final_earnings=final_earnings,
        minimum_earnings=minimum_earnings
    )
