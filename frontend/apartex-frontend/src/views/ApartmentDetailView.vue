<template>
  <div class="apartment-detail">
    <div v-if="apartmentsStore.loading" class="loading">Loading apartment details...</div>
    <div v-else-if="apartmentsStore.error" class="error">
      {{ apartmentsStore.error }}
    </div>
    <div v-else-if="apartment" class="apartment-content">
      <div class="apartment-header">
        <h1>{{ apartment.title }}</h1>
        <p class="location">{{ apartment.city }}</p>
        <div class="price">${{ apartment.price_per_night }} / night</div>
        <button class="wishlist-btn" @click="toggleWishlist">
          <svg width="24" height="24" viewBox="0 0 24 24" :fill="isApartmentWishlisted ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
          </svg>
          {{ isApartmentWishlisted ? 'Remove from Wishlist' : 'Add to Wishlist' }}
        </button>
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
import { useRoute, useRouter } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import { useWishlistStore } from '@/stores/wishlist';
import { useAuthStore } from '@/stores/auth';
import BookingForm from '@/components/BookingForm.vue';

const route = useRoute();
const router = useRouter();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();
const authStore = useAuthStore();

const apartment = computed(() => apartmentsStore.currentApartment);
const isApartmentWishlisted = computed(() => {
  return wishlistStore.wishlistItems.some(item => item.apartment_id === apartment.value?.id);
});

onMounted(async () => {
  await apartmentsStore.fetchApartmentById(route.params.id);
  await wishlistStore.fetchWishlist();
});

const toggleWishlist = async () => {
  if (!authStore.user) {
    alert('Please log in to manage your wishlist.');
    router.push('/login');
    return;
  }

  if (isApartmentWishlisted.value) {
    await wishlistStore.removeFromWishlist(apartment.value.id);
  } else {
    await wishlistStore.addToWishlist(apartment.value.id);
  }
};
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
  position: relative;
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

.wishlist-btn {
  position: absolute;
  top: 0;
  right: 0;
  background: none;
  border: 1px solid var(--primary);
  color: var(--primary);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.wishlist-btn:hover {
  background: var(--primary);
  color: white;
}

.wishlist-btn svg {
  transition: fill 0.2s ease;
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

.booking-section {
  /* Style as needed */
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

  .wishlist-btn {
    position: static;
    margin-top: 1rem;
    width: 100%;
    justify-content: center;
  }
}
</style>