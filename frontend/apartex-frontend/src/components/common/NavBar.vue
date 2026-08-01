<template>
  <div 
    class="sticky top-0 z-[100] px-3 sm:px-6 transition-all duration-300 pointer-events-none"
    :class="isScrolled ? 'pt-3 pb-3' : 'pt-4 pb-3'"
  >
    <!-- Main Floating Pill -->
    <nav 
      class="pointer-events-auto max-w-[1280px] mx-auto bg-white/80 backdrop-blur-xl border border-white/70 shadow-lg rounded-full px-4 sm:px-6 h-16 flex items-center justify-between transition-all duration-300 relative hover:shadow-xl hover:bg-white/90"
      :class="isScrolled ? 'shadow-xl bg-white/95 border-slate-200/90' : ''"
    >
      <!-- Left: Logo -->
      <router-link to="/" class="flex-shrink-0 flex items-center gap-2 text-xl font-black text-navy tracking-tight pl-1 hover:opacity-90 transition-all group no-underline">
        <img src="/logo.svg" alt="Apartex Logo" class="w-9 h-9 rounded-xl shadow-md group-hover:scale-105 transition-transform duration-300" />
        <span class="tracking-wider text-slate-900 font-black text-lg">APARTEX</span>
      </router-link>

      <!-- Center: Quick Nav Links (Desktop) -->
      <div class="hidden lg:flex items-center gap-1 absolute left-1/2 -translate-x-1/2 bg-slate-100/80 backdrop-blur-md p-1 rounded-full border border-slate-200/60 shadow-inner">
        <!-- Explore Stays -->
        <router-link
          to="/apartments"
          active-class="bg-white shadow-sm text-slate-900 font-extrabold"
          class="px-4 py-1.5 rounded-full text-xs font-bold text-slate-600 hover:text-slate-900 transition-all duration-200 no-underline flex items-center gap-1.5"
        >
          <i class="pi pi-search text-xs text-accent"></i>
          <span>Explore Stays</span>
        </router-link>

        <!-- How it works -->
        <button
          @click="scrollToAnchor('why-apartex')"
          :class="activeSection === 'why-apartex' ? 'bg-white shadow-sm text-slate-900 font-extrabold' : 'text-slate-600 hover:text-slate-900'"
          class="px-4 py-1.5 rounded-full text-xs font-bold transition-all duration-200 border-0 bg-transparent cursor-pointer flex items-center gap-1.5"
        >
          <i class="pi pi-info-circle text-xs text-blue-400"></i>
          <span>How it works</span>
        </button>
      </div>

      <!-- Right: Currency Selector & User Actions -->
      <div class="flex items-center gap-2 sm:gap-3">
        <!-- Currency Selector Dropdown (Desktop & Tablet) -->
        <div class="relative" ref="currencyDropdownRef">
          <button
            @click="isCurrencyOpen = !isCurrencyOpen"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-slate-200 bg-slate-50/80 hover:bg-white hover:border-slate-300 text-xs font-extrabold text-slate-700 transition-all cursor-pointer shadow-xs"
            title="Switch Currency"
          >
            <span class="text-sm leading-none">{{ currencyStore.activeCurrencyObj.flag }}</span>
            <span>{{ currencyStore.activeCurrencyObj.code }}</span>
            <i class="pi pi-chevron-down text-[10px] text-slate-400"></i>
          </button>

          <div
            v-show="isCurrencyOpen"
            class="absolute right-0 top-[calc(100%+8px)] w-48 bg-white border border-slate-200 rounded-2xl shadow-2xl py-2 flex flex-col z-50 origin-top-right overflow-hidden"
          >
            <div class="px-3 py-1.5 border-b border-slate-100 mb-1 bg-slate-50/50">
              <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Select Currency</span>
            </div>
            <button
              v-for="curr in currencyStore.currencies"
              :key="curr.code"
              @click="selectCurrency(curr.code)"
              :class="curr.code === currencyStore.currentCurrency ? 'bg-orange-50/80 font-black text-accent' : 'text-slate-700 font-bold hover:bg-slate-50'"
              class="w-full px-4 py-2 text-xs text-left transition-colors flex items-center justify-between border-0 bg-transparent cursor-pointer"
            >
              <span class="flex items-center gap-2">
                <span class="text-sm">{{ curr.flag }}</span>
                <span>{{ curr.code }} ({{ curr.symbol }})</span>
              </span>
              <i v-if="curr.code === currencyStore.currentCurrency" class="pi pi-check text-accent text-xs"></i>
            </button>
          </div>
        </div>

        <!-- Auth CTAs -->
        <div class="hidden sm:flex items-center gap-2">
          <template v-if="authStore.isAuthenticated">
            <!-- Owner dashboard shortcut — only shown to owners -->
            <router-link
              v-if="authStore.user?.role === 'owner'"
              to="/dashboard"
              class="hidden xl:flex items-center gap-1.5 px-4 py-2 rounded-full text-xs font-black text-white bg-navy hover:bg-navy-700 transition-colors no-underline"
            >
              <i class="pi pi-th-large text-xs"></i>
              <span>Dashboard</span>
            </router-link>

            <router-link
              to="/loyalty"
              class="hidden xl:flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-extrabold text-accent bg-accent-light hover:bg-orange-100 transition-colors no-underline border border-orange-200"
            >
              <i class="pi pi-star-fill text-xs"></i> Club
            </router-link>

            <div class="relative" ref="dropdownRef">
              <button
                @click="isDropdownOpen = !isDropdownOpen"
                class="flex items-center gap-2 pl-2.5 pr-2 py-1 border border-slate-200 rounded-full hover:shadow-md transition-all duration-200 bg-white cursor-pointer"
              >
                <i class="pi pi-bars text-slate-500 text-sm"></i>
                <div class="w-8 h-8 rounded-full bg-navy text-white font-black text-xs flex items-center justify-center shadow-sm uppercase">
                  {{ userInitials }}
                </div>
              </button>

              <div
                v-show="isDropdownOpen"
                class="absolute right-0 top-[calc(100%+12px)] w-56 bg-white border border-slate-200 rounded-2xl shadow-2xl py-2 flex flex-col z-50 origin-top-right overflow-hidden"
              >
                <div class="px-4 py-3 border-b border-slate-100 mb-1 bg-slate-50">
                  <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-0.5">Signed in as</p>
                  <p class="text-xs font-black text-slate-800 truncate">{{ authStore.user?.full_name || authStore.user?.email }}</p>
                </div>
                <router-link to="/profile" class="px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-user text-slate-400"></i> Profile</router-link>
                <router-link to="/bookings" class="px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-calendar text-slate-400"></i> My Bookings</router-link>
                <router-link to="/wishlist" class="px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-heart text-slate-400"></i> Wishlist</router-link>
                <router-link v-if="authStore.user?.role === 'owner'" to="/dashboard" class="px-4 py-2 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-chart-line text-slate-400"></i> Host Dashboard</router-link>
                <div class="h-px bg-slate-100 my-1"></div>
                <button @click="logout" class="px-4 py-2 text-xs font-bold text-red-600 hover:bg-red-50 text-left transition-colors flex items-center gap-3 w-full border-0 bg-transparent cursor-pointer"><i class="pi pi-sign-out"></i> Sign Out</button>
              </div>
            </div>
          </template>

          <template v-else>
            <router-link
              to="/login"
              class="px-3.5 py-2 text-xs font-bold text-slate-700 hover:text-slate-900 hover:bg-slate-100/80 rounded-full transition-all no-underline"
            >
              Sign In
            </router-link>
            <router-link
              to="/register"
              class="px-4 py-2 text-xs font-black text-white bg-slate-900 hover:bg-slate-800 rounded-full transition-all no-underline flex items-center gap-1.5"
            >
              Sign Up
            </router-link>
            <router-link
              to="/host"
              class="btn-accent text-xs font-black px-4 py-2 no-underline flex items-center gap-1.5 rounded-full"
            >
              <i class="pi pi-building text-xs"></i>
              <span>List Property</span>
            </router-link>
          </template>
        </div>

        <!-- Mobile Hamburger Button -->
        <button
          class="lg:hidden w-9 h-9 flex items-center justify-center text-slate-700 rounded-full hover:bg-slate-100 transition-colors duration-150 border border-slate-200 cursor-pointer"
          @click="isMobileMenuOpen = !isMobileMenuOpen"
          aria-label="Toggle Navigation Menu"
        >
          <i :class="isMobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'" class="text-base"></i>
        </button>
      </div>
    </nav>

    <!-- Mobile Floating Drawer -->
    <div 
      v-show="isMobileMenuOpen" 
      class="pointer-events-auto lg:hidden absolute top-[calc(100%+8px)] left-4 right-4 bg-white/95 backdrop-blur-2xl border border-slate-200 rounded-3xl shadow-2xl overflow-hidden flex flex-col z-50 origin-top p-3 transition-all duration-300"
    >
      <!-- Mobile Currency Switcher Strip -->
      <div class="px-3 py-2 bg-slate-50 rounded-2xl mb-2 flex items-center justify-between border border-slate-100">
        <span class="text-xs font-bold text-slate-500">Currency</span>
        <div class="flex items-center gap-1">
          <button
            v-for="curr in currencyStore.currencies"
            :key="curr.code"
            @click="selectCurrency(curr.code)"
            :class="curr.code === currencyStore.currentCurrency ? 'bg-navy text-white font-black shadow-xs' : 'text-slate-600 bg-white border border-slate-200'"
            class="px-2 py-1 rounded-full text-[10px] cursor-pointer transition-all border-0"
          >
            {{ curr.flag }} {{ curr.code }}
          </button>
        </div>
      </div>

      <!-- Mobile Drawer Content -->
      <div class="flex flex-col gap-1 p-1">
        <router-link
          to="/apartments"
          @click="isMobileMenuOpen = false"
          class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-slate-700 hover:bg-slate-50 no-underline transition-colors"
        >
          <i class="pi pi-search text-accent"></i> Explore Stays
        </router-link>

        <template v-if="authStore.isAuthenticated">
          <router-link
            v-if="authStore.user?.role === 'owner'"
            to="/dashboard"
            @click="isMobileMenuOpen = false"
            class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-white bg-navy no-underline transition-colors"
          >
            <i class="pi pi-th-large"></i> Host Dashboard
          </router-link>
          <router-link to="/bookings" @click="isMobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-slate-700 hover:bg-slate-50 no-underline transition-colors"><i class="pi pi-calendar text-slate-400"></i> My Bookings</router-link>
          <router-link to="/loyalty" @click="isMobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-slate-700 hover:bg-slate-50 no-underline transition-colors"><i class="pi pi-star text-accent"></i> Loyalty Club</router-link>
          <router-link to="/wishlist" @click="isMobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-slate-700 hover:bg-slate-50 no-underline transition-colors"><i class="pi pi-heart text-slate-400"></i> Wishlist</router-link>
          <router-link to="/profile" @click="isMobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-slate-700 hover:bg-slate-50 no-underline transition-colors"><i class="pi pi-user text-slate-400"></i> Profile</router-link>
          <div class="h-px bg-slate-100 my-1 mx-4"></div>
          <button @click="logout" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-red-500 hover:bg-red-50 w-full border-0 bg-transparent cursor-pointer transition-colors text-left"><i class="pi pi-sign-out"></i> Sign Out</button>
        </template>

        <template v-else>
          <div class="h-px bg-slate-100 my-1 mx-4"></div>
          <router-link to="/login" @click="isMobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-slate-700 hover:bg-slate-50 no-underline transition-colors"><i class="pi pi-sign-in text-slate-400"></i> Sign In</router-link>
          <router-link to="/register" @click="isMobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-white bg-slate-900 no-underline transition-colors"><i class="pi pi-user-plus"></i> Create Account</router-link>
          <router-link to="/host" @click="isMobileMenuOpen = false" class="flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold text-white bg-accent no-underline transition-colors"><i class="pi pi-building"></i> List Your Property</router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useCurrencyStore } from '@/stores/currency';
