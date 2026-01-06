<template>
  <div class="apartments-view">
    <div class="filters">
      <input 
        v-model="filters.search" 
        type="text" 
        placeholder="Search apartments..." 
        class="search-input"
      >
      <select v-model="filters.price_range" class="filter-select">
        <option value="">Any Price</option>
        <option value="0-100">$0 - $100</option>
        <option value="100-200">$100 - $200</option>
        <option value="200-500">$200 - $500</option>
      </select>
      <button @click="applyFilters" class="filter-btn">Apply Filters</button>
    </div>

    <div v-if="apartmentsStore.loading" class="loading">Loading apartments...</div>
    <div v-else-if="apartmentsStore.error" class="error">
      {{ apartmentsStore.error }}
    </div>
    <div v-else class="apartments-grid">
      <ApartmentCard 
        v-for="apartment in apartmentsStore.apartments" 
        :key="apartment.id" 
        :apartment="apartment" 
        :is-wishlisted="isApartmentWishlisted(apartment.id)"
        @toggle-wishlist="handleToggleWishlist"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useApartmentsStore } from '@/stores/apartments';
import { useWishlistStore } from '@/stores/wishlist';
import ApartmentCard from '@/components/ApartmentCard.vue';

const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();

const filters = ref({
  search: '',
  price_range: ''
});

const isApartmentWishlisted = computed(() => (apartmentId) => {
  return wishlistStore.wishlistItems.some(item => item.apartment_id === apartmentId);
});

const applyFilters = async () => {
  await apartmentsStore.fetchApartments(filters.value);
  await wishlistStore.fetchWishlist();
};

const handleToggleWishlist = async (apartmentId, isWishlisted) => {
  // The wishlist store already handles adding/removing.
  // We just need to ensure the local view is refreshed or the state is reacted to.
  // Pinia's reactivity should handle the icon change automatically.
  // Re-fetching the full wishlist to ensure consistency.
  await wishlistStore.fetchWishlist();
};

onMounted(async () => {
  await apartmentsStore.fetchApartments();
  await wishlistStore.fetchWishlist();
});
</script>

<style scoped>
.apartments-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-input, .filter-select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.search-input {
  flex: 1;
  min-width: 200px;
}

.filter-btn {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.filter-btn:hover {
  background-color: #0056b3;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
}

.apartments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .search-input, .filter-select {
    width: 100%;
  }
}
</style>