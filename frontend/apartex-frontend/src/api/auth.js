import apiClient from './index';

export const authApi = {
  register(userData) {
    return apiClient.post('/auth-enhanced/register', userData);
  },
  
  login(credentials) {
    return apiClient.post('/auth-enhanced/simple-login', credentials);
  },
  
  getCurrentUser() {
    return apiClient.get('/auth-enhanced/me');
  },
  
  logout() {
    return apiClient.post('/auth-enhanced/logout');
  }
};