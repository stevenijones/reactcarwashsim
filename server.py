from flask import Flask, jsonify, request
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
        # Get parameters from the request
        params = request.get_json()
        run_length = int(params.get('runLength', 500))  # Convert to integer
        num_systems = int(params.get('numSystems', 2))  # Convert to integer
        max_queue_length = int(params.get('maxQueueLength', 5))  # Convert to integer
        arrival_rate = float(params.get('arrivalRate', 0.6))  # Convert to float

        # Log the received parameters for debugging
        print(f"Received parameters: runLength={run_length}, numSystems={num_systems}, maxQueueLength={max_queue_length}, arrivalRate={arrival_rate}")

        # Run the car_wash_simulation.py script and capture metrics
        from car_wash_simulation import run_simulation_with_data
        _, _, _, longest_wait, average_wait, total_reneged = run_simulation_with_data(
            run_length=run_length, num_systems=num_systems, max_queue_length=max_queue_length, arrival_rate=arrival_rate
        )

        output = (
            f"Simulation completed successfully.\n"
            f"Longest Wait Time: {longest_wait} minutes\n"
            f"Average Wait Time: {average_wait} minutes\n"
            f"Total Reneged Cars: {total_reneged}"
        )

        # Log the response for debugging
        response = {
            'success': True,
            'output': output,
            'metrics': {
                'reneged_cars': total_reneged,
                'avg_wait_time': average_wait,
                'longest_wait_time': longest_wait
            }
        }
        print(f"Response: {response}")

        return jsonify(response)
    except Exception as e:
        error_response = {
            'success': False,
            'error': str(e)
        }
        print(f"Error Response: {error_response}")
        return jsonify(error_response)

if __name__ == '__main__':
    # Revert to HTTP
    app.run(debug=True)
