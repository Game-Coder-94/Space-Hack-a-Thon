from fastapi import APIRouter, HTTPException, UploadFile, File
from src.services.import_items_service import import_items_from_csv

router = APIRouter()

@router.post("/import/items", response_model=dict)
async def import_items_endpoint(file: UploadFile = File(...)):
    """
    Endpoint to import items from a CSV file.
    """
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    try:
        # Call the service function to process the CSV file
        result = await import_items_from_csv(file)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")