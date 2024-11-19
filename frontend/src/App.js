import React, { useState } from 'react';
import './App.css';
import {
    Home,
    BarChart3,
    Settings,
    ShieldAlert,
    ShieldCheck,
    Search,
} from 'lucide-react';

const VulnerabilityScannerWithSidebar = () => {
    const [scanResults, setScanResults] = useState([
        {
            url: 'https://example.com',
            status: 'high-risk',
            vulnerabilities: 3,
            lastScanned: '2024-02-15'
        },
        {
            url: 'https://test.org',
            status: 'in-progress',
            lastScanned: '2024-02-14'
        }
    ]);

    const getRiskColor = (status) => {
        switch(status) {
            case 'high-risk': return 'bg-red-500 text-white';
            case 'medium-risk': return 'bg-orange-500 text-white';
            case 'low-risk': return 'bg-green-500 text-white';
            case 'in-progress': return 'bg-yellow-500 text-white';
            default: return 'bg-gray-500 text-white';
        }
    };

    return (
        <div className="flex min-h-screen">
            {/* Barre de navigation latérale */}
            <div className="bg-gray-900 text-white w-64 p-6">
                <h1 className="text-2xl font-bold mb-8">FortiCheck</h1>
                <nav>
                    <a href="#" className="flex items-center mb-4 hover:text-blue-400">
                        <Home className="mr-2" />
                        Accueil
                    </a>
                    <a href="#" className="flex items-center mb-4 hover:text-blue-400">
                        <BarChart3 className="mr-2" />
                        Statistiques
                    </a>
                    <a href="#" className="flex items-center mb-4 hover:text-blue-400">
                        <Settings className="mr-2" />
                        Paramètres
                    </a>
                </nav>
            </div>

            {/* Contenu principal */}
            <div className="flex-1 bg-gray-100 p-8">
                <div className="bg-white rounded-lg shadow p-6 mb-8">
                    <h2 className="text-2xl font-bold mb-4">Scanner de Vulnérabilités Web</h2>
                    <div className="flex">
                        <input
                            type="text"
                            placeholder="Entrez l'URL de l'application web à scanner"
                            className="flex-grow p-2 border rounded-l-lg"
                        />
                        <button className="bg-green-500 text-white px-4 py-2 rounded-r-lg hover:bg-green-600">
                            Lancer le Scan
                        </button>
                    </div>
                </div>

                <div className="grid md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-white p-6 rounded-lg shadow">
                        <ShieldAlert className="text-red-500 mb-4" size={40} />
                        <h2 className="text-xl font-bold mb-2">Vulnérabilités Critiques</h2>
                        <p className="text-3xl font-bold text-red-600">12</p>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow">
                        <ShieldCheck className="text-green-500 mb-4" size={40} />
                        <h2 className="text-xl font-bold mb-2">Sites Sécurisés</h2>
                        <p className="text-3xl font-bold text-green-600">18</p>
                    </div>
                    <div className="bg-white p-6 rounded-lg shadow">
                        <BarChart3 className="text-blue-500 mb-4" size={40} />
                        <h2 className="text-xl font-bold mb-2">Total des Scans</h2>
                        <p className="text-3xl font-bold text-blue-600">30</p>
                    </div>
                </div>

                <div className="bg-white rounded-lg shadow overflow-hidden">
                    <div className="flex p-4 bg-gray-200 items-center">
                        <Search className="text-gray-500 mr-4" />
                        <input
                            type="text"
                            placeholder="Rechercher un site web"
                            className="bg-transparent w-full focus:outline-none"
                        />
                    </div>
                    <table className="w-full">
                        <thead className="bg-gray-200">
                        <tr>
                            <th className="p-4 text-left">URL</th>
                            <th className="p-4 text-left">Statut</th>
                            <th className="p-4 text-center">Vulnérabilités</th>
                            <th className="p-4 text-left">Dernière Analyse</th>
                            <th className="p-4 text-center">Actions</th>
                        </tr>
                        </thead>
                        <tbody>
                        {scanResults.map((result, index) => (
                            <tr key={index} className="border-b border-gray-200 hover:bg-gray-100">
                                <td className="p-4">{result.url}</td>
                                <td className="p-4">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full ${getRiskColor(result.status)}`}>
                      {result.status.replace('-', ' ')}
                    </span>
                                </td>
                                <td className="p-4 text-center">{result.vulnerabilities || '-'}</td>
                                <td className="p-4">{result.lastScanned}</td>
                                <td className="p-4 text-center">
                                    <button className="bg-blue-500 text-white hover:bg-blue-600 px-3 py-1 rounded">
                                        Voir le Rapport
                                    </button>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default VulnerabilityScannerWithSidebar;