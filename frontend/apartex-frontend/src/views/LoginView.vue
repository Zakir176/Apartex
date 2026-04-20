<template>
  <div class="auth-container">
    <!-- Left: Immersive Visual -->
    <div class="auth-visual" :style="{ backgroundImage: `url(${bgImage})` }">
      <div class="visual-overlay">
        <div class="visual-content">
          <h1 class="text-white font-bold text-5xl mb-3">Welcome to Apartex</h1>
          <p class="text-white opacity-80 text-xl font-medium">Experience the future of premium living.</p>
        </div>
      </div>
    </div>

    <!-- Right: Auth Form -->
    <div class="auth-form-wrapper flex align-items-center justify-content-center">
      <Card class="auth-card glass border-none shadow-none">
        <template #content>
          <div class="text-center mb-5">
            <h2 class="text-3xl font-bold mb-2">Member Login</h2>
            <p class="text-muted">Enter your credentials to access your account</p>
          </div>

          <!-- Role Toggle -->
          <div class="flex justify-content-center mb-5">
            <SelectButton 
              v-model="targetRole" 
              :options="roleOptions" 
              optionLabel="label" 
              optionValue="value" 
              aria-labelledby="basic"
              class="premium-toggle"
            />
          </div>

          <form @submit.prevent="handleLogin" class="p-fluid">
            <div class="field mb-4">
              <label for="email" class="font-bold block mb-2 text-sm uppercase tracking-wider text-gray-500">Email Address</label>
              <span class="p-input-icon-left">
                <i class="pi pi-envelope" />
                <InputText id="email" v-model="form.email" type="email" required placeholder="name@example.com" class="p-inputtext-lg" />
              </span>
            </div>
            
            <div class="field mb-5">
              <label for="password" class="font-bold block mb-2 text-sm uppercase tracking-wider text-gray-500">Password</label>
              <Password 
                id="password" 
                v-model="form.password" 
                :feedback="false" 
                toggleMask 
                required 
                placeholder="••••••••" 
                inputClass="p-inputtext-lg w-full" 
              />
            </div>
            
            <Button 
              type="submit" 
              :label="loading ? 'Authenticating...' : 'Sign In'" 
              :loading="loading" 
              class="p-button-lg p-button-primary font-bold py-3 text-xl border-round-xl" 
            />
            
            <Message v-if="error" severity="error" class="mt-4" :closable="false">{{ error }}</Message>
          </form>
          
          <div class="mt-5 text-center">
            <p class="text-gray-500">
              Don't have an account? 
              <router-link :to="registerPath" class="text-primary font-bold no-underline hover:underline ml-1">
                Create one now
              </router-link>
            </p>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// PrimeVue components
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Message from 'primevue/message';
import SelectButton from 'primevue/selectbutton';

// Assets
import bgImage from '/C:/Users/zakir/.gemini/antigravity/brain/6ff79adf-a3cc-4176-a870-ba2d422d47d4/luxury_auth_background_1776372436472.png';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const targetRole = ref(route.meta.targetRole || 'renter');
const roleOptions = [
  { label: 'Guest', value: 'renter' },
  { label: 'Host', value: 'owner' }
];

const form = ref({
  email: '',
  password: ''
});

const loading = ref(false);
const error = ref('');

const registerPath = computed(() => targetRole.value === 'owner' ? '/register?role=owner' : '/register');

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    await authStore.login(form.value);
    
    // Validate role match
    if (authStore.user?.role !== targetRole.value) {
      error.value = `This account is not registered as a ${targetRole.value === 'owner' ? 'Host' : 'Guest'}.`;
      await authStore.logout();
      return;
    }

    if (authStore.user?.role === 'owner') {
      router.push('/owner');
    } else {
      router.push('/');
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Invalid email or password. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.auth-visual {
  flex: 1.2;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 4rem;
}

.auth-visual::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(to top, rgba(15, 23, 42, 0.8) 0%, rgba(15, 23, 42, 0) 100%);
}

.visual-content {
  position: relative;
  z-index: 10;
}

.auth-form-wrapper {
  flex: 1;
  background-color: var(--surface-section);
  padding: 3rem;
}

.auth-card {
  width: 100%;
  max-width: 480px;
}

.premium-toggle :deep(.p-highlight) {
  background: var(--primary-color) !important;
  color: white !important;
  border-color: var(--primary-color) !important;
}

.premium-toggle :deep(.p-button) {
  padding: 0.75rem 2rem;
  font-weight: 700;
}

/* Glass effect for light/dark modes */
.glass {
  background: transparent !important;
}

@media (max-width: 1024px) {
  .auth-visual {
    display: none;
  }
}
</style>