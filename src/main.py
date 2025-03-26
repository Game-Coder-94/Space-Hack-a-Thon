from src.stowage_optimizer import ISSStowageOptimizer
from src.retrieval import suggest_fastest_retrieval
from src.utils import generate_stowage_response


def main():
    optimizer = ISSStowageOptimizer()
    optimizer.simulated_annealing()  # Run optimization
    retrieval = suggest_fastest_retrieval(optimizer)  # Suggest fastest item

    # Generate response
    response = generate_stowage_response(optimizer.stowage, retrieval)
    print(response)

if __name__ == "__main__":
    main()



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
    optimizer.suggest_fastest_retrieval()