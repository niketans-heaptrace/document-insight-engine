import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const documentAPI = {
  // Upload a document
  uploadDocument: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/api/v1/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get document by ID
  getDocument: async (documentId) => {
    const response = await api.get(`/api/v1/documents/${documentId}`);
    return response.data;
  },

  // Get all documents
  getAllDocuments: async () => {
    const response = await api.get('/api/v1/documents/');
    return response.data;
  },

  // Ask a question about a document
  askQuestion: async (documentId, question) => {
    const response = await api.post(`/api/v1/documents/${documentId}/ask`, {
      question,
    });
    return response.data;
  },

  // Compare documents
  compareDocuments: async (documentIds) => {
    const response = await api.post('/api/v1/documents/compare', {
      document_ids: documentIds,
    });
    return response.data;
  },
};

export default api;

