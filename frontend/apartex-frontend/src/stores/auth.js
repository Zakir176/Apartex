import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authApi } from '@/api/auth';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);
  const token = ref(localStorage.getItem('accessToken') || null);
  
  const isAuthenticated = computed(() => !!token.value);
  const isOwner = computed(() => user.value?.role === 'owner');
  
  async function register(userData) {
    try {
      const response = await authApi.register(userData);
      await handleAuthResponse(response);
      return response;
    } catch (error) {
      throw error;
    }
  }
  
  async function login(credentials) {
    try {
      const response = await authApi.login(credentials);
      await handleAuthResponse(response);
      return response;
    } catch (error) {
      throw error;
    }
  }
  
  async function logout() {
    try {
      await authApi.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      user.value = null;
      token.value = null;
      localStorage.removeItem('accessToken');
    }
  }
  
  async function fetchCurrentUser() {
    try {
      const response = await authApi.getCurrentUser();
      user.value = response.data;
      return response;
    } catch (error) {
      throw error;
    }
  }
  
  async function handleAuthResponse(response) {
    // Adjust based on your API response structure
    const accessToken = response.data.access_token || response.data.token;
    if (accessToken) {
      token.value = accessToken;
      localStorage.setItem('accessToken', accessToken);
      await fetchCurrentUser();
    }
  }
  
  return {
    user,
    token,
    isAuthenticated,
    isOwner,
    register,
    login,
    logout,
    fetchCurrentUser
  };
});