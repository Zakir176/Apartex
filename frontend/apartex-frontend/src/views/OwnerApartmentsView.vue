<template>
  <div class="max-w-[1200px] mx-auto px-6 py-8">
    <!-- Header Section -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-10 gap-4">
      <div>
        <h1 class="text-4xl font-extrabold text-slate-800 mb-2">Property Portfolio</h1>
        <p class="text-slate-500 font-medium text-lg">Manage your premium listings and optimize performance</p>
      </div>
      <button @click="openCreateModal" class="btn-accent shadow-accent inline-flex items-center gap-2">
        <i class="pi pi-plus-circle"></i>
        List New Property
      </button>
    </div>

    <!-- Stats Bar -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <div class="card-base p-6">
        <span class="block text-slate-500 text-xs font-bold uppercase mb-3 tracking-wider">Total Listings</span>
        <span class="text-4xl font-extrabold text-slate-800 tracking-tight">{{ apartmentsStore.apartments.length }}</span>
      </div>
      <div class="card-base p-6">
        <span class="block text-slate-500 text-xs font-bold uppercase mb-3 tracking-wider">Active Bookings</span>
        <span class="text-4xl font-extrabold text-slate-800 tracking-tight">12</span>
      </div>
      <div class="card-base p-6">
        <span class="block text-slate-500 text-xs font-bold uppercase mb-3 tracking-wider">Estimated Revenue</span>
        <span class="text-4xl font-extrabold text-blue-600 tracking-tight">$4,250</span>
      </div>
    </div>

    <!-- Listings Grid -->
    <div v-if="apartmentsStore.apartments.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="apt in apartmentsStore.apartments" :key="apt.id" class="card-base overflow-hidden flex flex-col group">
        <div class="relative w-full h-56 overflow-hidden">
          <img :src="apt.image_url || 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80'" :alt="apt.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
          <div class="absolute top-3 right-3 px-3 py-1.5 bg-black/80 backdrop-blur-md text-white rounded-lg font-bold text-sm shadow-md">
            ${{ apt.price_per_night }}<span class="font-medium text-white/70 text-xs ml-1">/ nt</span>
          </div>
        </div>
        
        <div class="p-5 flex-grow flex flex-col">
          <div class="flex items-center gap-1.5 text-accent text-[11px] font-bold uppercase tracking-widest mb-2">
            <i class="pi pi-map-marker"></i>
            {{ apt.city }}
          </div>
          <h3 class="text-xl font-extrabold text-slate-800 mb-4 line-clamp-1" :title="apt.title">{{ apt.title }}</h3>
          
          <div class="flex gap-2 mb-6">
            <span class="px-2.5 py-1.5 bg-slate-100 rounded-md text-[11px] font-bold text-slate-600 uppercase tracking-wider">{{ apt.capacity }} Guests</span>
            <span class="px-2.5 py-1.5 bg-slate-100 rounded-md text-[11px] font-bold text-slate-600 uppercase tracking-wider">{{ apt.bedrooms }} BR</span>
          </div>

          <div class="flex gap-2 pt-4 border-t border-surface-border mt-auto">
            <button @click="startEdit(apt)" class="flex-1 px-3 py-2 rounded-lg text-sm font-bold text-slate-600 hover:bg-slate-100 transition-colors inline-flex items-center justify-center gap-2">
              <i class="pi pi-pencil"></i> Edit
            </button>
            <button @click="openAvailability(apt)" class="flex-1 px-3 py-2 rounded-lg text-sm font-bold text-orange-600 hover:bg-orange-50 transition-colors inline-flex items-center justify-center gap-2">
              <i class="pi pi-calendar"></i> Dates
            </button>
            <button @click="confirmDelete($event, apt.id)" class="px-3 py-2 rounded-lg text-sm font-bold text-red-600 hover:bg-red-50 transition-colors inline-flex items-center justify-center">
              <i class="pi pi-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="card-base p-16 flex flex-col items-center justify-center text-center">
      <div class="w-20 h-20 rounded-full bg-slate-50 flex items-center justify-center mb-6">
        <i class="pi pi-home text-4xl text-slate-300"></i>
      </div>
      <h2 class="text-2xl font-extrabold text-slate-800 mb-3">Start your hosting journey</h2>
      <p class="text-slate-500 font-medium mb-8 max-w-md">List your first property and reach thousands of premium guests across the globe.</p>
      <button @click="openCreateModal" class="btn-accent inline-flex items-center gap-2">
        <i class="pi pi-plus"></i> Create First Listing
      </button>
    </div>

    <!-- Apartex Studio Wizard -->
    <Dialog 
      v-model:visible="showModal" 
      class="studio-wizard"
      :header="editingId ? 'Edit Listing' : 'Publish New Property'"
      :modal="true" 
      :style="{ width: '600px', maxWidth: '95vw' }"
      contentClass="pt-2"
    >
      <div class="flex flex-col gap-5 py-4">
        <!-- Step 1 -->
        <div v-if="currentStep === 1" class="flex flex-col gap-5">
          <div>
            <label class="label-base">Listing Title</label>
            <input v-model="form.title" class="input-base" placeholder="e.g. Modern Penthouse" />
          </div>
          <div>
            <label class="label-base">Description</label>
            <textarea v-model="form.description" class="input-base resize-none" rows="4" placeholder="Tell guests about your space..."></textarea>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label-base">City</label>
              <input v-model="form.city" class="input-base" placeholder="Lusaka" />
            </div>
            <div>
              <label class="label-base">Price per Night (USD)</label>
              <InputNumber v-model="form.price_per_night" mode="currency" currency="USD" locale="en-US" inputClass="input-base !w-full" class="w-full" />
            </div>
          </div>
        </div>

        <!-- Step 2 -->
        <div v-if="currentStep === 2" class="flex flex-col gap-5">
          <div>
            <label class="label-base">Full Address</label>
            <input v-model="form.address" class="input-base" placeholder="123 Luxury Lane" />
          </div>
          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="label-base">Capacity</label>
              <InputNumber v-model="form.capacity" showButtons :min="1" inputClass="input-base w-full" class="w-full" />
            </div>
            <div>
              <label class="label-base">Bedrooms</label>
              <InputNumber v-model="form.bedrooms" showButtons :min="0" inputClass="input-base w-full" class="w-full" />
            </div>
            <div>
              <label class="label-base">Bathrooms</label>
              <InputNumber v-model="form.bathrooms" showButtons :min="0" inputClass="input-base w-full" class="w-full" />
            </div>
          </div>
          <div>
            <label class="label-base">Cover Image URL</label>
            <input v-model="form.image_url" class="input-base" placeholder="https://..." />
          </div>
        </div>

        <!-- Step 3: Location Picker -->
        <div v-if="currentStep === 3">
          <LocationPicker 
            v-model="locationData" 
            :address="form.address" 
            :city="form.city" 
          />
        </div>
      </div>

      <template #footer>
        <div class="flex justify-between w-full pt-4 border-t border-surface-border mt-2">
          <button @click="closeModal" class="px-5 py-2.5 rounded-full text-sm font-bold text-slate-500 hover:bg-slate-100 transition-colors">Cancel</button>
          <div class="flex gap-3">
            <button v-if="currentStep > 1" @click="currentStep--" class="px-5 py-2.5 rounded-full text-sm font-bold text-slate-700 border border-surface-border hover:bg-slate-50 transition-colors inline-flex items-center gap-2">
              <i class="pi pi-arrow-left"></i> Back
            </button>
            <button v-if="currentStep < 3" @click="currentStep++" class="btn-accent inline-flex items-center gap-2">
              Next <i class="pi pi-arrow-right"></i>
            </button>
            <button v-else @click="submitForm" :disabled="apartmentsStore.loading" class="btn-accent inline-flex items-center gap-2">
              <i class="pi pi-check" v-if="!apartmentsStore.loading"></i>
              <i class="pi pi-spinner pi-spin" v-else></i>
              <span>{{ editingId ? 'Update Listing' : 'Publish Listing' }}</span>
            </button>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Availability Modal -->
    <Dialog v-model:visible="showAvailabilityModal" header="Property Availability" :modal="true" :style="{ width: '800px', maxWidth: '95vw' }">
      <AvailabilityCalendar v-if="selectedAptForAvailability" :apartment-id="selectedAptForAvailability.id" />
    </Dialog>

    <ConfirmPopup />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, computed } from 'vue';
