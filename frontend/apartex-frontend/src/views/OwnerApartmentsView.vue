<template>
  <div class="max-w-[1250px] mx-auto px-4 sm:px-6 py-8 text-slate-800">
    <!-- Header Section -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
      <div>
        <span class="text-xs font-black uppercase tracking-wider text-accent mb-1 block">Property Portfolio</span>
        <h1 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">Manage Listings</h1>
        <p class="text-slate-500 font-medium text-sm sm:text-base mt-1">Create, edit, and optimize your luxury apartments and villas across Zambia.</p>
      </div>

      <button @click="openCreateModal" class="btn-accent shadow-accent font-black text-xs px-6 py-3 rounded-full inline-flex items-center gap-2">
        <i class="pi pi-plus-circle text-sm"></i>
        <span>Publish New Property</span>
      </button>
    </div>

    <!-- Dynamic Portfolio Stats Strip -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm">
        <span class="block text-slate-400 text-xs font-black uppercase mb-2 tracking-wider">Total Properties</span>
        <span class="text-3xl font-black text-slate-900 tracking-tight">{{ apartmentsStore.apartments.length }}</span>
        <p class="text-xs text-slate-500 font-medium mt-1">Active on Apartex network</p>
      </div>

      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm">
        <span class="block text-slate-400 text-xs font-black uppercase mb-2 tracking-wider">Avg Nightly Rate</span>
        <span class="text-3xl font-black text-accent tracking-tight">K {{ averageNightlyRate?.toLocaleString() }}</span>
        <p class="text-xs text-slate-500 font-medium mt-1">Across all active listings</p>
      </div>

      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm">
        <span class="block text-slate-400 text-xs font-black uppercase mb-2 tracking-wider">Total Bed Capacity</span>
        <span class="text-3xl font-black text-slate-900 tracking-tight">{{ totalBedCapacity }} <span class="text-xs font-normal text-slate-400">Beds</span></span>
        <p class="text-xs text-slate-500 font-medium mt-1">Guest accommodation space</p>
      </div>

      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm">
        <span class="block text-slate-400 text-xs font-black uppercase mb-2 tracking-wider">Portfolio Health</span>
        <span class="text-3xl font-black text-emerald-600 tracking-tight">100%</span>
        <p class="text-xs text-emerald-600 font-bold mt-1">Verified & Published</p>
      </div>
    </div>

    <!-- Search & Filter Controls -->
    <div class="bg-white rounded-2xl border border-surface-border p-4 mb-8 flex flex-col sm:flex-row items-center justify-between gap-4 shadow-sm">
      <div class="relative w-full sm:w-80">
        <i class="pi pi-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search listing title or address..." 
          class="input-base !pl-9 !py-2 !text-xs w-full"
        />
      </div>

      <div class="flex items-center gap-3 w-full sm:w-auto justify-end">
        <select v-model="selectedCity" class="input-base !py-2 !text-xs w-full sm:w-44 cursor-pointer">
          <option value="">All Regions / Cities</option>
          <option value="Lusaka">Lusaka</option>
          <option value="Livingstone">Livingstone</option>
          <option value="Ndola">Ndola</option>
          <option value="Kitwe">Kitwe</option>
        </select>
      </div>
    </div>

    <!-- Listings Grid -->
    <div v-if="filteredApartments.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="apt in filteredApartments" 
        :key="apt.id" 
        class="bg-white rounded-3xl border border-surface-border overflow-hidden flex flex-col group shadow-sm hover:shadow-md transition-all"
      >
        <div class="relative w-full h-56 overflow-hidden bg-slate-100">
          <img 
            :src="resolveImageUrl(apt.image_url)" 
            :alt="apt.title" 
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
          />
          <div class="absolute top-3 right-3 px-3 py-1 bg-slate-900/90 backdrop-blur-md text-white rounded-full font-black text-xs shadow-md">
            K {{ apt.price_per_night?.toLocaleString() }}<span class="font-medium text-white/70 text-[10px] ml-0.5">/ nt</span>
          </div>

          <div class="absolute top-3 left-3 px-2.5 py-1 bg-emerald-500/90 backdrop-blur-md text-white rounded-full font-black text-[10px] uppercase tracking-wider shadow-sm flex items-center gap-1">
            <i class="pi pi-check-circle text-[10px]"></i> Published
          </div>
        </div>
        
        <div class="p-6 flex-grow flex flex-col">
          <div class="flex items-center gap-1 text-accent text-[10px] font-black uppercase tracking-widest mb-2">
            <i class="pi pi-map-marker text-[10px]"></i>
            {{ apt.city || 'Lusaka' }}
          </div>

          <h3 class="text-lg font-black text-slate-900 mb-3 line-clamp-1" :title="apt.title">{{ apt.title }}</h3>
          
          <p class="text-xs text-slate-500 line-clamp-2 mb-4 font-medium leading-relaxed">
            {{ apt.description || 'Luxury accommodation equipped with high-speed internet, air conditioning, and 24/7 security.' }}
          </p>

          <div class="flex gap-2 mb-6">
            <span class="px-2.5 py-1 bg-slate-100 rounded-md text-[10px] font-black text-slate-600 uppercase tracking-wider">
              {{ apt.capacity || 2 }} Guests
            </span>
            <span class="px-2.5 py-1 bg-slate-100 rounded-md text-[10px] font-black text-slate-600 uppercase tracking-wider">
              {{ apt.bedrooms || 1 }} BR
            </span>
            <span class="px-2.5 py-1 bg-slate-100 rounded-md text-[10px] font-black text-slate-600 uppercase tracking-wider">
              {{ apt.bathrooms || 1 }} Bath
            </span>
          </div>

          <div class="flex gap-2 pt-4 border-t border-surface-border mt-auto">
            <button @click="startEdit(apt)" class="flex-1 px-3 py-2 rounded-xl text-xs font-bold text-slate-700 hover:bg-slate-100 transition-colors inline-flex items-center justify-center gap-1.5">
              <i class="pi pi-pencil text-xs"></i> Edit
            </button>
            <button @click="openAvailability(apt)" class="flex-1 px-3 py-2 rounded-xl text-xs font-bold text-accent hover:bg-accent-light transition-colors inline-flex items-center justify-center gap-1.5">
              <i class="pi pi-calendar text-xs"></i> Dates
            </button>
            <button @click="confirmDelete($event, apt.id)" class="px-3 py-2 rounded-xl text-xs font-bold text-rose-600 hover:bg-rose-50 transition-colors inline-flex items-center justify-center">
              <i class="pi pi-trash text-xs"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-white rounded-3xl border border-surface-border p-16 flex flex-col items-center justify-center text-center shadow-sm">
      <div class="w-16 h-16 rounded-2xl bg-accent-light text-accent flex items-center justify-center mb-4">
        <i class="pi pi-building text-3xl"></i>
      </div>
      <h2 class="text-xl font-black text-slate-900 mb-2">No listings found matching criteria</h2>
      <p class="text-slate-500 text-xs font-medium mb-6 max-w-md">Try clearing search filters or create a new property listing to start receiving reservations.</p>
      <button @click="openCreateModal" class="btn-accent text-xs font-black px-6 py-2.5 rounded-full inline-flex items-center gap-2">
        <i class="pi pi-plus text-xs"></i> Create New Listing
      </button>
    </div>

    <!-- Create / Edit Property Dialog Studio Wizard -->
    <Dialog 
      v-model:visible="showModal" 
      :header="editingId ? 'Edit Property Listing' : 'Publish New Luxury Property'"
      :modal="true" 
      :style="{ width: '640px', maxWidth: '95vw' }"
      contentClass="pt-2"
    >
      <div class="flex flex-col gap-5 py-4">
        <div>
          <label class="label-base">Property Title</label>
          <input v-model="form.title" class="input-base" placeholder="e.g. Rhodes Park Luxury Penthouse" />
        </div>

        <div>
          <label class="label-base">Street Address / Location</label>
          <input v-model="form.address" class="input-base" placeholder="e.g. 14 Birdcage Walk, Kabulonga" />
        </div>

        <div>
          <label class="label-base">Description & Guest Experience</label>
          <textarea v-model="form.description" class="input-base resize-none" rows="3" placeholder="Describe ambiance, location highlights, security, and amenities..."></textarea>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label-base">Nightly Price (K ZMW)</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-sm font-semibold text-gray-500">K</span>
              <input
                v-model.number="form.price_per_night"
                type="number"
                min="1"
                step="50"
                class="input-base pl-8"
                placeholder="e.g. 500"
              />
            </div>
            <p class="text-xs text-gray-400 mt-1">Enter price in Zambian Kwacha (ZMW). Guests can view in their preferred currency.</p>
          </div>

          <div>
            <label class="label-base">City / Region</label>
            <select v-model="form.city" class="input-base cursor-pointer">
              <option value="Lusaka">Lusaka</option>
              <option value="Livingstone">Livingstone</option>
              <option value="Ndola">Ndola</option>
              <option value="Kitwe">Kitwe</option>
            </select>
          </div>
        </div>

        <!-- Location Pin -->
        <div class="flex flex-col gap-2">
          <label class="label-base">Pin Location on Map</label>
          <p class="text-xs text-gray-400 -mt-1">Click the map to drop a pin on your property's exact location. Guests will see this on the listing.</p>
          <LocationPicker
            v-model:lat="form.latitude"
            v-model:lng="form.longitude"
            :address="form.address"
            :city="form.city"
          />
        </div>

        <!-- Amenities -->
        <div class="flex flex-col gap-3">
          <label class="label-base">Amenities & Facilities</label>
          <p class="text-xs text-gray-400 -mt-1">Select all that apply. These will show with icons on your listing.</p>

          <!-- Predefined grid -->
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
            <button
              v-for="amenity in PREDEFINED_AMENITIES"
              :key="amenity.label"
              type="button"
              @click="toggleAmenity(amenity.label)"
              class="flex items-center gap-2 px-3 py-2.5 rounded-lg border text-xs font-medium transition-all duration-150 text-left cursor-pointer"
              :class="selectedAmenities.includes(amenity.label)
                ? 'bg-accent text-white border-accent'
                : 'bg-white text-gray-600 border-surface-border hover:border-accent/40'"
            >
              <i :class="amenity.icon" class="text-xs shrink-0"></i>
              <span class="truncate">{{ amenity.label }}</span>
            </button>
          </div>

          <!-- Custom amenity -->
          <div class="flex gap-2 mt-1">
            <input
              v-model="customAmenity"
              class="input-base flex-1"
              placeholder="Add custom amenity (e.g. River View, Private Chef)"
              @keydown.enter.prevent="addCustomAmenity"
            />
            <button
              type="button"
              @click="addCustomAmenity"
              class="btn-accent px-4 shrink-0 border-0 cursor-pointer"
            >
              <i class="pi pi-plus text-xs"></i>
            </button>
          </div>

          <!-- Selected summary -->
          <div v-if="selectedAmenities.length > 0" class="flex flex-wrap gap-1.5">
            <span
              v-for="a in selectedAmenities"
              :key="a"
              class="flex items-center gap-1 text-xs font-medium bg-accent-light text-accent px-2.5 py-1 rounded-md"
            >
              {{ a }}
              <button type="button" @click="toggleAmenity(a)" class="ml-1 text-accent/60 hover:text-accent border-0 bg-transparent cursor-pointer p-0">×</button>
            </span>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-4">
          <div>
            <label class="label-base">Max Guests</label>
            <InputNumber v-model="form.capacity" :min="1" inputClass="input-base !w-full" class="w-full" />
          </div>
          <div>
            <label class="label-base">Bedrooms</label>
            <InputNumber v-model="form.bedrooms" :min="1" inputClass="input-base !w-full" class="w-full" />
          </div>
          <div>
            <label class="label-base">Bathrooms</label>
            <InputNumber v-model="form.bathrooms" :min="1" inputClass="input-base !w-full" class="w-full" />
          </div>
        </div>

        <!-- Property Image Upload & URL Selection Component -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="label-base !mb-0">Property Cover Photo</label>
            
            <!-- Upload Mode Switcher -->
            <div class="flex items-center gap-1 bg-slate-100 p-0.5 rounded-lg text-[10px] font-bold">
              <button 
                type="button"
                @click="uploadMode = 'file'" 
                class="px-2.5 py-1 rounded-md transition-all border-none cursor-pointer"
                :class="uploadMode === 'file' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 bg-transparent'"
              >
                <i class="pi pi-upload text-[9px] mr-1"></i> Upload File
              </button>
              <button 
                type="button"
                @click="uploadMode = 'url'" 
                class="px-2.5 py-1 rounded-md transition-all border-none cursor-pointer"
                :class="uploadMode === 'url' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 bg-transparent'"
              >
                <i class="pi pi-link text-[9px] mr-1"></i> URL / Preset
              </button>
            </div>
          </div>

          <!-- File Upload Dropzone Mode -->
          <div v-if="uploadMode === 'file'" class="flex flex-col gap-3">
            <div 
              @click="triggerFileInput"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleFileDrop"
              class="border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all flex flex-col items-center justify-center min-h-[140px]"
              :class="isDragging ? 'border-accent bg-accent-light' : 'border-surface-border hover:border-accent hover:bg-slate-50'"
            >
              <input 
                ref="fileInputRef" 
                type="file" 
                accept="image/*" 
                class="hidden" 
                @change="onFileSelected" 
              />
              
              <div v-if="uploading" class="flex flex-col items-center gap-2">
                <i class="pi pi-spinner pi-spin text-2xl text-accent"></i>
                <span class="text-xs font-bold text-slate-600">Uploading photo to server...</span>
              </div>

              <div v-else-if="!form.image_url" class="flex flex-col items-center gap-2">
                <div class="w-10 h-10 rounded-full bg-accent-light text-accent flex items-center justify-center">
                  <i class="pi pi-cloud-upload text-lg"></i>
                </div>
                <div>
                  <p class="text-xs font-black text-slate-800">Click to choose image or drag & drop</p>
                  <p class="text-[10px] text-slate-400 font-medium">PNG, JPG, WEBP up to 10MB</p>
                </div>
              </div>

              <div v-else class="relative w-full h-36 rounded-xl overflow-hidden group">
                <img :src="resolveImageUrl(form.image_url)" class="w-full h-full object-cover" />
                <div class="absolute inset-0 bg-slate-900/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-3">
                  <button type="button" @click.stop="triggerFileInput" class="px-3 py-1.5 bg-white text-slate-900 text-xs font-bold rounded-lg border-none">
                    Change Image
                  </button>
                  <button type="button" @click.stop="form.image_url = ''" class="px-3 py-1.5 bg-rose-600 text-white text-xs font-bold rounded-lg border-none">
                    Remove
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- URL / Preset Selection Mode -->
          <div v-else class="flex flex-col gap-3">
            <input v-model="form.image_url" class="input-base" placeholder="Paste direct photo URL (https://...)" />

            <!-- Curated Luxury Image Presets -->
            <div class="flex flex-col gap-1.5">
              <span class="text-[10px] font-black uppercase text-slate-400">Or Select a Luxury Preset Photo:</span>
              <div class="grid grid-cols-4 gap-2">
                <div 
                  v-for="(preset, i) in imagePresets" 
                  :key="i"
                  @click="form.image_url = preset.url"
                  class="relative h-14 rounded-lg overflow-hidden cursor-pointer border-2 transition-all group"
                  :class="form.image_url === preset.url ? 'border-accent shadow-sm' : 'border-transparent opacity-75 hover:opacity-100'"
                >
                  <img :src="preset.url" :alt="preset.name" class="w-full h-full object-cover" />
                  <div class="absolute inset-0 bg-slate-900/40 flex items-end p-1">
                    <span class="text-[9px] font-black text-white truncate">{{ preset.name }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <p v-if="uploadError" class="text-xs font-bold text-rose-600 mt-1 flex items-center gap-1">
            <i class="pi pi-exclamation-circle text-xs"></i> {{ uploadError }}
          </p>
        </div>

      </div>

      <template #footer>
        <div class="flex gap-3 justify-end pt-4 border-t border-surface-border">
          <button @click="showModal = false" class="px-5 py-2.5 rounded-full text-xs font-bold text-slate-500 hover:bg-slate-100 transition-colors">Cancel</button>
          <button @click="saveProperty" :disabled="saving || uploading" class="btn-accent text-xs font-black inline-flex items-center gap-2 px-6 py-2.5">
            <i class="pi pi-check" v-if="!saving"></i>
            <i class="pi pi-spinner pi-spin" v-else></i>
            <span>{{ editingId ? 'Update Listing' : 'Publish Listing' }}</span>
          </button>
        </div>
      </template>
    </Dialog>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useApartmentsStore } from '@/stores/apartments';
