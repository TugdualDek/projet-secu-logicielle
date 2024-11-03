// client/src/components/auth/Signup.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import '../../styles/common.css'
import '../../styles/signup.css'


function Signup() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
    });
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        setError(''); // Effacer les erreurs précédentes lors de la modification
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/auth/signup', formData);
            console.log('Inscription réussie:', response.data);
            sessionStorage.setItem('user', JSON.stringify(response.data.user));
            navigate('/dashboard');
        } catch (err) {
            console.error('Erreur lors de linscription:', err);
            setError(err.response?.data?.error || 'Une erreur est survenue lors de l\'inscription');
        }
    };

    return (
        <div className="signup-container">
            <h1>Inscription</h1>
            {error && <p className="error-message">{error}</p>}
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <input
                        type="text"
                        name="first_name"
                        placeholder="Prénom"
                        value={formData.first_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <input
                        type="text"
                        name="last_name"
                        placeholder="Nom"
                        value={formData.last_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <input
                        type="password"
                        name="password"
                        placeholder="Mot de passe"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                </div>
                <button type="submit" className="signup-button">S'inscrire</button>
            </form>
            <div className="signup-links">
                <p>Déjà un compte ? <a href="/login">Connectez-vous</a></p>
            </div>
        </div>
    );
}

export default Signup;