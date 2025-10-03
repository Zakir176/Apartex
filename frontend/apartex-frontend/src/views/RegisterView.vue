<!-- src/views/RegisterView.vue -->
<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <div class="register-header">
          <router-link to="/" class="logo">🏠 Apartex</router-link>
          <h1>Create Account</h1>
          <p>Join Apartex today</p>
        </div>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="name-fields">
            <div class="form-group">
              <label for="firstName">First Name</label>
              <input
                type="text"
                id="firstName"
                v-model="form.firstName"
                placeholder="First name"
                required
                class="form-input"
              >
            </div>
            <div class="form-group">
              <label for="lastName">Last Name</label>
              <input
                type="text"
                id="lastName"
                v-model="form.lastName"
                placeholder="Last name"
                required
                class="form-input"
              >
            </div>
          </div>

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
              placeholder="Create a password"
              required
              class="form-input"
              minlength="6"
            >
            <div class="password-strength" :class="passwordStrength">
              Password strength: {{ passwordStrengthText }}
            </div>
          </div>

          <div class="form-group">
            <label for="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="form.confirmPassword"
              placeholder="Confirm your password"
              required
              class="form-input"
              :class="{ 'error': form.confirmPassword && !passwordsMatch }"
            >
            <div v-if="form.confirmPassword && !passwordsMatch" class="error-message">
              Passwords do not match
            </div>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.acceptTerms" required>
              <span>I agree to the <a href="#" class="link">Terms of Service</a> and <a href="#" class="link">Privacy Policy</a></span>
            </label>
          </div>

          <button type="submit" class="register-btn" :disabled="loading || !formValid">
            {{ loading ? 'Creating Account...' : 'Create Account' }}
          </button>

          <div class="divider">
            <span>Or sign up with</span>
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

        <div class="register-footer">
          <p>Already have an account? <router-link to="/login" class="login-link">Sign in</router-link></p>
        </div>
      </div>

      <div class="register-hero">
        <div class="hero-content">
          <h2>Start Your Journey</h2>
          <p>Join our community and discover amazing places around the world.</p>
          <div class="benefits">
            <div class="benefit">
              <span class="benefit-icon">🏆</span>
              <div>
                <h4>Earn Rewards</h4>
                <p>Get loyalty points with every booking</p>
              </div>
            </div>
            <div class="benefit">
              <span class="benefit-icon">⚡</span>
              <div>
                <h4>Instant Booking</h4>
                <p>Book your stay in just a few clicks</p>
              </div>
            </div>
            <div class="benefit">
              <span class="benefit-icon">🌟</span>
              <div>
                <h4>Exclusive Deals</h4>
                <p>Access member-only discounts</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterView',
  data() {
    return {
      loading: false,
      form: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        acceptTerms: false
      }
    }
  },
  computed: {
    passwordsMatch() {
      return this.form.password === this.form.confirmPassword
    },
    passwordStrength() {
      if (!this.form.password) return 'weak'
      if (this.form.password.length < 6) return 'weak'
      if (this.form.password.length < 8) return 'medium'
      return 'strong'
    },
    passwordStrengthText() {
      const strengths = {
        weak: 'Weak',
        medium: 'Medium', 
        strong: 'Strong'
      }
      return strengths[this.passwordStrength]
    },
    formValid() {
      return (
        this.form.firstName &&
        this.form.lastName &&
        this.form.email &&
        this.form.password.length >= 6 &&
        this.passwordsMatch &&
        this.form.acceptTerms
      )
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // For demo purposes, just redirect to login
        // In real app, you would create the account
        alert('Account created successfully! Please sign in.')
        this.$router.push('/login')
      } catch (error) {
        console.error('Registration failed:', error)
        alert('Registration failed. Please try again.')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.register-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1000px;
  width: 100%;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.register-card {
  padding: 3rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.register-header {
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

.register-header h1 {
  color: #2d3748;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.register-header p {
  color: #718096;
}

.register-form {
  space-y: 1.5rem;
}

.name-fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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

.form-input.error {
  border-color: #e53e3e;
}

.password-strength {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  text-align: center;
}

.password-strength.weak {
  background: #fed7d7;
  color: #c53030;
}

.password-strength.medium {
  background: #fefcbf;
  color: #d69e2e;
}

.password-strength.strong {
  background: #c6f6d5;
  color: #276749;
}

.error-message {
  color: #e53e3e;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  color: #4a5568;
  font-size: 0.9rem;
  cursor: pointer;
}

.checkbox-label input {
  margin-top: 0.25rem;
}

.link {
  color: #667eea;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.register-btn {
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

.register-btn:hover:not(:disabled) {
  background: #5a6fd8;
}

.register-btn:disabled {
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

.register-footer {
  text-align: center;
  margin-top: auto;
}

.register-footer p {
  color: #718096;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.login-link:hover {
  text-decoration: underline;
}

.register-hero {
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

.benefits {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.benefit {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.benefit-icon {
  font-size: 1.5rem;
  margin-top: 0.25rem;
}

.benefit h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.benefit p {
  margin: 0;
  opacity: 0.8;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .register-container {
    grid-template-columns: 1fr;
  }
  
  .register-hero {
    display: none;
  }
  
  .register-card {
    padding: 2rem;
  }
  
  .name-fields {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .register-card {
    padding: 1.5rem;
  }
  
  .social-login {
    grid-template-columns: 1fr;
  }
}
</style>