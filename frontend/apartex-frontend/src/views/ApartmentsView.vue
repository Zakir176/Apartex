<template>
  <div class="min-h-screen bg-slate-50 py-6 px-3 sm:px-6 lg:px-8">
    <div class="max-w-[1400px] mx-auto">
      
      <!-- HEADER SECTION -->
      <div class="flex flex-col lg:flex-row lg:items-center justify-between mb-8 gap-4">
        <div>
          <div class="flex items-center gap-2 mb-2">
            <span class="text-xs font-semibold text-accent uppercase tracking-widest bg-accent-light px-3 py-1 rounded-md border border-accent/20">
              <i class="pi pi-compass text-[10px] mr-1"></i> Stay Directory & Interactive Map
            </span>
          </div>
          <h1 class="text-3xl sm:text-4xl font-bold text-slate-900 tracking-tight">Explore Stays</h1>
          <p class="text-slate-500 font-medium text-xs sm:text-sm mt-1">Handpicked luxury apartments, villas, and boutique stays across Zambia.</p>
        </div>

        <!-- View Mode Switcher -->
        <div class="flex items-center gap-2 bg-white p-1.5 rounded-lg border border-slate-200 shadow-sm self-start lg:self-center">
          <button
            @click="viewMode = 'grid'"
            class="px-4 py-2 rounded-md text-xs font-semibold transition-all duration-200 flex items-center gap-2 cursor-pointer border-0"
            :class="viewMode === 'grid' ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 bg-transparent'"
          >
            <i class="pi pi-th-large text-xs"></i>
            <span>Grid View</span>
          </button>
          <button
            @click="viewMode = 'split'"
            class="px-4 py-2 rounded-md text-xs font-semibold transition-all duration-200 flex items-center gap-2 cursor-pointer border-0"
            :class="viewMode === 'split' ? 'bg-slate-900 text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 bg-transparent'"
          >
            <i class="pi pi-map text-xs"></i>
            <span>Split Map</span>
          </button>
        </div>
      </div>

      <!-- DYNAMIC STATS STRIP (Matching Owner Portfolio Framing) -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div class="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/80 shadow-xs">
          <span class="block text-slate-400 text-[10px] sm:text-xs font-semibold uppercase tracking-wider mb-1">Available Stays</span>
          <span class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">{{ filteredApartments.length }}</span>
          <p class="text-[11px] text-slate-500 font-medium mt-0.5">Matching active criteria</p>
        </div>

        <div class="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/80 shadow-xs">
          <span class="block text-slate-400 text-[10px] sm:text-xs font-semibold uppercase tracking-wider mb-1">Avg Nightly Rate</span>
          <span class="text-2xl sm:text-3xl font-bold text-accent tracking-tight">${{ averagePrice }}</span>
          <p class="text-[11px] text-slate-500 font-medium mt-0.5">Across listed properties</p>
        </div>

        <div class="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/80 shadow-xs">
          <span class="block text-slate-400 text-[10px] sm:text-xs font-semibold uppercase tracking-wider mb-1">Regions & Cities</span>
          <span class="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">{{ uniqueCitiesCount }} <span class="text-xs font-normal text-slate-400">Cities</span></span>
          <p class="text-[11px] text-slate-500 font-medium mt-0.5">Prime Zambian hubs</p>
        </div>

        <div class="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200/80 shadow-xs">
          <span class="block text-slate-400 text-[10px] sm:text-xs font-semibold uppercase tracking-wider mb-1">Guaranteed Quality</span>
          <span class="text-2xl sm:text-3xl font-bold text-accent tracking-tight">100%</span>
          <p class="text-[11px] text-accent font-bold mt-0.5">Verified & Direct Booking</p>
        </div>
      </div>

      <!-- UNIFIED SEARCH & CONTROL BAR -->
      <div class="bg-white rounded-2xl border border-slate-200/90 p-3 sm:p-4 mb-6 shadow-sm flex flex-col lg:flex-row items-center justify-between gap-3">
        <!-- Search input -->
        <div class="relative w-full lg:w-80">
          <i class="pi pi-search absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search stays, location or keyword..."
            class="input-base !pl-10 !py-2.5 !text-xs w-full bg-slate-50/70 hover:bg-white focus:bg-white"
          />
          <button 
            v-if="searchQuery" 
            @click="searchQuery = ''" 
            class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 border-0 bg-transparent cursor-pointer text-xs"
          >
            <i class="pi pi-times-circle"></i>
          </button>
        </div>

        <!-- Filter Controls Group -->
        <div class="flex items-center gap-2 w-full lg:w-auto overflow-x-auto scrollbar-hide pb-1 lg:pb-0">
          <!-- City Quick Filter Dropdown -->
          <select 
            v-model="filters.city" 
            @change="onCitySelectChange" 
            class="input-base !py-2.5 !text-xs w-auto min-w-[140px] cursor-pointer bg-slate-50 hover:bg-white font-bold text-slate-700"
          >
            <option value="">All Locations</option>
            <option v-for="city in ['Lusaka', 'Livingstone', 'Ndola', 'Kitwe', 'Solwezi']" :key="city" :value="city">
              {{ city }}
            </option>
          </select>

          <!-- Property Type Dropdown -->
          <select 
            v-model="filters.property_type" 
            @change="applyFilters" 
            class="input-base !py-2.5 !text-xs w-auto min-w-[130px] cursor-pointer bg-slate-50 hover:bg-white font-bold text-slate-700"
          >
            <option value="">All Property Types</option>
            <option v-for="t in propertyTypes" :key="t.value" :value="t.value">{{ t.label }}</option>
          </select>

          <!-- Price & More Filters Drawer Toggle Button -->
          <button
            @click="showFiltersModal = true"
            class="px-4 py-2.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-white text-xs font-semibold text-slate-700 flex items-center gap-2 whitespace-nowrap cursor-pointer transition-colors shadow-2xs"
          >
            <i class="pi pi-sliders-h text-accent text-xs"></i>
            <span>Price & Filters</span>
            <span v-if="activeFilterCount > 0" class="w-4 h-4 rounded-md bg-accent text-white text-[10px] font-semibold flex items-center justify-center">
              {{ activeFilterCount }}
            </span>
          </button>

          <!-- Reset Filters Button -->
          <button
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="px-3 py-2.5 rounded-xl text-xs font-bold text-rose-600 hover:bg-rose-50 border border-transparent transition-colors whitespace-nowrap cursor-pointer"
            title="Reset Filters"
          >
            <i class="pi pi-refresh text-xs mr-1"></i> Reset
          </button>
        </div>
      </div>

      <!-- MAIN CONTENT AREA: GRID VS SPLIT MAP VIEW -->
      
      <!-- LOADING STATE -->
      <div v-if="apartmentsStore.loading && apartmentsStore.apartments.length === 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="i in 6" :key="i" class="bg-white border border-slate-200 rounded-2xl p-4 flex flex-col gap-4">
          <div class="h-[200px] rounded-xl bg-slate-200 animate-pulse"></div>
          <div class="h-5 rounded bg-slate-200 animate-pulse w-3/5"></div>
          <div class="h-10 rounded bg-slate-200 animate-pulse w-full"></div>
        </div>
      </div>

      <!-- EMPTY STATE -->
      <div v-else-if="filteredApartments.length === 0" class="bg-white border border-slate-200 rounded-3xl p-8 sm:p-14 text-center max-w-md mx-auto my-8 sm:my-12 shadow-sm">
        <div class="w-16 h-16 rounded-full bg-accent-light text-accent flex items-center justify-center text-2xl mx-auto mb-4 border border-accent/20">
          <i class="pi pi-search"></i>
        </div>
        <h2 class="text-xl font-semibold text-slate-900 mb-2">No Stays Match Criteria</h2>
        <p class="text-xs text-slate-500 mb-6 font-medium leading-relaxed">We couldn't find any stays matching your selected search query and filters.</p>
        <button class="btn-accent px-6 py-3 rounded-lg text-xs font-semibold" @click="clearFilters">Reset All Filters</button>
      </div>

      <!-- VIEW MODE 1: STANDARD GRID VIEW -->
      <div v-else-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(apartment, index) in filteredApartments"
          :key="apartment.id"
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: index * 60, duration: 350 } }"
        >
          <ApartmentCard
            :apartment="apartment"
            :is-wishlisted="isApartmentWishlisted(apartment.id)"
            :isSelected="selectedApartmentId === apartment.id"
            @toggle-wishlist="handleToggleWishlist"
            @card-hover="(id) => selectedApartmentId = id"
            @card-leave="() => selectedApartmentId = null"
          />
        </div>
      </div>

      <!-- VIEW MODE 2: SPLIT MAP VIEW -->
      <div v-else class="flex flex-col lg:flex-row gap-6 items-start">
        <!-- Left Side: Listings Column -->
        <div class="w-full lg:w-7/12 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            v-for="(apartment, index) in filteredApartments"
            :key="apartment.id"
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: index * 50, duration: 300 } }"
          >
            <ApartmentCard
              :apartment="apartment"
              :is-wishlisted="isApartmentWishlisted(apartment.id)"
              :isSelected="selectedApartmentId === apartment.id"
              @toggle-wishlist="handleToggleWishlist"
              @card-hover="(id) => selectedApartmentId = id"
              @card-leave="() => selectedApartmentId = null"
            />
          </div>
        </div>

        <!-- Right Side: Sticky Interactive Map -->
        <div class="w-full lg:w-5/12 sticky top-24 h-[calc(100vh-120px)] rounded-3xl overflow-hidden border border-slate-200 shadow-md">
          <MapComponent
            :city="filters.city || 'Lusaka'"
            :markers="mapMarkers"
            :selectedId="selectedApartmentId"
            height="100%"
            @marker-hover="(id) => selectedApartmentId = id"
            @marker-leave="() => selectedApartmentId = null"
            @marker-click="handleMapMarkerClick"
          />
        </div>
      </div>

    </div>

    <!-- FILTER & PRICE DRAWER MODAL -->
    <Dialog
      v-model:visible="showFiltersModal"
      header="Filter Stays & Amenities"
      :modal="true"
      :style="{ width: '500px', maxWidth: '95vw' }"
    >
      <div class="flex flex-col gap-6 py-3">
        <!-- Price Range Slider -->
        <div>
          <div class="flex justify-between items-center mb-2">
            <label class="text-xs font-semibold uppercase text-slate-800 tracking-wider">Max Price Per Night</label>
            <span class="text-sm font-semibold text-accent">${{ filters.price_range[1] }} / nt</span>
          </div>
          <input
            type="range"
            min="20"
            max="1000"
            step="10"
            v-model.number="filters.price_range[1]"
            class="w-full accent-accent cursor-pointer"
          />
          <div class="flex justify-between text-[10px] font-bold text-slate-400 mt-1">
            <span>$20</span>
            <span>$500</span>
            <span>$1,000+</span>
          </div>
        </div>

        <!-- Guest Capacity -->
        <div>
          <label class="text-xs font-semibold uppercase text-slate-800 tracking-wider mb-2 block">Min Capacity (Guests)</label>
          <div class="flex gap-2">
            <button
              v-for="cap in [1, 2, 4, 6, 8]"
              :key="cap"
              @click="filters.min_capacity = cap"
              class="flex-1 py-2 rounded-xl text-xs font-bold border cursor-pointer transition-all"
              :class="filters.min_capacity === cap ? 'bg-slate-900 text-white border-slate-900 font-semibold' : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'"
            >
              {{ cap }}+
            </button>
          </div>
        </div>

        <!-- Bedrooms -->
        <div>
          <label class="text-xs font-semibold uppercase text-slate-800 tracking-wider mb-2 block">Min Bedrooms</label>
          <div class="flex gap-2">
            <button
              v-for="bed in [0, 1, 2, 3, 4]"
              :key="bed"
              @click="filters.min_bedrooms = bed"
              class="flex-1 py-2 rounded-xl text-xs font-bold border cursor-pointer transition-all"
              :class="filters.min_bedrooms === bed ? 'bg-slate-900 text-white border-slate-900 font-semibold' : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'"
            >
              {{ bed === 0 ? 'Any' : bed + '+' }}
            </button>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex items-center justify-between gap-3 pt-3 border-t border-slate-100">
          <button
            @click="clearFilters"
            class="px-4 py-2.5 rounded-lg text-xs font-bold text-slate-500 hover:text-slate-900 border-0 bg-transparent cursor-pointer"
          >
            Clear Filters
          </button>
          <button
            @click="applyFilters"
            class="btn-accent px-6 py-2.5 rounded-lg text-xs font-semibold"
          >
            Apply Filters ({{ filteredApartments.length }})
          </button>
        </div>
      </template>
    </Dialog>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import { useWishlistStore } from '@/stores/wishlist';
