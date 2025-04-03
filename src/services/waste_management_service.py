from datetime import datetime
from src.services.logs_service import log_action

def identify_waste(items):
    """
    Identifies waste items based on expiry date, usage limit, and priority.

    Args:
        items (list): A list of item dictionaries. Each item should have:
            - itemId (str): Unique identifier for the item.
            - itemName (str): Name of the item.
            - expiryDate (str): Expiry date in ISO format (YYYY-MM-DD).
            - usageLimit (int): Maximum allowed usage percentage.
            - currentUsage (int): Current usage percentage.
            - priority (int): Priority of the item (lower priority is more likely to be waste).

    Returns:
        list: A list of waste items.
    """
    waste_items = []
    current_date = datetime.now()

    for item in items:
        # Check if the item has expired
        if "expiryDate" in item:
            expiry_date = datetime.strptime(item["expiryDate"], "%Y-%m-%d")
            if expiry_date < current_date:
                waste_items.append({
                    "itemId": item["itemId"],
                    "reason": "Expired"
                })
                log_action({
                    "timestamp": current_date.isoformat(),
                    "userId": "system",
                    "actionType": "waste_marked",
                    "itemId": item["itemId"],
                    "details": {"reason": "Expired"}
                })
                continue

        # Check if the item's usage exceeds the allowed limit
        if "usageLimit" in item and "currentUsage" in item:
            if item["currentUsage"] > item["usageLimit"]:
                waste_items.append({
                    "itemId": item["itemId"],
                    "reason": "Exceeded usage limit"
                })
                log_action({
                    "timestamp": current_date.isoformat(),
                    "userId": "system",
                    "actionType": "waste_marked",
                    "itemId": item["itemId"],
                    "details": {"reason": "Exceeded usage limit"}
                })
                continue

        # Check if the item's priority is too low (e.g., priority < 20)
        if "priority" in item and item["priority"] < 20:
            waste_items.append({
                "itemId": item["itemId"],
                "reason": "Low priority"
            })
            log_action({
                "timestamp": current_date.isoformat(),
                "userId": "system",
                "actionType": "waste_marked",
                "itemId": item["itemId"],
                "details": {"reason": "Low priority"}
            })

    return waste_items


def handle_undocking(waste_items, undocking_module, max_weight):
    """
    Handles undocking by moving waste items to the undocking module and generating a manifest.

    Args:
        waste_items (list): A list of waste items to be moved.
        undocking_module (str): The module where waste will be moved.
        max_weight (float): The maximum weight allowed for undocking.

    Returns:
        dict: A manifest of the undocking process.
    """
    manifest = {
        "undockingModule": undocking_module,
        "totalWeight": 0,
        "items": []
    }

    total_weight = 0
    for item in waste_items:
        item_weight = item.get("weight", 0)
        if total_weight + item_weight > max_weight:
            break

        manifest["items"].append({
            "itemId": item["itemId"],
            "name": item.get("itemName", "Unknown"),
            "reason": item.get("reason", "Unknown"),
            "weight": item_weight
        })
        total_weight += item_weight

        # Log the movement of the item to the undocking module
        log_action({
            "timestamp": datetime.now().isoformat(),
            "userId": "system",
            "actionType": "undocking",
            "itemId": item["itemId"],
            "details": {
                "fromContainer": item.get("containerId", "Unknown"),
                "toContainer": undocking_module,
                "reason": "Undocking preparation"
            }
        })

    manifest["totalWeight"] = total_weight

    # Free up space after undocking
    free_up_space(manifest["items"])

    return manifest


def free_up_space(items):
    """
    Frees up space by removing items that have been undocked.

    Args:
        items (list): A list of items that have been undocked.
    """
    for item in items:
        log_action({
            "timestamp": datetime.now().isoformat(),
            "userId": "system",
            "actionType": "space_freed",
            "itemId": item["itemId"],
            "details": {"reason": "Item undocked"}
        })
    print(f"Freed up space for {len(items)} items.")


def log_action(action):
    """
    Logs an action into the database.

    Args:
        action (dict): The action details to log.
    """
    print(f"Action logged: {action}")