<!-- src/views/HomeView.vue -->
<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>Find Your Perfect Stay</h1>
        <p>Book apartments with ease and earn loyalty rewards</p>
        <SearchBar />
      </div>
    </section>
    
    <section class="featured-apartments">
      <div class="container">
        <h2>Featured Apartments</h2>
        <ApartmentList :apartments="featuredApartments" />
      </div>
    </section>
  </div>
</template>

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

    const loadFeaturedApartments = async () => {
      isLoading.value = true
      try {
        const response = await apartmentService.getFeatured()
        featuredApartments.value = response.data
      } catch (error) {
        console.error('Error loading featured apartments:', error)
      } finally {
        isLoading.value = false
      }
    }

    onMounted(() => {
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
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6rem 2rem;
  text-align: center;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.featured-apartments h2 {
  text-align: center;
  margin-bottom: 3rem;
  font-size: 2.5rem;
  color: #2d3748;
}
</style>