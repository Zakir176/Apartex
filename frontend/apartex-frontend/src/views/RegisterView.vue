<!-- src/views/RegisterView.vue -->
<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <h2>Create Account</h2>
        <p>Join Apartex today</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="register-form">
        <div class="form-row">
          <div class="field">
            <label for="firstName">First Name</label>
            <InputText 
              id="firstName"
              v-model="form.first_name"
              placeholder="Enter your first name"
              class="w-full"
              :class="{ 'p-invalid': errors.first_name }"
            />
            <small class="p-error" v-if="errors.first_name">{{ errors.first_name }}</small>
          </div>
          
          <div class="field">
            <label for="lastName">Last Name</label>
            <InputText 
              id="lastName"
              v-model="form.last_name"
              placeholder="Enter your last name"
              class="w-full"
              :class="{ 'p-invalid': errors.last_name }"
            />
            <small class="p-error" v-if="errors.last_name">{{ errors.last_name }}</small>
          </div>
        </div>
        
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
            toggleMask
            class="w-full"
            :class="{ 'p-invalid': errors.password }"
          />
          <small class="p-error" v-if="errors.password">{{ errors.password }}</small>
        </div>
        
        <div class="field">
          <label for="confirmPassword">Confirm Password</label>
          <Password 
            id="confirmPassword"
            v-model="form.confirm_password" 
            placeholder="Confirm your password"
            toggleMask
            class="w-full"
            :class="{ 'p-error': errors.confirm_password }"
          />
          <small class="p-error" v-if="errors.confirm_password">{{ errors.confirm_password }}</small>
        </div>
        
        <Button 
          type="submit" 
          label="Create Account" 
          class="w-full register-btn"
          :loading="authStore.isLoading"
        />
      </form>
      
      <div class="register-footer">
        <p>Already have an account? <router-link to="/login">Sign in</router-link></p>
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
  name: 'RegisterView',
  components: {
    InputText,
    Password,
    Button
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      confirm_password: ''
    })
    
    const errors = reactive({})
    
    const validateForm = () => {
      let isValid = true
      Object.keys(errors).forEach(key => delete errors[key])
      
      if (!form.first_name) {
        errors.first_name = 'First name is required'
        isValid = false
      }
      
      if (!form.last_name) {
        errors.last_name = 'Last name is required'
        isValid = false
      }
      
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
      } else if (form.password.length < 6) {
        errors.password = 'Password must be at least 6 characters'
        isValid = false
      }
      
      if (!form.confirm_password) {
        errors.confirm_password = 'Please confirm your password'
        isValid = false
      } else if (form.password !== form.confirm_password) {
        errors.confirm_password = 'Passwords do not match'
        isValid = false
      }
      
      return isValid
    }
    
    const handleRegister = async () => {
      if (!validateForm()) return
      
      try {
        await authStore.register(form)
        router.push('/login')
      } catch (error) {
        // Error handled in store
      }
    }
    
    return {
      form,
      errors,
      authStore,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.register-card {
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 450px;
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h2 {
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.register-header p {
  color: #718096;
}

.register-form {
  margin-bottom: 2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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

.register-btn {
  background: #667eea;
  border: none;
  padding: 0.75rem;
  font-size: 1rem;
}

.register-footer {
  text-align: center;
}

.register-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.register-footer a:hover {
  text-decoration: underline;
}
</style>