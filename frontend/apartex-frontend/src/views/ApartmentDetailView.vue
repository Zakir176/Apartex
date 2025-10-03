<!-- src/views/ApartmentDetailView.vue -->
<template>
  <div class="apartment-detail-page">
    <div class="container">
      <div v-if="apartmentStore.isLoading" class="loading">
        <p>Loading apartment details...</p>
      </div>
      
      <div v-else-if="apartmentStore.currentApartment" class="apartment-detail">
        <div class="apartment-header">
          <h1>{{ apartmentStore.currentApartment.title }}</h1>
          <p class="location">{{ apartmentStore.currentApartment.location }}</p>
        </div>

        <div class="apartment-gallery">
          <img :src="apartmentStore.currentApartment.image_url" :alt="apartmentStore.currentApartment.title" class="main-image">
        </div>

        <div class="apartment-content">
          <div class="apartment-info">
            <h2>About this apartment</h2>
            <p class="description">{{ apartmentStore.currentApartment.description }}</p>
            
            <div class="details-grid">
              <div class="detail-item">
                <span class="icon">👥</span>
                <span class="label">Guests:</span>
                <span class="value">{{ apartmentStore.currentApartment.max_guests }}</span>
              </div>
              <div class="detail-item">
                <span class="icon">🛏️</span>
                <span class="label">Bedrooms:</span>
                <span class="value">{{ apartmentStore.currentApartment.bedrooms }}</span>
              </div>
              <div class="detail-item">
                <span class="icon">🛁</span>
                <span class="label">Bathrooms:</span>
                <span class="value">{{ apartmentStore.currentApartment.bathrooms }}</span>
              </div>
            </div>

            <div class="amenities">
              <h3>Amenities</h3>
              <div class="amenities-list">
                <span v-for="amenity in apartmentStore.currentApartment.amenities" :key="amenity" class="amenity-item">
                  {{ amenity }}
                </span>
              </div>
            </div>
          </div>

          <div class="booking-card">
            <div class="price-section">
              <span class="price">${{ apartmentStore.currentApartment.price_per_night }}</span>
              <span class="period">per night</span>
            </div>
            <button @click="bookApartment" class="book-btn" :disabled="!authStore.isAuthenticated">
              {{ authStore.isAuthenticated ? 'Book Now' : 'Login to Book' }}
            </button>
          </div>
        </div>
      </div>

      <div v-else class="not-found">
        <h2>Apartment not found</h2>
        <router-link to="/apartments" class="back-link">Back to Apartments</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useApartmentStore } from '@/stores/apartments'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'ApartmentDetailView',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const apartmentStore = useApartmentStore()
    const authStore = useAuthStore()

    onMounted(async () => {
      try {
        await apartmentStore.loadApartmentDetail(route.params.id)
      } catch (error) {
        console.error('Failed to load apartment details:', error)
      }
    })

    const bookApartment = () => {
      if (!authStore.isAuthenticated) {
        router.push('/login')
        return
      }
      // TODO: Implement booking flow
      alert('Booking functionality to be implemented')
    }

    return {
      apartmentStore,
      authStore,
      bookApartment
    }
  }
}
</script>