import { uploadImage } from '@/api/uploads';
import LocationPicker from '@/components/LocationPicker.vue';

// PrimeVue components
import Dialog from 'primevue/dialog';
import InputNumber from 'primevue/inputnumber';

const PREDEFINED_AMENITIES = [
  { label: 'WiFi', icon: 'pi pi-wifi' },
  { label: 'Air Conditioning', icon: 'pi pi-sun' },
  { label: 'Parking', icon: 'pi pi-car' },
  { label: 'Swimming Pool', icon: 'pi pi-wave-pulse' },
  { label: 'Generator / Backup Power', icon: 'pi pi-bolt' },
  { label: 'Security / CCTV', icon: 'pi pi-shield' },
  { label: 'Kitchen', icon: 'pi pi-home' },
  { label: 'Laundry', icon: 'pi pi-refresh' },
  { label: 'Restaurant / Bar', icon: 'pi pi-star' },
  { label: 'Gym', icon: 'pi pi-heart' },
  { label: 'TV / DSTV', icon: 'pi pi-desktop' },
  { label: 'Hot Water', icon: 'pi pi-droplet' },
  { label: 'Game Drives', icon: 'pi pi-map' },
  { label: 'Airport Transfer', icon: 'pi pi-send' },
  { label: 'Breakfast Included', icon: 'pi pi-clock' },
  { label: 'Ensuite Bathroom', icon: 'pi pi-home' },
  { label: 'Balcony / Veranda', icon: 'pi pi-external-link' },
  { label: 'Wheelchair Accessible', icon: 'pi pi-user' },
  { label: 'Pet Friendly', icon: 'pi pi-heart-fill' },
  { label: 'Conference Room', icon: 'pi pi-users' },
];

