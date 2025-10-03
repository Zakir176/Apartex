<!-- src/views/LoginView.vue -->
<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <router-link to="/" class="logo">🏠 Apartex</router-link>
          <h1>Welcome Back</h1>
          <p>Sign in to your account</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email">Email Address</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              placeholder="Enter your email"
              required
              class="form-input"
            >
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              placeholder="Enter your password"
              required
              class="form-input"
            >
          </div>

          <button type="submit" class="login-btn" :disabled="authStore.isLoading">
            {{ authStore.isLoading ? 'Signing In...' : 'Sign In' }}
          </button>

          <div class="login-footer">
            <p>Don't have an account? <router-link to="/register" class="signup-link">Sign up</router-link></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      email: '',
      password: ''
    })

    const handleLogin = async () => {
      try {
        await authStore.login(form)
        router.push('/dashboard')
      } catch (error) {
        alert('Login failed. Please check your credentials.')
      }
    }

    return {
      form,
      authStore,
      handleLogin
    }
  }
}
</script>