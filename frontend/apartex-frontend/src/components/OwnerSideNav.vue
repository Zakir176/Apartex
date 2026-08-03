<template>
  <!-- Mobile overlay -->
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-slate-900/50 z-40 lg:hidden backdrop-blur-sm"
    @click="$emit('close')"
  ></div>

  <!-- Sidebar -->
  <aside
    class="fixed top-0 left-0 h-full w-64 bg-navy z-50 flex flex-col transition-transform duration-300 ease-in-out"
    :class="isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'"
  >
    <!-- Logo -->
    <div class="flex items-center justify-between px-6 py-5 border-b border-white/10">
      <router-link to="/" class="flex items-center gap-2 no-underline group">
        <div class="w-8 h-8 rounded-lg bg-accent flex items-center justify-center shrink-0">
          <i class="pi pi-building text-white text-sm"></i>
        </div>
        <span class="text-white font-black text-lg tracking-tight">APARTEX</span>
      </router-link>
      <button
        @click="$emit('close')"
        class="lg:hidden w-8 h-8 flex items-center justify-center text-white/50 hover:text-white rounded-lg hover:bg-white/10 transition-colors border-0 bg-transparent cursor-pointer"
      >
        <i class="pi pi-times text-sm"></i>
      </button>
    </div>

    <!-- Owner badge -->
    <div class="px-4 py-3 mx-3 mt-4 rounded-xl bg-white/5 border border-white/10">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-full bg-accent flex items-center justify-center text-white font-black text-sm shrink-0">
          {{ userInitials }}
        </div>
        <div class="min-w-0">
          <p class="text-white font-bold text-xs truncate mb-0">{{ authStore.user?.full_name || 'Property Host' }}</p>
          <p class="text-white/40 text-xs font-medium truncate mb-0">{{ authStore.user?.email }}</p>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-3 py-4 overflow-y-auto flex flex-col gap-1">

      <p class="text-white/30 text-[10px] font-black uppercase tracking-widest px-3 mb-2">Overview</p>

      <router-link
        v-for="item in mainNavItems"
        :key="item.to"
        :to="item.to"
        @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150 no-underline group"
        :class="isActive(item.to)
          ? 'bg-accent text-white shadow-accent'
          : 'text-white/60 hover:text-white hover:bg-white/10'"
      >
        <i :class="item.icon" class="text-base w-5 text-center shrink-0"></i>
        <span>{{ item.label }}</span>
        <span
          v-if="item.badge"
          class="ml-auto text-[10px] font-black px-2 py-0.5 rounded-full"
          :class="isActive(item.to) ? 'bg-white/20 text-white' : 'bg-accent/20 text-accent'"
        >{{ item.badge }}</span>
      </router-link>

      <div class="h-px bg-white/10 my-3 mx-1"></div>
      <p class="text-white/30 text-[10px] font-black uppercase tracking-widest px-3 mb-2">Management</p>

      <router-link
        v-for="item in managementNavItems"
        :key="item.to"
        :to="item.to"
        @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150 no-underline group"
        :class="isActive(item.to)
          ? 'bg-accent text-white shadow-accent'
          : 'text-white/60 hover:text-white hover:bg-white/10'"
      >
        <i :class="item.icon" class="text-base w-5 text-center shrink-0"></i>
        <span>{{ item.label }}</span>
      </router-link>

    </nav>

    <!-- Bottom actions -->
    <div class="px-3 py-4 border-t border-white/10 flex flex-col gap-1">
      <router-link
        to="/apartments"
        @click="$emit('close')"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold text-white/60 hover:text-white hover:bg-white/10 transition-all no-underline"
      >
        <i class="pi pi-arrow-left text-base w-5 text-center"></i>
        <span>Guest View</span>
      </router-link>
      <button
        @click="handleLogout"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold text-red-400 hover:text-red-300 hover:bg-red-500/10 transition-all w-full border-0 bg-transparent cursor-pointer text-left"
      >
        <i class="pi pi-sign-out text-base w-5 text-center"></i>
        <span>Sign Out</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

defineProps({
  isOpen: { type: Boolean, default: false },
});
defineEmits(['close']);

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const userInitials = computed(() => {
  const name = authStore.user?.full_name || 'H';
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
});

const mainNavItems = [
  { to: '/owner', label: 'Dashboard', icon: 'pi pi-th-large' },
  { to: '/dashboard', label: 'Analytics', icon: 'pi pi-chart-line' },
];

const managementNavItems = [
  { to: '/owner/apartments', label: 'My Properties', icon: 'pi pi-building' },
  { to: '/owner/bookings', label: 'Bookings', icon: 'pi pi-calendar' },
  { to: '/owner/payouts', label: 'Payouts', icon: 'pi pi-wallet' },
  { to: '/profile', label: 'Account', icon: 'pi pi-user' },
];

function isActive(path) {
  return route.path === path || route.path.startsWith(path + '/');
}

async function handleLogout() {
  await authStore.logout();
  router.push('/login');
}
</script>
