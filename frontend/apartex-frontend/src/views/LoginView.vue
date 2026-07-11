<template>
  <div class="auth-page-container">
    <div class="auth-card">
      <div class="brand-logo">APARTEX</div>
      <h1 class="headline">Welcome back</h1>
      
      <div class="role-selector">
        <label class="ax-label">Login as</label>
        <SelectButton 
          v-model="targetRole" 
          :options="roleOptions" 
          optionLabel="label" 
          optionValue="value" 
          class="full-width-select"
        />
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="field">
          <label for="email" class="ax-label">Email Address</label>
          <input 
            id="email" 
            v-model="form.email" 
            type="email" 
            required 
            placeholder="name@example.com" 
            class="ax-input" 
          />
        </div>
        
        <div class="field">
          <label for="password" class="ax-label">Password</label>
          <!-- Using PrimeVue Password but styling it directly to match specs -->
          <Password 
            id="password" 
            v-model="form.password" 
            :feedback="false" 
            toggleMask 
            required 
            placeholder="••••••••" 
            inputClass="ax-input" 
            class="w-full"
          />
        </div>

        <div class="checkbox-field">
          <Checkbox id="remember" v-model="rememberMe" :binary="true" class="mr-2" />
          <label for="remember" class="checkbox-label">Remember my session</label>
        </div>
        
        <button type="submit" :disabled="loading" class="ax-button">
          <i v-if="loading" class="pi pi-spin pi-spinner mr-2"></i>
          {{ loading ? 'Authenticating...' : 'Sign In' }}
        </button>
        
        <div v-if="error" class="error-alert">
          {{ error }}
        </div>
      </form>
      
      <div class="footer-link">
        Don't have an account yet? 
        <router-link :to="registerPath" class="link-accent">Register</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

import Password from 'primevue/password';
import SelectButton from 'primevue/selectbutton';
import Checkbox from 'primevue/checkbox';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const targetRole = ref(route.meta.targetRole || 'renter');
const rememberMe = ref(false);
const roleOptions = [
  { label: 'Guest', value: 'renter' },
  { label: 'Host', value: 'owner' }
];

const form = ref({ email: '', password: '' });
const loading = ref(false);
const error = ref('');

const registerPath = computed(() => targetRole.value === 'owner' ? '/register?role=owner' : '/register');

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  try {
    await authStore.login(form.value);
    if (authStore.user?.role !== targetRole.value) {
      error.value = `Unauthorized access to ${targetRole.value === 'owner' ? 'Host' : 'Guest'} portal.`;
      await authStore.logout();
      return;
    }
    router.push(authStore.user?.role === 'owner' ? '/owner' : '/');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Identity verification failed.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-page-container {
  min-height: 100vh;
  background-color: var(--color-bg);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--space-24) var(--space-8);
}

.auth-card {
  width: 100%;
  max-width: 440px;
  background: white;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  padding: var(--space-10);
  text-align: center;
}

.brand-logo {
  color: var(--color-navy);
  font-weight: 800;
  font-size: var(--font-size-2xl);
  margin-bottom: var(--space-4);
}

.headline {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--space-6);
}

.role-selector {
  text-align: left;
  margin-bottom: var(--space-6);
}

.auth-form {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.field {
  margin-bottom: var(--space-4);
  display: flex;
  flex-direction: column;
}

.ax-label {
  font-size: var(--font-size-sm);
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

:deep(.ax-input) {
  width: 100%;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  font-size: var(--font-size-base);
  font-family: var(--font-family);
  transition: var(--transition-fast);
}

:deep(.ax-input:focus) {
  border-color: var(--color-accent);
  outline: none;
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.checkbox-field {
  display: flex;
  align-items: center;
  margin-bottom: var(--space-6);
}
.checkbox-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  margin-left: var(--space-2);
}

.ax-button {
  width: 100%;
  background: var(--color-accent);
  color: white;
  font-weight: 700;
  border: none;
  border-radius: var(--radius-md);
  padding: var(--space-3);
  font-size: var(--font-size-base);
  cursor: pointer;
  transition: background var(--transition-base);
}

.ax-button:hover:not(:disabled) {
  background: var(--color-accent-hover);
}

.ax-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-alert {
  margin-top: var(--space-4);
  color: var(--color-error);
  background: var(--color-error-light);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  font-size: var(--font-size-sm);
  font-weight: 600;
}

.footer-link {
  margin-top: var(--space-6);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.link-accent {
  color: var(--color-accent);
  font-weight: 600;
  text-decoration: none;
}
.link-accent:hover {
  text-decoration: underline;
}

.w-full {
  width: 100%;
}
</style>
