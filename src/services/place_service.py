from datetime import datetime
import sqlite3
from pymongo import MongoClient

def place_item(data):
    """
    Handles the placement of an item in a container.

    Args:
        data (dict): The placement data containing:
            - itemId (str): The ID of the item.
            - userId (str): The ID of the user placing the item.
            - timestamp (str): The timestamp of the placement in ISO format.
            - containerId (str): The ID of the container.
            - position (dict): The position of the item in the container.

    Returns:
        bool: True if the placement is successful, False otherwise.
    """
    # Validate the timestamp
    try:
        timestamp = datetime.fromisoformat(data["timestamp"])
    except ValueError:
        raise ValueError("Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")

    # Connect to the MongoDB database
    client = MongoClient('mongodb://localhost:27017/')
    db = client['space_hackathon']
    placements_collection = db['placements']

    # Insert the placement data into the collection
    placement_data = {
        "itemId": data["itemId"],
        "userId": data["userId"],
        "timestamp": data["timestamp"],
        "containerId": data["containerId"],
        "position": data["position"]
    }
    placements_collection.insert_one(placement_data)

    # Close the connection
    client.close()

    # Return success
    return True