<template>
  <div class="ax-apartments-view">
    <!-- Top Hero Section (Internal) -->
    <div class="hero-header mb-8">
      <div class="flex flex-column gap-2 text-left">
        <h1 class="text-5xl font-extrabold tracking-tight">Discover your <span class="ax-text-gradient">ideal sanctuary.</span></h1>
        <p class="text-600 text-lg font-medium">Curated luxury stays across the globe's most iconic destinations.</p>
      </div>
    </div>

    <!-- Experience Bar: The Floating Search Pill -->
    <div class="search-pill-container flex justify-content-center gap-3">
      <div class="search-pill shadow-lg" @click="showFilters = true">
        <div class="pill-section border-right-1 border-100">
          <span class="label">Location</span>
          <span class="value">{{ filters.city || 'Anywhere' }}</span>
        </div>
        <div class="pill-section border-right-1 border-100">
          <span class="label">Price</span>
          <span class="value">{{ priceDisplayShort }}</span>
        </div>
        <div class="pill-section">
          <span class="label">Guests</span>
          <span class="value">{{ filters.min_capacity }} guests</span>
        </div>
        <div class="pill-action">
          <div class="search-btn">
            <i class="pi pi-sliders-h"></i>
          </div>
        </div>
      </div>

      <div class="map-toggle-pill shadow-lg" @click="viewMode = viewMode === 'grid' ? 'map' : 'grid'">
        <i :class="viewMode === 'grid' ? 'pi pi-map' : 'pi pi-th-large'"></i>
        <span>{{ viewMode === 'grid' ? 'Map' : 'Grid' }}</span>
      </div>
    </div>

    <!-- Active Filters Display -->
    <div v-if="hasActiveFilters" class="active-filters-row flex align-items-center justify-content-center gap-3 mb-6">
       <div class="filter-chip" v-if="filters.city" @click="filters.city = ''; applyFilters()">
         <span>{{ filters.city }}</span>
         <i class="pi pi-times"></i>
       </div>
       <div class="filter-chip" v-if="filters.price_range[0] > 0 || filters.price_range[1] < 1000" @click="filters.price_range = [0, 1000]; applyFilters()">
         <span>{{ priceDisplayShort }}</span>
         <i class="pi pi-times"></i>
       </div>
       <button @click="clearFilters" class="clear-all-btn">Reset All</button>
    </div>

    <!-- Main Content Area -->
    <div class="main-content-layout">
      <!-- Loading State: Premium Shimmer -->
      <div v-if="apartmentsStore.loading && apartmentsStore.apartments.length === 0" class="grid px-2">
          <div v-for="i in 8" :key="i" class="col-12 md:col-6 lg:col-4 xl:col-3 p-3">
              <div class="ax-card p-0 overflow-hidden" style="height: 100%;">
                  <Skeleton width="100%" height="240px" class="border-noround"></Skeleton>
                  <div class="p-4">
                      <Skeleton width="40%" height="0.75rem" class="mb-3"></Skeleton>
                      <Skeleton width="80%" height="1.5rem" class="mb-4"></Skeleton>
                      <Skeleton width="100%" height="3rem" class="mb-4"></Skeleton>
                      <div class="flex justify-content-between">
                        <Skeleton width="5rem" height="1rem"></Skeleton>
                        <Skeleton width="3rem" height="1rem"></Skeleton>
                      </div>
                  </div>
              </div>
          </div>
      </div>
      
      <!-- Empty State: Premium Illustration -->
      <div v-else-if="apartmentsStore.apartments.length === 0" class="empty-state-luxury py-8">
        <div class="illustration-wrapper mb-6">
             <div class="circle-bg"></div>
             <i class="pi pi-search-plus"></i>
        </div>
        <h3 class="text-4xl font-extrabold text-900 mb-2">Refine your search</h3>
        <p class="text-600 text-lg max-w-26rem mx-auto mb-6">No properties matched your specific criteria. Try adjusting your price range or exploring other destinations.</p>
        <button @click="clearFilters" class="ax-button">
          <i class="pi pi-refresh mr-2"></i>
          <span>Show All Properties</span>
        </button>
      </div>
      
      <!-- Grid: Premium Apartment Cards -->
      <div v-else-if="viewMode === 'grid'" class="grid px-2">
        <div v-for="apartment in apartmentsStore.apartments" :key="apartment.id" class="col-12 md:col-6 lg:col-4 xl:col-3 p-3">
          <ApartmentCard 
            :apartment="apartment" 
            :is-wishlisted="isApartmentWishlisted(apartment.id)"
            @toggle-wishlist="handleToggleWishlist"
          />
        </div>
      </div>

      <!-- Map View -->
      <div v-else class="map-view-container px-3 fadein animation-duration-500">
        <MapComponent 
          :markers="apartmentsStore.apartments" 
          height="700px" 
          @marker-click="(apt) => router.push(`/apartments/${apt.id}`)"
        />
      </div>
    </div>

    <!-- Filter Sidebar: Premium Modern Drawer -->
    <Sidebar v-model:visible="showFilters" position="right" class="ax-sidebar-premium" style="width: 480px; max-width: 100vw;">
      <template #header>
        <div class="flex flex-column gap-1 text-left">
          <h2 class="text-3xl font-extrabold text-900 m-0">Filters</h2>
          <p class="text-500 font-medium">Fine-tune your curated experience</p>
        </div>
      </template>

      <div class="sidebar-body p-4">
        <!-- Section: Destination -->
        <div class="sidebar-section mb-6">
          <label class="ax-label mb-3">Target Destination</label>
          <div class="ax-input-wrapper">
            <i class="pi pi-map-marker ax-input-icon"></i>
            <InputText v-model="filters.city" placeholder="Where would you like to stay?" class="ax-input icon-padding" />
          </div>
        </div>

        <!-- Section: Price -->
        <div class="sidebar-section mb-6">
          <div class="flex justify-content-between align-items-end mb-4">
             <label class="ax-label m-0">Price per night</label>
             <span class="text-900 font-extrabold text-lg">{{ priceDisplayShort }}</span>
          </div>
          <div class="px-2">
            <Slider v-model="filters.price_range" :range="true" :min="0" :max="1000" :step="10" />
            <div class="flex justify-content-between mt-4 text-xs font-bold text-500 uppercase tracking-widest">
              <span>$0</span>
              <span>$1,000+</span>
            </div>
          </div>
        </div>

        <!-- Section: Capacity -->
        <div class="sidebar-section mb-6">
          <label class="ax-label mb-4">Space & Occupancy</label>
          
          <div class="flex justify-content-between align-items-center mb-4 p-3 bg-slate-50 border-round-xl border-1 border-100">
            <div>
              <span class="block font-bold text-900">Minimum Guests</span>
              <span class="text-xs text-500 font-medium">Total capacity required</span>
            </div>
            <InputNumber v-model="filters.min_capacity" showButtons buttonLayout="horizontal" :min="1" 
              inputClass="text-center w-3rem border-none bg-transparent font-bold" class="capacity-stepper"
              incrementButtonClass="p-button-text p-button-secondary" decrementButtonClass="p-button-text p-button-secondary"
              incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus" />
          </div>

          <div class="flex justify-content-between align-items-center p-3 bg-slate-50 border-round-xl border-1 border-100">
            <div>
              <span class="block font-bold text-900">Bedrooms</span>
              <span class="text-xs text-500 font-medium">Private sleeping quarters</span>
            </div>
            <InputNumber v-model="filters.min_bedrooms" showButtons buttonLayout="horizontal" :min="0" 
              inputClass="text-center w-3rem border-none bg-transparent font-bold" class="capacity-stepper"
              incrementButtonClass="p-button-text p-button-secondary" decrementButtonClass="p-button-text p-button-secondary"
              incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus" />
          </div>
        </div>

        <!-- Section: Amenities -->
        <div class="sidebar-section">
           <label class="ax-label mb-4">Core Amenities</label>
           <div class="grid">
             <div v-for="amenity in commonAmenities" :key="amenity" class="col-6 mb-3">
               <div class="flex align-items-center gap-3">
                 <Checkbox v-model="filters.amenities" :inputId="amenity" name="amenity" :value="amenity" />
                 <label :for="amenity" class="font-bold text-700 text-sm cursor-pointer">{{ amenity }}</label>
               </div>
             </div>
           </div>
        </div>
      </div>

      <template #footer>
        <div class="flex gap-3 p-4 border-top-1 border-100">
          <button @click="clearFilters" class="p-button p-button-text p-button-secondary flex-1 font-bold">Reset</button>
          <button
            @click="applyFilters"
            class="ax-button flex-2"
          >
            <span>{{ pendingCountLabel }}</span>
            <i class="pi pi-arrow-right ml-2 text-xs"></i>
          </button>
        </div>
      </template>
    </Sidebar>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import { useWishlistStore } from '@/stores/wishlist';
