from src.services.rearrangement import RearrangementOptimizer

class StowageOptimizer:
    def __init__(self, containers, modules, initial_temp=1000, cooling_rate=0.99, min_temp=1):
        self.containers = containers  # List of container dictionaries
        self.modules = modules  # Dictionary of ISS Modules with dimensions
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.current_solution = self.initialize_solution()
        self.best_solution = self.current_solution

        # Initialize RearrangementOptimizer
        self.rearrangement_optimizer = RearrangementOptimizer(self.current_solution, self.get_container_capacities())

    def initialize_solution(self):
        """Creates an initial placement using a heuristic approach."""
        solution = {"placements": []}
        available_space = {module: [] for module in self.modules}

        for container in sorted(self.containers, key=self.get_container_volume, reverse=True):
            placed = False
            for module in self.modules:
                if self.can_fit(module, container, available_space[module]):
                    position = self.get_best_fit_position(module, container, available_space[module])
                    solution["placements"].append({
                        "itemId": container["id"],
                        "name": container["name"],
                        "position": position,
                        "containerId": module,
                        "priority": container["priority"]
                    })
                    placed = True
                    break

            if not placed:
                # Handle unplaced containers
                solution["placements"].append({
                    "itemId": container["id"],
                    "name": container["name"],
                    "position": None,
                    "containerId": None,
                    "priority": container["priority"],
                    "status": "unplaced"
                })

        return solution

    def get_container_capacities(self):
        """Returns a dictionary of container capacities."""
        return {module: self.modules[module]["width"] * self.modules[module]["depth"] * self.modules[module]["height"] for module in self.modules}

    def optimize_placements(self, new_item):
        """
        Optimizes the placement of a new item.
        """
        # Check if the new item can be placed directly
        preferred_zone = new_item["preferred-zone"]
        required_volume = self.get_container_volume(new_item)
        available_volume = self.rearrangement_optimizer.get_available_space(preferred_zone)

        if available_volume >= required_volume:
            # Place the item directly
            position = {
                "startCoordinates": {"width": 0, "depth": 0, "height": 0},
                "endCoordinates": {"width": new_item["width"], "depth": new_item["depth"], "height": new_item["height"]}
            }
            self.current_solution["placements"].append({
                "itemId": new_item["id"],
                "name": new_item["name"],
                "position": position,
                "containerId": preferred_zone,
                "priority": new_item["priority"]
            })
            return {"success": True, "message": "Item placed successfully."}

        # If not enough space, use RearrangementOptimizer
        rearrangement_result = self.rearrangement_optimizer.suggest_rearrangement(new_item)
        if rearrangement_result["success"]:
            return {
                "success": True,
                "message": "Rearrangement completed to fit the new item.",
                "rearrangements": rearrangement_result["rearrangements"]
            }
        else:
            return {
                "success": False,
                "message": "Unable to fit the new item even after rearrangement."
            }

    def get_container_volume(self, container):
        """Calculates the volume of a container."""
        return container["width"] * container["depth"] * container["height"]

    def can_fit(self, module, container, occupied_positions):
        """Checks if the container can fit in the module without overlapping."""
        module_dims = self.modules[module]
        container_volume = self.get_container_volume(container)
        available_volume = module_dims["width"] * module_dims["depth"] * module_dims["height"]
        return container_volume <= available_volume

    def get_best_fit_position(self, module, container, occupied_positions):
        """Finds the best position for the container in the module using Best-Fit Decreasing algorithm."""
        module_dims = self.modules[module]
        container_dims = (container["width"], container["depth"], container["height"])

        # Sort occupied positions by their start coordinates
        occupied_positions = sorted(occupied_positions, key=lambda pos: (
            pos["startCoordinates"]["width"],
            pos["startCoordinates"]["depth"],
            pos["startCoordinates"]["height"]
        ))

        # Iterate through the module space to find the best fit
        for width in range(module_dims["width"] - container_dims[0] + 1):
            for depth in range(module_dims["depth"] - container_dims[1] + 1):
                for height in range(module_dims["height"] - container_dims[2] + 1):
                    # Check if the container fits without overlapping
                    position = {
                        "startCoordinates": {"width": width, "depth": depth, "height": height},
                        "endCoordinates": {
                            "width": width + container_dims[0],
                            "depth": depth + container_dims[1],
                            "height": height + container_dims[2]
                        }
                    }
                    if not self.is_overlapping(position, occupied_positions):
                        return position

        # If no position is found, return None
        return None

    def is_overlapping(self, position, occupied_positions):
        """Checks if a position overlaps with any occupied positions."""
        for occupied in occupied_positions:
            if not (
                position["endCoordinates"]["width"] <= occupied["startCoordinates"]["width"] or
                position["startCoordinates"]["width"] >= occupied["endCoordinates"]["width"] or
                position["endCoordinates"]["depth"] <= occupied["startCoordinates"]["depth"] or
                position["startCoordinates"]["depth"] >= occupied["endCoordinates"]["depth"] or
                position["endCoordinates"]["height"] <= occupied["startCoordinates"]["height"] or
                position["startCoordinates"]["height"] >= occupied["endCoordinates"]["height"]
            ):
                return True
        return False

    def place(self, item, container_id):
        """
        Places an item in the specified container and updates the solution.
        """
        # Check if the container exists
        if container_id not in self.modules:
            return {"success": False, "message": "Invalid container ID."}

        # Check if the item can fit in the container
        container_dims = self.modules[container_id]
        item_volume = self.get_container_volume(item)
        container_volume = container_dims["width"] * container_dims["depth"] * container_dims["height"]

        if item_volume > container_volume:
            return {"success": False, "message": "Item does not fit in the specified container."}

        # Find the best position for the item in the container
        position = self.get_best_fit_position(container_id, item, [])

        # Add the item to the solution
        self.current_solution["placements"].append({
            "itemId": item["id"],
            "name": item["name"],
            "position": position,
            "containerId": container_id,
            "priority": item["priority"]
        })

        return {"success": True, "message": "Item placed and stored successfully."}