<template>
  <div class="ax-container py-8">
    <!-- Header Section -->
    <div class="flex align-items-center justify-content-between mb-8">
      <div>
        <h1 class="text-5xl font-bold text-900 mb-2">Property Portfolio</h1>
        <p class="text-500 font-medium text-lg text-muted">Manage your premium listings and optimize performance</p>
      </div>
      <button @click="openCreateModal" class="ax-button shadow-lg">
        <i class="pi pi-plus-circle mr-2"></i>
        List New Property
      </button>
    </div>

    <!-- Stats Bar -->
    <div class="grid mb-8">
      <div class="col-12 md:col-4">
        <div class="surface-0 p-4 border-round-xl border-1 border-200 shadow-sm">
           <span class="block text-500 text-xs font-bold uppercase mb-2 tracking-wider">Total Listings</span>
           <span class="text-4xl font-bold text-900">{{ apartmentsStore.apartments.length }}</span>
        </div>
      </div>
      <div class="col-12 md:col-4">
        <div class="surface-0 p-4 border-round-xl border-1 border-200 shadow-sm">
           <span class="block text-500 text-xs font-bold uppercase mb-2 tracking-wider">Active Bookings</span>
           <span class="text-4xl font-bold text-900">12</span>
        </div>
      </div>
      <div class="col-12 md:col-4">
        <div class="surface-0 p-4 border-round-xl border-1 border-200 shadow-sm">
           <span class="block text-500 text-xs font-bold uppercase mb-2 tracking-wider">Estimated Revenue</span>
           <span class="text-4xl font-bold text-blue-600">$4,250</span>
        </div>
      </div>
    </div>

    <!-- Listings Grid -->
    <div v-if="apartmentsStore.apartments.length > 0" class="grid">
      <div v-for="apt in apartmentsStore.apartments" :key="apt.id" class="col-12 md:col-6 lg:col-4 p-3">
        <div class="surface-0 border-round-xl border-1 border-200 overflow-hidden hover:shadow-lg transition-all transition-duration-300 h-full flex flex-column">
          <div class="relative">
            <img :src="apt.image_url || '/placeholder-apartment.png'" :alt="apt.title" class="w-full h-15rem object-cover" />
            <div class="absolute top-0 right-0 m-3 px-3 py-1 bg-black-alpha-80 text-white border-round-lg font-bold text-sm">
              ${{ apt.price_per_night }}<span class="font-normal opacity-70">/nt</span>
            </div>
          </div>
          
          <div class="p-4 flex-grow-1 flex flex-column">
            <div class="flex align-items-center gap-1 text-500 text-xs font-bold uppercase mb-2">
              <i class="pi pi-map-marker text-blue-500"></i>
              {{ apt.city }}
            </div>
            <h3 class="text-xl font-bold text-900 mb-3 truncate">{{ apt.title }}</h3>
            
            <div class="flex gap-2 mb-4">
              <span class="px-2 py-1 surface-100 border-round-md text-xs font-bold text-700">{{ apt.capacity }} Guests</span>
              <span class="px-2 py-1 surface-100 border-round-md text-xs font-bold text-700">{{ apt.bedrooms }} BR</span>
            </div>

            <div class="flex gap-2 pt-4 border-top-1 border-100 mt-auto">
              <Button icon="pi pi-pencil" label="Edit" @click="startEdit(apt)" class="p-button-text p-button-sm flex-1 font-bold" />
              <Button icon="pi pi-calendar" label="Dates" @click="openAvailability(apt)" class="p-button-text p-button-warning p-button-sm flex-1 font-bold" />
              <Button icon="pi pi-trash" label="Delete" @click="confirmDelete($event, apt.id)" class="p-button-text p-button-danger p-button-sm flex-1 font-bold" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="surface-0 p-8 border-round-3xl border-1 border-200 text-center shadow-sm">
      <i class="pi pi-home text-6xl text-200 mb-4"></i>
      <h2 class="text-3xl font-bold text-900 mb-2">Start your hosting journey</h2>
      <p class="text-500 font-medium mb-6">List your first property and reach thousands of premium guests.</p>
      <button @click="openCreateModal" class="ax-button">Create First Listing</button>
    </div>

    <!-- Apartex Studio Wizard -->
    <Dialog 
      v-model:visible="showModal" 
      class="studio-wizard"
      :header="editingId ? 'Edit Listing' : 'Publish New Property'"
      :modal="true" 
      style="width: 600px; max-width: 95vw;"
    >
      <div class="p-fluid py-2">
        <!-- Step 1 -->
        <div v-if="currentStep === 1">
          <div class="mb-4">
            <label class="ax-label">Listing Title</label>
            <input v-model="form.title" class="ax-input" placeholder="e.g. Modern Penthouse" />
          </div>
          <div class="mb-4">
            <label class="ax-label">Description</label>
            <textarea v-model="form.description" class="ax-input" rows="4" placeholder="Tell guests about your space..."></textarea>
          </div>
          <div class="grid">
            <div class="col-6">
              <label class="ax-label">City</label>
              <input v-model="form.city" class="ax-input" placeholder="Lusaka" />
            </div>
            <div class="col-6">
              <label class="ax-label">Price per Night (USD)</label>
              <InputNumber v-model="form.price_per_night" mode="currency" currency="USD" locale="en-US" inputClass="ax-input" />
            </div>
          </div>
        </div>

        <!-- Step 2 -->
        <div v-if="currentStep === 2">
          <div class="mb-4">
            <label class="ax-label">Full Address</label>
            <input v-model="form.address" class="ax-input" placeholder="123 Luxury Lane" />
          </div>
          <div class="grid mb-4">
            <div class="col-4">
              <label class="ax-label">Capacity</label>
              <InputNumber v-model="form.capacity" showButtons :min="1" inputClass="ax-input" />
            </div>
            <div class="col-4">
              <label class="ax-label">Bedrooms</label>
              <InputNumber v-model="form.bedrooms" showButtons :min="0" inputClass="ax-input" />
            </div>
            <div class="col-4">
              <label class="ax-label">Bathrooms</label>
              <InputNumber v-model="form.bathrooms" showButtons :min="0" inputClass="ax-input" />
            </div>
          </div>
          <div class="mb-2">
            <label class="ax-label">Cover Image URL</label>
            <input v-model="form.image_url" class="ax-input" placeholder="https://..." />
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
        <div class="flex justify-content-between w-full pt-4">
          <Button label="Cancel" @click="closeModal" class="p-button-text p-button-secondary font-bold" />
          <div class="flex gap-2">
            <Button v-if="currentStep > 1" label="Back" icon="pi pi-arrow-left" @click="currentStep--" class="p-button-outlined p-button-secondary font-bold" />
            <Button v-if="currentStep < 3" label="Next" icon="pi pi-arrow-right" iconPos="right" @click="currentStep++" class="p-button-primary font-bold px-4" />
            <Button v-else :label="editingId ? 'Update Listing' : 'Publish Listing'" icon="pi pi-check" @click="submitForm" class="p-button-primary font-bold px-4" :loading="apartmentsStore.loading" />
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Availability Modal -->
    <Dialog v-model:visible="showAvailabilityModal" header="Property Availability" :modal="true" style="width: 800px; max-width: 95vw;">
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
import Button from 'primevue/button';
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
    closeModal(); // FIX: Explicitly close modal after success
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

<style scoped>
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
