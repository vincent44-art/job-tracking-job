import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';

// We'll create these dashboard pages in the next step
import CEODashboard from './pages/CEODashboard';
import StorekeeperDashboard from './pages/StorekeeperDashboard'; // <-- Corrected path here
import SellerDashboard from './pages/SellerDashboard';
import PurchaserDashboard from './pages/PurchaserDashboard';
import DriverDashboard from './pages/DriverDashboard';

// A simple PrivateRoute component to protect dashboards based on role
const PrivateRoute = ({ children, role }) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        return <Navigate to="/login" replace />;
    }
    
    // Decode the token to check the user's role
    try {
        const tokenPayload = JSON.parse(atob(token.split('.')[1]));
        if (tokenPayload.sub.role !== role) {
            // Redirect to login if role doesn't match
            return <Navigate to="/login" replace />;
        }
    } catch (error) {
        // Handle invalid token
        return <Navigate to="/login" replace />;
    }

    return children;
};

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/" element={<Navigate to="/login" />} />
                    
                    {/* Protected Routes for each role */}
                    <Route path="/ceo/dashboard" element={
                        <PrivateRoute role="ceo">
                            <CEODashboard />
                        </PrivateRoute>
                    } />
                    <Route path="/storekeeper/dashboard" element={
                        <PrivateRoute role="storekeeper">
                            <StorekeeperDashboard />
                        </PrivateRoute>
                    } />
                    <Route path="/seller/dashboard" element={
                        <PrivateRoute role="seller">
                            <SellerDashboard />
                        </PrivateRoute>
                    } />
                    <Route path="/purchaser/dashboard" element={
                        <PrivateRoute role="purchaser">
                            <PurchaserDashboard />
                        </PrivateRoute>
                    } />
                    <Route path="/driver/dashboard" element={
                        <PrivateRoute role="driver">
                            <DriverDashboard />
                        </PrivateRoute>
                    } />

                </Routes>
            </div>
        </Router>
    );
}

export default App;