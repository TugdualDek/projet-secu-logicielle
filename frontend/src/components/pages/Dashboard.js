// frontend/src/components/dashboard/Dashboard.js

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import TargetForm from './TargetForm';
import ScanStatus from './ScanStatus';
import '../../styles/dashboard.css';

function Dashboard() {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [scanStatus, setScanStatus] = useState(null);

    useEffect(() => {
        const userData = sessionStorage.getItem('user');
        if (!userData) {
            navigate('/login');
            return;
        }
        setUser(JSON.parse(userData));
    }, [navigate]);

    const handleLogout = async () => {
        try {
            await api.post('/auth/logout');
            sessionStorage.removeItem('user');
            navigate('/login');
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    if (!user) return null;

    return (
        <div className="dashboard-container">
            <nav className="dashboard-nav">
                <h1>FortiCheck Dashboard</h1>
                <button onClick={handleLogout} className="logout-button">
                    Logout
                </button>
            </nav>

            <main className="dashboard-main">
                <section className="welcome-section">
                    <h2>Welcome, {user.username}!</h2>
                </section>

                <section className="scan-section">
                    <TargetForm onScanStart={setScanStatus} />
                    {scanStatus && <ScanStatus status={scanStatus} />}
                </section>
            </main>
        </div>
    );
}

export default Dashboard;