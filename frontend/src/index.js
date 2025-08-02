import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './App.css'; // We will create this file for basic styling

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);