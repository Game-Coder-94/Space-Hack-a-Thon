from fastapi import APIRouter, HTTPException, Request
from src.services.waste_management_service import complete_undocking

router = APIRouter()

@router.post("/complete-undocking", response_model=dict)
async def complete_undocking_endpoint(request: Request):
    """
    Endpoint to complete the undocking process for a container.
    """
    data = await request.json()

    # Validate required fields
    required_fields = ["undockingContainerId", "timestamp"]
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    try:
        # Call the service function to complete the undocking process
        result = complete_undocking(
            undocking_container_id=data["undockingContainerId"],
            timestamp=data["timestamp"]
        )
        return {"success": True, "itemsRemoved": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")