from flask import Flask, render_template, request, jsonify
from src.rearrangement import RearrangementOptimizer
from src.config import CONTAINER_CAPACITIES, INITIAL_STOWAGE_SOLUTION

app = Flask(__name__, template_folder='front_end')

# Initialize optimizer
rearrangement_optimizer = RearrangementOptimizer(INITIAL_STOWAGE_SOLUTION, CONTAINER_CAPACITIES)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json  # Get JSON data from frontend

    new_item = {
        "id": data["id"],
        "name": data["name"],
        "width": data["width"],
        "depth": data["depth"],
        "height": data["height"],
        "mass": data["mass"],
        "priority": data["priority"],
        "expiry": data["expiry"],
        "usage": data["usage"],
        "preferred-zone": data["preferred_zone"]
    }

    # Run rearrangement logic
    result = rearrangement_optimizer.suggest_rearrangement(new_item)
    
    return jsonify(result)  # Send JSON response

if __name__ == '__main__':
    app.run(debug=True)
