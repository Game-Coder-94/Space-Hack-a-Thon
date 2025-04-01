from datetime import datetime

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

    # Example logic: Simulate saving the placement to a database
    placement_log = {
        "itemId": data["itemId"],
        "userId": data["userId"],
        "timestamp": timestamp,
        "containerId": data["containerId"],
        "position": data["position"]
    }

    # Simulate saving to a database or performing some action
    print("Placement logged:", placement_log)

    # Return success
    return True