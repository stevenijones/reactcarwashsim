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
        # Run the car_wash_simulation.py script
        result = subprocess.run(['python', 'car_wash_simulation.py'], capture_output=True, text=True)
        return jsonify({
            'success': True,
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # Revert to HTTP
    app.run(debug=True)
