from fastapi import APIRouter, HTTPException, Request
from src.services.waste_management_service import identify_waste
# from database import get_all_items  # Assuming this function retrieves all items
from src.database import get_all_items

router = APIRouter()

@router.get("/")
async def waste_management_page(request: Request):
    return {"message": "Waste Management page"}

@router.get("/identify", response_model=dict)
async def identify_waste_endpoint():
    """
    Endpoint to identify waste items.
    """
    # Retrieve all items from the database
    items = get_all_items()

    if not items:
        raise HTTPException(status_code=404, detail="No items found")

    # Identify waste items
    waste_items = identify_waste(items)

    # Format the response
    response = {
        "success": True,
        "wasteItems": [
            {
                "itemId": item["itemId"],
                "name": item.get("itemName", "Unknown"),
                "reason": item["reason"],
                "containerId": item.get("containerId", "Unknown"),
                "position": item.get("position", {
                    "startCoordinates": {"width": 0, "depth": 0, "height": 0},
                    "endCoordinates": {"width": 0, "depth": 0, "height": 0}
                })
            }
            for item in waste_items
        ]
    }

    return response