import { useAuthStore } from '@/stores/auth';
import ApartmentCard from '@/components/ApartmentCard.vue';
import MapComponent from '@/components/MapComponent.vue';
import Dialog from 'primevue/dialog';

const route = useRoute();
const router = useRouter();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();
const authStore = useAuthStore();

const showFiltersModal = ref(false);
const viewMode = ref('grid');
const selectedApartmentId = ref(null);
const searchQuery = ref('');

const propertyTypes = [
  { value: 'apartment', label: 'Apartments', icon: 'pi pi-building' },
  { value: 'hotel', label: 'Hotels', icon: 'pi pi-star' },
  { value: 'lodge', label: 'Lodges', icon: 'pi pi-home' },
  { value: 'guest_house', label: 'Guest Houses', icon: 'pi pi-heart' },
];

const filters = ref({
  city: route.query.city || '',
  property_type: route.query.property_type || '',
  price_range: [0, 1000],
  min_capacity: 1,
  min_bedrooms: 0,
  amenities: []
});

// Coordinate mapping for city center defaults with offsets
const cityCoordinates = {
  'Lusaka': [-15.3875, 28.3228],
  'Livingstone': [-16.8561, 25.8528],
  'Ndola': [-12.9686, 28.6366],
  'Kitwe': [-12.8167, 28.2000],
  'Solwezi': [-12.1833, 26.4000]
};

