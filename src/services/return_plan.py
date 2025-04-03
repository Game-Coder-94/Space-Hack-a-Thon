from datetime import datetime
from src.services.waste_management_service import identify_waste

def generate_return_plan(undocking_container_id, undocking_date, max_weight):
    """
    Generates a return plan for waste items.

    Args:
        undocking_container_id (str): The ID of the undocking container.
        undocking_date (str): The undocking date in ISO format.
        max_weight (float): The maximum weight allowed for the return.

    Returns:
        dict: The return plan, retrieval steps, and return manifest.
    """
    # Validate the undocking date
    try:
        undocking_date = datetime.fromisoformat(undocking_date)
    except ValueError:
        raise ValueError("Invalid undocking date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")

    waste_items = identify_waste()

    # Filter items to fit within the max weight
    return_items = []
    total_weight = 0
    total_volume = 0
    for item in waste_items:
        if total_weight + item["weight"] <= max_weight:
            return_items.append(item)
            total_weight += item["weight"]
            total_volume += item["volume"]

    # Generate return plan steps
    return_plan = [
        {
            "step": idx + 1,
            "itemId": item["itemId"],
            "itemName": item["name"],
            "fromContainer": "storage1",
            "toContainer": undocking_container_id
        }
        for idx, item in enumerate(return_items)
    ]

    # Generate retrieval steps
    retrieval_steps = [
        {
            "step": idx + 1,
            "action": "retrieve",
            "itemId": item["itemId"],
            "itemName": item["name"]
        }
        for idx, item in enumerate(return_items)
    ]

    # Generate return manifest
    return_manifest = {
        "undockingContainerId": undocking_container_id,
        "undockingDate": undocking_date.isoformat(),
        "returnItems": [
            {"itemId": item["itemId"], "name": item["name"], "reason": item["reason"]}
            for item in return_items
        ],
        "totalVolume": total_volume,
        "totalWeight": total_weight
    }

    return {
        "returnPlan": return_plan,
        "retrievalSteps": retrieval_steps,
        "returnManifest": return_manifest
    }