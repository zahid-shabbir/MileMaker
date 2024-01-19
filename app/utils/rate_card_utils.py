from typing import Any, List
from app.models import RateCard, LineItem
from app.utils.line_item_utils import create_line_item

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
