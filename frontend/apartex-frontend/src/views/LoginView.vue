<template>
  <div class="min-h-screen bg-animated-mesh flex flex-col justify-center items-center py-12 px-6 relative">

    <!-- LOTTIE ANIMATION PHASE -->
    <Transition name="lottie-out">
      <div
        v-if="showAnimation"
        class="flex flex-col items-center justify-center gap-4"
      >
        <!-- Brand above animation -->
        <div
          class="text-accent font-black text-2xl tracking-tight flex items-center gap-2 mb-2"
          v-motion
          :initial="{ opacity: 0, y: -12 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 400 } }"
        >
          <i class="pi pi-building text-xl"></i> APARTEX
        </div>

        <!-- Lottie animation -->
        <Vue3Lottie
          animationLink="https://assets3.lottiefiles.com/packages/lf20_hu9cd9.json"
          :height="240"
          :width="240"
          :loop="false"
          :autoPlay="true"
          @onComplete="onAnimationComplete"
        />

        <p class="text-slate-400 text-sm font-medium animate-pulse">
          Welcome back...
        </p>

        <button
          @click="onAnimationComplete"
          class="text-xs text-slate-300 hover:text-slate-500 transition-colors duration-150 mt-2 underline underline-offset-2"
        >
          Skip
        </button>
      </div>
    </Transition>

    <!-- FORM PHASE -->
    <Transition name="form-in">
      <div
        v-if="showForm"
        class="w-full max-w-[440px] card-base p-10 text-center relative overflow-hidden z-10"
      >
        <!-- Accent top bar -->
        <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-accent to-orange-400"></div>

        <!-- Brand -->
        <div
          @click="router.push('/')"
          class="text-accent font-black text-2xl mb-4 tracking-tight flex items-center justify-center gap-2 cursor-pointer hover:opacity-80 transition-opacity"
        >
          <i class="pi pi-building text-xl"></i> APARTEX
        </div>

        <h1 class="text-3xl font-extrabold text-slate-800 mb-6">Welcome back</h1>

        <!-- Role selector -->
        <div class="text-left mb-6">
          <label class="label-base">Login as</label>
          <div class="grid grid-cols-2 gap-1 bg-slate-100 p-1 rounded-xl border border-surface-border">
            <button
              type="button"
              @click="targetRole = 'renter'"
              class="py-2.5 px-4 rounded-lg text-xs sm:text-sm font-extrabold transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer border-none"
              :class="targetRole === 'renter' ? 'bg-navy text-white shadow-md' : 'text-slate-500 hover:text-slate-900 bg-transparent'"
            >
              <i class="pi pi-user text-sm"></i> Guest
            </button>
            <button
              type="button"
              @click="targetRole = 'owner'"
              class="py-2.5 px-4 rounded-lg text-xs sm:text-sm font-extrabold transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer border-none"
              :class="targetRole === 'owner' ? 'bg-navy text-white shadow-md' : 'text-slate-500 hover:text-slate-900 bg-transparent'"
            >
              <i class="pi pi-building text-sm"></i> Host / Owner
            </button>
          </div>
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

          <div class="flex items-center mb-2 mt-1 cursor-pointer select-none" @click="rememberMe = !rememberMe">
            <div 
              class="w-5 h-5 rounded-md border flex items-center justify-center transition-all duration-200 shrink-0"
              :class="rememberMe ? 'bg-accent border-accent text-white shadow-sm' : 'bg-white border-slate-300 hover:border-slate-400'"
            >
              <i v-if="rememberMe" class="pi pi-check text-xs font-black"></i>
            </div>
            <span class="text-sm font-bold text-slate-700 ml-2.5">Remember my session</span>
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
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

import Password from 'primevue/password';
import SelectButton from 'primevue/selectbutton';
import Checkbox from 'primevue/checkbox';

const showAnimation = ref(true);
const showForm = ref(false);

function onAnimationComplete() {
  showAnimation.value = false;
  setTimeout(() => {
    showForm.value = true;
  }, 150);
}

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
    router.push(authStore.user?.role === 'owner' ? '/owner' : '/home');
  } catch (err) {
    const detail = err.response?.data?.detail;
    if (Array.isArray(detail)) {
      error.value = detail.map(d => d.msg || d.detail).join('. ');
    } else if (typeof detail === 'string') {
      error.value = detail;
    } else {
      error.value = 'Identity verification failed. Please check your credentials.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Lottie phase exits upward */
.lottie-out-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.lottie-out-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Form slides up and fades in */
.form-in-enter-active {
  transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.form-in-enter-from {
  opacity: 0;
  transform: translateY(32px);
}
</style>
