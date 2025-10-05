<template>
  <div class="apartment-detail">
    <div v-if="apartmentsStore.loading" class="loading">Loading apartment details...</div>
    <div v-else-if="apartmentsStore.error" class="error">
      {{ apartmentsStore.error }}
    </div>
    <div v-else-if="apartment" class="apartment-content">
      <div class="apartment-header">
        <h1>{{ apartment.title }}</h1>
        <p class="location">{{ apartment.location }}</p>
        <div class="price">${{ apartment.price_per_night }} / night</div>
      </div>

      <div class="apartment-grid">
        <div class="apartment-images">
          <img :src="apartment.image_url || '/placeholder-apartment.jpg'" :alt="apartment.title">
        </div>

        <div class="booking-section">
          <BookingForm :apartment="apartment" />
        </div>
      </div>

      <div class="apartment-details">
        <div class="details-section">
          <h3>Description</h3>
          <p>{{ apartment.description }}</p>
        </div>

        <div class="details-section">
          <h3>Amenities</h3>
          <div class="amenities-grid">
            <div class="amenity" v-if="apartment.bedrooms">
              <span>🛏️</span>
              <span>{{ apartment.bedrooms }} bedrooms</span>
            </div>
            <div class="amenity" v-if="apartment.bathrooms">
              <span>🚿</span>
              <span>{{ apartment.bathrooms }} bathrooms</span>
            </div>
            <div class="amenity" v-if="apartment.area">
              <span>📏</span>
              <span>{{ apartment.area }} sq ft</span>
            </div>
            <div class="amenity" v-if="apartment.wifi">
              <span>📶</span>
              <span>WiFi</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import BookingForm from '@/components/BookingForm.vue';

const route = useRoute();
const apartmentsStore = useApartmentsStore();

const apartment = computed(() => apartmentsStore.currentApartment);

onMounted(async () => {
  await apartmentsStore.fetchApartmentById(route.params.id);
});
</script>

<style scoped>
.apartment-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
}

.apartment-header {
  margin-bottom: 2rem;
}

.apartment-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
}

.location {
  color: #666;
  font-size: 1.1rem;
  margin: 0 0 1rem 0;
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #007bff;
}

.apartment-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}

.apartment-images img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
}

.apartment-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.details-section h3 {
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.amenities-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.amenity {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .apartment-grid {
    grid-template-columns: 1fr;
  }
  
  .apartment-details {
    grid-template-columns: 1fr;
  }
  
  .amenities-grid {
    grid-template-columns: 1fr;
  }
}
</style>