<!-- src/views/HomeView.vue -->
<template>
  <div class="home">
    <header class="hero">
      <h1>Find Your Perfect Stay</h1>
      <p>Book apartments with ease and earn loyalty rewards</p>
    </header>

    <main class="main-content">
      <h2>Featured Apartments</h2>
      
      <div v-if="apartmentStore.isLoading" class="loading">
        <p>Loading apartments...</p>
      </div>
      
      <div v-else class="apartments-grid">
        <div 
          v-for="apartment in apartmentStore.featuredApartments" 
          :key="apartment.id" 
          class="apartment-card"
          @click="$router.push(`/apartments/${apartment.id}`)"
        >
          <img :src="apartment.image_url" :alt="apartment.title" class="apartment-image">
          <div class="apartment-info">
            <h3>{{ apartment.title }}</h3>
            <p class="location">{{ apartment.location }}</p>
            <p class="price">${{ apartment.price_per_night }}/night</p>
            <div class="details">
              <span class="detail-item">
                <span class="icon">👥</span>
                {{ apartment.max_guests }} guests
              </span>
              <span class="detail-item">
                <span class="icon">🛏️</span>
                {{ apartment.bedrooms }} bedrooms
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useApartmentStore } from '@/stores/apartments'

export default {
  name: 'HomeView',
  setup() {
    const apartmentStore = useApartmentStore()

    onMounted(async () => {
      try {
        await apartmentStore.loadFeaturedApartments()
      } catch (error) {
        console.error('Failed to load featured apartments:', error)
      }
    })

    return {
      apartmentStore
    }
  }
}
</script>