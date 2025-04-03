from datetime import datetime
from src.services.waste_management_service import handle_undocking, free_up_space, log_action
from pymongo import MongoClient

def complete_undocking(undocking_container_id, timestamp, max_weight):
    """
    Completes the undocking process for a container.

    Args:
        undocking_container_id (str): The ID of the undocking container.
        timestamp (str): The timestamp of the undocking in ISO format.
        max_weight (float): The maximum weight allowed for undocking.

    Returns:
        dict: A manifest of the undocking process.
    """
    # Validate the timestamp
    try:
        timestamp = datetime.fromisoformat(timestamp)
    except ValueError:
        raise ValueError("Invalid timestamp format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")

    # Connect to the MongoDB database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["space_station"]
    collection = db["waste_items"]

    # Query the database to retrieve items in the specified container
    items_in_container = list(collection.find({"containerId": undocking_container_id}, {"_id": 0}))

    # Handle undocking by moving waste items to the undocking module and generating a manifest
    manifest = handle_undocking(items_in_container, undocking_container_id, max_weight)

    # Log the completion of the undocking process
    log_action({
        "timestamp": datetime.now().isoformat(),
        "userId": "system",
        "actionType": "undocking_completed",
        "details": {
            "undockingContainerId": undocking_container_id,
            "totalWeight": manifest["totalWeight"],
            "itemsRemoved": len(manifest["items"]),
            "timestamp": timestamp.isoformat()
        }
    })

    # Return the manifest
    return manifest