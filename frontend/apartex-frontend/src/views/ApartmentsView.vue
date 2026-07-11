<template>
  <div class="apartments-page">
    <!-- TOP BAR -->
    <div class="top-bar">
      <h1 class="page-title">Explore Stays</h1>
      <span class="result-count">{{ pendingCount }} properties found</span>
    </div>

    <!-- FILTER BAR -->
    <div class="filter-bar">
      <div 
        class="filter-chip" 
        :class="{ active: filters.city === '' }"
        @click="setCityFilter('')"
      >
        All
      </div>
      <div 
        v-for="city in ['Lusaka', 'Livingstone', 'Ndola', 'Kitwe']" 
        :key="city"
        class="filter-chip"
        :class="{ active: filters.city === city }"
        @click="setCityFilter(city)"
      >
        {{ city }}
      </div>
    </div>

    <!-- LOADING STATE -->
    <div v-if="apartmentsStore.loading && apartmentsStore.apartments.length === 0" class="card-grid">
      <div v-for="i in 6" :key="i" class="skeleton-card">
        <div class="skeleton-image pulse"></div>
        <div class="skeleton-text pulse title"></div>
        <div class="skeleton-text pulse desc"></div>
      </div>
    </div>

    <!-- EMPTY STATE -->
    <div v-else-if="apartmentsStore.apartments.length === 0" class="empty-state">
      <div class="empty-icon">🏜️</div>
      <h2>No properties found</h2>
      <p>We couldn't find any stays matching your criteria.</p>
      <button class="btn-reset" @click="clearFilters">Reset Filters</button>
    </div>

    <!-- CARD GRID -->
    <div v-else class="card-grid">
      <ApartmentCard 
        v-for="apartment in apartmentsStore.apartments" 
        :key="apartment.id"
        :apartment="apartment" 
        :is-wishlisted="isApartmentWishlisted(apartment.id)"
        :isSelected="selectedApartmentId === apartment.id"
        @toggle-wishlist="handleToggleWishlist"
        @card-hover="(id) => selectedApartmentId = id"
        @card-leave="() => selectedApartmentId = null"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import { useWishlistStore } from '@/stores/wishlist';
import ApartmentCard from '@/components/ApartmentCard.vue';
import MapComponent from '@/components/MapComponent.vue'; // Kept in imports just in case logic needs it

// PrimeVue components kept for logic compatibility
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import Slider from 'primevue/slider';
import Sidebar from 'primevue/sidebar';
import Checkbox from 'primevue/checkbox';
import Skeleton from 'primevue/skeleton';

const route = useRoute();
const router = useRouter();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();

const showFilters = ref(false);
const viewMode = ref('grid'); // 'grid' or 'map'
const selectedApartmentId = ref(null);
const mapBounds = ref(null);

const filters = ref({
  city: route.query.city || '',
  price_range: [0, 1000],
  min_capacity: 1,
  min_bedrooms: 0,
  amenities: []
});

const commonAmenities = ['WiFi', 'Pool', 'Parking', 'Kitchen', 'TV', 'Air Con', 'Gym', 'Laundry'];

const priceDisplayShort = computed(() => {
  const [min, max] = filters.value.price_range;
  if (min === 0 && max === 1000) return 'Any Price';
  if (max === 1000) return `$${min}+`;
  return `$${min}-$${max}`;
});

const hasActiveFilters = computed(() => {
  return filters.value.city || filters.value.price_range[0] > 0 || filters.value.price_range[1] < 1000 || filters.value.min_capacity > 1 || filters.value.min_bedrooms > 0;
});

const isApartmentWishlisted = computed(() => (apartmentId) => {
  return wishlistStore.wishlistItems.some(item => item.apartment_id === apartmentId);
});

const pendingCount = computed(() => {
  return apartmentsStore.apartments.filter(apt => {
    const [min, max] = filters.value.price_range;
    const cityOk = !filters.value.city || apt.city.toLowerCase().includes(filters.value.city.toLowerCase());
    const priceOk = apt.price_per_night >= min && (max === 1000 || apt.price_per_night <= max);
    const capacityOk = apt.capacity >= filters.value.min_capacity;
    const bedroomsOk = apt.bedrooms >= filters.value.min_bedrooms;
    const amenitiesOk = filters.value.amenities.length === 0 || (Array.isArray(apt.amenities) && filters.value.amenities.every(a => apt.amenities.includes(a)));
    return cityOk && priceOk && capacityOk && bedroomsOk && amenitiesOk;
  }).length;
});

