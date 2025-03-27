# === Container Capacities ===
CONTAINER_CAPACITIES = {
    "Crew_Quarters": 100000,
    "Destiny": 80000,
    "Columbus": 90000,
    "Kibo": 85000
}

# === Initial Stowage Solution ===
INITIAL_STOWAGE_SOLUTION = {
    "placements": [
        {
            "itemId": 1,
            "containerId": "Crew_Quarters",
            "position": {
                "startCoordinates": {"width": 0, "depth": 0, "height": 0},
                "endCoordinates": {"width": 50, "depth": 50, "height": 50}
            },
            "priority": 30
        },
        {
            "itemId": 2,
            "containerId": "Crew_Quarters",
            "position": {
                "startCoordinates": {"width": 0, "depth": 0, "height": 50},
                "endCoordinates": {"width": 30, "depth": 30, "height": 80}
            },
            "priority": 60
        }
    ]
}
