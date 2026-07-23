<template>
  <div 
    class="sticky top-0 z-[100] px-4 sm:px-6 transition-all duration-300 pointer-events-none"
    :class="isScrolled ? 'pt-3 pb-3' : 'pt-5 pb-4'"
  >
    <!-- Main Floating Pill -->
    <nav 
      class="pointer-events-auto max-w-[1240px] mx-auto bg-white/75 backdrop-blur-xl border border-white/60 shadow-lg rounded-full px-5 h-16 flex items-center justify-between transition-all duration-300 relative hover:shadow-xl hover:bg-white/85"
      :class="isScrolled ? 'shadow-xl bg-white/90 border-slate-200/80' : ''"
    >
      <!-- Left: Logo -->
      <router-link to="/" class="flex-shrink-0 flex items-center gap-2.5 text-xl font-black text-navy tracking-tight pl-2 hover:opacity-85 transition-all group no-underline">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-accent via-orange-500 to-amber-400 text-white flex items-center justify-center text-base shadow-md group-hover:scale-105 transition-transform duration-300">
          <i class="pi pi-building"></i>
        </div>
        <span class="tracking-wider text-slate-900 font-black text-lg">APARTEX</span>
      </router-link>

      <!-- Center: Quick Nav Links (Desktop) -->
      <div class="hidden xl:flex items-center gap-1 absolute left-1/2 -translate-x-1/2 bg-slate-100/70 backdrop-blur-md p-1 rounded-full border border-slate-200/60 shadow-inner">
        <!-- Browse Stays -->
        <router-link
          to="/apartments"
          active-class="bg-white shadow-sm text-slate-900 font-extrabold"
          class="px-4 py-2 rounded-full text-xs font-bold text-slate-600 hover:text-slate-900 transition-all duration-200 no-underline flex items-center gap-1.5"
        >
          <i class="pi pi-search text-xs text-accent"></i>
          <span>Browse Stays</span>
        </router-link>

        <!-- Why Apartex Anchor -->
        <button
          @click="scrollToAnchor('why-apartex')"
          :class="activeSection === 'why-apartex' ? 'bg-white shadow-sm text-slate-900 font-extrabold' : 'text-slate-600 hover:text-slate-900'"
          class="px-4 py-2 rounded-full text-xs font-bold transition-all duration-200 no-underline border-0 bg-transparent cursor-pointer flex items-center gap-1.5"
        >
          <i class="pi pi-shield text-xs text-blue-500"></i>
          <span>Why Apartex</span>
        </button>

        <!-- Host Pricing Anchor -->
        <button
          @click="scrollToAnchor('owner-pricing')"
          :class="activeSection === 'owner-pricing' ? 'bg-white shadow-sm text-slate-900 font-extrabold' : 'text-slate-600 hover:text-slate-900'"
          class="px-4 py-2 rounded-full text-xs font-bold transition-all duration-200 no-underline border-0 bg-transparent cursor-pointer flex items-center gap-1.5"
        >
          <i class="pi pi-tag text-xs text-amber-500"></i>
          <span>Host Pricing</span>
        </button>

        <!-- Host Calculator Anchor -->
        <button
          @click="scrollToAnchor('host-calculator')"
          :class="activeSection === 'host-calculator' ? 'bg-white shadow-sm text-slate-900 font-extrabold' : 'text-slate-600 hover:text-slate-900'"
          class="px-4 py-2 rounded-full text-xs font-bold transition-all duration-200 no-underline border-0 bg-transparent cursor-pointer flex items-center gap-1.5"
        >
          <i class="pi pi-calculator text-xs text-emerald-500"></i>
          <span>Host Calculator</span>
        </button>

        <!-- FAQ Anchor -->
        <button
          @click="scrollToAnchor('faq')"
          :class="activeSection === 'faq' ? 'bg-white shadow-sm text-slate-900 font-extrabold' : 'text-slate-600 hover:text-slate-900'"
          class="px-4 py-2 rounded-full text-xs font-bold transition-all duration-200 no-underline border-0 bg-transparent cursor-pointer flex items-center gap-1.5"
        >
          <i class="pi pi-question-circle text-xs text-purple-500"></i>
          <span>FAQ</span>
        </button>
      </div>

      <!-- Right: Direct CTAs & User Actions -->
      <div class="hidden xl:flex items-center gap-2.5">
        <template v-if="authStore.isAuthenticated">
          <router-link
            to="/loyalty"
            class="flex items-center gap-2 px-4 py-2 rounded-full text-xs font-bold text-accent bg-accent-light hover:bg-orange-100 transition-colors no-underline border border-orange-200 mr-1"
          >
            <i class="pi pi-star-fill text-xs"></i> Club
          </router-link>

          <div class="relative" ref="dropdownRef">
            <button
              @click="isDropdownOpen = !isDropdownOpen"
              class="flex items-center gap-2 pl-2.5 pr-2 py-1.5 border border-surface-border rounded-full hover:shadow-md transition-all duration-200 bg-white cursor-pointer"
            >
              <i class="pi pi-bars text-slate-500 text-sm"></i>
              <div class="w-8 h-8 rounded-full bg-navy text-white font-black text-xs flex items-center justify-center shadow-sm uppercase">
                {{ userInitials }}
              </div>
            </button>

            <div
              v-show="isDropdownOpen"
              class="absolute right-0 top-[calc(100%+12px)] w-56 bg-white border border-surface-border rounded-2xl shadow-2xl py-2 flex flex-col z-50 origin-top-right overflow-hidden"
            >
              <div class="px-4 py-3 border-b border-surface-border mb-1 bg-slate-50">
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-0.5">Signed in as</p>
                <p class="text-sm font-black text-slate-800 truncate">{{ authStore.user?.full_name || authStore.user?.email }}</p>
              </div>
              <router-link to="/profile" class="px-5 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-user text-slate-400"></i> Profile</router-link>
              <router-link to="/bookings" class="px-5 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-calendar text-slate-400"></i> My Bookings</router-link>
              <router-link v-if="authStore.user?.role === 'owner'" to="/dashboard" class="px-5 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-chart-line text-slate-400"></i> Host Dashboard</router-link>
              <div class="h-px bg-surface-border my-1"></div>
              <button @click="logout" class="px-5 py-2.5 text-xs font-bold text-red-600 hover:bg-red-50 text-left transition-colors flex items-center gap-3 w-full cursor-pointer"><i class="pi pi-sign-out"></i> Sign Out</button>
            </div>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="px-4 py-2 text-xs font-bold text-slate-700 hover:text-slate-900 hover:bg-slate-100/70 rounded-full transition-all no-underline">Sign In</router-link>
          <router-link to="/register?role=owner" class="btn-accent text-xs font-black px-5 py-2.5 shadow-accent hover:scale-105 transition-all duration-200 no-underline flex items-center gap-2 rounded-full">
            <i class="pi pi-building text-xs"></i>
            <span>List Your Property</span>
          </router-link>
        </template>
      </div>

      <!-- Mobile Hamburger Button -->
      <button
        class="xl:hidden w-10 h-10 flex items-center justify-center text-slate-700 rounded-full hover:bg-slate-100 transition-colors duration-150 border border-slate-200/80 cursor-pointer"
        @click="isMobileMenuOpen = !isMobileMenuOpen"
        aria-label="Toggle Navigation Menu"
      >
        <i :class="isMobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-lg"></i>
      </button>
    </nav>

    <!-- Mobile Floating Drawer -->
    <div 
      v-show="isMobileMenuOpen" 
      class="pointer-events-auto xl:hidden absolute top-[calc(100%+8px)] left-4 right-4 bg-white/95 backdrop-blur-2xl border border-surface-border rounded-3xl shadow-2xl overflow-hidden flex flex-col z-50 origin-top p-3 transition-all duration-300"
    >
      <div class="flex flex-col gap-1">
        <router-link to="/apartments" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-search text-accent"></i> Browse Stays</router-link>
        <button @click="scrollToAnchor('why-apartex')" class="w-full text-left px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3 bg-transparent border-0 cursor-pointer"><i class="pi pi-shield text-blue-500"></i> Why Apartex</button>
        <button @click="scrollToAnchor('owner-pricing')" class="w-full text-left px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3 bg-transparent border-0 cursor-pointer"><i class="pi pi-tag text-amber-500"></i> Host Pricing</button>
        <button @click="scrollToAnchor('host-calculator')" class="w-full text-left px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3 bg-transparent border-0 cursor-pointer"><i class="pi pi-calculator text-emerald-500"></i> Host Calculator</button>
        <button @click="scrollToAnchor('faq')" class="w-full text-left px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3 bg-transparent border-0 cursor-pointer"><i class="pi pi-question-circle text-purple-500"></i> FAQ</button>
        
        <template v-if="authStore.isAuthenticated">
          <div class="h-px bg-surface-border mx-2 my-1"></div>
          <router-link to="/loyalty" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-2xl text-xs font-bold text-accent bg-accent-light/50 hover:bg-accent-light no-underline transition-colors flex items-center gap-3"><i class="pi pi-star-fill"></i> Apartex Club</router-link>
          <router-link to="/bookings" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-calendar text-slate-400"></i> My Bookings</router-link>
          <router-link to="/profile" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-user text-slate-400"></i> Profile</router-link>
          <router-link v-if="authStore.user?.role === 'owner'" to="/dashboard" @click="isMobileMenuOpen = false" class="px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"><i class="pi pi-chart-line text-slate-400"></i> Host Dashboard</router-link>
          <div class="h-px bg-surface-border mx-2 my-1"></div>
          <button @click="logoutAndClose" class="px-4 py-3 rounded-2xl text-xs font-bold text-red-600 hover:bg-red-50 text-left transition-colors flex items-center gap-3 w-full cursor-pointer"><i class="pi pi-sign-out"></i> Sign Out</button>
        </template>
        
        <template v-else>
          <div class="h-px bg-surface-border mx-2 my-1"></div>
          <div class="grid grid-cols-2 gap-2 p-1">
            <router-link to="/login" @click="isMobileMenuOpen = false" class="btn-outline text-center no-underline py-2.5 text-xs">Sign In</router-link>
            <router-link to="/register?role=owner" @click="isMobileMenuOpen = false" class="btn-accent text-center no-underline py-2.5 text-xs font-black">List Property</router-link>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter, useRoute } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const isScrolled = ref(false);