const pendingCountLabel = computed(() => {
  if (apartmentsStore.loading) return 'Updating...';
  const n = pendingCount.value;
  return n === 0 ? 'No Results' : `View ${n} Properties`;
});

const setCityFilter = async (city) => {
  filters.value.city = city;
  router.replace({ query: { ...route.query, city: city || undefined } });
  await applyFilters();
};

const applyFilters = async (additionalParams = {}) => {
  const [min, max] = filters.value.price_range;
  const params = {
    city: filters.value.city,
    min_price: min,
    max_price: max === 1000 ? 999999 : max,
    capacity: filters.value.min_capacity,
    bedrooms: filters.value.min_bedrooms,
    amenities: filters.value.amenities.length > 0 ? filters.value.amenities : undefined,
    ...mapBounds.value,
    ...additionalParams
  };
  
  await apartmentsStore.fetchApartments(params);
  showFilters.value = false;
};

const handleBoundsChanged = (bounds) => {
  if (viewMode.value !== 'map') return;
  mapBounds.value = bounds;
  
  clearTimeout(window.mapSearchTimeout);
  window.mapSearchTimeout = setTimeout(() => {
    applyFilters();
  }, 500);
};

const clearFilters = async () => {
  filters.value = {
    city: '',
    price_range: [0, 1000],
    min_capacity: 1,
    min_bedrooms: 0,
    amenities: []
  };
  mapBounds.value = null;
  router.replace({ query: {} });
  await applyFilters();
  showFilters.value = false;
};

const handleToggleWishlist = async () => {
  await wishlistStore.fetchWishlist();
};

watch(() => route.query.city, (newCity) => {
  if (newCity !== filters.value.city) {
    filters.value.city = newCity || '';
    applyFilters();
  }
});

onMounted(async () => {
  await applyFilters();
  await wishlistStore.fetchWishlist();
});
</script>

<style scoped>
.apartments-page {
  background: var(--color-bg);
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
  min-height: 100vh;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: var(--space-6);
}

.page-title {
  font-size: var(--font-size-3xl);
  font-weight: 800;
  color: var(--color-text-primary);
  margin: 0;
}

.result-count {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  font-weight: 500;
}

.filter-bar {
  display: flex;
  gap: var(--space-3);
  overflow-x: auto;
  padding-bottom: var(--space-4);
  margin-bottom: var(--space-6);
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.filter-bar::-webkit-scrollbar {
  display: none;
}

.filter-chip {
  background: var(--color-surface);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-full);
  padding: var(--space-2) var(--space-4);
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-text-secondary);
  cursor: pointer;
  white-space: nowrap;
  transition: all var(--transition-fast);
}

.filter-chip:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
}

.filter-chip.active {
  background: var(--color-accent);
  color: white;
  border-color: var(--color-accent);
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);
}

@media (max-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--space-16) 0;
}

.empty-icon {
  font-size: var(--font-size-5xl);
  margin-bottom: var(--space-4);
}

.empty-state h2 {
  font-size: var(--font-size-xl);
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

.empty-state p {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-6);
}

.btn-reset {
  background: var(--color-accent);
  color: white;
  border: none;
  border-radius: var(--radius-full);
  padding: var(--space-3) var(--space-6);
  font-weight: 600;
  font-size: var(--font-size-base);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.btn-reset:hover {
  background: var(--color-accent-hover);
}

/* SKELETON CARDS */
.skeleton-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.skeleton-image {
  height: 200px;
  border-radius: var(--radius-md);
  background: #e2e8f0;
}

.skeleton-text {
  height: 20px;
  border-radius: var(--radius-sm);
  background: #e2e8f0;
}

.skeleton-text.title {
  width: 60%;
}

.skeleton-text.desc {
  width: 100%;
  height: 40px;
}

.pulse {
  animation: pulse 2s infinite ease-in-out;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 0.2; }
  100% { opacity: 0.6; }
}
</style>
