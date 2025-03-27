import datetime

class RetrievalOptimizer:
    def __init__(self, stowage_solution):
        self.stowage_solution = stowage_solution

    def is_obstructing(self, target_position, item_position):
        """
        Checks if an item obstructs the retrieval of another item.
        """
        # An item is obstructing if its position overlaps with the retrieval path
        return (
            item_position["startCoordinates"]["height"] < target_position["endCoordinates"]["height"]
            and item_position["endCoordinates"]["height"] > target_position["startCoordinates"]["height"]
        )

    def search_item(self, item_name):
        """
        Searches for an item based on ease of retrieval and closeness to expiry date.
        """
        candidates = [
            item for item in self.stowage_solution["placements"]
            if item["name"] == item_name
        ]

        if not candidates:
            return {"success": False, "message": "Item not found."}

        # Sort by expiry date (earliest first) and ease of retrieval (least obstructed)
        candidates.sort(
            key=lambda item: (
                item.get("expiryDate", datetime.datetime.max),
                self.get_obstruction_cost(item["position"])
            )
        )

        best_candidate = candidates[0]
        return {
            "success": True,
            "itemId": best_candidate["itemId"],
            "containerId": best_candidate["containerId"],
            "position": best_candidate["position"],
            "expiryDate": best_candidate.get("expiryDate"),
            "message": "Item found."
        }

    def retrieval_steps(self, item_id, new_container=None):
        """
        Returns the number of steps required to retrieve an item and optionally move it to a new container.
        """
        item_data = next((item for item in self.stowage_solution["placements"] if item["itemId"] == item_id), None)

        if not item_data:
            return {"success": False, "message": "Item not found in stowage."}

        target_position = item_data["position"]
        module = item_data["containerId"]

        obstructing_items = []

        for data in self.stowage_solution["placements"]:
            if data["itemId"] == item_id:
                continue  # Skip the item we're retrieving

            if data["containerId"] == module:
                if self.is_obstructing(target_position, data["position"]):
                    obstructing_items.append((data["itemId"], data["position"]))

        # If no obstruction, direct retrieval (0 moves)
        if not obstructing_items:
            retrieval_result = {
                "success": True,
                "retrieval_steps": 0,
                "rearrangements": [],
                "message": "Item is directly accessible."
            }
        else:
            # Sort obstructing items by least effort to move
            obstructing_items.sort(key=lambda x: self.get_obstruction_cost(x[1]))

            # Generate rearrangement steps
            rearrangements = []
            step_count = 1
            for blocking_id, position in obstructing_items:
                rearrangements.append({
                    "step": step_count,
                    "action": "move",
                    "itemId": blocking_id,
                    "fromContainer": module,
                    "fromPosition": position,
                    "toContainer": module,  # Temporarily placed somewhere else in the module
                    "toPosition": self.find_temporary_space(module)
                })
                step_count += 1

            retrieval_result = {
                "success": True,
                "retrieval_steps": len(rearrangements),
                "rearrangements": rearrangements,
                "message": f"Item retrieved with {len(rearrangements)} moves."
            }

        # If a new container is specified, log the relocation
        if new_container:
            retrieval_result["newContainer"] = new_container
            self.log_action(item_id, module, target_position, new_container)

        return retrieval_result

    def log_action(self, item_id, from_container, from_position, to_container):
        """
        Logs the retrieval action in the database.
        """
        log_entry = {
            "itemId": item_id,
            "retrievedBy": "Astronaut",  # Replace with actual user info
            "timestamp": datetime.datetime.now().isoformat(),
            "fromContainer": from_container,
            "fromPosition": from_position,
            "toContainer": to_container
        }
        # Simulate logging (replace with actual database call)
        print("Log Entry:", log_entry)

    def get_obstruction_cost(self, position):
        """
        Calculates the obstruction cost for a given position.
        """
        # Placeholder for obstruction cost calculation
        return position["startCoordinates"]["height"]

    def find_temporary_space(self, module):
        """
        Finds a temporary space in the module for rearranging items.
        """
        # Placeholder for finding temporary space
        return {"startCoordinates": {"height": 0}, "endCoordinates": {"height": 1}}
