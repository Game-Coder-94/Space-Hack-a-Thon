import math
import random
from datetime import datetime

class StowageOptimizer:
    def __init__(self, containers, modules, initial_temp=1000, cooling_rate=0.99, min_temp=1):
        self.containers = containers  # List of container dictionaries
        self.modules = modules  # Dictionary of ISS Modules with dimensions
        self.temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.current_solution = self.initialize_solution()
        self.best_solution = self.current_solution

    def initialize_solution(self):
        """Creates an initial placement using a heuristic approach."""
        solution = {}
        available_space = {module: [] for module in self.modules}  

        for container in sorted(self.containers, key=self.get_container_volume, reverse=True):
            placed = False
            for module in self.modules:
                if self.can_fit(module, container, available_space[module]):
                    position = self.get_best_fit_position(module, container, available_space[module])
                    solution[container["id"]] = {"module": module, "position": position}
                    available_space[module].append(position)  # Mark space as occupied
                    placed = True
                    break 

            if not placed:
                return None  

        return solution

    def get_container_volume(self, container):
        return container["width"] * container["depth"] * container["height"]

    def can_fit(self, module, container, occupied_positions):
        """Checks if the container can fit in the module without overlapping."""
        module_dims = self.modules[module]

        for x in range(0, module_dims["width"], 5):
            for y in range(0, module_dims["depth"], 5):
                for z in range(0, module_dims["height"], 5):
                    end_x = x + container["width"]
                    end_y = y + container["depth"]
                    end_z = z + container["height"]

                    if end_x > module_dims["width"] or end_y > module_dims["depth"] or end_z > module_dims["height"]:
                        continue

                    if not any(self.overlaps(x, y, z, end_x, end_y, end_z, occ) for occ in occupied_positions):
                        return True  

        return False

    def get_best_fit_position(self, module, container, occupied_positions):
        """Finds the best placement with minimal wasted space."""
        module_dims = self.modules[module]
        best_position = None
        min_waste = float('inf')

        for x in range(0, module_dims["width"], 5):
            for y in range(0, module_dims["depth"], 5):
                for z in range(0, module_dims["height"], 5):
                    end_x = x + container["width"]
                    end_y = y + container["depth"]
                    end_z = z + container["height"]

                    if end_x > module_dims["width"] or end_y > module_dims["depth"] or end_z > module_dims["height"]:
                        continue

                    if not any(self.overlaps(x, y, z, end_x, end_y, end_z, occ) for occ in occupied_positions):
                        waste = (module_dims["width"] * module_dims["depth"] * module_dims["height"]) - self.get_container_volume(container)
                        if waste < min_waste:
                            min_waste = waste
                            best_position = {
                                "startCoordinates": {"width": x, "depth": y, "height": z},
                                "endCoordinates": {"width": end_x, "depth": end_y, "height": end_z}
                            }

        return best_position

    def overlaps(self, x1, y1, z1, x2, y2, z2, occ):
        """Checks if two positions overlap."""
        return not (
            x2 <= occ["startCoordinates"]["width"] or x1 >= occ["endCoordinates"]["width"] or
            y2 <= occ["startCoordinates"]["depth"] or y1 >= occ["endCoordinates"]["depth"] or
            z2 <= occ["startCoordinates"]["height"] or z1 >= occ["endCoordinates"]["height"]
        )

    def objective_function(self, solution):
        """Evaluates the quality of the placement (minimize wasted space & prioritize expiry)."""
        total_wasted_space = 0
        priority_score = 0
        expiry_penalty = 0

        for container_id, data in solution.items():
            container = next(c for c in self.containers if c["id"] == container_id)
            module = data["module"]
            total_wasted_space += self.get_container_volume(container)

            # Priority factor (higher is better)
            priority_score += container["priority"]

            # Expiry factor (penalize expired items)
            expiry_date = datetime.strptime(container["expiry"], '%Y-%m-%d')
            days_to_expiry = (expiry_date - datetime.today()).days
            expiry_penalty += max(0, 100 - days_to_expiry)

        return priority_score - (total_wasted_space + expiry_penalty)

    def generate_neighbor(self, solution):
        """Creates a new solution by moving one container."""
        new_solution = solution.copy()
        container_id = random.choice(list(new_solution.keys()))
        new_module = random.choice(list(self.modules.keys()))

        if new_module != new_solution[container_id]["module"]:
            new_solution[container_id] = {
                "module": new_module,
                "position": self.get_best_fit_position(new_module, next(c for c in self.containers if c["id"] == container_id), [])
            }

        return new_solution

    def simulated_annealing(self):
        """Runs the Simulated Annealing process."""
        current_solution = self.current_solution
        best_solution = current_solution
        best_score = self.objective_function(current_solution)

        while self.temp > self.min_temp:
            new_solution = self.generate_neighbor(current_solution)
            new_score = self.objective_function(new_solution)

            delta = new_score - best_score
            if delta > 0 or math.exp(delta / self.temp) > random.random():
                current_solution = new_solution
                best_score = new_score

                if best_score > self.objective_function(best_solution):
                    best_solution = new_solution

            self.temp *= self.cooling_rate  

        self.best_solution = best_solution
        return self.generate_stowage_response()

    def generate_stowage_response(self):
        """Formats final placements into JSON structure."""
        placements = [
            {
                "itemId": item_id,
                "containerId": data["module"],
                "position": data["position"]
            }
            for item_id, data in self.best_solution.items()
        ]

        return {
            "success": True,
            "placements": placements,
            "rearrangements": []  # Retrieval logic will be added later
        }
