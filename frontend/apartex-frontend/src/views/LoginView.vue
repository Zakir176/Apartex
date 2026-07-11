<template>
  <div class="min-h-screen bg-animated-mesh flex justify-center items-center py-24 px-6 relative">
    <div class="w-full max-w-[440px] card-base p-10 text-center relative overflow-hidden z-10">
      <!-- Decorative element -->
      <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-accent to-orange-400"></div>

      <div class="text-accent font-black text-2xl mb-4 tracking-tight flex items-center justify-center gap-2">
        <i class="pi pi-compass text-xl"></i> APARTEX
      </div>
      <h1 class="text-3xl font-extrabold text-slate-800 mb-6">Welcome back</h1>
      
      <div class="text-left mb-6">
        <label class="label-base">Login as</label>
        <SelectButton 
          v-model="targetRole" 
          :options="roleOptions" 
          optionLabel="label" 
          optionValue="value" 
          class="w-full [&_.p-button]:flex-1"
        />
      </div>

      <form @submit.prevent="handleLogin" class="flex flex-col text-left gap-5">
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
          <label for="password" class="label-base">Password</label>
          <Password 
            id="password" 
            v-model="form.password" 
            :feedback="false" 
            toggleMask 
            required 
            placeholder="••••••••" 
            inputClass="input-base" 
            class="w-full [&>input]:w-full"
          />
        </div>

        <div class="flex items-center mb-2 mt-1">
          <Checkbox id="remember" v-model="rememberMe" :binary="true" class="mr-2" />
          <label for="remember" class="text-sm font-bold text-slate-600 ml-2 cursor-pointer">Remember my session</label>
        </div>
        
        <button type="submit" :disabled="loading" class="btn-accent shadow-accent w-full justify-center py-3.5 text-base mt-2">
          <i v-if="loading" class="pi pi-spin pi-spinner mr-2"></i>
          {{ loading ? 'Authenticating...' : 'Sign In' }}
        </button>
        
        <div v-if="error" class="mt-2 p-3 text-red-700 bg-red-50 border border-red-100 rounded-xl text-sm font-bold flex items-start gap-2">
          <i class="pi pi-exclamation-triangle mt-0.5"></i>
          <span>{{ error }}</span>
        </div>
      </form>
      
      <div class="mt-8 text-sm font-medium text-slate-500">
        Don't have an account yet? 
        <router-link :to="registerPath" class="text-accent font-bold no-underline hover:underline ml-1">Register</router-link>
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
