"use client";

import { Activity } from 'lucide-react';
import { useState } from "react";
import { scanService } from '@/services/api';

const SearchInput = ({ onClick }) => {

    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            await scanService.createScan(url);
            window.dispatchEvent(new Event('scanCreated'));
        } catch (error) {
            console.error('Erreur lors de la création du scan:', error);
        } finally {
            setLoading(false);
            setUrl("");
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-row items-center bg-white/10 p-2 rounded-full border border-white/15 mt-8">
            <input
                id='url'
                type="url"
                placeholder="Enter your URL"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                required
                className="w-72 bg-transparent outline-none px-2"
            />
            <button
                type="submit"
                onClick={onClick}
                className="h-10 w-10 flex items-center justify-center rounded-full text-black bg-white"
            >
                {loading ? 'Loading...' : <Activity size={18} /> }
                
            </button>
        </form>
    );
};

export default SearchInput;