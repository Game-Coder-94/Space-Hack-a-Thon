from fastapi import APIRouter, HTTPException, Request
from src.services.time_simulation_service import simulate_day

router = APIRouter()

@router.post("/simulate/day", response_model=dict)
async def simulate_day_endpoint(request: Request):
    """
    Endpoint to simulate the passage of days and update item statuses.
    """
    data = await request.json()

    # Validate required fields
    if "numOfDays" not in data and "toTimestamp" not in data:
        raise HTTPException(status_code=400, detail="Either 'numOfDays' or 'toTimestamp' must be provided.")
    if "itemsToBeUsedPerDay" not in data:
        raise HTTPException(status_code=400, detail="Missing required field: 'itemsToBeUsedPerDay'.")

    try:
        # Call the service function to simulate the day
        result = simulate_day(
            num_of_days=data.get("numOfDays"),
            to_timestamp=data.get("toTimestamp"),
            items_to_be_used_per_day=data["itemsToBeUsedPerDay"]
        )
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")