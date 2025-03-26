import json

def generate_stowage_response(stowage, retrieval):
    """Formats the output in the required JSON structure."""
    placements = [
        {
            "itemId": item_id,
            "containerId": module,
            "position": {
                "startCoordinates": {"width": 0, "depth": 0, "height": 0},  # Example coordinates
                "endCoordinates": {"width": 10, "depth": 10, "height": 10}
            }
        }
        for item_id, module in stowage.items()
    ]

    rearrangements = [
        {
            "step": 1,
            "action": "move",
            "itemId": retrieval["itemId"],
            "fromContainer": "Unknown",
            "fromPosition": {
                "startCoordinates": {"width": 5, "depth": 5, "height": 5},
                "endCoordinates": {"width": 15, "depth": 15, "height": 15}
            },
            "toContainer": retrieval["module"],
            "toPosition": {
                "startCoordinates": {"width": 0, "depth": 10, "height": 10},
                "endCoordinates": {"width": 10, "depth": 20, "height": 20}
            }
        }
    ]

    response = {
        "success": True,
        "placements": placements,
        "rearrangements": rearrangements
    }
    
    return json.dumps(response, indent=4)
