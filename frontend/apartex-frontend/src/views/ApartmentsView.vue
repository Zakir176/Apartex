<template>
  <div class="apartments-view fadein animation-duration-500">
    <!-- Top Experience Bar: The Search Pill -->
    <div class="search-pill-container flex justify-content-center mb-6">
      <div class="search-pill glass shadow-4 flex align-items-center">
        <div class="pill-section px-4 py-2 border-right-1 border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" @click="showFilters = true">
          <span class="block text-xs font-bold uppercase tracking-wider text-muted mb-1">Where</span>
          <span class="font-bold text-900">{{ filters.city || 'Anywhere' }}</span>
        </div>
        <div class="pill-section px-4 py-2 border-right-1 border-gray-200 cursor-pointer hover:bg-gray-50 transition-colors" @click="showFilters = true">
          <span class="block text-xs font-bold uppercase tracking-wider text-muted mb-1">Price</span>
          <span class="font-bold text-900">{{ priceDisplay }}</span>
        </div>
        <div class="pill-section px-4 py-2 cursor-pointer hover:bg-gray-50 transition-colors flex align-items-center gap-2" @click="showFilters = true">
          <div>
            <span class="block text-xs font-bold uppercase tracking-wider text-muted mb-1">Refine</span>
            <span class="font-bold text-900">Filters</span>
          </div>
          <div class="search-icon-btn p-2 bg-primary border-round-circle text-white flex align-items-center justify-content-center ml-2">
            <i class="pi pi-search text-xs"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Filters Display -->
    <div v-if="hasActiveFilters" class="active-filters-chips flex justify-content-center gap-2 mb-5">
       <Tag v-if="filters.city" :value="filters.city" @iconClick="filters.city = ''; applyFilters()" icon="pi pi-times" severity="secondary" rounded />
       <Tag v-if="filters.price_range[0] > 0 || filters.price_range[1] < 1000" :value="priceDisplay" @iconClick="filters.price_range = [0, 1000]; applyFilters()" icon="pi pi-times" severity="secondary" rounded />
       <Button label="Clear All" @click="clearFilters" class="p-button-text p-button-sm font-bold" />
    </div>

    <!-- Loading State -->
    <div v-if="apartmentsStore.loading && apartmentsStore.apartments.length === 0" class="loading-state flex flex-column align-items-center py-8">
      <ProgressSpinner style="width: 60px; height: 60px" strokeWidth="4" />
      <p class="mt-4 text-xl font-bold text-muted">Curating top-tier stays...</p>
    </div>
    
    <!-- Content Section -->
    <div v-else class="content-section">
      <div v-if="apartmentsStore.apartments.length === 0" class="empty-state text-center py-8">
        <div class="text-6xl mb-4 text-primary opacity-20">
          <i class="pi pi-map"></i>
        </div>
        <h3 class="text-3xl font-bold">No results found</h3>
        <p class="text-muted text-lg mt-2">Adjust your filters to see more incredible properties.</p>
        <Button label="Clear Filters" icon="pi pi-times" @click="clearFilters" class="mt-5 p-button-outlined" />
      </div>
      
      <div v-else class="apartments-grid grid mt-2 px-2">
        <div v-for="apartment in apartmentsStore.apartments" :key="apartment.id" class="col-12 md:col-6 lg:col-4 xl:col-3 p-3">
          <ApartmentCard 
            :apartment="apartment" 
            :is-wishlisted="isApartmentWishlisted(apartment.id)"
            @toggle-wishlist="handleToggleWishlist"
          />
        </div>
      </div>
    </div>

    <!-- Full-Screen Filter Sidebar -->
    <Sidebar v-model:visible="showFilters" position="right" class="filter-sidebar" style="width: 450px; max-width: 95vw;">
      <template #header>
        <div class="flex flex-column">
          <h2 class="text-2xl font-bold m-0">Refine Search</h2>
          <p class="text-muted text-sm">Fine-tune your perfect Apartex stay</p>
        </div>
      </template>

      <div class="p-fluid">
        <!-- Location -->
        <div class="filter-section mb-5 pb-5 border-bottom-1 border-gray-100">
          <label class="font-bold text-900 block mb-3">Destination</label>
          <span class="p-input-icon-left">
            <i class="pi pi-map-marker" />
            <InputText v-model="filters.city" placeholder="Which city are you visiting?" />
          </span>
        </div>

        <!-- Price Range -->
        <div class="filter-section mb-5 pb-5 border-bottom-1 border-gray-100">
          <div class="flex justify-content-between align-items-center mb-3">
             <label class="font-bold text-900">Price Range</label>
             <span class="text-primary font-bold">${{ filters.price_range[0] }} - ${{ filters.price_range[1] }}+</span>
          </div>
          <div class="px-2 mt-4">
            <Slider v-model="filters.price_range" :range="true" :min="0" :max="1000" :step="10" />
            <div class="flex justify-content-between mt-3 text-xs text-muted font-medium">
              <span>$0</span>
              <span>$1,000+</span>
            </div>
          </div>
        </div>

        <!-- Rooms & Capacity -->
        <div class="filter-section mb-5 pb-5 border-bottom-1 border-gray-100">
          <label class="font-bold text-900 block mb-4">Space Requirements</label>
          
          <div class="flex justify-content-between align-items-center mb-4">
            <span class="text-muted font-medium">Minimum Guests</span>
            <InputNumber v-model="filters.min_capacity" showButtons buttonLayout="horizontal" :min="1" 
              inputClass="text-center w-3rem" class="p-inputnumber-sm"
              incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus" />
          </div>

          <div class="flex justify-content-between align-items-center mb-4">
            <span class="text-muted font-medium">Minimum Bedrooms</span>
            <InputNumber v-model="filters.min_bedrooms" showButtons buttonLayout="horizontal" :min="0" 
              inputClass="text-center w-3rem" class="p-inputnumber-sm"
              incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus" />
          </div>
        </div>

        <!-- Amenities -->
        <div class="filter-section mb-5">
           <label class="font-bold text-900 block mb-3">Core Amenities</label>
           <div class="grid pt-2">
             <div v-for="amenity in commonAmenities" :key="amenity" class="col-6 mb-2">
               <div class="flex align-items-center">
                 <Checkbox v-model="filters.amenities" :inputId="amenity" name="amenity" :value="amenity" />
                 <label :for="amenity" class="ml-2 text-sm">{{ amenity }}</label>
               </div>
             </div>
           </div>
        </div>
      </div>

      <template #footer>
        <div class="flex gap-2 pt-4 border-top-1 border-gray-100">
          <Button label="Clear All" @click="clearFilters" class="p-button-text p-button-secondary flex-1 font-bold" />
          <Button label="Show Results" @click="applyFilters" class="p-button-primary flex-2 font-bold" />
        </div>
      </template>
    </Sidebar>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import { useWishlistStore } from '@/stores/wishlist';
