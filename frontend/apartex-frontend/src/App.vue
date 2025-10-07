<template>
  <div id="app">
    <nav v-if="authStore.isAuthenticated" class="navbar">
      <div class="nav-brand">Apartex</div>
      <div class="nav-links">
        <!-- Renter nav -->
        <template v-if="authStore.user?.role === 'renter'">
          <router-link to="/">Home</router-link>
          <router-link to="/apartments">Apartments</router-link>
          <router-link to="/bookings">My Bookings</router-link>
          <router-link to="/loyalty">Loyalty</router-link>
        </template>
        <!-- Owner nav -->
        <template v-else-if="authStore.user?.role === 'owner'">
          <router-link to="/owner">Owner Home</router-link>
          <router-link to="/dashboard">Dashboard</router-link>
        </template>
        <span class="user-info">Hello, {{ authStore.user?.name }}</span>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth';
import { useRouter } from 'vue-router';
import { useThemeStore } from './stores/theme';

const authStore = useAuthStore();
const router = useRouter();
// Initialize theme store so it applies the saved theme on app load
useThemeStore();

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};
</script>

<style>
:root {
  --bg: #ffffff;
  --text: #111827;
  --muted: #6b7280;
  --border: #e5e7eb;
  --primary: #2563eb;
  --primary-contrast: #ffffff;
}

.dark {
  --bg: #0b1220;
  --text: #e5e7eb;
  --muted: #9ca3af;
  --border: #1f2937;
  --primary: #3b82f6;
  --primary-contrast: #0b1220;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  background: var(--bg);
  color: var(--text);
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: var(--bg);
  border-bottom: 1px solid var(--border);
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary);
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: var(--text);
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  background-color: var(--border);
  color: var(--primary);
}

.user-info {
  color: var(--muted);
  padding: 0.5rem 1rem;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background-color: #ef4444;
  color: var(--primary-contrast);
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.logout-btn:hover { opacity: 0.9; }
</style>