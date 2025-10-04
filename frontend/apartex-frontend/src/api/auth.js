import apiClient from './index';

export const authApi = {
  register(userData) {
    return apiClient.post('/auth/register', userData);
  },
  
  login(credentials) {
    return apiClient.post('/auth/login', credentials);
  },
  
  getCurrentUser() {
    return apiClient.get('/auth-enhanced/me');
  },
  
  logout() {
    return apiClient.post('/auth-enhanced/logout');
  }
};