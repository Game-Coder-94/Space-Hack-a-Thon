from fastapi import APIRouter, HTTPException
from src.models import SearchRequest, SearchResponse
from src.services.search_service import search_item

router = APIRouter()

@router.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    result = search_item(itemId=request.itemId, itemName=request.itemName, userId=request.userId)

    if result:
        return SearchResponse(message="Item found", containerId=result['containerId'])
    else:
        raise HTTPException(status_code=404, detail="Item not found")