import ApartmentCard from '@/components/ApartmentCard.vue';

// PrimeVue components
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import Slider from 'primevue/slider';
import Sidebar from 'primevue/sidebar';
import Tag from 'primevue/tag';
import ProgressSpinner from 'primevue/progressspinner';
import Checkbox from 'primevue/checkbox';

const route = useRoute();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();

const showFilters = ref(false);

const filters = ref({
  city: route.query.city || '',
  price_range: [0, 1000],
  min_capacity: 1,
  min_bedrooms: 0,
  amenities: []
});

const commonAmenities = ['WiFi', 'Pool', 'Parking', 'Kitchen', 'TV', 'Air Con', 'Gym', 'Laundry'];

const priceDisplay = computed(() => {
  const [min, max] = filters.value.price_range;
  if (min === 0 && max === 1000) return 'Any Price';
  return `$${min} - $${max}${max === 1000 ? '+' : ''}`;
});

const hasActiveFilters = computed(() => {
  return filters.value.city || filters.value.price_range[0] > 0 || filters.value.price_range[1] < 1000 || filters.value.min_capacity > 1 || filters.value.min_bedrooms > 0;
});

const isApartmentWishlisted = computed(() => (apartmentId) => {
  return wishlistStore.wishlistItems.some(item => item.apartment_id === apartmentId);
});

const applyFilters = async () => {
  const [min, max] = filters.value.price_range;
  const params = {
    city: filters.value.city,
    min_price: min,
    max_price: max === 1000 ? 999999 : max,
    capacity: filters.value.min_capacity,
    bedrooms: filters.value.min_bedrooms
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
  await applyFilters();
  showFilters.value = false;
};

const handleToggleWishlist = async () => {
  await wishlistStore.fetchWishlist();
};

watch(() => route.query.city, (newCity) => {
  if (newCity) {
    filters.value.city = newCity;
    applyFilters();
  }
});

onMounted(async () => {
  await applyFilters();
  await wishlistStore.fetchWishlist();
});
</script>

<style scoped>
.apartments-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

/* Search Pill Styles */
.search-pill-container {
  position: sticky;
  top: 1rem;
  z-index: 100;
}

.search-pill {
  background: var(--surface-glass) !important;
  backdrop-filter: blur(20px);
  border: 1px solid var(--surface-border-glass);
  border-radius: 40px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding: 0.5rem;
  max-width: fit-content;
}

.search-pill:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
  transform: translateY(-2px);
}

.pill-section {
  min-width: 120px;
}

.search-icon-btn {
  width: 32px;
  height: 32px;
  box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.3);
}

/* Sidebar Customization */
:deep(.filter-sidebar) {
  border-top-left-radius: 30px !important;
  border-bottom-left-radius: 30px !important;
}

.filter-section label {
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.8rem;
  color: #64748b;
}

/* Dark Mode Adjustments */
.dark .search-pill {
  background: rgba(30, 41, 59, 0.7) !important;
}

.dark .pill-section:hover {
  background: rgba(51, 65, 85, 0.4);
}

.dark .pill-section {
  border-color: rgba(255, 255, 255, 0.1) !important;
}

@media (max-width: 768px) {
  .apartments-view {
    padding: 1.5rem 1rem;
  }
  
  .search-pill {
    width: 100%;
    justify-content: space-around;
  }

  .pill-section {
    min-width: auto;
    flex: 1;
    text-align: center;
  }
}
</style>