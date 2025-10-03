<!-- src/components/common/AppFooter.vue -->
<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>🏠 Apartex</h3>
        <p>Your trusted platform for apartment bookings and management.</p>
      </div>
      <div class="footer-section">
        <h4>Quick Links</h4>
        <router-link to="/apartments">Browse Apartments</router-link>
        <router-link to="/dashboard" v-if="isAuthenticated">Dashboard</router-link>
        <router-link to="/login" v-else>Login</router-link>
      </div>
      <div class="footer-section">
        <h4>Contact</h4>
        <p>Email: support@apartex.com</p>
        <p>Phone: +1 (555) 123-4567</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2024 Apartex. All rights reserved.</p>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'AppFooter',
  setup() {
    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    return {
      isAuthenticated
    }
  }
}
</script>

<style scoped>
.footer {
  background: #2d3748;
  color: white;
  padding: 2rem 0 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 0 2rem;
}

.footer-section h3,
.footer-section h4 {
  margin-bottom: 1rem;
  color: #667eea;
}

.footer-section a {
  display: block;
  color: #cbd5e0;
  text-decoration: none;
  margin-bottom: 0.5rem;
}

.footer-section a:hover {
  color: #667eea;
}

.footer-section p {
  color: #a0aec0;
  line-height: 1.6;
}

.footer-bottom {
  border-top: 1px solid #4a5568;
  margin-top: 2rem;
  padding: 1rem 2rem;
  text-align: center;
  color: #a0aec0;
}
</style>