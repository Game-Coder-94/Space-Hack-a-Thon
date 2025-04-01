# Container capacities for different modules
CONTAINER_CAPACITIES = {
    "Crew_Quarters": 100000,
    "Destiny": 80000,
    "Columbus": 90000
}

# Initial stowage solution (example data)
INITIAL_STOWAGE_SOLUTION = {
    "placements": [
        {
            "itemId": "item1",
            "name": "Food Pack",
            "position": {"startCoordinates": {"height": 1}, "endCoordinates": {"height": 2}},
            "containerId": "module1",
            "expiryDate": "2025-04-01"
        },
        {
            "itemId": "item2",
            "name": "Food Pack",
            "position": {"startCoordinates": {"height": 3}, "endCoordinates": {"height": 4}},
            "containerId": "module1",
            "expiryDate": "2025-03-30"
        }
    ]
}

# Simulated Database
# Search logic using this database
containers = {
    "A1": [{"itemId": "101", "itemName": "Oxygen Tank", "userId": "U123"},
           {"itemId": "102", "itemName": "Water Supply", "userId": "U124"}],
    "B1": [{"itemId": "201", "itemName": "Medical Kit", "userId": "U123"},
           {"itemId": "202", "itemName": "Food Pack", "userId": "U125"}]
}

def get_all_items():
    all_items = []
    for container_id, items in containers.items():
        for item in items:
            all_items.append({**item, "containerId": container_id})
    return sorted(all_items, key=lambda x: x['itemId'])