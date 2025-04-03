import csv
from io import StringIO
from pymongo import MongoClient

async def import_items_from_csv(file):
    """
    Processes a CSV file and imports items.

    Args:
        file (UploadFile): The uploaded CSV file.

    Returns:
        dict: A dictionary containing the number of items imported and any errors.
    """
    items_imported = 0
    errors = []

    # Read the file content
    content = await file.read()
    csv_data = StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_data)

    # Process each row in the CSV
    for row_number, row in enumerate(reader, start=1):
        try:
            # Validate required fields
            required_fields = ["itemId", "name", "width", "depth", "height", "mass", "priority"]
            for field in required_fields:
                if field not in row or not row[field]:
                    raise ValueError(f"Missing required field: {field}")

            # Save the item to MongoDB (replace with actual database logic)

            # Establish MongoDB connection (ensure to configure connection string properly)
            client = MongoClient("mongodb://localhost:27017/")
            db = client["space_hackathon"]
            collection = db["items"]

            # Create the item document
            item = {
                "itemId": row["itemId"],
                "name": row["name"],
                "width": float(row["width"]),
                "depth": float(row["depth"]),
                "height": float(row["height"]),
                "mass": float(row["mass"]),
                "priority": int(row["priority"])
            }

            # Insert the item into the collection
            collection.insert_one(item)
            items_imported += 1

        except Exception as e:
            # Log errors for invalid rows
            errors.append({"row": row_number, "message": str(e)})

    return {"itemsImported": items_imported, "errors": errors}