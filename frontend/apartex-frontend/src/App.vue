<template>
  <div id="app" :class="{ 'dark': themeStore.isDark }">
    <header v-if="authStore.isAuthenticated" class="surface-0 border-bottom-1 border-200 sticky top-0 z-5">
      <div class="ax-container flex align-items-center justify-content-between h-5rem">
        <div class="flex align-items-center gap-4">
          <!-- Mobile Menu Toggle -->
          <Button 
            icon="pi pi-bars" 
            @click="mobileMenuVisible = true" 
            class="p-button-text p-button-secondary lg:hidden" 
          />

          <div class="cursor-pointer" @click="goHome">
            <h1 class="text-2xl font-bold tracking-tight text-900">Apartex</h1>
          </div>
          
          <nav class="hidden lg:flex align-items-center gap-2">
            <!-- Renter nav -->
            <template v-if="authStore.user?.role === 'renter'">
              <router-link to="/" class="nav-link">Home</router-link>
              <router-link to="/apartments" class="nav-link">Explore</router-link>
              <router-link to="/bookings" class="nav-link">Bookings</router-link>
              <router-link to="/loyalty" class="nav-link">Loyalty Rewards</router-link>
            </template>
            
            <!-- Owner nav -->
            <template v-else-if="authStore.user?.role === 'owner'">
              <router-link to="/owner" class="nav-link">Overview</router-link>
              <router-link to="/dashboard" class="nav-link">Analytics</router-link>
              <router-link to="/owner/apartments" class="nav-link">Properties</router-link>
              <router-link to="/owner/bookings" class="nav-link">Reservations</router-link>
              <router-link to="/owner/payouts" class="nav-link">Payouts</router-link>
            </template>
          </nav>
        </div>

        <div class="flex align-items-center gap-2 sm:gap-3">
          <Button 
            :icon="themeStore.isDark ? 'pi pi-sun' : 'pi pi-moon'" 
            @click="themeStore.toggle" 
            class="p-button-text p-button-secondary p-button-sm" 
          />
          
          <div class="flex align-items-center gap-2 px-2 sm:px-3 py-2 border-round-xl bg-slate-50 border-1 border-200">
            <Avatar icon="pi pi-user" shape="circle" class="bg-primary text-white" size="small" />
            <span class="font-bold text-xs text-900 hidden sm:block">{{ authStore.user?.full_name }}</span>
          </div>
          
          <Button icon="pi pi-sign-out" @click="handleLogout" class="p-button-text p-button-danger p-button-sm" v-tooltip.bottom="'Sign Out'" />
        </div>
      </div>
    </header>

    <!-- Professional Mobile Sidebar -->
    <Sidebar v-model:visible="mobileMenuVisible" class="w-full sm:w-20rem">
      <template #header>
        <div class="flex align-items-center gap-2">
          <h1 class="text-xl font-bold tracking-tight text-900">Apartex</h1>
        </div>
      </template>
      
      <div class="flex flex-column h-full">
        <div class="flex-grow-1">
          <ul class="list-none p-0 m-0">
            <!-- Renter links -->
            <template v-if="authStore.user?.role === 'renter'">
              <li v-for="item in renterLinks" :key="item.to">
                <router-link :to="item.to" class="mobile-nav-link" @click="mobileMenuVisible = false">
                  <i :class="[item.icon, 'mr-3 text-xl']"></i>
                  <span>{{ item.label }}</span>
                </router-link>
              </li>
            </template>

            <!-- Owner links -->
            <template v-else-if="authStore.user?.role === 'owner'">
              <li v-for="item in ownerLinks" :key="item.to">
                <router-link :to="item.to" class="mobile-nav-link" @click="mobileMenuVisible = false">
                  <i :class="[item.icon, 'mr-3 text-xl']"></i>
                  <span>{{ item.label }}</span>
                </router-link>
              </li>
            </template>
          </ul>
        </div>

        <div class="mt-auto border-top-1 border-100 pt-4 pb-2">
          <div class="flex align-items-center gap-3 px-3 mb-4">
            <Avatar icon="pi pi-user" shape="circle" class="bg-primary text-white" />
            <div>
              <div class="font-bold text-900">{{ authStore.user?.full_name }}</div>
              <div class="text-xs text-500 uppercase font-bold tracking-wider">{{ authStore.user?.role }} Account</div>
            </div>
          </div>
          <Button label="Sign Out" icon="pi pi-sign-out" class="p-button-outlined p-button-danger w-full font-bold" @click="handleLogout" />
        </div>
      </div>
    </Sidebar>
    
    <main class="min-h-screen">
      <router-view />
    </main>

    <Toast position="bottom-right" />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import { useThemeStore } from './stores/theme';

// PrimeVue components
import Button from 'primevue/button';
import Avatar from 'primevue/avatar';
import Sidebar from 'primevue/sidebar';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';

const authStore = useAuthStore();
const themeStore = useThemeStore();
const router = useRouter();

const mobileMenuVisible = ref(false);

const renterLinks = [
  { label: 'Home', to: '/', icon: 'pi pi-home' },
  { label: 'Explore', to: '/apartments', icon: 'pi pi-search' },
  { label: 'My Bookings', to: '/bookings', icon: 'pi pi-calendar' },
  { label: 'Loyalty Rewards', to: '/loyalty', icon: 'pi pi-star' },
];

const ownerLinks = [
  { label: 'Overview', to: '/owner', icon: 'pi pi-home' },
  { label: 'Analytics', to: '/dashboard', icon: 'pi pi-chart-bar' },
  { label: 'My Properties', to: '/owner/apartments', icon: 'pi pi-building' },
  { label: 'Reservations', to: '/owner/bookings', icon: 'pi pi-book' },
  { label: 'Payouts', to: '/owner/payouts', icon: 'pi pi-wallet' },
];

const goHome = () => {
  if (authStore.user?.role === 'owner') router.push('/owner');
  else router.push('/');
};

const handleLogout = async () => {
  mobileMenuVisible.value = false;
  await authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.nav-link {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--surface-500);
  transition: 0.2s;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
}

.nav-link:hover, .nav-link.router-link-active {
  color: var(--surface-900);
  background-color: var(--surface-100);
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  padding: 1rem;
  color: var(--surface-600);
  font-weight: 600;
  border-radius: 12px;
  transition: 0.2s;
  margin-bottom: 0.5rem;
}

.mobile-nav-link:hover, .mobile-nav-link.router-link-active {
  background-color: var(--surface-100);
  color: var(--surface-900);
}

.mobile-nav-link.router-link-active i {
  color: var(--primary-color);
}
</style>