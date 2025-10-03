<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="logo">
          🏠 Apartex
        </router-link>
        <div class="nav-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/apartments" class="nav-link">Apartments</router-link>
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/register" class="nav-link signup">Sign Up</router-link>
        </div>
      </div>
    </nav>

    <router-view />

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>🏠 Apartex</h3>
          <p>Your trusted platform for apartment bookings and management.</p>
        </div>
        <div class="footer-section">
          <h4>Quick Links</h4>
          <router-link to="/apartments">Browse Apartments</router-link>
          <router-link to="/login">Login</router-link>
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
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
.navbar {
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: #4a5568;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
  padding: 0.5rem 0;
}

.nav-link:hover {
  color: #667eea;
}

.signup {
  background: #667eea;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.signup:hover {
  background: #5a6fd8;
  color: white;
}

.footer {
  background: #2d3748;
  color: white;
  padding: 3rem 0 1rem;
  margin-top: 4rem;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  padding: 0 1rem;
}

.footer-section h3 {
  margin-bottom: 1rem;
  color: #667eea;
  font-size: 1.5rem;
}

.footer-section h4 {
  margin-bottom: 1rem;
  color: #cbd5e0;
  font-size: 1.1rem;
}

.footer-section a {
  display: block;
  color: #a0aec0;
  text-decoration: none;
  margin-bottom: 0.5rem;
  transition: color 0.3s;
}

.footer-section a:hover {
  color: #667eea;
}

.footer-section p {
  color: #a0aec0;
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.footer-bottom {
  border-top: 1px solid #4a5568;
  margin-top: 2rem;
  padding: 1.5rem 1rem 0;
  text-align: center;
  color: #a0aec0;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-links {
    gap: 1rem;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    text-align: center;
  }
  
  .nav-container {
    flex-direction: column;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .footer {
    padding: 2rem 0 1rem;
  }
}

.router-link-active {
  color: #667eea !important;
}

.router-link-exact-active {
  color: #667eea !important;
}
</style>