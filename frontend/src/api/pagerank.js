const API_URL = process.env.NODE_ENV === 'production' 
  ? '/projects/pagerank/api'  // Prod
  : 'http://localhost:5000/api';  // Dev

export const createGraph = async (nodes, edges) => {
  const response = await fetch(`${API_URL}/graph`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Important: sends cookies
    body: JSON.stringify({ nodes, edges }),
  });

  if (!response.ok) {
    throw new Error('Failed to create graph');
  }

  return response.json();
};

export const computePageRank = async () => {
  const response = await fetch(`${API_URL}/pagerank`, {
    method: 'GET',
    credentials: 'include', // Important: sends cookies
  });

  if (!response.ok) {
    throw new Error('Failed to compute PageRank');
  }

  return response.json();
};

export const getVisualization = async () => {
  const response = await fetch(`${API_URL}/visualize`, {
    method: 'GET',
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Failed to get visualization');
  }

  return response.blob(); // Returns image as blob
};

export const clearGraph = async () => {
  const response = await fetch(`${API_URL}/clear`, {
    method: 'POST',
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Failed to clear graph');
  }

  return response.json();
};