// Filtered apartments taking search query into account
const filteredApartments = computed(() => {
  return apartmentsStore.apartments.filter(apt => {
    const query = searchQuery.value.toLowerCase().trim();
    if (query) {
      const matchTitle = apt.title?.toLowerCase().includes(query);
      const matchCity = apt.city?.toLowerCase().includes(query);
      const matchDesc = apt.description?.toLowerCase().includes(query);
      if (!matchTitle && !matchCity && !matchDesc) return false;
    }

    const [min, max] = filters.value.price_range;
    const cityOk = !filters.value.city || apt.city.toLowerCase().includes(filters.value.city.toLowerCase());
    const typeOk = !filters.value.property_type || apt.property_type === filters.value.property_type;
    const priceOk = apt.price_per_night >= min && (max === 1000 || apt.price_per_night <= max);
    const capacityOk = (apt.capacity || 1) >= filters.value.min_capacity;
    const bedroomsOk = (apt.bedrooms || 0) >= filters.value.min_bedrooms;

    return cityOk && typeOk && priceOk && capacityOk && bedroomsOk;
  });
});

const averagePrice = computed(() => {
  if (filteredApartments.value.length === 0) return 0;
  const sum = filteredApartments.value.reduce((acc, a) => acc + Number(a.price_per_night || 0), 0);
  return Math.round(sum / filteredApartments.value.length);
});

