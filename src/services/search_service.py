from datetime import datetime
from src.database import get_all_items, log_action

def binary_search(data, key, search_by):
    low, high = 0, len(data) - 1

    while low <= high:
        mid = (low + high) // 2
        if data[mid][search_by] == key:
            return data[mid]
        elif data[mid][search_by] < key:
            low = mid + 1
        else:
            high = mid - 1
    return None

def search_item(itemId=None, itemName=None, userId=None, newContainerId=None):
    """
    Searches for an item and provides retrieval instructions.

    Args:
        itemId (str): The ID of the item to search for.
        itemName (str): The name of the item to search for.
        userId (str): The ID of the user performing the search.
        newContainerId (str): The ID of the new container for placement (optional).

    Returns:
        dict: Retrieval instructions and item details.
    """
    data = get_all_items()

    # Search by itemId using Binary Search if itemId is provided
    if itemId:
        result = binary_search(data, itemId, 'itemId')
        if result:
            return handle_retrieval(result, userId, newContainerId)
        else:
            return {"success": False, "message": "Item not found."}

    # Linear Search if itemName is provided
    elif itemName:
        for item in data:
            if item['itemName'].lower() == itemName.lower():
                return handle_retrieval(item, userId, newContainerId)

    return {"success": False, "message": "Item not found."}


def handle_retrieval(item, userId, newContainerId):
    """
    Handles retrieval instructions, placement updates, and logging.

    Args:
        item (dict): The item details.
        userId (str): The ID of the user performing the retrieval.
        newContainerId (str): The ID of the new container for placement (optional).

    Returns:
        dict: Retrieval instructions and item details.
    """
    # Suggest module and position
    module = item.get("containerId")
    position = item.get("position")

    # Provide retrieval instructions
    retrieval_instructions = {
        "step": 1,
        "action": "retrieve",
        "itemId": item["itemId"],
        "fromContainer": module,
        "fromPosition": position
    }

    # Update placement if a new container is provided
    if newContainerId:
        item["containerId"] = newContainerId
        item["position"] = {"startCoordinates": {"width": 0, "depth": 0, "height": 0},
                            "endCoordinates": {"width": 10, "depth": 10, "height": 10}}
        retrieval_instructions["step"] = 2
        retrieval_instructions["action"] = "place"
        retrieval_instructions["toContainer"] = newContainerId
        retrieval_instructions["toPosition"] = item["position"]

    # Log the action
    log_action({
        "timestamp": datetime.now().isoformat(),
        "userId": userId,
        "actionType": "retrieval",
        "itemId": item["itemId"],
        "details": {
            "fromContainer": module,
            "toContainer": newContainerId or module,
            "reason": "Astronaut retrieval"
        }
    })

    return {
        "success": True,
        "item": item,
        "retrievalInstructions": retrieval_instructions
    }
