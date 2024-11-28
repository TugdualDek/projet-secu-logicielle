const API_BASE_URL = '/api';

export const scanService = {
  // Récupérer tous les scans
  getAllScans: async () => {
    const response = await fetch(`${API_BASE_URL}/scans/`);
    if (!response.ok) throw new Error('Failed to fetch scans');
    return response.json();
  },

  // Créer un nouveau scan
  createScan: async (target) => {
    const response = await fetch(`${API_BASE_URL}/scans/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ target }),
    });
    if (!response.ok) throw new Error('Failed to create scan');
    return response.json();
  },

  // Récupérer un rapport spécifique
  getReport: async (id) => {
    const response = await fetch(`${API_BASE_URL}/reports/${id}`);
    if (!response.ok) throw new Error('Failed to fetch report');
    return response.json();
  }
};
