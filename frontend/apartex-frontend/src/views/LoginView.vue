<!-- src/views/LoginView.vue -->
<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <router-link to="/" class="logo">🏠 Apartex</router-link>
          <h1>Welcome Back</h1>
          <p>Sign in to your account</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email">Email Address</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              placeholder="Enter your email"
              required
              class="form-input"
            >
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              placeholder="Enter your password"
              required
              class="form-input"
            >
          </div>

          <div class="form-options">
            <label class="remember-me">
              <input type="checkbox" v-model="form.rememberMe">
              Remember me
            </label>
            <a href="#" class="forgot-password">Forgot password?</a>
          </div>

          <button type="submit" class="login-btn" :disabled="loading">
            {{ loading ? 'Signing In...' : 'Sign In' }}
          </button>

          <div class="divider">
            <span>Or continue with</span>
          </div>

          <div class="social-login">
            <button type="button" class="social-btn google-btn">
              <span class="social-icon">🔍</span>
              Google
            </button>
            <button type="button" class="social-btn facebook-btn">
              <span class="social-icon">📘</span>
              Facebook
            </button>
          </div>
        </form>

        <div class="login-footer">
          <p>Don't have an account? <router-link to="/register" class="signup-link">Sign up</router-link></p>
        </div>
      </div>

      <div class="login-hero">
        <div class="hero-content">
          <h2>Find Your Perfect Stay</h2>
          <p>Join thousands of travelers who trust Apartex for their accommodation needs.</p>
          <div class="features">
            <div class="feature">
              <span class="feature-icon">⭐</span>
              <span>Verified Properties</span>
            </div>
            <div class="feature">
              <span class="feature-icon">🔒</span>
              <span>Secure Booking</span>
            </div>
            <div class="feature">
              <span class="feature-icon">🎁</span>
              <span>Loyalty Rewards</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      loading: false,
      form: {
        email: '',
        password: '',
        rememberMe: false
      }
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // For demo purposes, just redirect to dashboard
        // In real app, you would validate credentials and get token
        this.$router.push('/dashboard')
      } catch (error) {
        console.error('Login failed:', error)
        alert('Login failed. Please check your credentials.')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.login-card {
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  text-decoration: none;
  margin-bottom: 1rem;
  display: inline-block;
}

.login-header h1 {
  color: #2d3748;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.login-header p {
  color: #718096;
}

.login-form {
  space-y: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #4a5568;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid #cbd5e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a5568;
  font-size: 0.9rem;
}

.forgot-password {
  color: #667eea;
  text-decoration: none;
  font-size: 0.9rem;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-btn {
  width: 100%;
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 1.5rem;
}

.login-btn:hover:not(:disabled) {
  background: #5a6fd8;
}

.login-btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

.divider {
  text-align: center;
  position: relative;
  margin: 2rem 0;
  color: #718096;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e2e8f0;
}

.divider span {
  background: white;
  padding: 0 1rem;
  position: relative;
}

.social-login {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.social-btn:hover {
  border-color: #cbd5e0;
  background: #f7fafc;
}

.social-icon {
  font-size: 1.1rem;
}

.login-footer {
  text-align: center;
  margin-top: auto;
}

.login-footer p {
  color: #718096;
}

.signup-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.signup-link:hover {
  text-decoration: underline;
}

.login-hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-content h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
}

.feature-icon {
  font-size: 1.25rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-container {
    grid-template-columns: 1fr;
  }
  
  .login-hero {
    display: none;
  }
  
  .login-card {
    padding: 2rem;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
  }
  
  .social-login {
    grid-template-columns: 1fr;
  }
  
  .form-options {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>