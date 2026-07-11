<template>
  <div class="min-h-screen bg-[#F8F7F4] py-8 px-6">
    <div class="max-w-[1400px] mx-auto">
      <!-- TOP BAR -->
      <div class="flex justify-between items-end mb-6">
        <h1 class="text-3xl font-extrabold text-slate-800 m-0">Explore Stays</h1>
        <span class="text-sm font-medium text-slate-400">{{ pendingCount }} properties found</span>
      </div>

      <!-- FILTER BAR -->
      <div class="flex gap-3 overflow-x-auto pb-4 mb-6 scrollbar-hide">
        <div 
          class="bg-white border-[1.5px] border-surface-border rounded-full px-4 py-2 text-sm font-semibold text-slate-500 cursor-pointer whitespace-nowrap transition-all duration-150 hover:border-surface-border-strong hover:text-slate-800" 
          :class="filters.city === '' ? '!bg-accent !text-white !border-accent' : ''"
          @click="setCityFilter('')"
        >
          All
        </div>
        <div 
          v-for="city in ['Lusaka', 'Livingstone', 'Ndola', 'Kitwe']" 
          :key="city"
          class="bg-white border-[1.5px] border-surface-border rounded-full px-4 py-2 text-sm font-semibold text-slate-500 cursor-pointer whitespace-nowrap transition-all duration-150 hover:border-surface-border-strong hover:text-slate-800"
          :class="filters.city === city ? '!bg-accent !text-white !border-accent' : ''"
          @click="setCityFilter(city)"
        >
          {{ city }}
        </div>
      </div>

      <!-- LOADING STATE -->
      <div v-if="apartmentsStore.loading && apartmentsStore.apartments.length === 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-white border border-surface-border rounded-lg p-4 flex flex-col gap-4">
          <div class="h-[200px] rounded-md bg-slate-200 animate-pulse"></div>
          <div class="h-5 rounded-sm bg-slate-200 animate-pulse w-3/5"></div>
          <div class="h-10 rounded-sm bg-slate-200 animate-pulse w-full"></div>
        </div>
      </div>

      <!-- EMPTY STATE -->
      <div v-else-if="apartmentsStore.apartments.length === 0" class="flex flex-col items-center justify-center text-center py-16">
        <div class="text-6xl mb-4">🏜️</div>
        <h2 class="text-xl font-bold text-slate-800 mb-2">No properties found</h2>
        <p class="text-slate-500 mb-6">We couldn't find any stays matching your criteria.</p>
        <button class="btn-accent px-6 py-3" @click="clearFilters">Reset Filters</button>
      </div>

      <!-- CARD GRID -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
