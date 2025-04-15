from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the Car Wash Simulation API"

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content

@app.route('/run-simulation', methods=['POST'])
def run_simulation():
    try:
        # Run the car_wash_simulation.py script and capture metrics
        from car_wash_simulation import run_simulation_with_data
        _, _, _, longest_wait, average_wait, total_reneged = run_simulation_with_data(
            run_length=500, num_systems=2, max_queue_length=5, arrival_rate=0.6
        )

        return jsonify({
            'success': True,
            'metrics': {
                'reneged_cars': total_reneged,
                'avg_wait_time': average_wait,
                'longest_wait_time': longest_wait
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # Revert to HTTP
    app.run(debug=True)
