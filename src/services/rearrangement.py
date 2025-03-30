class RearrangementOptimizer:
    def __init__(self, stowage_solution, container_capacity):
        self.stowage_solution = stowage_solution
        self.container_capacity = container_capacity  # Dict {containerId: max volume}

    def suggest_rearrangement(self, new_item):
        """Suggests which low-priority items to move if space is insufficient."""
        # Ensure the new item has a valid position
        if "position" not in new_item or not new_item["position"]:
            return {"success": False, "message": "New item is missing position data."}

        container_id = new_item["preferred-zone"]
        required_volume = self.calculate_volume(new_item)

        # Check if there's enough space in the preferred container
        available_volume = self.get_available_space(container_id)

        if available_volume >= required_volume:
            return {
                "success": True,
                "message": "Sufficient space available. No rearrangement needed."
            }

        # If space is not enough, find low-priority items to move
        removable_items = sorted(
            [item for item in self.stowage_solution["placements"] if item["containerId"] == container_id],
            key=lambda x: x["priority"]
        )

        moved_items = []
        freed_space = 0
        step_count = 1

        for item in removable_items:
            item_volume = self.calculate_volume(item)
            moved_items.append({
                "step": step_count,
                "action": "move",
                "itemId": item["itemId"],
                "fromContainer": container_id,
                "toContainer": self.find_alternative_container(container_id, item_volume),
            })
            freed_space += item_volume
            step_count += 1

            if freed_space >= required_volume:
                break

        if freed_space < required_volume:
            return {
                "success": False,
                "message": "Insufficient space, cannot accommodate new item."
            }

        return {
            "success": True,
            "message": "Rearrangement required to fit new item.",
            "rearrangements": moved_items
        }

    def calculate_volume(self, item):
        """Calculates volume of an item."""
        if "position" not in item or not item["position"]:
            raise KeyError("Item is missing 'position' key.")

        return (
            (item["position"]["endCoordinates"]["width"] - item["position"]["startCoordinates"]["width"]) *
            (item["position"]["endCoordinates"]["depth"] - item["position"]["startCoordinates"]["depth"]) *
            (item["position"]["endCoordinates"]["height"] - item["position"]["startCoordinates"]["height"])
        )

    def get_available_space(self, container_id):
        """Calculates available space in a container."""
        used_volume = sum(self.calculate_volume(item) for item in self.stowage_solution["placements"] if item["containerId"] == container_id)
        return self.container_capacity[container_id] - used_volume

    def find_alternative_container(self, current_container, item_volume):
        """Finds an alternative container with enough space."""
        for container, max_capacity in self.container_capacity.items():
            if container != current_container and self.get_available_space(container) >= item_volume:
                return container
        return "No alternative found"
