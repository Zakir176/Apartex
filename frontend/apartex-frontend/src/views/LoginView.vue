<template>
  <div class="grid grid-nogutter min-h-screen">
    <!-- Left: Immersive Visual Panel -->
    <div class="hidden lg:block lg:col-6 relative overflow-hidden">
      <div class="absolute inset-0 bg-cover bg-center" style="background-image: url('https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&q=80&w=1920');"></div>
      <div class="absolute inset-0 bg-black-alpha-40 flex flex-column justify-content-end p-8">
        <h1 class="text-white text-7xl font-bold mb-3 line-height-1">Elegance <br/>in Every Stay.</h1>
        <p class="text-white opacity-70 text-xl max-w-28rem font-medium">Bespoke living experiences curated for the world's most discerning travelers.</p>
      </div>
    </div>

    <!-- Right: Login Form Panel -->
    <div class="col-12 lg:col-6 flex align-items-center justify-content-center bg-white p-6">
      <div class="w-full max-w-26rem">
        <div class="mb-6">
          <h2 class="text-4xl font-bold text-900 mb-2">Member Login</h2>
          <p class="text-500 font-medium">Enter your credentials to access your account</p>
        </div>

        <div class="flex justify-content-center mb-6">
          <SelectButton 
            v-model="targetRole" 
            :options="roleOptions" 
            optionLabel="label" 
            optionValue="value" 
            class="w-full"
          />
        </div>

        <form @submit.prevent="handleLogin">
          <div class="mb-4">
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
          
          <div class="mb-2">
            <div class="flex justify-content-between align-items-center mb-1">
              <label for="password" class="ax-label mb-0">Password</label>
              <a href="#" class="text-xs font-bold text-900 no-underline hover:underline uppercase tracking-wider">Forgot?</a>
            </div>
            <Password 
              id="password" 
              v-model="form.password" 
              :feedback="false" 
              toggleMask 
              required 
              placeholder="••••••••" 
              inputClass="ax-input w-full" 
            />
          </div>

          <div class="flex align-items-center mb-6">
            <Checkbox id="remember" v-model="rememberMe" :binary="true" class="mr-2" />
            <label for="remember" class="text-600 text-sm font-medium cursor-pointer">Remember me</label>
          </div>
          
          <button type="submit" :disabled="loading" class="ax-button w-full shadow-lg">
            {{ loading ? 'Verifying...' : 'Sign In' }}
          </button>
          
          <Transition name="fade">
            <div v-if="error" class="mt-4 p-3 border-round-xl bg-red-50 text-red-600 text-sm font-bold flex align-items-center gap-2">
              <i class="pi pi-exclamation-circle"></i>
              <span>{{ error }}</span>
            </div>
          </Transition>
        </form>
        
        <div class="mt-8 pt-6 border-top-1 border-100 text-center">
          <p class="text-500 font-medium">
            New to Apartex? 
            <router-link :to="registerPath" class="text-900 font-bold no-underline hover:underline ml-1">
              Create Account
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
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>