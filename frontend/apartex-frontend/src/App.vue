<template>
  <div id="app" :class="{ 'dark': themeStore.isDark }">
    <!-- Floating Navbar -->
    <div 
      v-if="authStore.isAuthenticated"
      class="sticky top-0 z-[100] px-4 sm:px-6 transition-all duration-300"
      :class="isScrolled ? 'pt-3 pb-3 bg-white/50 backdrop-blur-md' : 'pt-6 pb-4'"
    >
      <nav 
        class="max-w-[1100px] mx-auto bg-white border border-surface-border rounded-full px-5 h-16 flex items-center justify-between transition-all duration-300 relative"
        :class="isScrolled ? 'shadow-lg bg-white/95' : 'shadow-md hover:shadow-lg'"
      >
        <!-- Left: Logo -->
        <div class="flex-shrink-0 flex items-center gap-2 text-xl font-black text-navy tracking-tight pl-2 cursor-pointer hover:opacity-80 transition-opacity" @click="goHome">
          <div class="w-8 h-8 rounded-lg bg-accent text-white flex items-center justify-center text-sm">
            <i class="pi pi-home"></i>
          </div>
          APARTEX
        </div>

        <!-- Center: Nav Links (Desktop) -->
        <div class="hidden lg:flex items-center gap-1 absolute left-1/2 -translate-x-1/2 bg-surface-alt/50 p-1 rounded-full border border-surface-border">
          <template v-if="authStore.user?.role === 'renter'">
            <router-link
              v-for="item in renterLinks" :key="item.to"
              :to="item.to"
              exact-active-class="bg-white shadow-sm text-slate-900 font-bold"
              class="px-5 py-2 rounded-full text-sm font-semibold text-slate-500 hover:text-slate-800 transition-all duration-200 no-underline"
            >{{ item.label }}</router-link>
          </template>
          <template v-else-if="authStore.user?.role === 'owner'">
            <router-link
              v-for="item in ownerLinks" :key="item.to"
              :to="item.to"
              exact-active-class="bg-white shadow-sm text-slate-900 font-bold"
              class="px-5 py-2 rounded-full text-sm font-semibold text-slate-500 hover:text-slate-800 transition-all duration-200 no-underline"
            >{{ item.label }}</router-link>
          </template>
        </div>

        <!-- Right: User Actions -->
        <div class="hidden lg:flex items-center gap-3">
          <router-link
            v-if="authStore.user?.role === 'renter'"
            to="/loyalty"
            class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-bold text-accent bg-accent-light hover:bg-orange-100 transition-colors no-underline border border-orange-200 mr-2"
          >
            <i class="pi pi-star-fill text-xs"></i> Club
          </router-link>

          <!-- Authenticated Dropdown -->
          <div class="relative" ref="dropdownRef">
            <button
              @click="isDropdownOpen = !isDropdownOpen"
              class="flex items-center gap-2 pl-2 pr-1.5 py-1.5 border border-surface-border rounded-full hover:shadow-md transition-all duration-200 bg-white"
            >
              <i class="pi pi-bars text-slate-500 text-sm ml-1"></i>
              <div class="w-8 h-8 rounded-full bg-navy text-white font-bold text-xs flex items-center justify-center shadow-sm uppercase">
                {{ userInitials }}
              </div>
            </button>

            <!-- Dropdown Menu -->
            <div
              v-show="isDropdownOpen"
              class="absolute right-0 top-[calc(100%+12px)] w-56 bg-white border border-surface-border rounded-2xl shadow-xl py-2 flex flex-col z-50 origin-top-right overflow-hidden"
            >
              <div class="px-4 py-3 border-b border-surface-border mb-1 bg-slate-50">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">{{ authStore.user?.role }} Account</p>
                <p class="text-sm font-bold text-slate-800 truncate">{{ authStore.user?.full_name || authStore.user?.email }}</p>
              </div>
              <router-link v-if="authStore.user?.role === 'owner'" to="/dashboard" @click="isDropdownOpen = false" class="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-chart-line text-slate-400"></i> Analytics</router-link>
              <router-link v-if="authStore.user?.role === 'owner'" to="/owner/apartments" @click="isDropdownOpen = false" class="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-home text-slate-400"></i> My Properties</router-link>
              <router-link v-if="authStore.user?.role === 'renter'" to="/profile" @click="isDropdownOpen = false" class="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-user text-slate-400"></i> Profile</router-link>
              
              <div class="h-px bg-surface-border my-1"></div>
              <button @click="handleLogout" class="px-5 py-2.5 text-sm font-semibold text-red-600 hover:bg-red-50 text-left transition-colors flex items-center gap-3 w-full"><i class="pi pi-sign-out"></i> Sign Out</button>
            </div>
          </div>
        </div>

        <!-- Mobile Hamburger -->
        <button
          class="lg:hidden w-10 h-10 flex items-center justify-center text-slate-700 rounded-full hover:bg-surface-alt transition-colors duration-150 border border-transparent hover:border-surface-border"
          @click="mobileMenuVisible = !mobileMenuVisible"
        >
          <i :class="mobileMenuVisible ? 'pi pi-times' : 'pi pi-bars'" class="text-xl"></i>
        </button>
      </nav>

      <!-- Mobile Menu Floating Card -->
      <div 
        v-show="mobileMenuVisible" 
        class="lg:hidden absolute top-[calc(100%+8px)] left-4 right-4 bg-white border border-surface-border rounded-2xl shadow-xl overflow-hidden flex flex-col z-50 origin-top"
      >
        <div class="p-2 flex flex-col gap-1">
          <template v-if="authStore.user?.role === 'renter'">
            <router-link 
              v-for="item in renterLinks" :key="item.to" 
              :to="item.to" 
              @click="mobileMenuVisible = false" 
              class="px-4 py-3 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"
            >
              <i :class="[item.icon, 'text-slate-400']"></i> {{ item.label }}
            </router-link>
          </template>

          <template v-else-if="authStore.user?.role === 'owner'">
            <router-link 
              v-for="item in ownerLinks" :key="item.to" 
              :to="item.to" 
              @click="mobileMenuVisible = false" 
              class="px-4 py-3 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"
            >
              <i :class="[item.icon, 'text-slate-400']"></i> {{ item.label }}
            </router-link>
          </template>
          
          <div class="h-px bg-surface-border mx-2 my-1"></div>
          <button @click="handleLogout" class="px-4 py-3 rounded-xl text-sm font-bold text-red-600 hover:bg-red-50 text-left transition-colors flex items-center gap-3 w-full"><i class="pi pi-sign-out"></i> Sign Out</button>
        </div>
      </div>
    </div>
    
    <main class="min-h-screen">
      <router-view />
    </main>

    <Toast position="bottom-right" />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import { useThemeStore } from './stores/theme';

