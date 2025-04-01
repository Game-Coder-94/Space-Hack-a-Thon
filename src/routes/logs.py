from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from src.services.logs_service import get_logs

router = APIRouter()

@router.get("/logs", response_model=dict)
async def fetch_logs(
    startDate: str = Query(..., description="Start date in ISO format"),
    endDate: str = Query(..., description="End date in ISO format"),
    itemId: Optional[str] = Query(None, description="Filter by item ID"),
    userId: Optional[str] = Query(None, description="Filter by user ID"),
    actionType: Optional[str] = Query(None, description="Filter by action type (e.g., placement, retrieval, etc.)")
):
    """
    Endpoint to fetch logs based on query parameters.
    """
    try:
        # Call the service function to fetch logs
        logs = get_logs(start_date=startDate, end_date=endDate, item_id=itemId, user_id=userId, action_type=actionType)
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")