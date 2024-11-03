import React, { useState } from 'react';
import api from '../../services/api';
import '../../styles/dashboard.css';

function TargetForm({ onScanStart }) {
    const [target, setTarget] = useState('');
    const [scanning, setScanning] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setScanning(true);

        try {
            const response = await api.post('/scan/start', {
                target: target,
                scan_type: 'bruteforce'
            });

            onScanStart(response.data);
        } catch (err) {
            setError(err.response?.data?.error || 'Scan failed');
        } finally {
            setScanning(false);
        }
    };

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

export default TargetForm;