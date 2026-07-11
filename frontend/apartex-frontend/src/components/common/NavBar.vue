<template>
  <nav class="navbar" :class="{ 'is-scrolled': isScrolled }">
    <div class="nav-container">
      <!-- Left: Logo -->
      <router-link to="/" class="logo">APARTEX</router-link>
      
      <!-- Center: Desktop Links -->
      <div class="nav-links desktop-only">
        <router-link to="/" class="nav-link" exact-active-class="active">Home</router-link>
        <router-link to="/apartments" class="nav-link" active-class="active">Explore Stays</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/bookings" class="nav-link" active-class="active">My Bookings</router-link>
        <router-link v-if="authStore.isAuthenticated" to="/loyalty" class="nav-link" active-class="active">Loyalty</router-link>
      </div>

      <!-- Right: Desktop Actions -->
      <div class="nav-actions desktop-only">
        <button class="theme-btn" @click="toggleTheme">
          <i :class="theme.isDark ? 'pi pi-sun' : 'pi pi-moon'"></i>
        </button>

        <template v-if="authStore.isAuthenticated">
          <div class="user-dropdown-container" ref="dropdownRef">
            <button class="avatar-btn" @click="isDropdownOpen = !isDropdownOpen">
              {{ userInitials }}
            </button>
            
            <div v-show="isDropdownOpen" class="dropdown-menu">
              <router-link to="/profile" class="dropdown-item">Profile</router-link>
              <router-link to="/bookings" class="dropdown-item">My Bookings</router-link>
              <router-link v-if="authStore.user?.role === 'owner'" to="/dashboard" class="dropdown-item">Dashboard</router-link>
              <div class="dropdown-divider"></div>
              <button @click="logout" class="dropdown-item logout-btn text-error">Logout</button>
            </div>
          </div>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link-login">Login</router-link>
          <router-link to="/register" class="btn-signup">Sign Up</router-link>
        </template>
      </div>

      <!-- Mobile: Hamburger -->
      <button class="mobile-toggle" @click="isMobileMenuOpen = !isMobileMenuOpen">
        <i :class="isMobileMenuOpen ? 'pi pi-times' : 'pi pi-bars'"></i>
      </button>
    </div>

    <!-- Mobile Menu -->
    <div v-show="isMobileMenuOpen" class="mobile-menu">
      <router-link to="/" class="mobile-link" exact-active-class="active" @click="isMobileMenuOpen = false">Home</router-link>
      <router-link to="/apartments" class="mobile-link" active-class="active" @click="isMobileMenuOpen = false">Explore Stays</router-link>
      
      <template v-if="authStore.isAuthenticated">
        <router-link to="/bookings" class="mobile-link" active-class="active" @click="isMobileMenuOpen = false">My Bookings</router-link>
        <router-link to="/loyalty" class="mobile-link" active-class="active" @click="isMobileMenuOpen = false">Loyalty</router-link>
        <router-link to="/profile" class="mobile-link" active-class="active" @click="isMobileMenuOpen = false">Profile</router-link>
        <router-link v-if="authStore.user?.role === 'owner'" to="/dashboard" class="mobile-link" active-class="active" @click="isMobileMenuOpen = false">Dashboard</router-link>
        <button @click="toggleTheme" class="mobile-link text-left">Toggle Theme</button>
        <button @click="logoutAndClose" class="mobile-link text-left text-error">Logout</button>
      </template>
      <template v-else>
        <button @click="toggleTheme" class="mobile-link text-left">Toggle Theme</button>
        <router-link to="/login" class="mobile-link" @click="isMobileMenuOpen = false">Login</router-link>
        <router-link to="/register" class="mobile-link text-accent font-bold" @click="isMobileMenuOpen = false">Sign Up</router-link>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useThemeStore } from '@/stores/theme';

const authStore = useAuthStore();
const theme = useThemeStore();

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

const toggleTheme = () => theme.toggle();

const logout = () => {
  authStore.logout();
  window.location.href = '/';
};

const logoutAndClose = () => {
  isMobileMenuOpen.value = false;
  logout();
};
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--color-border);
  transition: box-shadow var(--transition-base);
}

.navbar.is-scrolled {
  box-shadow: var(--shadow-sm);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--space-6);
  height: 4.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-navy);
  text-decoration: none;
  letter-spacing: -0.02em;
}

.nav-links {
  display: flex;
  gap: var(--space-8);
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: var(--font-size-sm);
  padding: var(--space-2) 0;
  border-bottom: 2px solid transparent;
  transition: color var(--transition-fast), border-color var(--transition-fast);
}

.nav-link:hover {
  color: var(--color-text-primary);
}

.nav-link.active {
  color: var(--color-accent);
  border-bottom-color: var(--color-accent);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--space-6);
}

.theme-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  font-size: 1.125rem;
  cursor: pointer;
  padding: var(--space-2);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.theme-btn:hover {
  background: var(--color-surface-alt);
  color: var(--color-text-primary);
}

.user-dropdown-container {
  position: relative;
}

.avatar-btn {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--radius-full);
  background: var(--color-navy);
  color: white;
  border: none;
  font-weight: 700;
  font-size: var(--font-size-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--transition-fast);
}

.avatar-btn:hover {
  transform: scale(1.05);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + var(--space-2));
  right: 0;
  width: 200px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  padding: var(--space-2) 0;
  display: flex;
  flex-direction: column;
}

.dropdown-item {
  text-decoration: none;
  color: var(--color-text-primary);
  padding: var(--space-3) var(--space-4);
  font-size: var(--font-size-sm);
  font-weight: 500;
  transition: background var(--transition-fast);
  background: transparent;
  border: none;
  text-align: left;
  cursor: pointer;
  width: 100%;
}

.dropdown-item:hover {
  background: var(--color-surface-alt);
}

.dropdown-divider {
  height: 1px;
  background: var(--color-border);
  margin: var(--space-2) 0;
}

.text-error {
  color: var(--color-error);
}

.nav-link-login {
  text-decoration: none;
  color: var(--color-text-primary);
  font-weight: 600;
  font-size: var(--font-size-sm);
}

.btn-signup {
  text-decoration: none;
  background: var(--color-accent);
  color: white;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  font-weight: 600;
  font-size: var(--font-size-sm);
  transition: background var(--transition-fast);
}

.btn-signup:hover {
  background: var(--color-accent-hover);
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: var(--color-text-primary);
  font-size: 1.5rem;
  cursor: pointer;
  padding: var(--space-2);
}

.mobile-menu {
  display: none;
  flex-direction: column;
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: var(--space-4) var(--space-6);
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  box-shadow: var(--shadow-md);
}

.mobile-link {
  text-decoration: none;
  color: var(--color-text-primary);
  font-weight: 500;
  font-size: var(--font-size-base);
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--color-border);
  background: transparent;
  border-top: none;
  border-left: none;
  border-right: none;
  cursor: pointer;
}

.mobile-link:last-child {
  border-bottom: none;
}

.text-left {
  text-align: left;
}

.text-accent {
  color: var(--color-accent);
}

@media (max-width: 768px) {
  .desktop-only {
    display: none;
  }
  .mobile-toggle {
    display: flex;
  }
  .mobile-menu {
    display: flex;
  }
}
</style>