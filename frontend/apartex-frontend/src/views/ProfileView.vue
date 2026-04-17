<template>
  <div class="profile-dashboard fadein animation-duration-500">
    <div class="dashboard-header mb-5">
      <h1 class="text-4xl font-bold mb-2">Account Dashboard</h1>
      <p class="text-muted text-lg">Manage your personal identity and security preferences</p>
    </div>

    <div class="grid">
      <!-- Left Column: Avatar & Quick Info -->
      <div class="col-12 lg:col-4">
        <Card class="identity-card mb-4 border-none shadow-sm">
          <template #content>
            <div class="flex flex-column align-items-center py-4">
              <div class="avatar-container mb-4">
                <Avatar 
                  :image="authStore.user?.avatar_url || '/placeholder-avatar.png'" 
                  size="xlarge" 
                  shape="circle" 
                  class="profile-avatar shadow-lg" 
                />
                <Button 
                  icon="pi pi-camera" 
                  class="p-button-rounded p-button-primary avatar-edit-btn" 
                  @click="$refs.avatarInput.click()"
                />
                <input type="file" ref="avatarInput" hidden accept="image/*" @change="handleAvatarUpload" />
              </div>
              <h2 class="text-2xl font-bold mb-1">{{ authStore.user?.full_name || 'Anonymous' }}</h2>
              <Tag 
                :value="authStore.user?.role?.toUpperCase()" 
                :severity="authStore.user?.role === 'owner' ? 'warning' : 'info'" 
                rounded 
                class="px-3 py-1 font-bold tracking-wider"
              />
              
              <div class="mt-5 w-full flex flex-column gap-3 pt-4 border-top-1 border-gray-100">
                <div class="flex justify-content-between text-sm">
                  <span class="text-muted">Member Since</span>
                  <span class="font-bold">April 2024</span>
                </div>
                <div class="flex justify-content-between text-sm">
                  <span class="text-muted">Verified</span>
                  <i class="pi pi-verified text-primary"></i>
                </div>
              </div>
            </div>
          </template>
        </Card>
      </div>

      <!-- Right Column: Settings Form -->
      <div class="col-12 lg:col-8">
        <Card class="settings-card border-none shadow-sm">
          <template #title>
            <div class="flex align-items-center gap-2 mb-2">
              <i class="pi pi-user text-primary"></i>
              <span>Personal Information</span>
            </div>
          </template>
          <template #content>
            <form @submit.prevent="saveProfile" class="p-fluid grid mt-2">
              <div class="field col-12 md:col-6 mb-4">
                <label for="fullName" class="font-bold text-sm block mb-2 text-muted uppercase">Full Display Name</label>
                <InputText id="fullName" v-model="fullName" placeholder="Your full name" class="p-inputtext-lg" />
              </div>
              
              <div class="field col-12 md:col-6 mb-4">
                <label for="email" class="font-bold text-sm block mb-2 text-muted uppercase">Email Address</label>
                <InputText id="email" :value="authStore.user?.email" disabled class="p-inputtext-lg opacity-60" />
                <small class="text-muted block mt-1"><i class="pi pi-lock mr-1"></i>Email cannot be changed</small>
              </div>

              <div class="col-12 border-top-1 border-gray-100 mt-4 pt-4 mb-4">
                <div class="flex align-items-center gap-2 mb-4">
                  <i class="pi pi-shield text-primary"></i>
                  <span class="text-xl font-bold">Account Security</span>
                </div>
                <div class="field col-12 md:col-6">
                  <label class="font-bold text-sm block mb-2 text-muted uppercase">Password</label>
                  <Button 
                    label="Reset My Password" 
                    icon="pi pi-refresh" 
                    class="p-button-text p-button-sm font-bold p-0 w-fit" 
                    @click="confirmPasswordReset"
                  />
                </div>
              </div>

              <div class="col-12 flex justify-content-end mt-4">
                <Button 
                  type="submit" 
                  label="Save Updates" 
                  icon="pi pi-check" 
                  :loading="saving" 
                  class="p-button-primary p-button-lg px-5 font-bold border-round-xl" 
                />
              </div>
            </form>
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { authApi } from '@/api/auth';
import { useAuthStore } from '@/stores/auth';
import { uploadImage } from '@/api/uploads';
import { useConfirm } from "primevue/useconfirm";

// PrimeVue components
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Avatar from 'primevue/avatar';
import Tag from 'primevue/tag';

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

<style scoped>
.profile-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.identity-card, .settings-card {
  background: var(--surface-card) !important;
  border: 1px solid var(--surface-border) !important;
  border-radius: 20px !important;
}

.avatar-container {
  position: relative;
}

.profile-avatar {
  width: 140px !important;
  height: 140px !important;
  border: 4px solid white;
}

.avatar-edit-btn {
  position: absolute;
  bottom: 5px;
  right: 5px;
  width: 40px !important;
  height: 40px !important;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
}

.dark .profile-avatar {
  border-color: #1e293b;
}

:deep(.p-card-title) {
  font-size: 1.5rem !important;
  font-weight: 800 !important;
}

@media (max-width: 991px) {
  .profile-dashboard {
    padding: 2rem 1rem;
  }
}
</style>
