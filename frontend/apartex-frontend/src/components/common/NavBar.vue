<!-- src/components/common/NavBar.vue -->
<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="nav-logo">
        🏠 Apartex
      </router-link>
      
      <div class="nav-menu">
        <router-link to="/apartments" class="nav-link">Apartments</router-link>
        
        <template v-if="isAuthenticated">
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
          <router-link to="/bookings" class="nav-link">My Bookings</router-link>
          <router-link to="/loyalty" class="nav-link">Loyalty</router-link>
          <button @click="logout" class="nav-link logout-btn">Logout</button>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/register" class="nav-link register-btn">Sign Up</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'NavBar',
  setup() {
    const authStore = useAuthStore()
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    const logout = () => {
      authStore.logout()
      window.location.href = '/'
    }
    
    return {
      isAuthenticated,
      logout
    }
  }
}
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 1rem 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
}

.nav-logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: #4a5568;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #667eea;
}

.register-btn {
  background: #667eea;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-family: inherit;
}
</style>