import ApartmentCard from '@/components/ApartmentCard.vue';
import MapComponent from '@/components/MapComponent.vue';

// PrimeVue components
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

const applyFilters = async () => {
  const [min, max] = filters.value.price_range;
  const params = {
    city: filters.value.city,
    min_price: min,
    max_price: max === 1000 ? 999999 : max,
    capacity: filters.value.min_capacity,
    bedrooms: filters.value.min_bedrooms,
    amenities: filters.value.amenities.length > 0 ? filters.value.amenities : undefined
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
.ax-apartments-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 4rem 2rem;
  text-align: center;
}

.hero-header { max-width: 48rem; margin: 0 auto 5rem auto; }

/* The Search Pill - Premium Floating Style */
.search-pill-container {
  position: sticky;
  top: 1.5rem;
  z-index: 1000;
  margin-bottom: 4rem;
}

.search-pill {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(12px);
  border: 1px solid var(--surface-100);
  border-radius: 999px;
  display: flex;
  align-items: center;
  padding: 0.5rem;
  cursor: pointer;
  transition: var(--transition);
  max-width: 100%;
}

.search-pill:hover {
  transform: translateY(-2px);
  background: #fff;
  border-color: var(--surface-200);
}

.pill-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0.5rem 1.75rem;
  text-align: left;
}

