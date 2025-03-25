import random
import math
from datetime import datetime

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

    def generate_initial_solution(self):
        return{container['id'] : random.choice(self.modules) for container in self.containers}
    
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

    def generate_neighbour(self, stowage):
        new_stowage = stowage.copy()
        container_id = random.choice(list(stowage.keys()))
        new_stowage[container_id] = random.choice(self.modules)
        return new_stowage
    
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
        return best_solution
    
    def display_solution(self):
        print('\n  Optimized ISS Stowage Plan  ')
        for container in self.containers:
            print(f'Container {container["id"]} ({container["name"]}) -> {self.best_solution[container["id"]]}')



# Example data
if __name__ == "__main__":
    MODULES = ["Destiny", "Columbus", "Kibo", "Unity", "Zvezda"]
    
    # List of container dictionaries with detailed attributes
    CONTAINERS = [
        {
            'id': 1, 'name': 'Food items', 'width': 10, 'depth': 10, 'height': 10, 'mass': 5,
            'priority': 80, 'expiry': '2025-05-20', 'usage': 30, 'preferred-zone': 'Crew_Quaters'
        },
        {
            'id': 2, 'name': 'Medical Kit', 'width': 5, 'depth': 5, 'height': 5, 'mass': 2,
            'priority': 95, 'expiry': '2024-12-15', 'usage': 70, 'preferred-zone': 'Destiny'
        },
        {
            'id': 3, 'name': 'Toolbox', 'width': 15, 'depth': 10, 'height': 10, 'mass': 8,
            'priority': 60, 'expiry': '2030-01-01', 'usage': 20, 'preferred-zone': 'Unity'
        }
    ]

    optimizer = ISSStowageOptimizer(MODULES, CONTAINERS)
    optimizer.simulated_annealing()
    optimizer.display_solution()