// PrimeVue components
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';

const authStore = useAuthStore();
const themeStore = useThemeStore();
const router = useRouter();

const isScrolled = ref(false);
const isDropdownOpen = ref(false);
const mobileMenuVisible = ref(false);
const dropdownRef = ref(null);

const renterLinks = [
  { label: 'Home', to: '/', icon: 'pi pi-home' },
  { label: 'Explore', to: '/apartments', icon: 'pi pi-search' },
  { label: 'Bookings', to: '/bookings', icon: 'pi pi-calendar' },
  { label: 'Loyalty', to: '/loyalty', icon: 'pi pi-star' },
];

const ownerLinks = [
  { label: 'Overview', to: '/owner', icon: 'pi pi-home' },
  { label: 'Analytics', to: '/dashboard', icon: 'pi pi-chart-bar' },
  { label: 'Properties', to: '/owner/apartments', icon: 'pi pi-building' },
  { label: 'Reservations', to: '/owner/bookings', icon: 'pi pi-book' },
  { label: 'Payouts', to: '/owner/payouts', icon: 'pi pi-wallet' },
];

const userInitials = computed(() => {
  const name = authStore.user?.full_name || authStore.user?.email || 'U';
  return name.charAt(0);
});

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
};

const closeDropdown = (e) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    isDropdownOpen.value = false;
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  window.addEventListener('click', closeDropdown);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('click', closeDropdown);
});

const goHome = () => {
  if (authStore.user?.role === 'owner') router.push('/owner');
  else router.push('/');
};

const handleLogout = async () => {
  mobileMenuVisible.value = false;
  isDropdownOpen.value = false;
  await authStore.logout();
  router.push('/login');
};
</script>