<template>
  <div class="home">
    <!-- 🌆 HERO SECTION -->
    <section class="hero-section">
      <!-- Animated background -->
      <div class="hero-background"></div>
      <div class="hero-gradient"></div>

      <div class="hero-content">
        <h1 class="hero-title">
          Find Your Perfect Stay
        </h1>
        <p class="hero-subtitle">
          Discover amazing apartments for your next trip
        </p>

        <!-- Search bar -->
        <div class="search-bar">
          <input
            type="text"
            placeholder="Search destination..."
            class="search-input"
          />
          <button class="search-button">
            Search
          </button>
        </div>
      </div>

      <!-- Floating decoration elements -->
      <div class="floating-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
      </div>
    </section>

    <!-- 🏢 FEATURED APARTMENTS -->
    <section class="featured-section">
      <h2 class="section-title">
        Featured Apartments
      </h2>

      <div v-if="apartmentsStore.loading" class="loading-container">
        <div class="spinner"></div>
        <p class="loading-text">Finding perfect stays for you...</p>
      </div>

      <div v-else class="apartments-grid">
        <ApartmentCard
          v-for="apartment in apartmentsStore.featuredApartments"
          :key="apartment.id"
          :apartment="apartment"
        />
      </div>

      <div
        v-if="!apartmentsStore.loading && apartmentsStore.featuredApartments.length === 0"
        class="empty-state"
      >
        <div class="empty-icon">🏠</div>
        <p>No featured apartments available right now.</p>
        <p class="empty-subtitle">Check back soon for new listings!</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useApartmentsStore } from '@/stores/apartments'
import ApartmentCard from '@/components/ApartmentCard.vue'

const apartmentsStore = useApartmentsStore()

onMounted(async () => {
  if (apartmentsStore.apartments.length === 0) {
    await apartmentsStore.fetchApartments()
  }
})
</script>

<style scoped>
.home {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 🌆 HERO SECTION */
.hero-section {
  position: relative;
  width: 100%;
  height: 70vh;
  min-height: 500px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
}

.hero-background {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(251, 147, 251, 0.3), transparent 50%),
    radial-gradient(circle at 40% 20%, rgba(102, 126, 234, 0.3), transparent 50%);
  animation: pulseBackground 15s ease-in-out infinite;
}

@keyframes pulseBackground {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}

.hero-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.2) 100%);
}

.hero-content {
  position: relative;
  z-index: 10;
  max-width: 800px;
  padding: 0 2rem;
  animation: fadeInUp 1s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  color: white;
  margin: 0 0 1rem 0;
  line-height: 1.2;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.95);
  margin: 0 0 2.5rem 0;
  font-weight: 400;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.search-bar {
  display: flex;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border-radius: 50px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.search-bar:hover {
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
  transform: translateY(-2px);
}

.search-input {
  flex: 1;
  padding: 1rem 1.5rem;
  background: transparent;
  border: none;
  color: white;
  font-size: 1rem;
  outline: none;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.search-button {
  padding: 1rem 2rem;
  background: white;
  color: #667eea;
  border: none;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.search-button:hover {
  background: #f8f9ff;
  transform: scale(1.05);
}

.search-button:active {
  transform: scale(0.98);
}

/* Floating decorative shapes */
.floating-shapes {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}

.shape {
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: float 20s infinite ease-in-out;
}

.shape-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  left: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 200px;
  height: 200px;
  bottom: 20%;
  right: -50px;
  animation-delay: 5s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  top: 60%;
  left: 20%;
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(30px, -30px) rotate(120deg); }
  66% { transform: translate(-20px, 20px) rotate(240deg); }
}

/* 🏢 FEATURED SECTION */
.featured-section {
  width: 100%;
  max-width: 1400px;
  padding: 5rem 2rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin: 0 0 3rem 0;
  color: #1a202c;
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 2px;
}

/* Loading state */
.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 5rem 0;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(102, 126, 234, 0.1);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1.5rem;
  color: #667eea;
  font-size: 1.1rem;
  font-weight: 500;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Apartments grid */
.apartments-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #718096;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  font-size: 1.1rem;
  margin: 0.5rem 0;
}

.empty-subtitle {
  font-size: 0.95rem;
  color: #a0aec0;
}

/* Responsive design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .search-bar {
    flex-direction: column;
    border-radius: 20px;
  }

  .search-button {
    border-radius: 0 0 20px 20px;
  }

  .section-title {
    font-size: 2rem;
  }

  .apartments-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }

  .featured-section {
    padding: 3rem 1rem;
  }
}
</style>