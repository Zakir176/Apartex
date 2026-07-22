<template>
  <div class="min-h-screen bg-animated-mesh flex justify-center items-center py-24 px-6 relative">
    <div class="w-full max-w-[440px] card-base p-10 text-center relative overflow-hidden z-10">
      <!-- Decorative element -->
      <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-accent to-orange-400"></div>

      <div @click="router.push('/')" class="text-accent font-black text-2xl mb-4 tracking-tight flex items-center justify-center gap-2 cursor-pointer hover:opacity-80 transition-opacity">
        <i class="pi pi-building text-xl"></i> APARTEX
      </div>
      <h1 class="text-3xl font-extrabold text-slate-800 mb-6">Create your account</h1>
      
      <div class="text-left mb-6">
        <label class="label-base">I want to be a</label>
        <div class="grid grid-cols-2 gap-1 bg-slate-100 p-1 rounded-xl border border-surface-border">
          <button
            type="button"
            @click="targetRole = 'renter'"
            class="py-2.5 px-4 rounded-lg text-xs sm:text-sm font-extrabold transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer border-none"
            :class="targetRole === 'renter' ? 'bg-navy text-white shadow-md' : 'text-slate-500 hover:text-slate-900 bg-transparent'"
          >
            <i class="pi pi-user text-xs"></i> Guest
          </button>
          <button
            type="button"
            @click="targetRole = 'owner'"
            class="py-2.5 px-4 rounded-lg text-xs sm:text-sm font-extrabold transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer border-none"
            :class="targetRole === 'owner' ? 'bg-navy text-white shadow-md' : 'text-slate-500 hover:text-slate-900 bg-transparent'"
          >
            <i class="pi pi-building text-xs"></i> Host / Owner
          </button>
        </div>
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
          <label for="referral" class="label-base">Referral Code (Optional)</label>
          <input 
            id="referral" 
            v-model="form.referral_code" 
            type="text" 
            placeholder="e.g. A1B2C3D4" 
            class="input-base uppercase" 
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

        <div class="flex items-center mb-2 mt-1 cursor-pointer select-none" @click="acceptTerms = !acceptTerms">
          <div 
            class="w-5 h-5 rounded-md border flex items-center justify-center transition-all duration-200 shrink-0"
            :class="acceptTerms ? 'bg-accent border-accent text-white shadow-sm' : 'bg-white border-slate-300 hover:border-slate-400'"
          >
            <i v-if="acceptTerms" class="pi pi-check text-xs font-black"></i>
          </div>
          <span class="text-sm font-bold text-slate-700 ml-2.5">
            I agree to the <a href="#" @click.stop class="text-accent no-underline hover:underline">Membership Terms</a>
          </span>
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

const form = ref({ name: '', email: '', password: '', referral_code: '' });
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
