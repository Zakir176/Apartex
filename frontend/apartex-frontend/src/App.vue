<template>
  <div id="app" class="min-h-screen bg-[#F8F7F4]" :class="{ 'dark': themeStore.isDark }">

    <!-- Owner layout: side nav + content -->
    <template v-if="isOwnerPage && authStore.isAuthenticated">
      <OwnerSideNav
        :isOpen="sideNavOpen"
        @close="sideNavOpen = false"
      />

      <!-- Owner content area — offset by sidebar width on desktop -->
      <div class="lg:pl-64 min-h-screen flex flex-col">
        <!-- Owner top bar (mobile hamburger + page title) -->
        <header class="sticky top-0 z-30 bg-white border-b border-surface-border px-4 sm:px-6 h-14 flex items-center justify-between lg:hidden">
          <button
            @click="sideNavOpen = true"
            class="w-9 h-9 flex items-center justify-center rounded-lg text-slate-600 hover:bg-slate-100 transition-colors border-0 bg-transparent cursor-pointer"
          >
            <i class="pi pi-bars text-lg"></i>
          </button>
          <span class="font-black text-navy text-base tracking-tight">APARTEX</span>
          <div class="w-9"></div>
        </header>

        <!-- Page content -->
        <main class="flex-1 p-4 sm:p-6">
          <router-view v-slot="{ Component, route: r }">
            <Transition name="page" mode="out-in">
              <component :is="Component" :key="r.path" />
            </Transition>
          </router-view>
        </main>
      </div>
    </template>

    <!-- Guest layout: top navbar + content -->
    <template v-else>
      <div 
        v-if="!isAuthPage"
        class="sticky top-0 z-[100] px-2 sm:px-6 transition-all duration-300 pointer-events-none"
        :class="isScrolled ? 'pt-2 pb-2 sm:pt-3 sm:pb-3' : 'pt-3 pb-3 sm:pt-5 sm:pb-4'"
      >
        <nav 
          class="pointer-events-auto max-w-[1240px] mx-auto bg-white/75 backdrop-blur-xl border border-white/60 shadow-lg rounded-full px-3.5 sm:px-5 h-14 sm:h-16 flex items-center justify-between transition-all duration-300 relative hover:shadow-xl hover:bg-white/85"
          :class="isScrolled ? 'shadow-xl bg-white/90 border-slate-200/80' : ''"
        >
          <!-- Left: Logo -->
          <div class="flex-shrink-0 flex items-center gap-2 text-base sm:text-xl font-black text-navy tracking-tight pl-0.5 sm:pl-1 cursor-pointer hover:opacity-85 transition-all group" @click="goHome">
            <img src="/logo.svg" alt="Apartex Logo" class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl shadow-md group-hover:scale-105 transition-transform duration-300" />
            <span class="tracking-wider text-slate-900 font-black text-sm sm:text-lg">APARTEX</span>
          </div>

          <!-- Center: Quick Nav Links (Desktop) -->
          <div class="hidden xl:flex items-center gap-1 absolute left-1/2 -translate-x-1/2 bg-slate-100/70 backdrop-blur-md p-1 rounded-full border border-slate-200/60 shadow-inner">
            <template v-if="authStore.isAuthenticated">
              <template v-if="authStore.user?.role === 'renter'">
                <router-link
                  v-for="item in renterLinks" :key="item.to"
                  :to="item.to"
                  exact-active-class="bg-white shadow-sm text-slate-900 font-extrabold"
                  class="px-4 py-2 rounded-full text-xs font-bold text-slate-600 hover:text-slate-900 transition-all duration-200 no-underline flex items-center gap-1.5"
                >
                  <i :class="[item.icon, 'text-xs text-accent']"></i>
                  <span>{{ item.label }}</span>
                </router-link>
              </template>
              <template v-else-if="authStore.user?.role === 'owner'">
                <router-link
                  v-for="item in ownerLinks" :key="item.to"
                  :to="item.to"
                  exact-active-class="bg-white shadow-sm text-slate-900 font-extrabold"
                  class="px-4 py-2 rounded-full text-xs font-bold text-slate-600 hover:text-slate-900 transition-all duration-200 no-underline flex items-center gap-1.5"
                >
                  <i :class="[item.icon, 'text-xs text-accent']"></i>
                  <span>{{ item.label }}</span>
                </router-link>
              </template>
            </template>

            <template v-else-if="isLandingPage">
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
            </template>

            <template v-else>
              <router-link
                v-for="item in guestLinks" :key="item.to"
                :to="item.to"
                exact-active-class="bg-white shadow-sm text-slate-900 font-extrabold"
                class="px-4 py-2 rounded-full text-xs font-bold text-slate-600 hover:text-slate-900 transition-all duration-200 no-underline flex items-center gap-1.5"
              >
                <i :class="[item.icon, 'text-xs text-accent']"></i>
                <span>{{ item.label }}</span>
              </router-link>
            </template>
          </div>

          <!-- Right: Direct CTAs & User Actions -->
          <div class="hidden xl:flex items-center gap-2.5">
            <template v-if="authStore.isAuthenticated">
              <router-link
                v-if="authStore.user?.role === 'renter'"
                to="/loyalty"
                class="flex items-center gap-2 px-4 py-2 rounded-full text-xs font-bold text-accent bg-accent-light hover:bg-orange-100 transition-colors no-underline border border-orange-200 mr-1"
              >
                <i class="pi pi-star-fill text-xs"></i> Club
              </router-link>

              <!-- Authenticated Dropdown -->
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

                <!-- Dropdown Menu -->
                <div
                  v-show="isDropdownOpen"
                  class="absolute right-0 top-[calc(100%+12px)] w-56 bg-white border border-surface-border rounded-2xl shadow-2xl py-2 flex flex-col z-50 origin-top-right overflow-hidden"
                >
                  <div class="px-4 py-3 border-b border-surface-border mb-1 bg-slate-50">
                    <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-0.5">{{ authStore.user?.role }} Account</p>
                    <p class="text-sm font-black text-slate-800 truncate">{{ authStore.user?.full_name || authStore.user?.email }}</p>
                  </div>
                  <router-link v-if="authStore.user?.role === 'owner'" to="/dashboard" @click="isDropdownOpen = false" class="px-5 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-chart-line text-slate-400"></i> Analytics</router-link>
                  <router-link v-if="authStore.user?.role === 'owner'" to="/owner/apartments" @click="isDropdownOpen = false" class="px-5 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-home text-slate-400"></i> My Properties</router-link>
                  <router-link v-if="authStore.user?.role === 'renter'" to="/profile" @click="isDropdownOpen = false" class="px-5 py-2.5 text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-slate-900 no-underline transition-colors flex items-center gap-3"><i class="pi pi-user text-slate-400"></i> Profile</router-link>
                  
                  <div class="h-px bg-surface-border my-1"></div>
                  <button @click="handleLogout" class="px-5 py-2.5 text-xs font-bold text-red-600 hover:bg-red-50 text-left transition-colors flex items-center gap-3 w-full cursor-pointer"><i class="pi pi-sign-out"></i> Sign Out</button>
                </div>
              </div>
            </template>

            <template v-else>
              <!-- Sign In Direct CTA -->
              <router-link
                to="/login"
                class="px-4 py-2 text-xs font-bold text-slate-700 hover:text-slate-900 hover:bg-slate-100/70 rounded-full transition-all no-underline"
              >
                Sign In
              </router-link>

              <!-- List Your Property Direct CTA -->
              <router-link
                to="/register?role=owner"
                class="btn-accent text-xs font-black px-5 py-2.5 shadow-accent hover:scale-105 transition-all duration-200 no-underline flex items-center gap-2 rounded-full"
              >
                <i class="pi pi-building text-xs"></i>
                <span>List Your Property</span>
              </router-link>
            </template>
          </div>

          <!-- Mobile Hamburger Button -->
          <button
            class="xl:hidden w-10 h-10 flex items-center justify-center text-slate-700 rounded-full hover:bg-slate-100 transition-colors duration-150 border border-slate-200/80 cursor-pointer"
            @click="mobileMenuVisible = !mobileMenuVisible"
            aria-label="Toggle Navigation Menu"
          >
            <i :class="mobileMenuVisible ? 'pi pi-times' : 'pi pi-bars'" class="text-lg"></i>
          </button>
        </nav>

        <!-- Mobile Floating Menu Drawer -->
        <div 
          v-show="mobileMenuVisible" 
          class="pointer-events-auto xl:hidden absolute top-[calc(100%+8px)] left-4 right-4 bg-white/95 backdrop-blur-2xl border border-surface-border rounded-3xl shadow-2xl overflow-hidden flex flex-col z-50 origin-top p-3 transition-all duration-300"
        >
          <div class="flex flex-col gap-1">
            <template v-if="authStore.isAuthenticated">
              <template v-if="authStore.user?.role === 'renter'">
                <router-link 
                  v-for="item in renterLinks" :key="item.to" 
                  :to="item.to" 
                  @click="mobileMenuVisible = false" 
                  class="px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"
                >
                  <i :class="[item.icon, 'text-slate-400']"></i> {{ item.label }}
                </router-link>
              </template>
              <template v-else-if="authStore.user?.role === 'owner'">
                <router-link 
                  v-for="item in ownerLinks" :key="item.to" 
                  :to="item.to" 
                  @click="mobileMenuVisible = false" 
                  class="px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"
                >
                  <i :class="[item.icon, 'text-slate-400']"></i> {{ item.label }}
                </router-link>
              </template>
              
              <div class="h-px bg-surface-border mx-2 my-1"></div>
              <button @click="handleLogout" class="px-4 py-3 rounded-2xl text-xs font-bold text-red-600 hover:bg-red-50 text-left transition-colors flex items-center gap-3 w-full cursor-pointer"><i class="pi pi-sign-out"></i> Sign Out</button>
            </template>

            <template v-else-if="isLandingPage">
              <!-- Mobile Quick Nav Links -->
              <router-link 
                to="/apartments" 
                @click="mobileMenuVisible = false" 
                class="px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"
              >
                <i class="pi pi-search text-accent"></i> Browse Stays
              </router-link>

              <button 
                @click="scrollToAnchor('why-apartex')" 
                class="w-full text-left px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3 bg-transparent border-0 cursor-pointer"
              >
                <i class="pi pi-shield text-blue-500"></i> Why Apartex
              </button>

              <button 
                @click="scrollToAnchor('owner-pricing')" 
                class="w-full text-left px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3 bg-transparent border-0 cursor-pointer"
              >
                <i class="pi pi-tag text-amber-500"></i> Host Pricing
              </button>

              <button 
                @click="scrollToAnchor('host-calculator')" 
                class="w-full text-left px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3 bg-transparent border-0 cursor-pointer"
              >
                <i class="pi pi-calculator text-emerald-500"></i> Host Calculator
              </button>

              <button 
                @click="scrollToAnchor('faq')" 
                class="w-full text-left px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3 bg-transparent border-0 cursor-pointer"
              >
                <i class="pi pi-question-circle text-purple-500"></i> FAQ
              </button>

              <div class="h-px bg-surface-border mx-2 my-1"></div>
              <!-- Mobile Direct CTAs -->
              <div class="grid grid-cols-2 gap-2 p-1">
                <router-link to="/login" @click="mobileMenuVisible = false" class="btn-outline text-center no-underline py-2.5 text-xs">Sign In</router-link>
                <router-link to="/register?role=owner" @click="mobileMenuVisible = false" class="btn-accent text-center no-underline py-2.5 text-xs font-black">List Property</router-link>
              </div>
            </template>

            <template v-else>
              <router-link 
                v-for="item in guestLinks" :key="item.to" 
                :to="item.to" 
                @click="mobileMenuVisible = false" 
                class="px-4 py-3 rounded-2xl text-xs font-bold text-slate-700 hover:bg-slate-50 hover:text-accent no-underline transition-colors flex items-center gap-3"
              >
                <i :class="[item.icon, 'text-slate-400']"></i> {{ item.label }}
              </router-link>

              <div class="h-px bg-surface-border mx-2 my-1"></div>
              <div class="grid grid-cols-2 gap-2 p-1">
                <router-link to="/login" @click="mobileMenuVisible = false" class="btn-outline text-center no-underline py-2.5 text-xs">Sign In</router-link>
                <router-link to="/register?role=owner" @click="mobileMenuVisible = false" class="btn-accent text-center no-underline py-2.5 text-xs font-black">List Property</router-link>
              </div>
            </template>
          </div>
        </div>
      </div>

      <main class="min-h-screen">
        <router-view v-slot="{ Component, route: r }">
          <Transition name="page" mode="out-in">
            <component :is="Component" :key="r.path" />
          </Transition>
        </router-view>
      </main>
    </template>

    <!-- Floating Offline Status Banner -->
    <div 
      v-if="isOffline" 
      class="fixed bottom-4 left-1/2 -translate-x-1/2 z-[200] bg-slate-900/95 text-white backdrop-blur-xl px-5 py-2.5 rounded-full shadow-2xl border border-slate-700 text-xs font-bold flex items-center gap-3 animate-bounce"
    >
      <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping"></span>
      <span>Offline Mode — Browsing Cached Apartex Content</span>
      <button @click="isOffline = false" class="text-slate-400 hover:text-white bg-transparent border-0 cursor-pointer ml-1">✕</button>
    </div>

    <!-- Global components -->
    <Toast position="bottom-right" />
    <ConfirmDialog />
    <Analytics />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { Analytics } from '@vercel/analytics/vue';
