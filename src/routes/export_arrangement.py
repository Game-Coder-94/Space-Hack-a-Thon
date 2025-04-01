from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from src.services.export_service import get_current_arrangement
import csv
from io import StringIO

router = APIRouter()

@router.get("/export/arrangement", response_class=StreamingResponse)
async def export_arrangement_endpoint():
    """
    Endpoint to export the current arrangement as a CSV file.
    """
    try:
        # Get the current arrangement from the service
        arrangement = get_current_arrangement()

        # Create a CSV file in memory
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(["Item ID", "Container ID", "Coordinates (W1,D1,H1)", "Coordinates (W2,D2,H2)"])
        for item in arrangement:
            writer.writerow([
                item["itemId"],
                item["containerId"],
                f"({item['startCoordinates']['width']},{item['startCoordinates']['depth']},{item['startCoordinates']['height']})",
                f"({item['endCoordinates']['width']},{item['endCoordinates']['depth']},{item['endCoordinates']['height']})"
            ])
        csv_file.seek(0)

        # Return the CSV file as a streaming response
        response = StreamingResponse(csv_file, media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=arrangement.csv"
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")