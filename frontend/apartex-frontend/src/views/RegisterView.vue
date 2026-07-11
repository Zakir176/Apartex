<template>
  <div class="auth-page-container">
    <div class="auth-card">
      <div class="brand-logo">APARTEX</div>
      <h1 class="headline">Create your account</h1>
      
      <div class="role-selector">
        <label class="ax-label">I want to be a</label>
        <SelectButton 
          v-model="targetRole" 
          :options="roleOptions" 
          optionLabel="label" 
          optionValue="value" 
          class="full-width-select"
        />
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="field">
          <label for="name" class="ax-label">Full Name</label>
          <input 
            id="name" 
            v-model="form.name" 
            type="text" 
            required 
            placeholder="John Doe" 
            class="ax-input" 
          />
        </div>

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
          <label for="password" class="ax-label">Create Password</label>
          <Password 
            id="password" 
            v-model="form.password" 
            toggleMask 
            required 
            minlength="8"
            placeholder="••••••••" 
            inputClass="ax-input" 
            class="w-full"
          >
            <template #footer>
              <Divider />
              <p class="mt-2 font-bold text-xs uppercase text-500 mb-2">Security Advice</p>
              <ul class="pl-3 m-0 text-xs line-height-3 text-600">
                <li>Use at least 8 characters</li>
                <li>Include numbers and symbols</li>
              </ul>
            </template>
          </Password>
        </div>

        <div class="checkbox-field">
          <Checkbox id="terms" v-model="acceptTerms" :binary="true" class="mr-2" />
          <label for="terms" class="checkbox-label">
            I agree to the <a href="#" class="link-accent">Membership Terms</a>
          </label>
        </div>
        
        <button type="submit" :disabled="loading || !acceptTerms" class="ax-button">
          <i v-if="loading" class="pi pi-spin pi-spinner mr-2"></i>
          {{ loading ? 'Initializing...' : 'Register Now' }}
        </button>
        
        <div v-if="error" class="error-alert">
          {{ error }}
        </div>
      </form>
      
      <div class="footer-link">
        Already have an account? 
        <router-link to="/login" class="link-accent">Sign In</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

import Password from 'primevue/password';
import SelectButton from 'primevue/selectbutton';
import Checkbox from 'primevue/checkbox';
import Divider from 'primevue/divider';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const targetRole = ref('renter');
const acceptTerms = ref(false);
const roleOptions = [
  { label: 'Guest', value: 'renter' },
  { label: 'Host', value: 'owner' }
];

const form = ref({ name: '', email: '', password: '' });
const loading = ref(false);
const error = ref('');

onMounted(() => {
  if (route.query.role === 'owner') targetRole.value = 'owner';
});

const handleRegister = async () => {
  if (!acceptTerms.value) return;
  loading.value = true;
  error.value = '';
  try {
    await authStore.register({ ...form.value, role: targetRole.value });
    router.push(targetRole.value === 'owner' ? '/owner' : '/');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Account creation failed.';
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