import { useAuthStore } from './stores/auth';
import { useRouter, useRoute } from 'vue-router';
import { useThemeStore } from './stores/theme';
import OwnerSideNav from '@/components/OwnerSideNav.vue';

// PrimeVue components
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';

const authStore = useAuthStore();

const appReady = ref(false);

onMounted(async () => {
  if (authStore.token && !authStore.user) {
    try {
      await authStore.fetchCurrentUser();
    } catch {
      // Token is stale — clear it so the user is treated as unauthenticated
      authStore.token = null;
      localStorage.removeItem('accessToken');
    }
  }
  appReady.value = true;
});
const themeStore = useThemeStore();
const router = useRouter();
const route = useRoute();

const isAuthPage = computed(() => ['/login', '/register'].includes(route.path));
const isLandingPage = computed(() => (route.path === '/' || route.path === '') && !authStore.isAuthenticated);

const isOwnerPage = computed(() => {
  if (authStore.user?.role === 'owner' && route.path === '/profile') return true;
  const ownerPaths = ['/owner', '/dashboard'];
  return ownerPaths.some(p => route.path === p || route.path.startsWith(p + '/'));
});

const sideNavOpen = ref(false);
const isScrolled = ref(false);
const isDropdownOpen = ref(false);
const mobileMenuVisible = ref(false);
const dropdownRef = ref(null);
const activeSection = ref('');
const isOffline = ref(!navigator.onLine);

