/*Composant principal de l'application.*/

import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Signup from './components/auth/Signup';
import Login from './components/auth/Login';
import Home from './components/pages/Home';
import Dashboard from './components/pages/Dashboard';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate to="/login" />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/login" element={<Login />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </Router>
    );
}


// Optionnel : Composant NotFound pour les routes non définies
function NotFound() {
    return (
        <div className="not-found">
            <h2>404 - Page non trouvée</h2>
            <p>La page que vous recherchez n'existe pas.</p>
        </div>
    );
}

export default App;
