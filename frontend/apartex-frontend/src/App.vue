<template>
  <div id="app">
    <nav v-if="authStore.isAuthenticated" class="navbar shadow-sm">
      <div class="nav-brand" @click="goHome">
        <span class="text-primary font-bold text-2xl cursor-pointer">Apartex</span>
      </div>
      
      <div class="nav-links">
        <!-- Renter nav -->
        <template v-if="authStore.user?.role === 'renter'">
          <router-link to="/" class="nav-item">Home</router-link>
          <router-link to="/apartments" class="nav-item">Apartments</router-link>
          <router-link to="/bookings" class="nav-item">My Bookings</router-link>
          <router-link to="/loyalty" class="nav-item">Loyalty</router-link>
        </template>
        
        <!-- Owner nav -->
        <template v-else-if="authStore.user?.role === 'owner'">
          <router-link to="/owner" class="nav-item">Home</router-link>
          <router-link to="/dashboard" class="nav-item">Dashboard</router-link>
          <router-link to="/owner/apartments" class="nav-item">My Apartments</router-link>
          <router-link to="/owner/bookings" class="nav-item">Bookings</router-link>
          <router-link to="/owner/payouts" class="nav-item">Payouts</router-link>
        </template>

        <div class="divider mx-3"></div>

        <div class="user-section">
          <!-- Theme Toggle -->
          <Button 
            :icon="themeStore.isDark ? 'pi pi-sun' : 'pi pi-moon'" 
            @click="themeStore.toggle" 
            class="p-button-rounded p-button-text p-button-secondary mr-2" 
          />
          
          <Avatar icon="pi pi-user" shape="circle" class="mr-2" />
          <span class="user-name">{{ authStore.user?.name }}</span>
          <Button icon="pi pi-sign-out" @click="handleLogout" class="p-button-text p-button-danger p-button-sm ml-2" />
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view />
    </main>

    <Toast position="bottom-right" />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import { useThemeStore } from './stores/theme';

// PrimeVue components
import Button from 'primevue/button';
import Avatar from 'primevue/avatar';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';

const authStore = useAuthStore();
const themeStore = useThemeStore();
const router = useRouter();

const goHome = () => {
  if (authStore.user?.role === 'owner') router.push('/owner');
  else router.push('/');
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style>
/* Modern CSS Variable System */
:root {
  --primary-color: #3b82f6;
  --primary-light: #eff6ff;
  --surface-ground: #f8fafc;
  --surface-section: #ffffff;
  --surface-card: #ffffff;
  --surface-border: #e2e8f0;
  --text-color: #1e293b;
  --text-muted: #64748b;
  --nav-bg: #ffffff;
  --transition-speed: 0.3s;
}

/* Dark Mode Overrides */
.dark {
  --surface-ground: #0f172a;/* slate-900 */
  --surface-section: #1e293b;/* slate-800 */
  --surface-card: #1e293b;
  --surface-border: #334155;/* slate-700 */
  --text-color: #f1f5f9;/* slate-100 */
  --text-muted: #94a3b8;/* slate-400 */
  --nav-bg: #1e293b;
  --primary-light: #1e293b;
}

* {
  transition: background-color var(--transition-speed), border-color var(--transition-speed), color var(--transition-speed);
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: var(--surface-ground);
  color: var(--text-color);
  min-h: 100vh;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 2rem;
  background-color: var(--nav-bg);
  border-bottom: 1px solid var(--surface-border);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-item {
  text-decoration: none;
  color: var(--text-color);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s;
  font-size: 0.95rem;
}

.nav-item:hover,
.nav-item.router-link-active {
  background-color: var(--primary-light);
  color: var(--primary-color);
}

.divider {
  width: 1px;
  height: 24px;
  background-color: var(--surface-border);
}

.user-section {
  display: flex;
  align-items: center;
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-color);
}

.main-content {
  min-height: calc(100vh - 64px);
}

/* Global Premium Theme Overrides */
:root {
  /* Core Palette */
  --primary: #6366f1;
  --primary-gradient: linear-gradient(135deg, #06b6d4 0%, #6366f1 100%);
  --surface-glass: rgba(255, 255, 255, 0.7);
  --surface-border-glass: rgba(255, 255, 255, 0.3);
  
  /* Aura Shadows */
  --shadow-premium: 0 10px 30px -5px rgba(0, 0, 0, 0.1), 0 4px 12px -4px rgba(0, 0, 0, 0.05);
  --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.3);
}

.dark {
  --surface-glass: rgba(15, 23, 42, 0.6);
  --surface-border-glass: rgba(255, 255, 255, 0.1);
}

/* Global Button Overhaul */
:deep(.p-button.p-button-primary) {
  background: var(--primary-gradient) !important;
  border: none !important;
  padding: 0.75rem 1.5rem;
  border-radius: 14px;
  font-weight: 700;
  letter-spacing: -0.2px;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: var(--shadow-premium);
}

:deep(.p-button.p-button-primary:hover) {
  transform: translateY(-2px) scale(1.02);
  box-shadow: var(--shadow-glow);
}

:deep(.p-button.p-button-primary:active) {
  transform: scale(0.98);
}

:deep(.p-button.p-button-text) {
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.2s;
}

:deep(.p-button.p-button-outlined) {
  border: 1px solid var(--surface-border-glass) !important;
  background: var(--surface-glass) !important;
  backdrop-filter: blur(8px);
  border-radius: 12px;
}

/* Card & Glassmorphism */
:deep(.p-card) {
  border-radius: 24px;
  border: 1px solid var(--surface-border-glass) !important;
  background: var(--surface-card) !important;
  box-shadow: var(--shadow-premium);
  overflow: hidden;
}

/* Form Polish */
:deep(.p-inputtext), :deep(.p-inputnumber-input) {
  border-radius: 12px !important;
  color: var(--text-color) !important;
}

.p-button.p-button-text.p-button-secondary {
  color: var(--text-muted) !important;
}

.p-button.p-button-text.p-button-secondary:hover {
  background: var(--primary-light) !important;
  color: var(--primary-color) !important;
}
</style>