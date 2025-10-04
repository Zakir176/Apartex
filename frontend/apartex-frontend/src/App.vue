<template>
  <div id="app">
    <nav v-if="authStore.isAuthenticated" class="navbar">
      <div class="nav-brand">Apartment Booking</div>
      <div class="nav-links">
        <router-link to="/">Home</router-link>
        <router-link to="/apartments">Apartments</router-link>
        <router-link to="/bookings">My Bookings</router-link>
        <router-link to="/loyalty">Loyalty</router-link>
        <router-link v-if="authStore.isOwner" to="/dashboard">Dashboard</router-link>
        <span class="user-info">Hello, {{ authStore.user?.name }}</span>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style>
/* Previous styles remain the same, just adding user-info */
.user-info {
  color: #495057;
  padding: 0.5rem 1rem;
}
</style>