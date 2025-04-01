from fastapi import APIRouter, HTTPException, Request
from src.services.place_service import place_item

router = APIRouter()

@router.post("/place", response_model=dict)
async def place(request: Request):
    """
    Endpoint to place an item in a container.
    """
    data = await request.json()

    # Validate required fields
    required_fields = ["itemId", "userId", "timestamp", "containerId", "position"]
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    # Call the service function to handle the placement logic
    try:
        success = place_item(data)
        return {"success": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")