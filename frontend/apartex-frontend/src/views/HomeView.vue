<!-- src/views/HomeView.vue -->
<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">Find Your Perfect Stay</h1>
          <p class="hero-subtitle">Book apartments with ease and earn loyalty rewards</p>
          <SearchBar />
        </div>
      </div>
    </section>

    <!-- Featured Apartments Section -->
    <section class="featured-section">
      <div class="container">
        <div class="section-header">
          <h2>Featured Apartments</h2>
          <p>Discover our most popular properties</p>
        </div>
        <ApartmentList :apartments="featuredApartments" :loading="isLoading" />
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🏆</div>
            <h3>Loyalty Rewards</h3>
            <p>Earn points with every booking and unlock exclusive benefits</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3>Secure Booking</h3>
            <p>Your payments and personal information are always protected</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">⭐</div>
            <h3>Verified Properties</h3>
            <p>All apartments are carefully vetted for quality and comfort</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<!-- src/views/HomeView.vue - updated setup function -->
<script>
import { ref, onMounted } from 'vue'
import SearchBar from '@/components/apartments/SearchBar.vue'
import ApartmentList from '@/components/apartments/ApartmentList.vue'
import apartmentService from '@/services/apartments'

export default {
  name: 'HomeView',
  components: {
    SearchBar,
    ApartmentList
  },
  setup() {
    const featuredApartments = ref([])
    const isLoading = ref(false)

    // Fallback data in case service fails
    const fallbackApartments = [
      {
        id: 1,
        title: "Luxury Downtown Apartment",
        location: "New York, NY",
        price_per_night: 150,
        max_guests: 4,
        bedrooms: 2,
        bathrooms: 2,
        rating: 4.8,
        review_count: 124,
        image_url: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400",
        is_featured: true
      },
      {
        id: 2,
        title: "Beachfront Condo",
        location: "Miami, FL",
        price_per_night: 200,
        max_guests: 6,
        bedrooms: 3,
        bathrooms: 2,
        rating: 4.9,
        review_count: 89,
        image_url: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400", 
        is_featured: true
      }
    ]

    const loadFeaturedApartments = async () => {
      isLoading.value = true
      try {
        console.log('Attempting to load apartments...')
        const response = await apartmentService.getFeatured()
        console.log('Service response:', response)
        
        if (response && response.data && response.data.length > 0) {
          featuredApartments.value = response.data
          console.log('Successfully loaded', featuredApartments.value.length, 'apartments')
        } else {
          console.log('No data from service, using fallback')
          featuredApartments.value = fallbackApartments
        }
      } catch (error) {
        console.error('Error loading apartments, using fallback:', error)
        featuredApartments.value = fallbackApartments
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
      console.log('HomeView component mounted')
      loadFeaturedApartments()
    })

    return {
      featuredApartments,
      isLoading
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 1rem;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><polygon fill="rgba(255,255,255,0.05)" points="0,1000 1000,0 1000,1000"/></svg>');
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.1;
}

.hero-subtitle {
  font-size: clamp(1.125rem, 2.5vw, 1.5rem);
  margin-bottom: 3rem;
  opacity: 0.9;
  font-weight: 300;
}

/* Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Featured Section */
.featured-section {
  padding: 5rem 0;
  background: #f8fafc;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-header h2 {
  font-size: clamp(2rem, 4vw, 2.5rem);
  color: #2d3748;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.section-header p {
  font-size: 1.125rem;
  color: #718096;
}

/* Features Section */
.features-section {
  padding: 5rem 0;
  background: white;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.feature-card {
  text-align: center;
  padding: 2rem;
  border-radius: 1rem;
  background: #f8fafc;
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  color: #2d3748;
  margin-bottom: 1rem;
  font-weight: 600;
}

.feature-card p {
  color: #718096;
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero {
    padding: 3rem 1rem;
  }
  
  .featured-section,
  .features-section {
    padding: 3rem 0;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .feature-card {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 2rem 1rem;
  }
  
  .featured-section,
  .features-section {
    padding: 2rem 0;
  }
}
</style>