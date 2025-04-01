from fastapi import APIRouter, HTTPException, Request
from src.services.return_plan import generate_return_plan

router = APIRouter()

@router.post("/return-plan", response_model=dict)
async def return_plan_endpoint(request: Request):
    """
    Endpoint to generate a return plan for waste items.
    """
    data = await request.json()

    # Validate required fields
    required_fields = ["undockingContainerId", "undockingDate", "maxWeight"]
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    try:
        # Call the service function to generate the return plan
        return_plan = generate_return_plan(
            undocking_container_id=data["undockingContainerId"],
            undocking_date=data["undockingDate"],
            max_weight=data["maxWeight"]
        )
        return {"success": True, **return_plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")