const selectedAmenities = ref([]);
const customAmenity = ref('');

function toggleAmenity(label) {
  const idx = selectedAmenities.value.indexOf(label);
  if (idx === -1) {
    selectedAmenities.value.push(label);
  } else {
    selectedAmenities.value.splice(idx, 1);
  }
  form.value.amenities = JSON.stringify(selectedAmenities.value);
}

function addCustomAmenity() {
  const val = customAmenity.value.trim();
  if (val && !selectedAmenities.value.includes(val)) {
    selectedAmenities.value.push(val);
    form.value.amenities = JSON.stringify(selectedAmenities.value);
  }
  customAmenity.value = '';
}

// When editing existing property, pre-populate selected amenities
watch(() => form.value.amenities, (val) => {
  if (val && typeof val === 'string') {
    try {
      selectedAmenities.value = JSON.parse(val);
    } catch {
      selectedAmenities.value = [];
    }
  } else if (Array.isArray(val)) {
    selectedAmenities.value = [...val];
  }
}, { immediate: true });

const apartmentsStore = useApartmentsStore();

const showModal = ref(false);
const editingId = ref(null);
const saving = ref(false);
const searchQuery = ref('');
const selectedCity = ref('');

// Upload state
const uploadMode = ref('file');
const fileInputRef = ref(null);
const isDragging = ref(false);
const uploading = ref(false);
const uploadError = ref('');