const updateOnlineStatus = () => {
  isOffline.value = !navigator.onLine;
};

const renterLinks = [
  { label: 'Home', to: '/home', icon: 'pi pi-home' },
  { label: 'Explore', to: '/apartments', icon: 'pi pi-search' },
  { label: 'Bookings', to: '/bookings', icon: 'pi pi-calendar' },
  { label: 'Loyalty', to: '/loyalty', icon: 'pi pi-star' },
];

const guestLinks = [
  { label: 'Home', to: '/', icon: 'pi pi-home' },
  { label: 'Browse Stays', to: '/apartments', icon: 'pi pi-search' },
  { label: 'Loyalty Club', to: '/loyalty', icon: 'pi pi-star' },
  { label: 'List Property', to: '/register?role=owner', icon: 'pi pi-building' }
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

const scrollToAnchor = async (anchorId) => {
  mobileMenuVisible.value = false;
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
    const yOffset = -90; // account for floating sticky glass header height
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
  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  if (route.query.scrollTo) {
    setTimeout(() => {
      performSmoothScroll(route.query.scrollTo);
    }, 150);
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('click', closeDropdown);
  window.removeEventListener('online', updateOnlineStatus);
  window.removeEventListener('offline', updateOnlineStatus);
});

watch(() => route.query.scrollTo, (newAnchor) => {
  if (newAnchor && route.path === '/') {
    setTimeout(() => {
      performSmoothScroll(newAnchor);
    }, 150);
  }
});

const goHome = () => {
  if (authStore.user?.role === 'owner') router.push('/owner');
  else if (authStore.user?.role === 'renter') router.push('/home');
  else router.push('/');
};

const handleLogout = async () => {
  mobileMenuVisible.value = false;
  isDropdownOpen.value = false;
  await authStore.logout();
  router.push('/login');
};
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
