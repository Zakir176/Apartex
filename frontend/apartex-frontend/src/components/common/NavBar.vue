<template>
  <div 
    class="sticky top-0 z-50 px-4 sm:px-6 transition-all duration-300"
    :class="isScrolled ? 'pt-3 pb-3 bg-white/50 backdrop-blur-md' : 'pt-6 pb-4'"
  >
    <!-- Main Floating Pill -->
    <nav 
      class="max-w-[1100px] mx-auto bg-white border border-surface-border rounded-full px-5 h-16 flex items-center justify-between transition-all duration-300 relative"
      :class="isScrolled ? 'shadow-lg bg-white/95' : 'shadow-md hover:shadow-lg'"
    >
      <!-- Left: Logo -->
      <router-link to="/" class="flex-shrink-0 flex items-center gap-2 text-xl font-black text-navy tracking-tight no-underline pl-2 hover:opacity-80 transition-opacity">
        <div class="w-8 h-8 rounded-lg bg-accent text-white flex items-center justify-center text-sm">
          <i class="pi pi-home"></i>
        </div>
        APARTEX
      </router-link>

      <!-- Center: Nav Links (Desktop) -->
      <div class="hidden md:flex items-center gap-1 absolute left-1/2 -translate-x-1/2 bg-surface-alt/50 p-1 rounded-full border border-surface-border">
        <router-link
          to="/"
          exact-active-class="bg-white shadow-sm text-slate-900 font-bold"
          class="px-5 py-2 rounded-full text-sm font-semibold text-slate-500 hover:text-slate-800 transition-all duration-200 no-underline"
        >Home</router-link>
        <router-link
          to="/apartments"
          active-class="bg-white shadow-sm text-slate-900 font-bold"
          class="px-5 py-2 rounded-full text-sm font-semibold text-slate-500 hover:text-slate-800 transition-all duration-200 no-underline"
        >Explore</router-link>
        <router-link
          v-if="authStore.isAuthenticated"
          to="/bookings"
          active-class="bg-white shadow-sm text-slate-900 font-bold"
          class="px-5 py-2 rounded-full text-sm font-semibold text-slate-500 hover:text-slate-800 transition-all duration-200 no-underline"
        >Bookings</router-link>
      </div>

      <!-- Right: User Actions -->
      <div class="hidden md:flex items-center gap-3">
        <router-link
          v-if="authStore.isAuthenticated"
          to="/loyalty"
          class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-bold text-accent bg-accent-light hover:bg-orange-100 transition-colors no-underline border border-orange-200 mr-2"
        >
          <i class="pi pi-star-fill text-xs"></i> Club
        </router-link>

        <!-- Authenticated Dropdown -->
        <template v-if="authStore.isAuthenticated">
          <div class="relative" ref="dropdownRef">
            <button
              @click="isDropdownOpen = !isDropdownOpen"
              class="flex items-center gap-2 pl-2 pr-1.5 py-1.5 border border-surface-border rounded-full hover:shadow-md transition-all duration-200 bg-white"
            >
              <i class="pi pi-bars text-slate-500 text-sm ml-1"></i>
              <div class="w-8 h-8 rounded-full bg-navy text-white font-bold text-xs flex items-center justify-center shadow-sm">
                {{ userInitials }}
              </div>
            </button>

            <!-- Dropdown Menu -->
            <div
              v-show="isDropdownOpen"
              class="absolute right-0 top-[calc(100%+12px)] w-56 bg-white border border-surface-border rounded-2xl shadow-xl py-2 flex flex-col z-50 origin-top-right overflow-hidden"
            >
              <div class="px-4 py-3 border-b border-surface-border mb-1 bg-slate-50">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Signed in as</p>
                <p class="text-sm font-bold text-slate-800 truncate">{{ authStore.user?.full_name || authStore.user?.email }}</p>
              </div>
              <router-link to="/profile" class="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-user text-slate-400"></i> Profile</router-link>
              <router-link to="/bookings" class="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-calendar text-slate-400"></i> My Bookings</router-link>
              <router-link v-if="authStore.user?.role === 'owner'" to="/dashboard" class="px-5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-chart-line text-slate-400"></i> Host Dashboard</router-link>
              <div class="h-px bg-surface-border my-1"></div>
              <button @click="logout" class="px-5 py-2.5 text-sm font-semibold text-red-600 hover:bg-red-50 text-left transition-colors flex items-center gap-3 w-full"><i class="pi pi-sign-out"></i> Sign Out</button>
            </div>
          </div>
        </template>

        <!-- Unauthenticated -->
        <template v-else>
          <router-link to="/login" class="px-4 py-2 text-sm font-bold text-slate-600 hover:text-slate-900 no-underline transition-colors">Log In</router-link>
          <router-link to="/register" class="px-5 py-2.5 text-sm font-bold bg-navy text-white rounded-full hover:bg-slate-800 transition-colors shadow-sm no-underline">Sign Up</router-link>
        </template>
      </div>

      <!-- Mobile Hamburger -->
      <button
        class="md:hidden w-10 h-10 flex items-center justify-center text-slate-700 rounded-full hover:bg-surface-alt transition-colors duration-150 border border-transparent hover:border-surface-border"
        @click="isMobileMenuOpen = !isMobileMenuOpen"
      >
        <i :class="isMobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-xl"></i>
      </button>
    </nav>

    <!-- Mobile Menu Floating Card -->
    <div 
      v-show="isMobileMenuOpen" 
      class="md:hidden absolute top-[calc(100%+8px)] left-4 right-4 bg-white border border-surface-border rounded-2xl shadow-xl overflow-hidden flex flex-col z-50 origin-top"
    >
      <div class="p-2 flex flex-col gap-1">
        <router-link to="/" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-home text-slate-400"></i> Home</router-link>
        <router-link to="/apartments" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-search text-slate-400"></i> Explore Stays</router-link>
        
        <template v-if="authStore.isAuthenticated">
          <div class="h-px bg-surface-border mx-2 my-1"></div>
          <router-link to="/loyalty" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-xl text-sm font-bold text-accent bg-accent-light/50 hover:bg-accent-light no-underline transition-colors flex items-center gap-3"><i class="pi pi-star-fill"></i> Apartex Club</router-link>
          <router-link to="/bookings" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-calendar text-slate-400"></i> My Bookings</router-link>
          <router-link to="/profile" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-user text-slate-400"></i> Profile</router-link>
          <router-link v-if="authStore.user?.role === 'owner'" to="/dashboard" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-chart-line text-slate-400"></i> Host Dashboard</router-link>
          <div class="h-px bg-surface-border mx-2 my-1"></div>
          <button @click="logoutAndClose" class="px-4 py-3 rounded-xl text-sm font-bold text-red-600 hover:bg-red-50 text-left transition-colors flex items-center gap-3 w-full"><i class="pi pi-sign-out"></i> Sign Out</button>
        </template>
        
        <template v-else>
          <div class="h-px bg-surface-border mx-2 my-1"></div>
          <router-link to="/login" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-xl text-sm font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-sign-in text-slate-400"></i> Log In</router-link>
          <router-link to="/register" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-xl text-sm font-bold text-accent hover:bg-accent-light no-underline transition-colors flex items-center gap-3"><i class="pi pi-user-plus text-accent/70"></i> Sign Up</router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const isScrolled = ref(false);
const isDropdownOpen = ref(false);
const isMobileMenuOpen = ref(false);
const dropdownRef = ref(null);

const userInitials = computed(() => {
  const name = authStore.user?.full_name || authStore.user?.email || 'U';
  return name.charAt(0).toUpperCase();
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

const logout = () => {
  authStore.logout();
  window.location.href = '/';
};

const logoutAndClose = () => {
  isMobileMenuOpen.value = false;
  logout();
};
</script>