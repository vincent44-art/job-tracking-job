import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = "http://127.0.0.1:5000/api/dashboard/overview";

function DriverDashboard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchDashboardData = async () => {
            const token = localStorage.getItem('access_token');
            if (!token) {
                navigate('/login');
                return;
            }

            try {
                const response = await axios.get(API_URL, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                setStats(response.data.data);
                setLoading(false);
            } catch (err) {
                setError('Failed to fetch dashboard data.');
                setLoading(false);
                if (err.response && err.response.status === 401) {
                    localStorage.removeItem('access_token');
                    navigate('/login');
                }
            }
        };

        fetchDashboardData();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        navigate('/login');
    };

    if (loading) return <div>Loading dashboard...</div>;
    if (error) return <div className="dashboard-container"><p className="error-message">{error}</p><button onClick={handleLogout}>Logout</button></div>;

    return (
        <div className="dashboard-container">
            <h2>Driver Dashboard</h2>
            <p>Welcome, {stats.username}!</p>
            <div className="stats-grid">
                <div className="stat-card">
                    <h3>Pending Deliveries</h3>
                    <p>{stats.pending_deliveries}</p>
                </div>
                <div className="stat-card">
                    <h3>Completed Deliveries</h3>
                    <p>{stats.completed_deliveries}</p>
                </div>
            </div>
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
}

export default DriverDashboard;