# tests/test_api.py
from app.utils import ActivityLog, calculate_hours_worked, apply_rate_card, calculate_quantity, has_long_route, has_loyalty_routes
from datetime import datetime, timedelta
import datetime
import pytest
from app.api import calculate_earnings
from unittest.mock import Mock
from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app
from app.models import ActivityLog, LineItemResponse, RateCard, EarningsStatement
from datetime import datetime, timezone

client = TestClient(app)

activity_logs = [
    ActivityLog(
        route_id="RT5QHQ6M3A937H",
        attempt_date_time="2023-12-18T08:33:18.588934+00:00",
        success=True
    ),
    ActivityLog(
        route_id="RT5QHQ6M3A937H",
        attempt_date_time="2023-12-18T08:37:11.897203+00:00",
        success=True
    ),
]


def test_calculate_earnings():
    tier = "bronze_tier"
    # Convert ActivityLog instances to dictionaries
    payload = [
        {
            "route_id": log.route_id,
            "attempt_date_time": log.attempt_date_time.isoformat(),
            "success": log.success,
        }
        for log in activity_logs
    ]

    with TestClient(app) as client:
        response = client.post(f"/earnings/{tier}", json=payload)
        print(response.text)
    assert response.status_code == 200

    # Check the response JSON for expected values
    assert "line_items_subtotal" in response.json()
    assert "hours_worked" in response.json()
    assert "minimum_earnings" in response.json()
    assert "final_earnings" in response.json()
    assert "line_items" in response.json()


# Assuming the classes and methods are in a module named 'module'

def test_calculate_quantity():
    activity_logs = [
        ActivityLog(
            route_id="RT5QHQ6M3A937H",
            attempt_date_time=datetime.now(),
            success=True
        ),
        ActivityLog(
            route_id="RT5QHQ6M3A937H",
            attempt_date_time=datetime.now() + timedelta(hours=1),
            success=False
        ),
    ]
    assert calculate_quantity("Per successful attempt", activity_logs) == 1
    assert calculate_quantity("Per unsuccessful attempt", activity_logs) == 1


def test_has_loyalty_routes():
    activity_logs = [ActivityLog(route_id=f"RT5QHQ6M3A937{i}", attempt_date_time=datetime.now(
    ), success=True) for i in range(10)]
    assert has_loyalty_routes(activity_logs) == True


def test_has_long_route():
    # Create 31 ActivityLog instances with the same route_id
    activity_logs = [ActivityLog(route_id="RT5QHQ6M3A937H", attempt_date_time=datetime.now(
    ), success=True) for _ in range(31)]
    assert has_long_route(activity_logs) == True


def test_calculate_hours_worked():
    activity_logs = [
        ActivityLog(
            route_id="RT5QHQ6M3A937H",
            attempt_date_time=datetime.now(),
            success=True
        ),
        ActivityLog(
            route_id="RT5QHQ6M3A937H",
            attempt_date_time=datetime.now() + timedelta(hours=1),
            success=True
        ),
    ]
    assert calculate_hours_worked(activity_logs) == pytest.approx(1.0, 0.00001)