const uniqueCitiesCount = computed(() => {
  const cities = new Set(filteredApartments.value.map(a => a.city || 'Lusaka'));
  return cities.size || 1;
});

const activeFilterCount = computed(() => {
  let count = 0;
  if (filters.value.price_range[1] < 1000) count++;
  if (filters.value.min_capacity > 1) count++;
  if (filters.value.min_bedrooms > 0) count++;
  if (filters.value.property_type) count++;
  return count;
});

const hasActiveFilters = computed(() => {
  return !!filters.value.city || !!filters.value.property_type || searchQuery.value !== '' || activeFilterCount.value > 0;
});

const mapMarkers = computed(() => {
  return filteredApartments.value.map((apt, idx) => {
    let lat = apt.latitude;
    let lng = apt.longitude;

    if (!lat || !lng) {
      const base = cityCoordinates[apt.city] || cityCoordinates['Lusaka'];
      // Generate deterministic slight offset based on ID so markers don't stack directly
      const offsetLat = ((idx % 5) - 2) * 0.008;
      const offsetLng = (((idx * 3) % 5) - 2) * 0.008;
      lat = base[0] + offsetLat;
      lng = base[1] + offsetLng;
    }

    return {
      id: apt.id,
      position: [lat, lng],
      title: apt.title,
      price: apt.price_per_night,
      raw: apt
    };
  });
});

const isApartmentWishlisted = computed(() => (apartmentId) => {
  return wishlistStore.wishlistItems.some(item => item.apartment_id === apartmentId);
});

const onCitySelectChange = async () => {
  router.replace({ query: { ...route.query, city: filters.value.city || undefined } });
  await applyFilters();
};

const applyFilters = async () => {
  const [min, max] = filters.value.price_range;
  const params = {
    city: filters.value.city || undefined,
    property_type: filters.value.property_type || undefined,
    min_price: min,
    max_price: max === 1000 ? 999999 : max,
    capacity: filters.value.min_capacity,
    bedrooms: filters.value.min_bedrooms
  };
  
  await apartmentsStore.fetchApartments(params);
  showFiltersModal.value = false;
};

const clearFilters = async () => {
  filters.value = {
    city: '',
    property_type: '',
    price_range: [0, 1000],
    min_capacity: 1,
    min_bedrooms: 0,
    amenities: []
  };
  searchQuery.value = '';
  router.replace({ query: {} });
  await applyFilters();
  showFiltersModal.value = false;
};

const handleMapMarkerClick = (apt) => {
  if (apt && apt.id) {
    router.push({ name: 'ApartmentDetail', params: { id: apt.id } });
  }
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

