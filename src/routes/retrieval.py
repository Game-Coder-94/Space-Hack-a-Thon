from fastapi import APIRouter, HTTPException, Request
from src.services.retrieval_service import RetrievalOptimizer
from src.services.placement_service import StowageOptimizer

# Include the router from retrieval.py
router = APIRouter()

@router.post("/")
async def retrieve_item(request: Request):
    body = await request.json()
    item_id = body.get("itemId")
    user_id = body.get("userId")
    timestamp = body.get("timestamp")

    if not item_id or not user_id or not timestamp:
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Use the RetrievalOptimizer from retrieval.py for retrieval logic
    stowage_solution = StowageOptimizer.initialize_solution()
    optimizer = RetrievalOptimizer(stowage_solution)
    success = optimizer.optimize_retrieval(item_id, user_id, timestamp)

    return {"success": success}