.pill-section .label {
  font-size: 0.625rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.075em;
  color: var(--surface-400);
  margin-bottom: 0.125rem;
}

.pill-section .value {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--surface-900);
}

.pill-action { padding: 0.25rem; }

.search-btn {
  width: 2.75rem;
  height: 2.75rem;
  background: var(--surface-900);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  transition: var(--transition);
}

.search-pill:hover .search-btn { background: #000; }

/* Active Filter Chips */
.filter-chip {
  background: var(--surface-900);
  color: #fff;
  padding: 0.5rem 1rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: var(--transition);
}

.filter-chip:hover { opacity: 0.9; transform: scale(0.95); }

.clear-all-btn {
  background: transparent;
  border: none;
  font-size: 0.75rem;
  font-weight: 800;
  color: var(--surface-400);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
}

.clear-all-btn:hover { color: var(--surface-900); }

/* Empty State */
.empty-state-luxury {
  background: var(--surface-0);
  border-radius: 2rem;
  padding: 5rem 2rem;
  border: 1px solid var(--surface-100);
  box-shadow: var(--shadow-sm);
}

.illustration-wrapper {
  position: relative;
  width: 8rem;
  height: 8rem;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.circle-bg {
  position: absolute;
  width: 100%; height: 100%;
  background: var(--primary-50);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.illustration-wrapper i {
  position: relative;
  font-size: 3rem;
  color: var(--primary-500);
}

@keyframes pulse {
  0% { transform: scale(0.95); opacity: 0.5; }
  50% { transform: scale(1.05); opacity: 0.8; }
  100% { transform: scale(0.95); opacity: 0.5; }
}

/* Sidebar Styling */
:deep(.ax-sidebar-premium) {
  border-top-left-radius: 2rem;
  border-bottom-left-radius: 2rem;
}

.ax-input-wrapper { position: relative; display: flex; align-items: center; }
.ax-input-icon { position: absolute; left: 1rem; color: var(--surface-400); pointer-events: none; z-index: 2; }
.icon-padding { padding-left: 3rem !important; }

.capacity-stepper :deep(.p-inputtext) { border: none !important; box-shadow: none !important; }

@media (max-width: 768px) {
  .ax-apartments-view { padding: 2rem 1rem; }
  .search-pill { border-radius: 1.5rem; flex-wrap: wrap; }
  .pill-section { flex: 1; border: none !important; min-width: 50%; padding: 0.75rem 1rem; }
  .pill-action { width: 100%; padding: 0.5rem; }
  .search-btn { width: 100%; border-radius: 0.75rem; }
}

.map-toggle-pill {
  background: var(--surface-900);
  color: #fff;
  border-radius: 999px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0 1.5rem;
  cursor: pointer;
  transition: var(--transition);
  font-weight: 700;
  font-size: 0.875rem;
}

.map-toggle-pill:hover {
  background: #000;
  transform: translateY(-2px);
}

.map-view-container {
  border-radius: 2rem;
  overflow: hidden;
  border: 1px solid var(--surface-100);
  box-shadow: var(--shadow-lg);
  margin-top: 2rem;
}
</style>
