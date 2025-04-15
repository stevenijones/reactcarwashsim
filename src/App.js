import React, { useState } from 'react';
import './App.css';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from 'recharts';

function App() {
  const [metrics, setMetrics] = useState(null);
  const [detailedData, setDetailedData] = useState(null);
  const [parameters, setParameters] = useState({
    runLength: 500,
    numSystems: 2,
    maxQueueLength: 5,
    arrivalRate: 0.6,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setParameters({
      ...parameters,
      [name]: value,
    });
  };

  const runSimulation = async () => {
    try {
      setMetrics(null); // Reset metrics before making a new request
      setDetailedData(null); // Reset detailed data
      const response = await fetch('http://127.0.0.1:5000/run-simulation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(parameters),
      });
      const data = await response.json();
      if (data.success) {
        setMetrics(data.metrics);
        setDetailedData(data.detailed_data);
      } else {
        console.error(`Error: ${data.error}`);
      }
    } catch (error) {
      console.error(`Request failed: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="banner">Car Wash Simulation</div>
        <p className="description">
          Welcome to the Car Wash Simulation! Adjust the parameters below and click the button to run the simulation.
        </p>
        <div className="parameters">
          <div className="parameter-row">
            <label>
              Run Length:
              <input
                type="number"
                name="runLength"
                value={parameters.runLength}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="parameter-row">
            <label>
              Number of Systems:
              <input
                type="number"
                name="numSystems"
                value={parameters.numSystems}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="parameter-row">
            <label>
              Max Queue Length:
              <input
                type="number"
                name="maxQueueLength"
                value={parameters.maxQueueLength}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <div className="parameter-row">
            <label>
              Arrival Rate:
              <input
                type="number"
                step="0.1"
                name="arrivalRate"
                value={parameters.arrivalRate}
                onChange={handleInputChange}
              />
            </label>
          </div>
        </div>
        <button className="run-button" onClick={runSimulation}>Run Simulation</button>
        {metrics && (
          <div className="metrics">
            <h2>Simulation Metrics</h2>
            <p>Reneged Cars: {metrics.reneged_cars}</p>
            <p>Average Wait Time: {metrics.avg_wait_time.toFixed(1)} minutes</p>
            <p>Longest Wait Time: {metrics.longest_wait_time.toFixed(1)} minutes</p>
          </div>
        )}
        {detailedData && (
          <div className="charts">
            <h2>Detailed Data</h2>
            <div className="chart">
              <h3>Queue Data</h3>
              <LineChart width={600} height={300} data={detailedData.queue_data}>
                <Line type="monotone" dataKey="value" stroke="#8884d8" />
                <CartesianGrid stroke="#ccc" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
              </LineChart>
            </div>
            <div className="chart">
              <h3>Car Wash Data</h3>
              <LineChart width={600} height={300} data={detailedData.car_wash_data}>
                <Line type="monotone" dataKey="value" stroke="#82ca9d" />
                <CartesianGrid stroke="#ccc" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
              </LineChart>
            </div>
            <div className="chart">
              <h3>Lost Cars Data</h3>
              <LineChart width={600} height={300} data={detailedData.lost_cars_data}>
                <Line type="monotone" dataKey="value" stroke="#ff7300" />
                <CartesianGrid stroke="#ccc" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />
              </LineChart>
            </div>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
