
from typing import Any, List
from app.models import ActivityLog, LineItem
from app.utils.activity_log_utils import has_long_route, has_loyalty_routes

def calculate_quantity(line_item_name: str, activity_logs: List[ActivityLog]) -> int:
    if line_item_name == "Per successful attempt":
        return sum(log.success for log in activity_logs)
    elif line_item_name == "Per unsuccessful attempt":
        return sum(not log.success for log in activity_logs)
    elif line_item_name == "Long route bonus":
        return 1 if has_long_route(activity_logs) else 0
    elif line_item_name == "Loyalty bonus (routes)":
        return 1 if has_loyalty_routes(activity_logs) else 0
    else:
        return 0


def create_line_item(name: str, rate: float, conditions: list) -> LineItem:
    return LineItem(name=name, rate=rate, conditions=conditions)
