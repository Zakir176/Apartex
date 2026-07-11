<template>
  <div class="min-h-screen bg-animated-mesh flex justify-center items-center py-24 px-6 relative">
    <div class="w-full max-w-[440px] card-base p-10 text-center relative overflow-hidden z-10">
      <!-- Decorative element -->
      <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-accent to-orange-400"></div>

      <div class="text-accent font-black text-2xl mb-4 tracking-tight flex items-center justify-center gap-2">
        <i class="pi pi-compass text-xl"></i> APARTEX
      </div>
      <h1 class="text-3xl font-extrabold text-slate-800 mb-6">Create your account</h1>
      
      <div class="text-left mb-6">
        <label class="label-base">I want to be a</label>
        <SelectButton 
          v-model="targetRole" 
          :options="roleOptions" 
          optionLabel="label" 
          optionValue="value" 
          class="w-full [&_.p-button]:flex-1"
        />
      </div>

      <form @submit.prevent="handleRegister" class="flex flex-col text-left gap-5">
        <div>
          <label for="name" class="label-base">Full Name</label>
          <input 
            id="name" 
            v-model="form.name" 
            type="text" 
            required 
            placeholder="John Doe" 
            class="input-base" 
          />
        </div>

        <div>
          <label for="email" class="label-base">Email Address</label>
          <input 
            id="email" 
            v-model="form.email" 
            type="email" 
            required 
            placeholder="name@example.com" 
            class="input-base" 
          />
        </div>
        
        <div>
          <label for="password" class="label-base">Create Password</label>
          <Password 
            id="password" 
            v-model="form.password" 
            toggleMask 
            required 
            minlength="8"
            placeholder="••••••••" 
            inputClass="input-base" 
            class="w-full [&>input]:w-full"
          >
            <template #footer>
              <Divider />
              <p class="mt-2 font-bold text-xs uppercase text-slate-400 mb-2 tracking-widest">Security Advice</p>
              <ul class="pl-3 m-0 text-xs leading-5 text-slate-600 font-medium">
                <li>Use at least 8 characters</li>
                <li>Include numbers and symbols</li>
              </ul>
            </template>
          </Password>
        </div>

        <div class="flex items-center mb-2 mt-1">
          <Checkbox id="terms" v-model="acceptTerms" :binary="true" class="mr-2" />
          <label for="terms" class="text-sm font-bold text-slate-600 ml-2 cursor-pointer">
            I agree to the <a href="#" class="text-accent no-underline hover:underline">Membership Terms</a>
          </label>
        </div>
        
        <button type="submit" :disabled="loading || !acceptTerms" class="btn-accent shadow-accent w-full justify-center py-3.5 text-base mt-2">
          <i v-if="loading" class="pi pi-spin pi-spinner mr-2"></i>
          {{ loading ? 'Initializing...' : 'Register Now' }}
        </button>
        
        <div v-if="error" class="mt-2 p-3 text-red-700 bg-red-50 border border-red-100 rounded-xl text-sm font-bold flex items-start gap-2">
          <i class="pi pi-exclamation-triangle mt-0.5"></i>
          <span>{{ error }}</span>
        </div>
      </form>
      
      <div class="mt-8 text-sm font-medium text-slate-500">
        Already have an account? 
        <router-link to="/login" class="text-accent font-bold no-underline hover:underline ml-1">Sign In</router-link>
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
