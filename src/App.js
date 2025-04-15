import React, { useState } from 'react';
import './App.css';

function App() {
  const [metrics, setMetrics] = useState(null);

  const runSimulation = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/run-simulation', {
        method: 'POST',
      });
      const data = await response.json();
      if (data.success) {
        setMetrics(data.metrics);
        alert(`Simulation Output: ${data.output}`);
      } else {
        alert(`Error: ${data.error}`);
      }
    } catch (error) {
      alert(`Request failed: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="banner">Car Wash Simulation</div>
        <p className="description">
          Welcome to the Car Wash Simulation! This simulation models the operations of a car wash, 
          providing insights into efficiency and customer service. Click the button below to run the simulation.
        </p>
        <button className="run-button" onClick={runSimulation}>Run Simulation</button>
        {metrics && (
          <div className="metrics">
            <h2>Simulation Metrics</h2>
            <p>Reneged Cars: {metrics.reneged_cars}</p>
            <p>Average Wait Time: {metrics.avg_wait_time} minutes</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
