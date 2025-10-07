<template>
  <div class="register-container">
    <div class="register-form">
      <h2>Owner Register</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="name">Full Name</label>
          <input id="name" v-model="form.name" type="text" required placeholder="Enter your full name" />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="form.email" type="email" required placeholder="Enter your email" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" v-model="form.password" type="password" required placeholder="Enter your password" />
        </div>
        <button type="submit" :disabled="loading" class="btn-primary">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
      <p class="login-link">
        Already have an owner account? <router-link to="/owner/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const form = ref({ name: '', email: '', password: '' });
const loading = ref(false);
const error = ref('');

const handleRegister = async () => {
  loading.value = true;
  error.value = '';
  try {
    await authStore.register({ ...form.value, role: 'owner' });
    if (authStore.user?.role !== 'owner') {
      error.value = 'Registered user is not an owner.';
      return;
    }
    router.push('/owner');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.register-form {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group { margin-bottom: 1rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
input, select {
  width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem;
}
.btn-primary { width: 100%; padding: 0.75rem; background-color: #007bff; color: white; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; }
.btn-primary:disabled { background-color: #6c757d; cursor: not-allowed; }
.error-message { color: #dc3545; margin-top: 1rem; text-align: center; }
.login-link { text-align: center; margin-top: 1rem; }
</style>
