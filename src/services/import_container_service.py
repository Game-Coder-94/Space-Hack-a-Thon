import csv
from io import StringIO

async def import_containers_from_csv(file):
    """
    Processes a CSV file and imports containers.

    Args:
        file (UploadFile): The uploaded CSV file.

    Returns:
        dict: A dictionary containing the number of containers imported and any errors.
    """
    containers_imported = 0
    errors = []

    # Read the file content
    content = await file.read()
    csv_data = StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_data)

    # Process each row in the CSV
    for row_number, row in enumerate(reader, start=1):
        try:
            # Validate required fields
            required_fields = ["containerId", "zone", "width", "depth", "height"]
            for field in required_fields:
                if field not in row or not row[field]:
                    raise ValueError(f"Missing required field: {field}")

            # Example logic: Simulate saving the container (replace with actual database logic)
            container = {
                "containerId": row["containerId"],
                "zone": row["zone"],
                "width": float(row["width"]),
                "depth": float(row["depth"]),
                "height": float(row["height"])
            }
            print(f"Imported container: {container}")  # Replace with actual database save logic
            containers_imported += 1

        except Exception as e:
            # Log errors for invalid rows
            errors.append({"row": row_number, "message": str(e)})

    return {"containersImported": containers_imported, "errors": errors}