# app/utils.py
from datetime import datetime
from typing import Any, List
from app.models import ActivityLog, RateCard, EarningsStatement, LineItem, LineItemResponse


def parse_iso_datetime(dt_str: datetime) -> datetime:
    return dt_str


def calculate_hours_worked(activity_logs: List[ActivityLog]) -> float:
    # Implement logic to calculate hours worked from activity logs

    print('activity_logs:', activity_logs)
    if not activity_logs:
        return 0.0

    # Assuming the logs are sorted by attempt_date_time
    # start_time = parse_iso_datetime(activity_logs[0].attempt_date_time)
    # end_time = parse_iso_datetime(activity_logs[-1].attempt_date_time)

    start_time = activity_logs[0].attempt_date_time
    end_time = activity_logs[-1].attempt_date_time

    # Calculate the difference in hours
    # hours_worked = (end_time - start_time).total_seconds() / 3600.0
    hours_worked = (end_time - start_time).total_seconds() / 3600.0
    return hours_worked


def apply_rate_card(activity_logs: List[ActivityLog], rate_card: RateCard) -> EarningsStatement:
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

    line_items_subtotal = sum(item.total for item in line_items)
    hours_worked = calculate_hours_worked(activity_logs)
    minimum_earnings = max(rate_card.minimum_earnings, line_items_subtotal)
    final_earnings = max(minimum_earnings, line_items_subtotal)

    return EarningsStatement(
        line_items=line_items,
        line_items_subtotal=line_items_subtotal,
        hours_worked=hours_worked,
        final_earnings=final_earnings,
        minimum_earnings=minimum_earnings

    )


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


def has_long_route(activity_logs: List[ActivityLog]) -> bool:
    # Implement logic to check if there is a long route
    # For example, check if the total successful drops on at least one route are more than 30
    routes_with_successful_drops = {}
    for log in activity_logs:
        if log.success:
            routes_with_successful_drops.setdefault(log.route_id, 0)
            routes_with_successful_drops[log.route_id] += 1

    return any(count > 30 for count in routes_with_successful_drops.values())


def has_loyalty_routes(activity_logs: List[ActivityLog]) -> bool:
    # Implement logic to check if there are at least 10 different routes
    unique_routes = set(log.route_id for log in activity_logs)
    return len(unique_routes) >= 10


def create_line_item(name: str, rate: float, conditions: list) -> LineItem:
    return LineItem(name=name, rate=rate, conditions=conditions)


def create_rate_card(tier: str, line_items: list, minimum_earnings: float) -> RateCard:
    return RateCard(tier=tier, line_items=line_items, minimum_earnings=minimum_earnings)


def get_rate_card(tier: str) -> RateCard:
    rate_cards = {
        "bronze_tier": create_rate_card(
            "bronze_tier",
            [
                create_line_item("Per successful attempt", 0.459, []),
                create_line_item("Per unsuccessful attempt", 0.229, []),
                create_line_item("Long route bonus", 10, [
                                 "More than 30 successful drops on at least one route. Only paid once per week."]),
                create_line_item("Loyalty bonus (routes)", 20, [
                                 "Courier participated in at least 10 different routes in the course of the week. Only paid once per week."]),
            ],
            14.50
        ),

        "silver_tier": create_rate_card(
            tier="silver_tier",
            line_items=[
                LineItem(name="Per successful attempt",
                         rate=0.65, conditions=[]),
                LineItem(name="Per unsuccessful attempt",
                         rate=0.0, conditions=[]),
                LineItem(name="Loyalty bonus (attempts)", rate=19, conditions=[
                         "Courier completed at least 150 successful attempts in the course of the week. Only paid once per week"]),
                LineItem(name="Quality bonus", rate=25, conditions=[
                         "The courier’s success rate on attempts over the week was at least 97.0%, and the courier made at least 20 attempts (regardless of success). Only paid once per week."]),
            ],
            minimum_earnings=14.50,
        ),
        "gold_tier": create_rate_card(
            tier="gold_tier",
            line_items=[
                LineItem(name="Per successful attempt",
                         rate=0.511, conditions=[]),
                LineItem(name="Per unsuccessful attempt",
                         rate=0.126, conditions=[]),
                LineItem(name="Consistency bonus", rate=32, conditions=[
                         "More than 30 successful drops on at least one route. Only paid once per week."]),
            ],
            minimum_earnings=14.50,
        ),

        "platinum_tier": create_rate_card(
            tier="platinum_tier",
            line_items=[
                LineItem(name="Per successful attempt",
                         rate=0.667, conditions=[]),
                LineItem(name="Per unsuccessful attempt",
                         rate=0.155, conditions=[]),
                LineItem(name="Long route bonus", rate=12.0, conditions=[
                         "(Identical to the corresponding bronze_tier line item)."]),
                LineItem(name="Loyalty bonus (attempts", rate=18.0, conditions=[
                         "(Identical to the corresponding silver_tier line item)."]),
                LineItem(name="Consistency bonus", rate=34.50, conditions=[
                         "(Identical to the corresponding gold_tier line item)."]),
            ],
            minimum_earnings=14.50,
        ),
        # Add other rate cards as needed
    }

    return rate_cards.get(tier, None)
