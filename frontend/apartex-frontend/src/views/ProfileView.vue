<template>
  <div class="max-w-[1200px] mx-auto px-6 py-12">
    <!-- Header -->
    <div class="mb-10 text-center md:text-left">
      <h1 class="text-4xl font-extrabold text-slate-800 mb-2">Account Dashboard</h1>
      <p class="text-slate-500 font-medium text-lg">Manage your personal identity and security preferences</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Left Column: Avatar & Quick Info -->
      <div class="lg:col-span-1">
        <div class="card-base p-8 text-center flex flex-col items-center">
          <div class="relative mb-6">
            <div class="w-36 h-36 rounded-full overflow-hidden border-4 border-white shadow-xl bg-slate-100 flex items-center justify-center">
              <img v-if="authStore.user?.avatar_url" :src="authStore.user?.avatar_url" alt="Avatar" class="w-full h-full object-cover" />
              <i v-else class="pi pi-user text-5xl text-slate-300"></i>
            </div>
            <button 
              @click="$refs.avatarInput.click()"
              class="absolute bottom-1 right-1 w-10 h-10 rounded-full bg-accent text-white shadow-lg flex items-center justify-center hover:bg-orange-600 transition-colors transform hover:scale-105 active:scale-95"
            >
              <i class="pi pi-camera"></i>
            </button>
            <input type="file" ref="avatarInput" hidden accept="image/*" @change="handleAvatarUpload" />
          </div>
          
          <h2 class="text-2xl font-black text-slate-800 mb-2">{{ authStore.user?.full_name || 'Anonymous' }}</h2>
          <span 
            class="px-4 py-1.5 rounded-full text-xs font-extrabold uppercase tracking-wider mb-8 inline-block"
            :class="authStore.user?.role === 'owner' ? 'bg-accent-light text-accent border border-orange-200' : 'bg-navy-50 text-navy border border-navy-100'"
          >
            <i :class="authStore.user?.role === 'owner' ? 'pi pi-building' : 'pi pi-user'" class="mr-1 text-[10px]"></i>
            {{ authStore.user?.role === 'owner' ? 'Host / Owner' : 'Guest / Renter' }}
          </span>
          
          <div class="w-full pt-6 border-t border-surface-border flex flex-col gap-4 text-left">
            <div class="flex justify-between items-center text-sm">
              <span class="text-slate-500 font-medium">Member Since</span>
              <span class="font-bold text-slate-800">April 2024</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="text-slate-500 font-medium">Verified Status</span>
              <div class="flex items-center gap-1.5 text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded-md">
                <i class="pi pi-verified text-xs"></i> Verified
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Settings Form -->
      <div class="lg:col-span-2">
        <div class="card-base">
          <div class="p-6 md:p-8 border-b border-surface-border flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <i class="pi pi-user text-lg"></i>
            </div>
            <h2 class="text-2xl font-bold text-slate-800">Personal Information</h2>
          </div>
          
          <div class="p-6 md:p-8">
            <form @submit.prevent="saveProfile" class="flex flex-col gap-8">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="label-base">Full Display Name</label>
                  <input v-model="fullName" type="text" class="input-base" placeholder="Your full name" />
                </div>
                
                <div>
                  <label class="label-base">Email Address</label>
                  <input :value="authStore.user?.email" disabled type="email" class="input-base opacity-60 bg-slate-50 cursor-not-allowed" />
                  <p class="text-xs font-medium text-slate-400 mt-2 flex items-center gap-1.5">
                    <i class="pi pi-lock"></i> Email cannot be changed
                  </p>
                </div>
              </div>

              <div class="pt-8 border-t border-surface-border">
                <div class="flex items-center gap-3 mb-6">
                  <div class="w-10 h-10 rounded-xl bg-orange-50 text-accent flex items-center justify-center">
                    <i class="pi pi-shield text-lg"></i>
                  </div>
                  <h3 class="text-xl font-bold text-slate-800">Account Security</h3>
                </div>
                
                <div>
                  <label class="label-base">Password</label>
                  <button type="button" @click="confirmPasswordReset" class="px-5 py-2.5 rounded-full border border-surface-border text-sm font-bold text-slate-600 hover:bg-slate-50 transition-colors inline-flex items-center gap-2">
                    <i class="pi pi-refresh"></i>
                    Reset My Password
                  </button>
                </div>
              </div>

              <div class="pt-6 flex justify-end">
                <button type="submit" :disabled="saving" class="btn-accent shadow-accent inline-flex items-center gap-2 px-8 py-3.5 text-base">
                  <i class="pi pi-check" v-if="!saving"></i>
                  <i class="pi pi-spinner pi-spin" v-else></i>
                  Save Updates
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { authApi } from '@/api/auth';
import { useAuthStore } from '@/stores/auth';
import { uploadImage } from '@/api/uploads';
import { useConfirm } from "primevue/useconfirm";

// PrimeVue components
import ConfirmDialog from 'primevue/confirmdialog';

const authStore = useAuthStore();
const confirm = useConfirm();
const fullName = ref('');
const saving = ref(false);

onMounted(async () => {
  if (!authStore.user) {
    try { await authStore.fetchCurrentUser(); } catch {}
  }
  fullName.value = authStore.user?.full_name || '';
});

async function saveProfile() {
  saving.value = true;
  try {
    await authApi.updateProfile({ full_name: fullName.value });
    await authStore.fetchCurrentUser();
  } finally {
    saving.value = false;
  }
}

async function handleAvatarUpload(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  
  try {
    const { url } = await uploadImage(file);
    await authApi.updateProfile({ avatar_url: url });
    await authStore.fetchCurrentUser();
  } catch (err) {
    console.error('Avatar upload failed', err);
  }
}

const confirmPasswordReset = () => {
  confirm.require({
    message: 'We will send a password reset link to your email. Continue?',
    header: 'Security Update',
    icon: 'pi pi-exclamation-triangle',
    accept: () => {
      // Logic for reset
    }
  });
};
</script>
