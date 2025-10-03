// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authService from '@/services/auth'
import { useAppToast } from '@/utils/toast'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('apartex_token'))
  const isLoading = ref(false)
  const { showSuccess, showError } = useAppToast()

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const login = async (credentials) => {
    isLoading.value = true
    try {
      const response = await authService.login(credentials)
      token.value = response.data.access_token
      user.value = response.data.user
      localStorage.setItem('apartex_token', token.value)
      showSuccess('Login successful!')
      return response
    } catch (error) {
      showError(error.response?.data?.detail || 'Login failed')
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData) => {
    isLoading.value = true
    try {
      const response = await authService.register(userData)
      showSuccess('Registration successful! Please login.')
      return response
    } catch (error) {
      showError(error.response?.data?.detail || 'Registration failed')
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('apartex_token')
    showSuccess('Logged out successfully')
  }

  const fetchUser = async () => {
    if (!token.value) return
    
    try {
      const response = await authService.getCurrentUser()
      user.value = response.data
    } catch (error) {
      logout()
    }
  }

  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser
  }
})