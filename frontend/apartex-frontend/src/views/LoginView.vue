<!-- src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>Welcome Back</h2>
        <p>Sign in to your Apartex account</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="field">
          <label for="email">Email</label>
          <InputText 
            id="email"
            v-model="form.email"
            type="email" 
            placeholder="Enter your email"
            class="w-full"
            :class="{ 'p-invalid': errors.email }"
          />
          <small class="p-error" v-if="errors.email">{{ errors.email }}</small>
        </div>
        
        <div class="field">
          <label for="password">Password</label>
          <Password 
            id="password"
            v-model="form.password" 
            placeholder="Enter your password"
            :feedback="false"
            toggleMask
            class="w-full"
            :class="{ 'p-invalid': errors.password }"
          />
          <small class="p-error" v-if="errors.password">{{ errors.password }}</small>
        </div>
        
        <Button 
          type="submit" 
          label="Sign In" 
          class="w-full login-btn"
          :loading="authStore.isLoading"
        />
      </form>
      
      <div class="login-footer">
        <p>Don't have an account? <router-link to="/register">Sign up</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'

export default {
  name: 'LoginView',
  components: {
    InputText,
    Password,
    Button
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      email: '',
      password: ''
    })
    
    const errors = reactive({})
    
    const validateForm = () => {
      let isValid = true
      errors.email = ''
      errors.password = ''
      
      if (!form.email) {
        errors.email = 'Email is required'
        isValid = false
      } else if (!/\S+@\S+\.\S+/.test(form.email)) {
        errors.email = 'Email is invalid'
        isValid = false
      }
      
      if (!form.password) {
        errors.password = 'Password is required'
        isValid = false
      }
      
      return isValid
    }
    
    const handleLogin = async () => {
      if (!validateForm()) return
      
      try {
        await authStore.login(form)
        router.push('/dashboard')
      } catch (error) {
        // Error handled in store
      }
    }
    
    return {
      form,
      errors,
      authStore,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h2 {
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #718096;
}

.login-form {
  margin-bottom: 2rem;
}

.field {
  margin-bottom: 1.5rem;
}

.field label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4a5568;
  font-weight: 500;
}

.login-btn {
  background: #667eea;
  border: none;
  padding: 0.75rem;
  font-size: 1rem;
}

.login-footer {
  text-align: center;
}

.login-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.login-footer a:hover {
  text-decoration: underline;
}
</style>