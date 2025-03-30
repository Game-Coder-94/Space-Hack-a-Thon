from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.services.placement_service import StowageOptimizer

router = APIRouter()

@router.get("/")
async def placement_page(request: Request):
    return {"message": "Placement page"}

@router.post("/")
async def place_items(request: Request):
    data = await request.json()  # Get JSON data from the request

    # Extract items and containers from the payload
    items = data.get("items", [])
    containers = data.get("containers", [])

    # Validate input
    if not items or not containers:
        return JSONResponse(
            content={"success": False, "message": "Items and containers are required."},
            status_code=400
        )

    # Define ISS Modules (example modules, replace with actual data)
    modules = {
        "Crew_Quarters": {"width": 100, "depth": 100, "height": 200},
        "Columbus": {"width": 150, "depth": 150, "height": 250}
    }

    # Initialize StowageOptimizer
    optimizer = StowageOptimizer(containers, modules)

    # Run placement optimization
    placement_result = []
    for item in items:
        result = optimizer.optimize_placements(item)
        placement_result.append(result)

    return JSONResponse(content={"success": True, "placements": placement_result})