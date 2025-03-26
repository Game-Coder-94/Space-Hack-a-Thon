from datetime import datetime   
import json

def retrival_steps(optimizer, item_id):
    """
    Calculate the number of items that must be moved to retrieve a specific item.
    - If the item is directly visible, return 0.
    - Otherwise, count the number of blocking items.
    """
    module = optimizer.stowage[item_id]
    items_in_module = [c for c in optimizer.containers if optimizer.stowage[c['id']] == module]

    items_in_module.sort(key=lambda x: x.get('depth', 0), reverse=True)

    steps = 0
    for item in items_in_module:
        if item['id'] == item_id:
            return steps
        steps += 1

    return steps

def suggest_fastest_retrieval(optimizer):
    
    retrival_list = []

    for container in optimizer.containers:
        item_id = container['id']
        steps = optimizer.retrival_steps(item_id)
        expiry_date_str = container.get('expiry', '2100-01-01')
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
        days_to_expiry = (expiry_date - datetime.today()).days

        retrival_list.append((container['name'], steps, days_to_expiry, optimizer.stowage[item_id]))

    retrival_list.sort(key=lambda x: (x[1], x[2]))      # sorts by steps and expiry

    best_item = retrival_list[0]
    print()
    print(f"📦 Suggested Item for Quick Retrieval: {best_item[0]}")
    print(f"   🔹 Retrieval Steps Needed: {best_item[1]}")
    print(f"   ⏳ Days Until Expiry: {best_item[2]}")
    print(f"   📍 Stored in Module: {best_item[3]}")


def generate_stowage_response(success, placements, rearrangements):
    
    response = {
        'success' : success,
        'placements' : placements,
        'rearrangements' : rearrangements
    }
    return json.dump(response, indent=4)

# Example Data
placements = [
    {
        "itemId": "C001",
        "containerId": "ISS-Storage-1",
        "position": {
            "startCoordinates": {"width": 0, "depth": 0, "height": 0},
            "endCoordinates": {"width": 10, "depth": 10, "height": 10}
        }
    }
]

rearrangements = [
    {
        "step": 1,
        "action": "move",
        "itemId": "C002",
        "fromContainer": "ISS-Storage-3",
        "fromPosition": {
            "startCoordinates": {"width": 5, "depth": 5, "height": 5},
            "endCoordinates": {"width": 15, "depth": 15, "height": 15}
        },
        "toContainer": "ISS-Storage-1",
        "toPosition": {
            "startCoordinates": {"width": 0, "depth": 10, "height": 10},
            "endCoordinates": {"width": 10, "depth": 20, "height": 20}
        }
    }
]

# Generate JSON response
response_json = generate_stowage_response(True, placements, rearrangements)
print(response_json)