const isDropdownOpen = ref(false);
const isMobileMenuOpen = ref(false);
const dropdownRef = ref(null);
const activeSection = ref('');

const userInitials = computed(() => {
  const name = authStore.user?.full_name || authStore.user?.email || 'U';
  return name.charAt(0).toUpperCase();
});

const scrollToAnchor = async (anchorId) => {
  isMobileMenuOpen.value = false;
  activeSection.value = anchorId;
  if (route.path !== '/') {
    await router.push({ path: '/', query: { scrollTo: anchorId } });
  } else {
    performSmoothScroll(anchorId);
  }
};

const performSmoothScroll = (anchorId) => {
  const el = document.getElementById(anchorId);
  if (el) {
    const yOffset = -90;
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({ top: y, behavior: 'smooth' });
  }
};

const updateActiveSectionOnScroll = () => {
  if (route.path !== '/') return;
  const sections = ['why-apartex', 'owner-pricing', 'host-calculator', 'faq'];
  const scrollPosition = window.scrollY + 120;

  for (const sectionId of sections) {
    const el = document.getElementById(sectionId);
    if (el) {
      const top = el.offsetTop;
      const height = el.offsetHeight;
      if (scrollPosition >= top && scrollPosition < top + height) {
        activeSection.value = sectionId;
        break;
      }
    }
  }
};

const handleScroll = () => {
  isScrolled.value = window.scrollY > 20;
  updateActiveSectionOnScroll();
};

const closeDropdown = (e) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    isDropdownOpen.value = false;
  }
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  window.addEventListener('click', closeDropdown);
  if (route.query.scrollTo) {
    setTimeout(() => {
      performSmoothScroll(route.query.scrollTo);
    }, 150);
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('click', closeDropdown);
});

watch(() => route.query.scrollTo, (newAnchor) => {
  if (newAnchor && route.path === '/') {
    setTimeout(() => {
      performSmoothScroll(newAnchor);
    }, 150);
  }
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