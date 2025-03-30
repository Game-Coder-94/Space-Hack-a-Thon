from datetime import datetime

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
                continue

        # Check if the item's usage exceeds the allowed limit
        if "usageLimit" in item and "currentUsage" in item:
            if item["currentUsage"] > item["usageLimit"]:
                waste_items.append({
                    "itemId": item["itemId"],
                    "reason": "Exceeded usage limit"
                })
                continue

        # Check if the item's priority is too low (e.g., priority < 20)
        if "priority" in item and item["priority"] < 20:
            waste_items.append({
                "itemId": item["itemId"],
                "reason": "Low priority"
            })

    return waste_items