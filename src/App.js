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
      <div className="banner">
        <h1>Car Wash Simulation</h1>
        <p>Welcome to the Car Wash Simulation! Adjust the parameters below and click the button to run the simulation.</p>
      </div>
      <div className="content">
        <div className="parameters-container">
          <h2>Simulation Parameters</h2>
          <div className="parameters">
            <label>
              <span>Run Length:</span>
              <input
                type="number"
                name="runLength"
                value={parameters.runLength}
                onChange={handleInputChange}
              />
            </label>
            <label>
              <span>Number of Systems:</span>
              <input
                type="number"
                name="numSystems"
                value={parameters.numSystems}
                onChange={handleInputChange}
              />
            </label>
            <label>
              <span>Max Queue Length:</span>
              <input
                type="number"
                name="maxQueueLength"
                value={parameters.maxQueueLength}
                onChange={handleInputChange}
              />
            </label>
            <label>
              <span>Arrival Rate:</span>
              <input
                type="number"
                step="0.1"
                name="arrivalRate"
                value={parameters.arrivalRate}
                onChange={handleInputChange}
              />
            </label>
          </div>
          <button className="run-button" onClick={runSimulation}>Run Simulation</button>
        </div>
        <div className="results-container">
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
              <div className="chart">
                <h3>Queue Data</h3>
                <LineChart width={400} height={200} data={detailedData.queue_data}>
                  <Line type="monotone" dataKey="value" stroke="#61dafb" dot={false} />
                  <CartesianGrid stroke="#444" />
                  <XAxis dataKey="time" stroke="#a0a0a0" />
                  <YAxis stroke="#a0a0a0" />
                  <Tooltip contentStyle={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }} />
                  <Legend />
                </LineChart>
              </div>
              <div className="chart">
                <h3>Car Wash Data</h3>
                <LineChart width={400} height={200} data={detailedData.car_wash_data}>
                  <Line type="monotone" dataKey="value" stroke="#82ca9d" dot={false} />
                  <CartesianGrid stroke="#444" />
                  <XAxis dataKey="time" stroke="#a0a0a0" />
                  <YAxis stroke="#a0a0a0" />
                  <Tooltip contentStyle={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }} />
                  <Legend />
                </LineChart>
              </div>
              <div className="chart">
                <h3>Lost Cars Data</h3>
                <LineChart width={400} height={200} data={detailedData.lost_cars_data}>
                  <Line type="monotone" dataKey="value" stroke="#ff7300" dot={false} />
                  <CartesianGrid stroke="#444" />
                  <XAxis dataKey="time" stroke="#a0a0a0" />
                  <YAxis stroke="#a0a0a0" />
                  <Tooltip contentStyle={{ backgroundColor: '#2a2a2a', border: '1px solid #444' }} />
                  <Legend />
                </LineChart>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
