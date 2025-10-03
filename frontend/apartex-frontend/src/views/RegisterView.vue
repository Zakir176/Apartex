<!-- src/views/RegisterView.vue -->
<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <router-link to="/" class="logo">🏠 Apartex</router-link>
          <h1>Create Your Account</h1>
          <p>Join Apartex today</p>
        </div>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-row">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <input
                type="text"
                id="firstName"
                v-model="form.first_name"
                placeholder="First Name"
                required
                class="form-input"
              >
            </div>
            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input
                type="text"
                id="lastName"
                v-model="form.last_name"
                placeholder="Last Name"
                required
                class="form-input"
              >
            </div>
          </div>

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
              placeholder="Create a password"
              required
              class="form-input"
            >
          </div>

          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="form.password_confirmation"
              placeholder="Confirm your password"
              required
              class="form-input"
            >
          </div>

          <button type="submit" class="register-btn" :disabled="authStore.isLoading">
            {{ authStore.isLoading ? 'Creating Account...' : 'Create Account' }}
          </button>

          <div class="register-footer">
            <p>Already have an account? <router-link to="/login" class="login-link">Sign in</router-link></p>
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
  name: 'RegisterView',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      password_confirmation: ''
    })

    const handleRegister = async () => {
      try {
        await authStore.register(form)
        router.push('/login')
      } catch (error) {
        alert('Registration failed. Please try again.')
      }
    }

    return {
      form,
      authStore,
      handleRegister
    }
  }
}
</script>

<style scoped>
.form-row {
  display: flex;
  gap: 1rem;
}

.form-row .form-group {
  flex: 1;
}
</style>