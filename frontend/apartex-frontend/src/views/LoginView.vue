<template>
  <div class="auth-page-container">
    <!-- Left: Visual Panel (Hidden on mobile) -->
    <div class="auth-visual-panel">
      <div class="bg-image"></div>
      <div class="bg-overlay">
        <div class="visual-content">
          <span class="badge">Established 2024</span>
          <h1 class="visual-title">Elegance <br/>in Every Stay.</h1>
          <p class="visual-text">Bespoke living experiences curated for the world's most discerning travelers.</p>
        </div>
      </div>
    </div>

    <!-- Right: Form Panel -->
    <div class="auth-form-panel">
      <div class="form-container">
        <!-- Brand Identity -->
        <div class="brand-wrapper">
          <div class="brand-icon">
            <i class="pi pi-bolt"></i>
          </div>
          <div class="brand-text">
            <h1 class="brand-name">APARTEX</h1>
            <p class="brand-tagline">Luxury Rentals</p>
          </div>
        </div>

        <div class="header-section">
          <h2 class="title">Welcome back</h2>
          <p class="subtitle">Please enter your credentials to continue</p>
        </div>

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
            <div class="ax-input-wrapper">
              <i class="pi pi-envelope ax-input-icon"></i>
              <input 
                id="email" 
                v-model="form.email" 
                type="email" 
                required 
                placeholder="name@example.com" 
                class="ax-input icon-padding" 
              />
            </div>
          </div>
          
          <div class="field">
            <div class="field-header">
              <label for="password" class="ax-label">Password</label>
              <a href="#" class="forgot-link">Forgot?</a>
            </div>
            <div class="ax-input-wrapper">
              <i class="pi pi-lock ax-input-icon z-2"></i>
              <Password 
                id="password" 
                v-model="form.password" 
                :feedback="false" 
                toggleMask 
                required 
                placeholder="••••••••" 
                inputClass="ax-input icon-padding w-full" 
                class="w-full"
              />
            </div>
          </div>

          <div class="checkbox-field">
            <Checkbox id="remember" v-model="rememberMe" :binary="true" class="mr-2" />
            <label for="remember" class="checkbox-label">Remember my session</label>
          </div>
          
          <div class="action-field">
            <button type="submit" :disabled="loading" class="ax-button full-width-btn">
              <i v-if="loading" class="pi pi-spin pi-spinner"></i>
              <span>{{ loading ? 'Authenticating...' : 'Sign In to Account' }}</span>
              <i v-if="!loading" class="pi pi-arrow-right"></i>
            </button>
          </div>
          
          <Transition name="fade">
            <div v-if="error" class="error-alert">
              <i class="pi pi-exclamation-circle"></i>
              <span>{{ error }}</span>
            </div>
          </Transition>
        </form>
        
        <div class="footer-links">
          <p>
            Don't have an account yet? 
            <router-link :to="registerPath" class="register-link">
              Create one now
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// PrimeVue components
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
/* Strict layout preventing horizontal scroll */
.auth-page-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  background-color: #fff;
}

/* Left Visual Panel */
.auth-visual-panel {
  display: none;
  flex: 1;
  position: relative;
  overflow: hidden;
  background-color: #0f172a;
}

@media (min-width: 1024px) {
  .auth-visual-panel {
    display: block;
  }
}

.bg-image {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background-image: url('https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&q=80&w=1920');
  background-size: cover;
  background-position: center;
  z-index: 0;
}

.bg-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.8));
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 4rem;
  z-index: 1;
}

.visual-content { text-align: left; }
.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background-color: rgba(255,255,255,0.2);
  border-radius: 9999px;
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 1rem;
  backdrop-filter: blur(4px);
}
.visual-title { color: #fff; font-size: 4.5rem; font-weight: 700; margin-bottom: 0.75rem; line-height: 1.1; }
.visual-text { color: rgba(255,255,255,0.8); font-size: 1.25rem; font-weight: 500; line-height: 1.5; max-width: 28rem; }

/* Right Form Panel */
.auth-form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8fafc;
  padding: 2rem;
  width: 100%;
}

.form-container {
  width: 100%;
  max-width: 28rem;
}

.brand-wrapper { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 2rem; }
.brand-icon {
  width: 3rem; height: 3rem;
  background-color: #0f172a;
  border-radius: 0.75rem;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}
.brand-icon i { color: #fff; font-size: 1.5rem; }
.brand-text { text-align: left; }
.brand-name { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.025em; margin: 0; }
.brand-tagline { font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin: 0; }

.header-section { text-align: left; margin-bottom: 1.5rem; }
.title { font-size: 2.25rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; letter-spacing: -0.025em; }
.subtitle { color: #64748b; font-weight: 500; }

.role-selector { text-align: left; margin-bottom: 1.5rem; }
.full-width-select { width: 100%; }

.auth-form { width: 100%; }
.field { margin-bottom: 1rem; text-align: left; }
.field-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem; }
.forgot-link { font-size: 0.75rem; font-weight: 700; color: #2563eb; text-transform: uppercase; letter-spacing: 0.05em; }
.forgot-link:hover { text-decoration: underline; }

.ax-input-wrapper { position: relative; display: flex; align-items: center; }
.ax-input-icon { position: absolute; left: 1rem; color: #94a3b8; pointer-events: none; z-index: 2; }
.icon-padding { padding-left: 3rem !important; }

.checkbox-field { display: flex; align-items: center; margin-bottom: 1.5rem; text-align: left; }
.checkbox-label { color: #475569; font-size: 0.875rem; font-weight: 600; cursor: pointer; }

.full-width-btn { width: 100%; gap: 0.5rem; }

.error-alert {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 0.75rem;
  background-color: #fef2f2;
  border: 1px solid #fee2e2;
  color: #dc2626;
  font-size: 0.875rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.footer-links { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #f1f5f9; text-align: center; }
.footer-links p { color: #64748b; font-weight: 500; }
.register-link { color: #0f172a; font-weight: 700; margin-left: 0.25rem; }
.register-link:hover { text-decoration: underline; }

.fade-enter-active, .fade-leave-active { transition: all 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-10px); }

.z-2 { z-index: 2; }
.w-full { width: 100% !important; }
</style>
