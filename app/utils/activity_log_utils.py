from typing import Any, List
from app.models import ActivityLog


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
