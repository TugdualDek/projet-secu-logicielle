// login.js
// Importations
import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import  api from '../../services/api';
import '../../styles/common.css'
import '../../styles/login.css'

function Login() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    })

    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
        setError('');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/auth/login', formData);
            console.log('connexion réussie:', response.data);
            sessionStorage.setItem('user', JSON.stringify(response.data.user));
            navigate('/dashboard');
        } catch (err) {
            console.error('Erreur lors de la connexion:', err);
            setError(err.response?.data?.error || 'Email ou mot de passe incorrect');
        }
    };
    return (
        <div className="login-container">
            <h1>Connexion</h1>
            {error && <p className="error-message">{error}</p>}
            <form onSubmit={handleSubmit}>
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
                <button type="submit" className="login-button">Se connecter</button>
            </form>
            <div className="login-links">
                <p>Pas encore de compte ? <a href="/signup">Inscrivez vous</a></p>
            </div>
        </div>
    );
}
export default Login;