<template>
  <div class="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-[1400px] mx-auto">
      <!-- TOP BAR -->
      <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-6 gap-4">
        <div>
          <span class="text-xs font-black text-accent uppercase tracking-widest bg-orange-50 px-3 py-1 rounded-full border border-orange-100">Stay Directory</span>
          <h1 class="text-3xl font-black text-slate-900 mt-2 mb-0">Explore Stays</h1>
        </div>
        <span class="text-xs font-bold text-slate-500 bg-white px-3.5 py-1.5 rounded-full border border-slate-200 shadow-xs">{{ pendingCount }} properties found</span>
      </div>

      <!-- FILTER BAR -->
      <div class="flex gap-2 overflow-x-auto pb-4 mb-6 scrollbar-hide">
        <div 
          class="bg-white border border-slate-200 rounded-full px-4 py-2 text-xs font-bold text-slate-600 cursor-pointer whitespace-nowrap transition-all duration-150 hover:border-slate-300 hover:text-slate-900" 
          :class="filters.city === '' ? '!bg-slate-900 !text-white !border-slate-900 !font-black' : ''"
          @click="setCityFilter('')"
        >
          All Locations
        </div>
        <div 
          v-for="city in ['Lusaka', 'Livingstone', 'Ndola', 'Kitwe', 'Solwezi']" 
          :key="city"
          class="bg-white border border-slate-200 rounded-full px-4 py-2 text-xs font-bold text-slate-600 cursor-pointer whitespace-nowrap transition-all duration-150 hover:border-slate-300 hover:text-slate-900"
          :class="filters.city === city ? '!bg-slate-900 !text-white !border-slate-900 !font-black' : ''"
          @click="setCityFilter(city)"
        >
          {{ city }}
        </div>
      </div>

      <!-- LOADING STATE -->
      <div v-if="apartmentsStore.loading && apartmentsStore.apartments.length === 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-white border border-slate-200 rounded-2xl p-4 flex flex-col gap-4">
          <div class="h-[200px] rounded-xl bg-slate-200 animate-pulse"></div>
          <div class="h-5 rounded bg-slate-200 animate-pulse w-3/5"></div>
          <div class="h-10 rounded bg-slate-200 animate-pulse w-full"></div>
        </div>
      </div>

      <!-- EMPTY STATE -->
      <div v-else-if="apartmentsStore.apartments.length === 0" class="bg-white border border-slate-200 rounded-3xl p-12 text-center max-w-md mx-auto my-12 shadow-sm">
        <div class="w-16 h-16 rounded-full bg-orange-50 text-accent flex items-center justify-center text-2xl mx-auto mb-4 border border-orange-100">
          <i class="pi pi-search"></i>
        </div>
        <h2 class="text-xl font-black text-slate-900 mb-2">No Stays Found</h2>
        <p class="text-xs text-slate-500 mb-6 font-medium">We couldn't find any stays matching your selected criteria.</p>
        <button class="btn-accent px-6 py-3 rounded-full text-xs font-black" @click="clearFilters">Reset All Filters</button>
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
import { useAuthStore } from '@/stores/auth';
import ApartmentCard from '@/components/ApartmentCard.vue';

const route = useRoute();
const router = useRouter();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();
const authStore = useAuthStore();

const showFilters = ref(false);
const viewMode = ref('grid');
const selectedApartmentId = ref(null);
const mapBounds = ref(null);

const filters = ref({
  city: route.query.city || '',
  price_range: [0, 1000],
  min_capacity: 1,
  min_bedrooms: 0,
  amenities: []
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
    return cityOk && priceOk && capacityOk && bedroomsOk;
  }).length;
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
    ...mapBounds.value,
    ...additionalParams
  };
  
  await apartmentsStore.fetchApartments(params);
  showFilters.value = false;
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
  if (authStore.isAuthenticated) {
    await wishlistStore.fetchWishlist();
  }
};

watch(() => route.query.city, (newCity) => {
  if (newCity !== filters.value.city) {
    filters.value.city = newCity || '';
    applyFilters();
  }
});

onMounted(async () => {
  await applyFilters();
  if (authStore.isAuthenticated) {
    await wishlistStore.fetchWishlist();
  }
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
