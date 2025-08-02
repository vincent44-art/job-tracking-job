import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// The URL for your Flask backend login endpoint
const API_URL = "http://127.0.0.1:5000/api/auth/login";

function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await axios.post(API_URL, {
                email,
                password
            });
            
            const { access_token } = response.data;
            localStorage.setItem('access_token', access_token);
            
            // Decode the token to get the user's role and redirect
            const tokenPayload = JSON.parse(atob(access_token.split('.')[1]));
            const userRole = tokenPayload.sub.role;
            
            // Redirect based on the user's role
            switch (userRole) {
                case 'ceo':
                    navigate('/ceo/dashboard');
                    break;
                case 'storekeeper':
                    navigate('/storekeeper/dashboard');
                    break;
                case 'seller':
                    navigate('/seller/dashboard');
                    break;
                case 'purchaser':
                    navigate('/purchaser/dashboard');
                    break;
                case 'driver':
                    navigate('/driver/dashboard');
                    break;
                default:
                    setError('Unknown user role. Please contact support.');
            }
        } catch (err) {
            setError('Invalid email or password. Please try again.');
        }
    };

    return (
        <div className="login-container">
            <h2>Login to Fruit Track</h2>
            <form onSubmit={handleLogin}>
                <div className="form-group">
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p className="error-message">{error}</p>}
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default LoginPage;