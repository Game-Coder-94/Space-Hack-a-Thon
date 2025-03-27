from config import CONTAINER_CAPACITIES, INITIAL_STOWAGE_SOLUTION
from stowage_optimizer import StowageOptimizer
from rearrangement import RearrangementOptimizer
from retrieval import RetrievalOptimizer
from datetime import datetime
from rearrangement import RearrangementOptimizer


# Initialize with container capacities
container_capacities = {
    "Crew_Quarters": 100000,
    "Destiny": 80000,
    "Columbus": 90000
}

# Sample Containers
containers = [
    {
        "id": 1,
        "name": "Food Items",
        "width": 50,
        "depth": 50,
        "height": 50,
        "mass": 5,
        "priority": 80,
        "expiry": "2025-05-20",
        "usage": 30,
        "preferred-zone": "Crew_Quarters"
    },
    {
        "id": 2,
        "name": "Medical Kit",
        "width": 30,
        "depth": 30,
        "height": 30,
        "mass": 2,
        "priority": 90,
        "expiry": "2024-12-15",
        "usage": 60,
        "preferred-zone": "Columbus"
    }
]

rearrangement_optimizer = RearrangementOptimizer(INITIAL_STOWAGE_SOLUTION, CONTAINER_CAPACITIES)

new_item = {
    "id": 3,
    "name": "Medical Kit",
    "width": 20,
    "depth": 20,
    "height": 20,
    "mass": 10,
    "priority": 90,
    "expiry": "2026-01-01",
    "usage": 50,
    "preferred-zone": "Crew_Quarters"
}



# Define ISS Modules (width, depth, height in cm)
modules = {
    "Crew_Quarters": {"width": 100, "depth": 100, "height": 200},
    "Columbus": {"width": 150, "depth": 150, "height": 250}
}

if __name__ == "__main__":
    # Assuming you have an instance of RetrievalOptimizer
    stowage_solution = {
        "placements": [
            {
                "itemId": "item1",
                "name": "Food Pack",
                "position": {"startCoordinates": {"height": 1}, "endCoordinates": {"height": 2}},
                "containerId": "module1",
                "expiryDate": datetime(2025, 4, 1)
            },
            {
                "itemId": "item2",
                "name": "Food Pack",
                "position": {"startCoordinates": {"height": 3}, "endCoordinates": {"height": 4}},
                "containerId": "module1",
                "expiryDate": datetime(2025, 3, 30)
            }
        ]
    }

    optimizer = RetrievalOptimizer(stowage_solution)

    # Search for an item by name
    result = optimizer.search_item("Food Pack")

    # Print the result
    if result["success"]:
        print("Item found:", result)
    else:
        print("Error:", result["message"])

    rearrangement_result = rearrangement_optimizer.suggest_rearrangement(new_item)
    print("Rearrangement Result:", rearrangement_result)
