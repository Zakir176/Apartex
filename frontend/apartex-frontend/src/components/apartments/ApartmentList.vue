<!-- src/components/apartments/ApartmentList.vue -->
<template>
  <div class="apartment-list">
    <div v-if="loading" class="loading">
      <ProgressSpinner />
    </div>
    
    <div v-else-if="apartments.length === 0" class="empty-state">
      <p>No apartments found</p>
    </div>
    
    <div v-else class="apartments-grid">
      <div 
        v-for="apartment in apartments" 
        :key="apartment.id" 
        class="apartment-card"
        @click="$router.push(`/apartments/${apartment.id}`)"
      >
        <div class="apartment-image">
          <img :src="apartment.image_url || '/placeholder-apartment.jpg'" :alt="apartment.title" />
          <div class="apartment-price">
            ${{ apartment.price_per_night }}/night
          </div>
        </div>
        <div class="apartment-info">
          <h3>{{ apartment.title }}</h3>
          <p class="location">{{ apartment.location }}</p>
          <div class="apartment-features">
            <span><i class="pi pi-users"></i> {{ apartment.max_guests }} guests</span>
            <span><i class="pi pi-home"></i> {{ apartment.bedrooms }} bedrooms</span>
          </div>
          <div class="rating">
            <Rating :modelValue="apartment.rating" :readonly="true" :cancel="false" />
            <span>({{ apartment.review_count }})</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProgressSpinner from 'primevue/progressspinner'
import Rating from 'primevue/rating'

export default {
  name: 'ApartmentList',
  components: {
    ProgressSpinner,
    Rating
  },
  props: {
    apartments: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.apartments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.apartment-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.apartment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.apartment-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.apartment-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.apartment-price {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-weight: 600;
  color: #2d3748;
}

.apartment-info {
  padding: 1.5rem;
}

.apartment-info h3 {
  margin-bottom: 0.5rem;
  color: #2d3748;
}

.location {
  color: #718096;
  margin-bottom: 1rem;
}

.apartment-features {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  color: #4a5568;
}

.apartment-features span {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading, .empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4rem;
}

.empty-state p {
  color: #718096;
  font-size: 1.125rem;
}
</style>