from src.config import MODULE_DIMENSIONS
from datetime import datetime
import random
import math

containers = [{
    'id' : 1,
    'name' : 'food-packet',
    'width' : 10,
    'height' : 10,
    'mass' : 5,
    'priority' : 80,
    'expiry-date' : '2025-05-20',
    'usage-limit' : 30,
    'preferred-zone' : 'crew-quaters'
}]

container = {
    'id' : 1,
    'name' : 'food-packet',
    'width' : 10,
    'height' : 10,
    'mass' : 5,
    'priority' : 80,
    'expiry' : '2025-05-20',
    'usage' : 30,
    'preferred-zone' : 'crew-quaters'
}

# containers = [container]

# Optimizer starts
class ISSStowageOptimizer:
    def __init__(self, modules, containers, initial_temp=100, cooling_rate=0.95, min_temp=1):
        self.modules = modules
        self.containers = containers
        self.temperature = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temp
        self.best_solution = None
        self.stowage = {}

    def initialize_solution(self):
        """Creates an initial placement using a heuristic (BFD-like)."""
        solution = {}
        available_space = {module: [] for module in self.modules}   # Track free spaces

        for container in sorted(self.containers, key=self.get_caontainer_volume, reverse=True):
            placed = False
            for module in self.modules:
                if self.can_fit(module, container, available_space[module]):
                    position = self.get_best_fit_position(module, container, available_space[module])
                    solution[container['id']] = {'module' : module, 'position' : position}
                    available_space[module].append(position)    # Mark space is occupied
                    placed = True
                    break   # Stop once placed

            if not placed:
                return None # No feasible initial solution
            
        return solution
    
    # Calculate Volume of a container
    def get_container_volume(self, container):
        return container['width'] * container['height'] * container['depth']
    
    def can_fit(self, module, container, occupied_positions):
        """Checks if the container can fit in the module without overlapping"""
        module_dims = self.modules[module]

        for x in range(0, module_dims['width'], 5):
            for y in range(0, module_dims['depth'], 5):
                for z in range(0, module_dims['height'], 5):
                    end_x = x + container['width']
                    end_y = y + container['depth']
                    end_z = z + container['height']

                    # Check if within module dimensions
                    if end_x > module_dims['width'] or end_y > module_dims['depth'] or end_z > module_dims['height']:
                        continue

                    # Check overlapping
                    if not any(self.overlaps(x, y, z, end_x, end_y, end_z, occ) for occ in occupied_positions):
                        return True
                    
        return False
    
    def get_best_fit_position(self, module, container, occupied_positions):
        """Finds the best placement with minimal wasted space"""
        module_dims = self.modules[module]
        best_position = None
        min_waste = float('inf')    # Didn't get it (understand)

        for x in range(0, module_dims['width'], 5):
            for y in range(0, module_dims['depth'], 5):
                for z in range(0, module_dims['height'], 5):
                    end_x = x + container['width']
                    end_y = y + container['depth']
                    end_z = z + container['height']

                    # Check if within module dimensions
                    if end_x > module_dims['width'] or end_y > module_dims['depth'] or end_z > module_dims['height']:
                        continue

                    # Check overlapping
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
        """Checks if two positions overlap"""
        return not (
            x2 <= occ["startCoordinates"]["width"] or x1 >= occ["endCoordinates"]["width"] or
            y2 <= occ["startCoordinates"]["depth"] or y1 >= occ["endCoordinates"]["depth"] or
            z2 <= occ["startCoordinates"]["height"] or z1 >= occ["endCoordinates"]["height"]
        )

    
    # # Function to find avaialble space
    # def find_space_in_module(self, module, container):
    #     """Finds an available space in the module for the container."""
    #     module_dims = MODULE_DIMENSIONS[module]
    #     occupied = []  # List of occupied spaces

    #     for placed in self.stowage.values():
    #         if placed["containerId"] == module:
    #             occupied.append(placed["position"])

    #     # Brute-force search for an available space
    #     for x in range(0, module_dims["width"], 5):
    #         for y in range(0, module_dims["depth"], 5):
    #             for z in range(0, module_dims["height"], 5):
    #                 end_x, end_y, end_z = x + container["width"], y + container["depth"], z + container["height"]

    #                 # Check if within module boundaries
    #                 if end_x > module_dims["width"] or end_y > module_dims["depth"] or end_z > module_dims["height"]:
    #                     continue

    #                 # Check for overlap with occupied spaces
    #                 overlap = False
    #                 for occ in occupied:
    #                     if not (
    #                         end_x <= occ["startCoordinates"]["width"] or
    #                         x >= occ["endCoordinates"]["width"] or
    #                         end_y <= occ["startCoordinates"]["depth"] or
    #                         y >= occ["endCoordinates"]["depth"] or
    #                         end_z <= occ["startCoordinates"]["height"] or
    #                         z >= occ["endCoordinates"]["height"]
    #                     ):
    #                         overlap = True
    #                         break

    #                 if not overlap:
    #                     return {
    #                         "startCoordinates": {"width": x, "depth": y, "height": z},
    #                         "endCoordinates": {"width": end_x, "depth": end_y, "height": end_z}
    #                     }

    #     return None  # No space found
    
    # Objective Function
    def objective_function(self, stwoage):
        module_weights = {module : 0 for module in self.modules}
        total_penalty = 0

        for container in self.containers:
            module = stwoage[container['id']]
            module_weights[module] += container['mass']

            priority = container.get('mass', 0)            

            if 'preferred-zone' in container and module == container['preferred-zone']:
                # Reward for correct placement
                total_penalty -= 20 * (priority / 100)
            else: 
                total_penalty += 15 * (priority / 100)
            
            expiry_date_str = container.get('expiry', '2100-01-01')     # Default (far future date expiry)
            expiry_date = datetime.strptime(container['expiry'], '%Y-%m-%d')
            days_to_expiry = (expiry_date - datetime.today()).days
            
            if days_to_expiry < 90:
                total_penalty += 10 * (priority / 100)
            
            usage = container.get('usage', 0)   # Default usage

            if container['usage'] > 50 and module not in ['Destiny', 'Columbus', 'Kibo']:
                total_penalty += 15 * (priority / 100)

        mass_imbalance = max(module_weights.values()) - min(module_weights.values())
        
        return mass_imbalance + total_penalty

    # Finding neighbour (slightly different )
    def generate_neighbour(self, stowage):
        new_stowage = stowage.copy()
        container_id = random.choice(list(stowage.keys()))
        new_stowage[container_id] = random.choice(self.modules)
        return new_stowage
    
    # Implementation of Simulated Anneling
    def simulated_annealing(self):
        current_solution = self.generate_initial_solution()
        best_solution = current_solution.copy()
        T = self.temperature

        while T > self.min_temperature:
            new_solution = self.generate_neighbour(current_solution)
            delta = self.objective_function(new_solution) - self.objective_function(current_solution)

            if delta < 0 or random.random() < math.exp(-delta / T):
                current_solution = new_solution.copy()
                if self.objective_function(current_solution) > self.objective_function(best_solution):
                    best_solution = current_solution.copy()

            T *= self.cooling_rate

        self.best_solution = best_solution
        self.stowage = best_solution
        return best_solution
    
    def display_solution(self):
        print('\n  Optimized ISS Stowage Plan  ')
        for container in self.containers:
            print(f'Container {container["id"]} ({container["name"]}) -> {self.best_solution[container["id"]]}')


