import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,  // Increased to 120 seconds for image analysis
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add request interceptor for better error handling
apiClient.interceptors.request.use(
  config => {
    console.log('API Request:', config.url);
    return config;
  },
  error => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor
apiClient.interceptors.response.use(
  response => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  error => {
    console.error('Response error:', error);
    return Promise.reject(error);
  }
);

export const analysisService = {
  uploadAndAnalyze: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await apiClient.post('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      });
      return response.data;
    } catch (error) {
      console.error('Analysis error:', error);
      if (error.response?.data) {
        throw error.response.data;
      } else if (error.message) {
        throw error.message;
      } else {
        throw 'Network Error - Please make sure the backend server is running';
      }
    }
  },

  getHealth: async () => {
    try {
      const response = await apiClient.get('/api/health');
      return response.data;
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }
};

export default apiClient;
