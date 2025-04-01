from fastapi import APIRouter, HTTPException, UploadFile, File
from src.services.import_container_service import import_containers_from_csv

router = APIRouter()

@router.post("/import/containers", response_model=dict)
async def import_containers_endpoint(file: UploadFile = File(...)):
    """
    Endpoint to import containers from a CSV file.
    """
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV file.")

    try:
        # Call the service function to process the CSV file
        result = await import_containers_from_csv(file)
        return {"success": True, **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")