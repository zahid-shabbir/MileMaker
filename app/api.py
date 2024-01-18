# app/api.py
from fastapi import HTTPException, Request, APIRouter, FastAPI
from typing import List
from app.models import ActivityLog, EarningsStatement
from app.utils import get_rate_card, apply_rate_card
from fastapi import HTTPException

VALID_TIERS = ["bronze_tier", "silver_tier", "gold_tier", "platinum_tier"]

router = APIRouter()

@router.post("/earnings/{tier}")
async def calculate_earnings(tier: str, request: Request):
    # Check if the tier is valid
    if tier not in VALID_TIERS:
        raise HTTPException(status_code=400, detail=f"Invalid tier: {tier}")

    try:
        # Retrieving rate card based on the URL parameter
        rate_card = get_rate_card(tier)
        if not rate_card:
            raise HTTPException(status_code=404, detail="Rate card not found")

        # Parsing activity logs and convert them to instances of ActivityLog
        activity_logs_data = await request.json()
        print('activity_logs_data: ', activity_logs_data)
        activity_logs = [ActivityLog(**log_data)
                         for log_data in activity_logs_data]

        # Calculate earnings
        earnings_statement = apply_rate_card(activity_logs, rate_card)
        print('earnings_statement', earnings_statement)
        return earnings_statement

    except HTTPException as fastapi_exception:
        # Catching FastAPI's HTTPException and check if it's due to validation errors
        if 'field required' in fastapi_exception.detail:
            # If the error is related to a required field, raise a more specific exception
            raise HTTPException(
                status_code=400, detail="Missing required field in request payload")

        # If it's not a validation error or not related to the specific field, re-raise the original exception
        raise fastapi_exception

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
