<template>
  <div class="auth-page-wrapper">
    <div class="grid grid-nogutter min-h-screen">
      <!-- Left: Immersive Visual Panel -->
      <div class="hidden lg:block lg:col-6 relative overflow-hidden bg-900">
        <div class="absolute top-0 left-0 w-full h-full z-0 bg-image"></div>
        <div class="absolute top-0 left-0 w-full h-full z-1 bg-overlay flex flex-column justify-content-end p-8">
          <div class="mb-4 text-left">
            <span class="inline-block px-3 py-1 bg-white-alpha-20 border-round-xl text-white text-xs font-bold uppercase tracking-widest mb-4 backdrop-blur-sm">Join the Network</span>
            <h1 class="text-white text-7xl font-bold mb-3 line-height-1">Join the <br/>Elite.</h1>
            <p class="text-white opacity-80 text-xl max-w-28rem font-medium line-height-3">Unlock exclusive access to premium properties and world-class host tools.</p>
          </div>
        </div>
      </div>

      <!-- Right: Register Form Panel -->
      <div class="col-12 lg:col-6 flex align-items-center justify-content-center bg-slate-50 p-4 lg:p-8">
        <div class="w-full max-w-28rem">
          <!-- Brand Identity -->
          <div class="flex align-items-center gap-2 mb-8">
            <div class="w-3rem h-3rem bg-900 border-round-xl flex align-items-center justify-content-center shadow-lg">
              <i class="pi pi-bolt text-white text-2xl"></i>
            </div>
            <div class="text-left">
              <h1 class="text-2xl font-bold tracking-tight">APARTEX</h1>
              <p class="text-xs font-bold text-500 uppercase tracking-widest">Luxury Rentals</p>
            </div>
          </div>

          <div class="mb-6 text-left">
            <h2 class="text-4xl font-extrabold text-900 mb-2 tracking-tight">Create Account</h2>
            <p class="text-600 font-medium">Start your journey with Apartex today</p>
          </div>

          <div class="mb-6 text-left">
            <label class="ax-label mb-3">I want to be a</label>
            <SelectButton 
              v-model="targetRole" 
              :options="roleOptions" 
              optionLabel="label" 
              optionValue="value" 
              class="w-full"
            />
          </div>

          <form @submit.prevent="handleRegister" class="grid grid-nogutter">
            <div class="col-12 mb-4 text-left">
              <label for="name" class="ax-label">Full Name</label>
              <div class="ax-input-wrapper">
                <i class="pi pi-user ax-input-icon"></i>
                <input 
                  id="name" 
                  v-model="form.name" 
                  type="text" 
                  required 
                  placeholder="John Doe" 
                  class="ax-input pl-10" 
                />
              </div>
            </div>

            <div class="col-12 mb-4 text-left">
              <label for="email" class="ax-label">Email Address</label>
              <div class="ax-input-wrapper">
                <i class="pi pi-envelope ax-input-icon"></i>
                <input 
                  id="email" 
                  v-model="form.email" 
                  type="email" 
                  required 
                  placeholder="name@example.com" 
                  class="ax-input pl-10" 
                />
              </div>
            </div>

            <div class="col-12 mb-5 text-left">
              <label for="password" class="ax-label">Create Password</label>
              <div class="ax-input-wrapper">
                <i class="pi pi-lock ax-input-icon z-2"></i>
                <Password 
                  id="password" 
                  v-model="form.password" 
                  toggleMask 
                  required 
                  minlength="8"
                  placeholder="••••••••" 
                  inputClass="ax-input pl-10 w-full" 
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
            </div>

            <div class="col-12 flex align-items-center mb-6">
              <Checkbox id="terms" v-model="acceptTerms" :binary="true" class="mr-2" />
              <label for="terms" class="text-600 text-sm font-semibold cursor-pointer">
                I agree to the <a href="#" class="text-900 font-bold no-underline hover:underline">Membership Terms</a>
              </label>
            </div>

            <div class="col-12">
              <button type="submit" :disabled="loading || !acceptTerms" class="ax-button w-full">
                <i v-if="loading" class="pi pi-spin pi-spinner mr-2"></i>
                <span>{{ loading ? 'Initializing...' : 'Register Now' }}</span>
                <i v-if="!loading" class="pi pi-check-circle ml-2 text-xs"></i>
              </button>
            </div>

            <Transition name="fade">
              <div v-if="error" class="col-12 mt-4 p-3 border-round-xl bg-red-50 text-red-600 text-sm font-bold flex align-items-center gap-2 border-1 border-red-100">
                <i class="pi pi-exclamation-circle"></i>
                <span>{{ error }}</span>
              </div>
            </Transition>
          </form>

          <div class="mt-8 pt-6 border-top-1 border-100 text-center">
            <p class="text-500 font-medium">
              Already have an account? 
              <router-link to="/login" class="text-900 font-bold no-underline hover:underline ml-1">
                Sign In
              </router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// PrimeVue components
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
.auth-page-wrapper {
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
  position: relative;
}
.bg-slate-50 { background-color: #f8fafc; }
.bg-image {
  background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=1920');
  background-size: cover;
  background-position: center;
}
.bg-overlay {
  background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.8));
}
.ax-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.ax-input-icon {
  position: absolute;
  left: 1rem;
  color: var(--surface-400);
  pointer-events: none;
}
.pl-10 { padding-left: 3rem !important; }
.z-0 { z-index: 0; }
.z-1 { z-index: 1; }
.z-2 { z-index: 2; }
.fade-enter-active, .fade-leave-active { transition: all 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-10px); }

/* Ensure left panel fills height */
.lg\:col-6 {
  min-height: 100vh;
}
</style>
