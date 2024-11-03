import React from 'react';
import '../../styles/dashboard.css';

function ScanStatus({ status }) {
    if (!status) return null;

    const { results } = status;
    const successful = results.successful_attempts || [];

    return (
        <div className="scan-status">
            <h3>Scan Results</h3>

            <div className="status-details">
                <p><strong>Status:</strong> {results.status}</p>
                <p><strong>Target:</strong> {results.target}</p>
                <p><strong>Duration:</strong> {results.duration?.toFixed(2)}s</p>
                <p><strong>Total Attempts:</strong> {results.total_attempts}</p>
                <p><strong>Severity:</strong>
                    <span className={`severity-${results.severity}`}>
                        {results.severity}
                    </span>
                </p>
            </div>

            {successful.length > 0 && (
                <div className="vulnerabilities-found">
                    <h4>Vulnerabilities Found:</h4>
                    <ul>
                        {successful.map((attempt, index) => (
                            <li key={index}>
                                Username: {attempt.username}, Password: {attempt.password}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {results.error && (
                <div className="scan-error">
                    <p>Error: {results.error}</p>
                </div>
            )}
        </div>
    );
}

export default ScanStatus;