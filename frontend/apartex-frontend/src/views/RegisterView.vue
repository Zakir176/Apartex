<template>
  <div class="grid grid-nogutter min-h-screen">
    <!-- Left: Immersive Visual Panel -->
    <div class="hidden lg:block lg:col-6 relative overflow-hidden">
      <div class="absolute inset-0 bg-cover bg-center" style="background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=1920');"></div>
      <div class="absolute inset-0 bg-black-alpha-40 flex flex-column justify-content-end p-8">
        <h1 class="text-white text-7xl font-bold mb-3 line-height-1">Join the <br/>Elite.</h1>
        <p class="text-white opacity-70 text-xl max-w-28rem font-medium">Unlock exclusive access to premium properties and world-class host tools.</p>
      </div>
    </div>

    <!-- Right: Register Form Panel -->
    <div class="col-12 lg:col-6 flex align-items-center justify-content-center bg-white p-6">
      <div class="w-full max-w-26rem">
        <div class="mb-6">
          <h2 class="text-4xl font-bold text-900 mb-2">Create Account</h2>
          <p class="text-500 font-medium">Start your journey with Apartex today</p>
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

        <form @submit.prevent="handleRegister">
          <div class="mb-4">
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

          <div class="mb-5">
            <label for="password" class="ax-label">Create Password</label>
            <Password 
              id="password" 
              v-model="form.password" 
              toggleMask 
              required 
              minlength="8"
              placeholder="••••••••" 
              inputClass="ax-input w-full" 
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

          <div class="flex align-items-center mb-6">
            <Checkbox id="terms" v-model="acceptTerms" :binary="true" class="mr-2" />
            <label for="terms" class="text-600 text-sm font-medium cursor-pointer">
              I agree to the <a href="#" class="text-900 font-bold no-underline hover:underline">Membership Terms</a>
            </label>
          </div>

          <button type="submit" :disabled="loading || !acceptTerms" class="ax-button w-full shadow-lg">
            {{ loading ? 'Initializing...' : 'Register Now' }}
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
            Already have an account? 
            <router-link to="/login" class="text-900 font-bold no-underline hover:underline ml-1">
              Sign In
            </router-link>
          </p>
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
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>