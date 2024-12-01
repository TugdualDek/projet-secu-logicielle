const API_BASE_URL = '/api';

export const scanService = {
  // Récupérer tous les scans
  getAllScans: async () => {
    const response = await fetch(`${API_BASE_URL}/scans/`);
    if (!response.ok) throw new Error('Failed to fetch scans');
    return response.json();
  },

  // Récupérer un scan spécifique
  getScan: async (id) => {
    const response = await fetch(`${API_BASE_URL}/scans/${id}`);
    if (!response.ok) throw new Error('Failed to fetch scan');
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
    const response = await fetch(`${API_BASE_URL}/reports/scan/${id}`);
    if (!response.ok) throw new Error('Failed to fetch report');
    return response.json();
  }
};
