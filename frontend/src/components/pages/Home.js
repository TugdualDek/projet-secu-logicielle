import React, {useState, useEffect} from 'react'
import { useNavigate} from "react-router-dom";
import api from '../../services/api';
//essayer le tild ~pour path '~/api';
import '../../styles/home.css'

function Home() {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Récupérer les informations de l'utilisateur depuis la session
        const userData = sessionStorage.getItem('user');
        if (!userData) {
            navigate('/login');
            return;
        }
        setUser(JSON.parse(userData));
    }, [navigate]);

    // handle logout
    const handleLogout = async () => {
        try {
            await api.post('/logout');
        } catch (error) {
            console.error('Erreur lors de la déconnexion', error);
        } finally {
            sessionStorage.removeItem('user');
            navigate('/login');
        }
    };

    if (!user) {
        return null;
    }


    return (
        <div className="home-container">
            <div className="logout-wrapper">
                <button onClick={handleLogout} className="logout-button">
                    Déconnexion
                </button>
            </div>

            <h1 className="welcome-message">
                Bienvenue {user.first_name} !
            </h1>

            <p className="home-subtitile">
                Vous êtes sur la page d'accueil !
            </p>
        </div>
    );
}
export default Home;