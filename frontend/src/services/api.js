import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Создаем экземпляр axios с базовой конфигурацией
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Для работы с CSRF токенами Django
  headers: {
    'Content-Type': 'application/json',
  },
});

// Интерсептор для добавления CSRF токена
api.interceptors.request.use((config) => {
  // Получаем CSRF токен из cookies
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
  
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

// Интерсептор для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Перенаправляем на страницу входа при 401 ошибке
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API для аутентификации
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  logout: () => api.post('/auth/logout/'),
  getProfile: () => api.get('/auth/profile/'),
  createUser: (userData) => api.post('/auth/create/', userData),
  getUserList: () => api.get('/auth/list/'),
};

// API для отчетов
export const reportsAPI = {
  getData: (params) => api.get('/reports/data/', { params }),
  getYieldComparison: (params) => api.get('/reports/yield-comparison/', { params }),
  getFieldEfficiency: (params) => api.get('/reports/field-efficiency/', { params }),
  getVarietyPerformance: (params) => api.get('/reports/variety-performance/', { params }),
  getDashboardStats: () => api.get('/reports/dashboard-stats/'),
  getTemplates: () => api.get('/reports/templates/'),
};

// API для загрузки файлов
export const uploadAPI = {
  uploadFile: (formData) => api.post('/upload/file/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    withCredentials: true,
  }),
  getUploadHistory: () => api.get('/upload/history/'),
  getUploadStatus: (uploadId) => api.get(`/upload/status/${uploadId}/`),
  deleteUploadData: (uploadId) => api.delete(`/upload/delete/${uploadId}/`),
  deleteAllData: () => api.delete('/upload/delete-all/'),
};

export default api;