const imagePresets = [
  { name: 'Lusaka Penthouse', url: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80' },
  { name: 'Safari Cottage', url: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=600&q=80' },
  { name: 'Modern Villa', url: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80' },
  { name: 'Luxury Suite', url: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80' }
];

const form = ref({
  title: '',
  description: '',
  price_per_night: 500,
  city: 'Lusaka',
  capacity: 2,
  bedrooms: 1,
  bathrooms: 1,
  image_url: '',
  latitude: null,
  longitude: null,
  amenities: '[]'
});

onMounted(async () => {
  await apartmentsStore.fetchApartments();
});

const filteredApartments = computed(() => {
  return apartmentsStore.apartments.filter(apt => {
    const matchesSearch = !searchQuery.value || apt.title?.toLowerCase().includes(searchQuery.value.toLowerCase()) || apt.city?.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesCity = !selectedCity.value || apt.city === selectedCity.value;
    return matchesSearch && matchesCity;
  });
});

const averageNightlyRate = computed(() => {
  if (apartmentsStore.apartments.length === 0) return 0;
  const total = apartmentsStore.apartments.reduce((sum, a) => sum + (Number(a.price_per_night) || 0), 0);
  return Math.round(total / apartmentsStore.apartments.length);
});

const totalBedCapacity = computed(() => {
  return apartmentsStore.apartments.reduce((sum, a) => sum + (Number(a.capacity) || 2), 0);
});

function resolveImageUrl(url) {
  if (!url) return 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80';
  if (url.startsWith('http') || url.startsWith('data:')) return url;
  return `http://localhost:8000${url}`;
}

function triggerFileInput() {
  if (fileInputRef.value) {
    fileInputRef.value.click();
  }
}

async function onFileSelected(event) {
  const file = event.target.files?.[0];
  if (file) await handleFileUpload(file);
}

async function handleFileDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer?.files?.[0];
  if (file) await handleFileUpload(file);
}

async function handleFileUpload(file) {
  if (!file.type.startsWith('image/')) {
    uploadError.value = 'Please select a valid image file (PNG, JPG, WEBP).';
    return;
  }

  uploading.value = true;
  uploadError.value = '';
  
  try {
    const res = await uploadImage(file);
    if (res?.url) {
      form.value.image_url = res.url;
    }
  } catch (err) {
    uploadError.value = err.response?.data?.detail || 'Failed to upload image. Please try again.';
  } finally {
    uploading.value = false;
  }
}

function openCreateModal() {
  editingId.value = null;
  uploadMode.value = 'file';
  uploadError.value = '';
  selectedAmenities.value = [];
  form.value = {
    title: '',
    address: '',
    description: '',
    price_per_night: 500,
    city: 'Lusaka',
    capacity: 2,
    bedrooms: 1,
    bathrooms: 1,
    property_type: 'apartment',
    image_url: '',
    latitude: null,
    longitude: null,
    amenities: '[]'
  };
  showModal.value = true;
}

function startEdit(apt) {
  editingId.value = apt.id;
  uploadMode.value = 'file';
  uploadError.value = '';
  form.value = { ...apt };
  if (apt.amenities) {
    if (typeof apt.amenities === 'string') {
      try {
        selectedAmenities.value = JSON.parse(apt.amenities);
      } catch {
        selectedAmenities.value = [];
      }
    } else if (Array.isArray(apt.amenities)) {
      selectedAmenities.value = [...apt.amenities];
    }
  } else {
    selectedAmenities.value = [];
  }
  showModal.value = true;
}

function openAvailability(apt) {
  // Navigation or availability modal hook
}

async function saveProperty() {
  if (!form.value.title) return;
  saving.value = true;
  const payload = {
    ...form.value,
    address: form.value.address || `${form.value.title}, ${form.value.city}`,
    property_type: form.value.property_type || 'apartment',
    // Coerce numerics — InputNumber or text input can emit null when cleared
    price_per_night: parseFloat(form.value.price_per_night) || 100,
    capacity: parseInt(form.value.capacity) || 2,
    bedrooms: parseInt(form.value.bedrooms) || 1,
    bathrooms: parseInt(form.value.bathrooms) || 1,
    latitude: form.value.latitude,
    longitude: form.value.longitude,
    amenities: JSON.stringify(selectedAmenities.value)
  };

  try {
    if (editingId.value) {
      await apartmentsStore.updateApartment(editingId.value, payload);
    } else {
      await apartmentsStore.createApartment(payload);
    }
    showModal.value = false;
  } catch (err) {
    console.error(err);
  } finally {
    saving.value = false;
  }
}

async function confirmDelete(event, id) {
  if (confirm("Are you sure you want to remove this property listing?")) {
    await apartmentsStore.deleteApartment(id);
  }
}
</script>