import { useApartmentsStore } from '@/stores/apartments';
import { useConfirm } from "primevue/useconfirm";

// PrimeVue components
import Dialog from 'primevue/dialog';
import InputNumber from 'primevue/inputnumber';
import ConfirmPopup from 'primevue/confirmpopup';
import AvailabilityCalendar from '@/components/AvailabilityCalendar.vue';
import LocationPicker from '@/components/LocationPicker.vue';

const apartmentsStore = useApartmentsStore();
const confirm = useConfirm();

const showModal = ref(false);
const editingId = ref(null);
const currentStep = ref(1);

const showAvailabilityModal = ref(false);
const selectedAptForAvailability = ref(null);

const initialForm = {
  title: '',
  description: '',
  address: '',
  city: '',
  price_per_night: 0,
  capacity: 1,
  bedrooms: 1,
  bathrooms: 1,
  image_url: '',
  latitude: null,
  longitude: null
};

const form = reactive({ ...initialForm });

const locationData = computed({
  get: () => ({ lat: form.latitude, lng: form.longitude }),
  set: (val) => {
    form.latitude = val.lat;
    form.longitude = val.lng;
  }
});

onMounted(async () => {
  await apartmentsStore.fetchMyApartments();
});

const openCreateModal = () => {
  editingId.value = null;
  currentStep.value = 1;
  Object.assign(form, initialForm);
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const openAvailability = (apt) => {
  selectedAptForAvailability.value = apt;
  showAvailabilityModal.value = true;
};

const startEdit = (apt) => {
  editingId.value = apt.id;
  currentStep.value = 1;
  Object.assign(form, {
    ...apt,
    price_per_night: Number(apt.price_per_night)
  });
  showModal.value = true;
};

const submitForm = async () => {
  try {
    if (editingId.value) {
      await apartmentsStore.updateApartment(editingId.value, { ...form });
    } else {
      await apartmentsStore.createApartment({ ...form });
    }
    await apartmentsStore.fetchMyApartments();
    closeModal();
  } catch (err) {
    console.error('Submission failed', err);
  }
};

const confirmDelete = (event, id) => {
  confirm.require({
    target: event.currentTarget,
    message: 'Delete this property permanently?',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      await apartmentsStore.deleteApartment(id);
      await apartmentsStore.fetchMyApartments();
    }
  });
};
</script>
