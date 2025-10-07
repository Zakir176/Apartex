<!-- src/components/common/NavBar.vue -->
<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">🏠 Apartex</router-link>
      
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/apartments" class="nav-link">Apartments</router-link>
        
        <template v-if="authStore.isAuthenticated">
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/bookings" class="nav-link">My Bookings</router-link>
          <router-link to="/loyalty" class="nav-link">Loyalty</router-link>
          <div class="user-menu">
            <button class="nav-link" @click="toggleTheme">{{ theme.isDark ? 'Light' : 'Dark' }} Mode</button>
            <span class="user-name">Hi, {{ authStore.user?.full_name || authStore.user?.email }}</span>
            <button @click="logout" class="nav-link logout-btn">Logout</button>
          </div>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/register" class="nav-link signup">Sign Up</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

export default {
  name: 'NavBar',
  setup() {
    const authStore = useAuthStore()
    const theme = useThemeStore()
    
    const logout = () => {
      authStore.logout()
      window.location.href = '/'
    }

    const toggleTheme = () => theme.toggle()
    
    return {
      authStore,
      logout,
      theme,
      toggleTheme
    }
  }
}
</script>

<style scoped>
.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name { color: var(--muted); font-weight: 500; }

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
}
</style>