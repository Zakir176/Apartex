<!-- src/views/ApartmentsView.vue -->
<template>
  <div class="apartments-page">
    <div class="page-header">
      <div class="container">
        <h1>Find Your Perfect Apartment</h1>
        <p>Discover amazing places to stay around the world</p>
      </div>
    </div>

    <div class="container main-layout">
      <!-- Filters Sidebar -->
      <aside class="filters-sidebar">
        <div class="filters-card">
          <h3>Filters</h3>
          
          <div class="filter-group">
            <label>Price Range</label>
            <div class="price-inputs">
              <input type="number" v-model="filters.minPrice" placeholder="Min" class="price-input">
              <span>-</span>
              <input type="number" v-model="filters.maxPrice" placeholder="Max" class="price-input">
            </div>
          </div>

          <div class="filter-group">
            <label>Guests</label>
            <select v-model="filters.guests" class="filter-select">
              <option value="">Any</option>
              <option value="1">1 guest</option>
              <option value="2">2 guests</option>
              <option value="4">4+ guests</option>
              <option value="6">6+ guests</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Bedrooms</label>
            <select v-model="filters.bedrooms" class="filter-select">
              <option value="">Any</option>
              <option value="1">1 bedroom</option>
              <option value="2">2 bedrooms</option>
              <option value="3">3+ bedrooms</option>
            </select>
          </div>

          <button @click="searchApartments" class="apply-filters-btn">Apply Filters</button>
          <button @click="clearFilters" class="clear-filters-btn">Clear All</button>
        </div>
      </aside>

      <!-- Apartments Grid -->
      <main class="apartments-main">
        <div class="results-header">
          <h2>{{ apartmentStore.apartments.length }} apartments found</h2>
        </div>

        <div v-if="apartmentStore.isLoading" class="loading">
          <p>Loading apartments...</p>
        </div>

        <div v-else class="apartments-grid">
          <div 
            v-for="apartment in apartmentStore.apartments" 
            :key="apartment.id" 
            class="apartment-card"
            @click="$router.push(`/apartments/${apartment.id}`)"
          >
            <img :src="apartment.image_url" :alt="apartment.title" class="apartment-image">
            <div class="apartment-info">
              <h3>{{ apartment.title }}</h3>
              <p class="location">{{ apartment.location }}</p>
              <p class="price">${{ apartment.price_per_night }}/night</p>
              <div class="rating">
                <span class="stars">⭐ {{ apartment.rating || '4.5' }}</span>
                <span class="reviews">({{ apartment.review_count || '25' }} reviews)</span>
              </div>
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

        <div v-if="!apartmentStore.isLoading && apartmentStore.apartments.length === 0" class="no-results">
          <h3>No apartments found</h3>
          <p>Try adjusting your search criteria</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { onMounted, reactive } from 'vue'
import { useApartmentStore } from '@/stores/apartments'

export default {
  name: 'ApartmentsView',
  setup() {
    const apartmentStore = useApartmentStore()
    
    const filters = reactive({
      minPrice: '',
      maxPrice: '',
      guests: '',
      bedrooms: '',
      amenities: []
    })

    const searchApartments = async () => {
      try {
        await apartmentStore.searchApartments(filters)
      } catch (error) {
        console.error('Failed to search apartments:', error)
      }
    }

    const clearFilters = () => {
      Object.keys(filters).forEach(key => {
        if (Array.isArray(filters[key])) {
          filters[key] = []
        } else {
          filters[key] = ''
        }
      })
      searchApartments()
    }

    onMounted(async () => {
      try {
        await apartmentStore.loadAllApartments()
      } catch (error) {
        console.error('Failed to load apartments:', error)
      }
    })

    return {
      apartmentStore,
      filters,
      searchApartments,
      clearFilters
    }
  }
}
</script>