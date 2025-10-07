<template>
  <div class="login-container">
    <div class="login-form">
      <h2>Owner Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" v-model="form.email" type="email" required placeholder="Enter your email" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" v-model="form.password" type="password" required minlength="6" placeholder="Enter your password" />
        </div>
        <button type="submit" :disabled="loading || !form.email || form.password.length < 6" class="btn-primary">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
      <p class="register-link">
        Don't have an owner account? <router-link to="/owner/register">Register here</router-link>
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

const form = ref({ email: '', password: '' });
const loading = ref(false);
const error = ref('');

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  try {
    await authStore.login(form.value);
    if (authStore.user?.role !== 'owner') {
      error.value = 'This account is not an owner account.';
      return;
    }
    router.push('/owner');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container { display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
.login-form { width: 100%; max-width: 420px; padding: 2rem; border: 1px solid var(--border); border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.06); background: var(--bg); }
.form-group { margin-bottom: 1rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
input { width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: 8px; font-size: 1rem; background: var(--bg); color: var(--text); }
input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
.btn-primary { width: 100%; padding: 0.75rem; background-color: var(--primary); color: var(--primary-contrast); border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.error-message { color: #ef4444; margin-top: 1rem; text-align: center; }
.register-link { text-align: center; margin-top: 1rem; }
</style>