import { useRouter, useRoute } from 'vue-router';

const authStore = useAuthStore();
const currencyStore = useCurrencyStore();
const router = useRouter();
const route = useRoute();

const isScrolled = ref(false);
const isDropdownOpen = ref(false);
const isCurrencyOpen = ref(false);
const isMobileMenuOpen = ref(false);
const dropdownRef = ref(null);
const currencyDropdownRef = ref(null);
const activeSection = ref('');

const userInitials = computed(() => {
  const name = authStore.user?.full_name || authStore.user?.email || 'U';
  return name.charAt(0).toUpperCase();
});

const selectCurrency = (code) => {
  currencyStore.setCurrency(code);
  isCurrencyOpen.value = false;
};

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

const closeDropdowns = (e) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    isDropdownOpen.value = false;
  }
  if (currencyDropdownRef.value && !currencyDropdownRef.value.contains(e.target)) {
    isCurrencyOpen.value = false;
  }
};

onMounted(() => {
  currencyStore.autoDetectCurrency();
  window.addEventListener('scroll', handleScroll);
  window.addEventListener('click', closeDropdowns);
  if (route.query.scrollTo) {
    setTimeout(() => {
      performSmoothScroll(route.query.scrollTo);
    }, 150);
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('click', closeDropdowns);
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