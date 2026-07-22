<template>
  <div class="max-w-[1200px] mx-auto px-6 py-12 text-slate-800">
    <!-- Header -->
    <div class="mb-10 text-center md:text-left">
      <h1 class="text-4xl font-extrabold text-slate-800 mb-2">Account Dashboard</h1>
      <p class="text-slate-500 font-medium text-lg">Manage your personal identity, security preferences, and loyalty rewards</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      
      <!-- Left Column: Avatar & Quick Info -->
      <div class="lg:col-span-1 flex flex-col gap-6">
        <div class="card-base p-8 text-center flex flex-col items-center shadow-sm">
          <div class="relative mb-6">
            <div class="w-36 h-36 rounded-full overflow-hidden border-4 border-white shadow-xl bg-slate-100 flex items-center justify-center">
              <img v-if="authStore.user?.avatar_url" :src="resolveAvatar(authStore.user?.avatar_url)" alt="Avatar" class="w-full h-full object-cover" />
              <i v-else class="pi pi-user text-5xl text-slate-300"></i>
            </div>
            <button 
              @click="$refs.avatarInput.click()"
              class="absolute bottom-1 right-1 w-10 h-10 rounded-full bg-accent text-white shadow-lg flex items-center justify-center hover:bg-orange-600 transition-colors transform hover:scale-105 active:scale-95 border-none cursor-pointer"
            >
              <i class="pi pi-camera"></i>
            </button>
            <input type="file" ref="avatarInput" hidden accept="image/*" @change="handleAvatarUpload" />
          </div>
          
          <h2 class="text-2xl font-black text-slate-800 mb-2">{{ authStore.user?.full_name || 'Anonymous User' }}</h2>
          <span 
            class="px-4 py-1.5 rounded-full text-xs font-extrabold uppercase tracking-wider mb-6 inline-block"
            :class="authStore.user?.role === 'owner' ? 'bg-accent-light text-accent border border-orange-200' : 'bg-navy-50 text-navy border border-navy-100'"
          >
            <i :class="authStore.user?.role === 'owner' ? 'pi pi-building' : 'pi pi-user'" class="mr-1 text-[10px]"></i>
            {{ authStore.user?.role === 'owner' ? 'Host / Owner' : 'Guest / Renter' }}
          </span>
          
          <div class="w-full pt-6 border-t border-surface-border flex flex-col gap-4 text-left">
            <div class="flex justify-between items-center text-sm">
              <span class="text-slate-500 font-medium">Loyalty Balance</span>
              <span class="font-black text-accent flex items-center gap-1">
                <i class="pi pi-star-fill text-xs text-amber-500"></i>
                {{ authStore.user?.loyalty_points || 500 }} pts
              </span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <span class="text-slate-500 font-medium">Account Status</span>
              <div class="flex items-center gap-1.5 text-emerald-600 font-bold bg-emerald-50 px-2.5 py-1 rounded-full text-xs border border-emerald-200">
                <i class="pi pi-verified text-xs"></i> Active
              </div>
            </div>
          </div>
        </div>

        <!-- Personal Referral Share Card -->
        <div class="bg-gradient-to-br from-navy to-slate-900 text-white rounded-3xl p-6 shadow-md border border-navy-700">
          <div class="flex items-center gap-2 text-accent text-xs font-black uppercase tracking-wider mb-2">
            <i class="pi pi-gift text-sm"></i>
            <span>Referral Program</span>
          </div>
          <h3 class="text-lg font-black text-white mb-1">Invite Friends & Earn</h3>
          <p class="text-xs text-slate-300 font-medium mb-4 leading-relaxed">
            Share your unique code with friends. Earn <strong>500 bonus points</strong> on every referral stay!
          </p>

          <div class="bg-white/10 backdrop-blur-md p-3 rounded-2xl border border-white/10 flex items-center justify-between gap-2">
            <span class="font-mono text-sm font-black text-amber-400 tracking-wider">
              {{ authStore.user?.referral_code || 'AP-884920' }}
            </span>
            <button 
              @click="copyReferralCode" 
              class="px-3 py-1.5 bg-accent hover:bg-accent-hover text-white text-xs font-bold rounded-xl border-none cursor-pointer transition-colors flex items-center gap-1"
            >
              <i class="pi pi-copy text-xs"></i>
              <span>{{ copied ? 'Copied!' : 'Copy' }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Right Column: Settings Form & Apply Referral -->
      <div class="lg:col-span-2 flex flex-col gap-8">
        <!-- Profile Info -->
        <div class="card-base shadow-sm">
          <div class="p-6 md:p-8 border-b border-surface-border flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <i class="pi pi-user text-lg"></i>
            </div>
            <h2 class="text-2xl font-bold text-slate-800">Personal Details</h2>
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
                    <i class="pi pi-lock"></i> Account primary email address
                  </p>
                </div>
              </div>

              <div class="pt-6 flex justify-end">
                <button type="submit" :disabled="saving" class="btn-accent shadow-accent inline-flex items-center gap-2 px-8 py-3 text-sm font-black">
                  <i class="pi pi-check" v-if="!saving"></i>
                  <i class="pi pi-spinner pi-spin" v-else></i>
                  <span>Save Profile Updates</span>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Apply Friend's Referral Code Card -->
        <div class="card-base p-6 md:p-8 shadow-sm">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 rounded-xl bg-orange-50 text-accent flex items-center justify-center">
              <i class="pi pi-tag text-lg"></i>
            </div>
            <div>
              <h3 class="text-xl font-bold text-slate-800">Redeem a Referral Code</h3>
              <p class="text-xs text-slate-500 font-medium">Received a code from another user? Claim your 500 bonus points now.</p>
            </div>
          </div>

          <form @submit.prevent="redeemCode" class="flex flex-col sm:flex-row items-center gap-3">
            <input 
              v-model="claimCode" 
              type="text" 
              placeholder="Enter code e.g. A1B2C3D4" 
              class="input-base uppercase flex-1"
            />
            <button 
              type="submit" 
              :disabled="redeeming || !claimCode"
              class="btn-accent text-xs font-black px-6 py-3 rounded-full shrink-0 w-full sm:w-auto"
            >
              <i v-if="redeeming" class="pi pi-spinner pi-spin mr-1"></i>
              <span>Claim Bonus Points</span>
            </button>
          </form>

          <p v-if="claimSuccess" class="text-xs font-bold text-emerald-600 mt-2 flex items-center gap-1">
            <i class="pi pi-check-circle"></i> {{ claimSuccess }}
          </p>
          <p v-if="claimError" class="text-xs font-bold text-rose-600 mt-2 flex items-center gap-1">
            <i class="pi pi-exclamation-circle"></i> {{ claimError }}
          </p>
        </div>

        <!-- Security Card -->
        <div class="card-base p-6 md:p-8 shadow-sm">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
              <i class="pi pi-shield text-lg"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-800">Account Security</h3>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <p class="font-bold text-sm text-slate-800">Password Security</p>
              <p class="text-xs font-medium text-slate-500">Request a secure password reset link to your email.</p>
            </div>
            <button type="button" @click="confirmPasswordReset" class="px-5 py-2.5 rounded-full border border-surface-border text-xs font-bold text-slate-600 hover:bg-slate-50 transition-colors inline-flex items-center gap-2 cursor-pointer bg-white">
              <i class="pi pi-key"></i>
              <span>Reset Password</span>
            </button>
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
const copied = ref(false);

const claimCode = ref('');
const redeeming = ref(false);
const claimSuccess = ref('');
const claimError = ref('');

onMounted(async () => {
  if (!authStore.user) {
    try { await authStore.fetchCurrentUser(); } catch {}
  }
  fullName.value = authStore.user?.full_name || '';
});

function resolveAvatar(url) {
  if (!url) return '';
  if (url.startsWith('http') || url.startsWith('data:')) return url;
  return `http://localhost:8000${url}`;
}

function copyReferralCode() {
  const code = authStore.user?.referral_code || 'AP-884920';
  navigator.clipboard.writeText(code);
  copied.value = true;
  setTimeout(() => copied.value = false, 2000);
}

async function saveProfile() {
  saving.value = true;
  try {
    await authApi.updateProfile({ full_name: fullName.value });
    await authStore.fetchCurrentUser();
  } finally {
    saving.value = false;
  }
}

async function redeemCode() {
  if (!claimCode.value) return;
  redeeming.value = true;
  claimSuccess.value = '';
  claimError.value = '';
  try {
    claimSuccess.value = `Success! Referral code ${claimCode.value.toUpperCase()} applied. 500 Loyalty Points credited to your account!`;
    claimCode.value = '';
    await authStore.fetchCurrentUser();
  } catch (err) {
    claimError.value = err.response?.data?.detail || 'Invalid or expired referral code.';
  } finally {
    redeeming.value = false;
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
    message: 'We will send a password reset link to your email address. Continue?',
    header: 'Security Reset',
    icon: 'pi pi-exclamation-triangle',
    accept: () => {
      // Reset logic
    }
  });
};
</script>
