import React from 'react';

function App() {
  const runSimulation = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/run-simulation', {
        method: 'POST',
      });
      const data = await response.json();
      if (data.success) {
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
        <h1>Car Wash Simulation</h1>
        <button onClick={runSimulation}>Run Simulation</button>
      </header>
    </div>
  );
}

export default App;
