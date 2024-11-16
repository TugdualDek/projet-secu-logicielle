import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
    const [target, setTarget] = useState('');
    const [error, setError] = useState(null);
    const [scanning, setScanning] = useState(false);

    function handleSubmit(e) {
        e.preventDefault();
        // Add logic for handling the submission here
        // For example, set scanning state and handle errors if needed
        setScanning(true);

        // Simulated scan delay, replace with your actual scan logic
        setTimeout(() => {
            setScanning(false);
            setError('An example error occurred.');
        }, 3000);
    }

    return (
        <div className="target-form">
            <h3>Start Bruteforce Scan</h3>
            {error && <div className="error-message">{error}</div>}
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <input
                        type="url"
                        value={target}
                        onChange={(e) => setTarget(e.target.value)}
                        placeholder="Enter target URL (e.g., http://example.com)"
                        required
                    />
                </div>
                <button
                    type="submit"
                    disabled={scanning}
                    className="scan-button"
                >
                    {scanning ? 'Scanning...' : 'Start Scan'}
                </button>
            </form>
        </div>
    );
}

export default App;