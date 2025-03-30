from database import CONTAINER_CAPACITIES, INITIAL_STOWAGE_SOLUTION
from rearrangement import RearrangementOptimizer
from retrieval import RetrievalOptimizer
from services.placement_service import StowageOptimizer
from datetime import datetime

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
    # Initialize StowageOptimizer
    optimizer = StowageOptimizer(containers, modules)

    # Run the optimization
    placement_result = optimizer.simulated_annealing()

    # Print the result
    print("Placement Result:", placement_result)

    # Initialize RetrievalOptimizer
    retrieval_optimizer = RetrievalOptimizer(INITIAL_STOWAGE_SOLUTION)

    # Search for an item by name
    result = retrieval_optimizer.search_item("Food Pack")

    # Print the result
    if result["success"]:
        print("Item found:", result)
    else:
        print("Error:", result["message"])

    # Initialize RearrangementOptimizer
    rearrangement_optimizer = RearrangementOptimizer(INITIAL_STOWAGE_SOLUTION, CONTAINER_CAPACITIES)

    # Suggest rearrangement for the new item
    rearrangement_result = rearrangement_optimizer.suggest_rearrangement(new_item)
    print("Rearrangement Result:", rearrangement_result)
