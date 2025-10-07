// src/services/auth.js
import api from './api'

export default {
  login(credentials) {
    return api.post('/auth-enhanced/simple-login', credentials)
  },
  
  register(userData) {
    return api.post('/auth-enhanced/register', userData)
  },
  
  getCurrentUser() {
    return api.get('/auth-enhanced/me')
  },
  
  refreshToken() {
    return api.post('/auth-enhanced/refresh')
  }
}