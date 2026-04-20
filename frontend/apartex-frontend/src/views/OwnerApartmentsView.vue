<template>
  <div class="owner-apartments-container">
    <div class="header-section">
      <div class="title-area">
        <h1>Property Portfolio</h1>
        <p class="subtitle text-muted">Manage your premium listings and maximize your revenue</p>
      </div>
      <Button 
        label="List New Property" 
        icon="pi pi-plus-circle" 
        @click="openCreateModal" 
        class="p-button-raised p-button-primary p-button-lg px-4" 
      />
    </div>

    <!-- Stats Bar -->
    <div class="mb-6 grid">
      <div class="col-12 md:col-4">
        <div class="stat-card p-4 border-round-xl bg-white shadow-sm border-1 border-gray-100 dark:bg-slate-800 dark:border-slate-700">
           <span class="block text-muted text-sm font-bold uppercase mb-2">Total Listings</span>
           <span class="text-3xl font-bold">{{ apartmentsStore.apartments.length }}</span>
        </div>
      </div>
      <div class="col-12 md:col-4">
        <div class="stat-card p-4 border-round-xl bg-white shadow-sm border-1 border-gray-100 dark:bg-slate-800 dark:border-slate-700">
           <span class="block text-muted text-sm font-bold uppercase mb-2">Active Bookings</span>
           <span class="text-3xl font-bold">12</span>
        </div>
      </div>
      <div class="col-12 md:col-4">
        <div class="stat-card p-4 border-round-xl bg-white shadow-sm border-1 border-gray-100 dark:bg-slate-800 dark:border-slate-700">
           <span class="block text-muted text-sm font-bold uppercase mb-2">Est. Revenue</span>
           <span class="text-3xl font-bold text-primary">$4,250</span>
        </div>
      </div>
    </div>

    <!-- Loading State: Skeleton Cards -->
    <div v-if="apartmentsStore.loading && apartmentsStore.apartments.length === 0" class="listings-grid fadein animation-duration-500">
      <Card v-for="i in 3" :key="i" class="apt-card">
        <template #header>
          <div class="apt-image-wrapper">
            <Skeleton width="100%" height="220px" class="border-noround" />
          </div>
        </template>
        <template #title>
          <Skeleton width="75%" height="1.5rem" />
        </template>
        <template #subtitle>
          <Skeleton width="40%" height="1rem" class="mt-1" />
        </template>
        <template #content>
          <div class="flex gap-2 mb-3">
            <Skeleton width="5rem" height="1.8rem" class="border-round-2xl" />
            <Skeleton width="4rem" height="1.8rem" class="border-round-2xl" />
          </div>
          <Skeleton width="100%" height="3.5rem" />
        </template>
        <template #footer>
          <div class="flex gap-2">
            <Skeleton width="50%" height="2.5rem" class="border-round-lg" />
            <Skeleton width="50%" height="2.5rem" class="border-round-lg" />
          </div>
        </template>
      </Card>
    </div>

    <!-- Empty State -->
    <div v-else-if="apartmentsStore.apartments.length === 0" class="empty-state card shadow-sm">
      <div class="empty-icon text-primary opacity-50">
        <i class="pi pi-home" style="font-size: 5rem"></i>
      </div>
      <h3 class="text-2xl font-bold mt-4">Growth Starts Here</h3>
      <p class="text-muted mt-2">Ready to welcome your first guests? List your space in minutes.</p>
      <Button label="Create Listing" icon="pi pi-plus" @click="openCreateModal" class="mt-4 p-button-lg" />
    </div>

    <!-- Listings Grid -->
    <div v-else class="listings-grid fadein animation-duration-500">
      <Card v-for="apt in apartmentsStore.apartments" :key="apt.id" class="apt-card hover:shadow-lg">
        <template #header>
          <div class="apt-image-wrapper">
            <img :src="apt.image_url || '/placeholder-apartment.png'" :alt="apt.title" />
            <div class="price-badge">{{ formatCurrency(apt.price_per_night) }}<span class="text-xs font-normal">/night</span></div>
          </div>
        </template>
        <template #title>
          <div class="apt-title">{{ apt.title }}</div>
        </template>
        <template #subtitle>
          <div class="apt-location flex align-items-center">
            <i class="pi pi-map-marker mr-1 text-primary"></i>
            {{ apt.city }}
          </div>
        </template>
        <template #content>
          <div class="apt-details mb-3">
            <Tag :value="`${apt.capacity} Guests`" rounded severity="info" class="mr-2" />
            <Tag :value="`${apt.bedrooms} Beds`" rounded severity="secondary" />
          </div>
          <p class="apt-description text-sm line-height-3">{{ truncateText(apt.description, 90) }}</p>
        </template>
        <template #footer>
          <div class="apt-actions pt-2 border-top-1 border-gray-100 flex flex-wrap gap-2">
            <Button icon="pi pi-pencil" label="Edit" @click="startEdit(apt)" class="p-button-text p-button-sm flex-1" />
            <Button icon="pi pi-calendar" label="Availability" @click="openAvailability(apt)" class="p-button-text p-button-warning p-button-sm flex-1" />
            <Button icon="pi pi-trash" label="Delete" @click="confirmDelete($event, apt.id)" class="p-button-text p-button-danger p-button-sm flex-1" />
          </div>
        </template>
      </Card>
    </div>

    <!-- Apartex Studio Wizard -->
    <Dialog 
      v-model:visible="showModal" 
      class="studio-wizard"
      header="Apartex Studio: Create Your Listing"
      :modal="true" 
      :dismissableMask="false"
      :closable="!apartmentsStore.loading && !showSuccess"
      @hide="onDialogHide"
    >
      <!-- Success Overlay -->
      <div v-if="showSuccess" class="success-overlay flex flex-column align-items-center justify-content-center">
        <div class="success-burst mb-5">
          <div class="burst-ring ring-1"></div>
          <div class="burst-ring ring-2"></div>
          <div class="burst-ring ring-3"></div>
          <div class="success-icon-wrap">
            <i class="pi pi-check success-check"></i>
          </div>
        </div>
        <h2 class="text-3xl font-bold text-900 mb-2">Listing Published!</h2>
        <p class="text-gray-500 text-center mb-5 max-w-20rem">
          <strong class="text-900">"{{ publishedTitle }}"</strong> is now live and discoverable by guests on Apartex.
        </p>
        <Button label="View My Listings" icon="pi pi-arrow-right" iconPos="right" @click="closeModal" class="p-button-primary p-button-lg font-bold px-5" />
        <Button label="Add Another Property" icon="pi pi-plus" @click="addAnother" class="p-button-text mt-2 font-bold" />
      </div>

      <div v-else class="wizard-container">
        <!-- Sidebar: Steps -->
        <div class="wizard-sidebar hidden lg:flex flex-column gap-3 p-4 border-right-1 border-gray-100">
          <div 
            v-for="step in wizardSteps" 
            :key="step.index"
            class="step-item flex align-items-center gap-3"
            :class="{ 'active': currentStep === step.index, 'completed': currentStep > step.index }"
          >
            <div class="step-circle flex align-items-center justify-content-center">
              <i v-if="currentStep > step.index" class="pi pi-check"></i>
              <span v-else>{{ step.index }}</span>
            </div>
            <div class="step-label font-semibold">{{ step.label }}</div>
          </div>
        </div>

        <!-- Main Content: Form -->
        <div class="wizard-main p-4 overflow-y-auto" style="flex: 1">
          <div class="mb-4">
            <small class="text-primary font-bold uppercase tracking-wider">Step {{ currentStep }} of 4</small>
            <h2 class="text-2xl font-bold mt-1 text-900">{{ wizardSteps[currentStep-1].title }}</h2>
            <p class="text-muted text-sm mt-1">{{ wizardSteps[currentStep-1].description }}</p>
          </div>

          <transition name="fade-slide" mode="out-in">
            <!-- Step 1: Identity -->
            <div v-if="currentStep === 1" key="step1" class="p-fluid">
              <div class="field mb-4">
                <label class="font-bold mb-2 block">Listing Title <span class="text-red-500">*</span></label>
                <InputText
                  v-model="form.title"
                  placeholder="e.g. Modern Penthouse with Skyline View"
                  :class="{ 'p-invalid': v$.title }"
                  @blur="touchedFields.title = true"
                />
                <small v-if="touchedFields.title && !form.title" class="p-error block mt-1">Title is required.</small>
                <small v-else class="text-muted block mt-1">Make it catchy! This is the first thing guests see.</small>
              </div>
              <div class="field">
                <label class="font-bold mb-2 block">Description <span class="text-red-500">*</span></label>
                <Textarea
                  v-model="form.description"
                  rows="5"
                  placeholder="Highlight what makes your place unique..."
                  :class="{ 'p-invalid': touchedFields.description && !form.description }"
                  @blur="touchedFields.description = true"
                />
                <small v-if="touchedFields.description && !form.description" class="p-error block mt-1">Description is required.</small>
              </div>
            </div>

            <!-- Step 2: Space & Location -->
            <div v-else-if="currentStep === 2" key="step2" class="p-fluid">
              <div class="formgrid grid">
                <div class="field col-12 mb-4">
                  <label class="font-bold mb-2 block">Full Address <span class="text-red-500">*</span></label>
                  <InputText
                    v-model="form.address"
                    placeholder="123 Luxury Ave, Lusaka"
                    :class="{ 'p-invalid': touchedFields.address && !form.address }"
                    @blur="touchedFields.address = true"
                  />
                  <small v-if="touchedFields.address && !form.address" class="p-error block mt-1">Address is required.</small>
                </div>
                <div class="field col-6">
                  <label class="font-bold mb-2 block">City <span class="text-red-500">*</span></label>
                  <InputText
                    v-model="form.city"
                    placeholder="e.g. Lusaka"
                    :class="{ 'p-invalid': touchedFields.city && !form.city }"
                    @blur="touchedFields.city = true"
                  />
                  <small v-if="touchedFields.city && !form.city" class="p-error block mt-1">City is required.</small>
                </div>
                <div class="field col-6">
                  <label class="font-bold mb-2 block">Max Guests</label>
                  <InputNumber v-model="form.capacity" showButtons :min="1" />
                </div>
                <div class="field col-6">
                  <label class="font-bold mb-2 block">Bedrooms</label>
                  <InputNumber v-model="form.bedrooms" showButtons :min="0" />
                </div>
                <div class="field col-6">
                  <label class="font-bold mb-2 block">Bathrooms</label>
                  <InputNumber v-model="form.bathrooms" showButtons :min="0" />
                </div>
              </div>
            </div>

            <!-- Step 3: Amenities -->
            <div v-else-if="currentStep === 3" key="step3">
              <label class="font-bold mb-4 block">Select Included Amenities</label>
              <div class="amenity-grid">
                <div 
                  v-for="amenity in availableAmenities" 
                  :key="amenity.id"
                  class="amenity-item flex flex-column align-items-center justify-content-center p-3 border-1 border-gray-200 border-round-xl cursor-pointer transition-all transition-duration-200"
                  :class="{ 'selected border-primary bg-blue-50 text-primary scalein': isAmenitySelected(amenity.label) }"
                  @click="toggleAmenity(amenity.label)"
                >
                  <i :class="amenity.icon" style="font-size: 1.5rem"></i>
                  <span class="text-xs font-bold mt-2 text-center">{{ amenity.label }}</span>
                </div>
              </div>
            </div>

            <!-- Step 4: Media & Pricing -->
            <div v-else-if="currentStep === 4" key="step4" class="p-fluid">
              <div class="field mb-4">
                <label class="font-bold mb-2 block">Nightly Rate (USD)</label>
                <div class="p-inputgroup mb-2">
                  <span class="p-inputgroup-addon">$</span>
                  <InputNumber v-model="form.price_per_night" :min="0" placeholder="0.00" />
                </div>
                
                <!-- Market Advisor Component -->
                <div v-if="form.city" class="market-advisor p-3 border-round-xl bg-blue-50 border-1 border-blue-100 flex align-items-center gap-3">
                   <div class="advisor-icon p-2 bg-primary border-round-circle text-white">
                      <i class="pi pi-bolt"></i>
                   </div>
                   <div style="flex: 1">
                      <span class="block text-xs font-bold text-primary uppercase">Market Advisor</span>
                      <p class="text-sm text-blue-900 m-0">The average rate in <strong>{{ form.city }}</strong> is <strong>{{ formatCurrency(averageCityPrice) }}</strong>. Your price is {{ priceComparisonLabel }}.</p>
                   </div>
                </div>
              </div>
              
              <div class="field">
                <label class="font-bold mb-2 block text-900 border-top-1 border-gray-100 pt-3">Property Gallery</label>
                <div class="gallery-uploader">
                  <FileUpload 
                    name="demo[]" 
                    url="/api/upload" 
                    multiple 
                    accept="image/*" 
                    :maxFileSize="1000000"
                    customUpload
                    @uploader="handleGalleryUpload"
                    class="premium-uploader mb-3"
                  >
                    <template #empty>
                      <div class="flex flex-column align-items-center justify-content-center py-4">
                        <i class="pi pi-images text-4xl text-gray-400 mb-2"></i>
                        <p class="text-muted font-bold">Drag and drop photos here</p>
                      </div>
                    </template>
                  </FileUpload>
                  
                  <div v-if="form.image_url" class="relative group mt-2">
                    <img :src="form.image_url" class="w-full border-round-xl shadow-lg" style="max-height: 250px; object-fit: cover" />
                    <div class="absolute inset-0 bg-black-alpha-40 opacity-0 group-hover:opacity-100 transition-opacity flex align-items-center justify-content-center border-round-xl">
                       <Button icon="pi pi-trash" class="p-button-rounded p-button-danger p-button-lg" @click="form.image_url = ''" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </transition>

          <!-- Wizard Footer -->
          <div class="flex justify-content-between align-items-center mt-5 pt-4 border-top-1 border-gray-100">
            <Button 
              label="Back" 
              icon="pi pi-arrow-left" 
              class="p-button-text p-button-secondary font-bold" 
              @click="prevStep"
              :disabled="currentStep === 1 || apartmentsStore.loading"
            />
            <div class="flex gap-2">
              <Button label="Cancel" class="p-button-text p-button-secondary font-bold" @click="closeModal" />
              <Button 
                v-if="currentStep < 4"
                label="Continue" 
                icon="pi pi-arrow-right" 
                iconPos="right"
                class="p-button-primary font-bold px-4" 
                @click="nextStep"
                :disabled="!canContinue"
              />
              <Button 
                v-else
                :label="editingId ? 'Update Listing' : 'Publish Listing'" 
                icon="pi pi-send" 
                class="p-button-primary font-bold px-4" 
                @click="submitForm" 
                :loading="apartmentsStore.loading" 
              />
            </div>
          </div>
        </div>

        <!-- Sidebar: Live Preview -->
        <div class="wizard-preview hidden xl:flex flex-column align-items-center p-4 bg-gray-50 border-left-1 border-gray-100 dark:bg-slate-900" style="width: 380px;">
          <h3 class="text-sm font-bold uppercase text-muted mb-4 tracking-wider">Live Preview</h3>
          <div class="preview-card-wrapper scalein animation-duration-500">
             <Card class="apt-card shadow-4" style="width: 320px; background: white;">
              <template #header>
                <div class="apt-image-wrapper">
                  <img :src="form.image_url || '/placeholder-apartment.png'" />
                  <div class="price-badge">${{ form.price_per_night || '0' }}<span class="text-xs font-normal">/night</span></div>
                </div>
              </template>
              <template #title>
                <div class="text-xl font-bold text-900">{{ form.title || 'Property Title Goes Here' }}</div>
              </template>
              <template #subtitle>
                <div class="flex align-items-center text-sm">
                  <i class="pi pi-map-marker mr-1 text-primary"></i>
                  {{ form.city || 'City' }}
                </div>
              </template>
              <template #content>
                 <div class="apt-details mb-3">
                  <Tag :value="`${form.capacity || 1} Guests`" rounded severity="info" class="mr-2" />
                  <Tag :value="`${form.bedrooms || 0} Beds`" rounded severity="secondary" />
                </div>
                <p class="text-sm text-gray-600 line-height-3">{{ truncateText(form.description, 70) || 'Your property description will appear here as you write it.' }}</p>
              </template>
            </Card>
          </div>
          <p class="text-center text-xs text-muted mt-5 cursor-default select-none">
            <i class="pi pi-info-circle mr-1"></i>
            This is how guests will see your listing on the homepage.
          </p>
        </div>
      </div>
    </Dialog>

    <!-- Availability Management Modal -->
    <Dialog 
      v-model:visible="showAvailabilityModal" 
      header="Property Availability" 
      :modal="true" 
      class="availability-dialog"
      style="width: 800px; max-width: 95vw;"
    >
      <AvailabilityCalendar 
        v-if="selectedAptForAvailability" 
        :apartment-id="selectedAptForAvailability.id"
      />
    </Dialog>

    <!-- Delete Confirmation -->
    <ConfirmPopup />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref, computed } from 'vue';
import { useApartmentsStore } from '@/stores/apartments';
import { uploadImage } from '@/api/uploads';
import { useConfirm } from "primevue/useconfirm";

// PrimeVue components
import Button from 'primevue/button';
import Card from 'primevue/card';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Textarea from 'primevue/textarea';
import ProgressSpinner from 'primevue/progressspinner';
import ConfirmPopup from 'primevue/confirmpopup';
import FileUpload from 'primevue/fileupload';
import Skeleton from 'primevue/skeleton';
import AvailabilityCalendar from '@/components/AvailabilityCalendar.vue';

const apartmentsStore = useApartmentsStore();
const confirm = useConfirm();

const showModal = ref(false);
const editingId = ref(null);
const currentStep = ref(1);
const showSuccess = ref(false);
const publishedTitle = ref('');

const showAvailabilityModal = ref(false);
const selectedAptForAvailability = ref(null);

// Touched-field map for real-time per-field validation
const touchedFields = reactive({ title: false, description: false, address: false, city: false });
// v$ provides CSS class logic: field is invalid if touched AND empty
const v$ = computed(() => ({
  title: touchedFields.title && !form.title,
  description: touchedFields.description && !form.description,
  address: touchedFields.address && !form.address,
  city: touchedFields.city && !form.city
}));

const wizardSteps = [
  { index: 1, label: 'Identity', title: 'Give your space a personality', description: 'What should we call your beautiful property?' },
  { index: 2, label: 'The Space', title: 'Map out the specifics', description: 'Detail the location and physical capacity of your listing.' },
  { index: 3, label: 'Offerings', title: 'What do you offer?', description: 'Select the amenities that make your space stay-ready.' },
  { index: 4, label: 'Media & Price', title: 'Visualize and Value', description: 'Photo gallery and pricing configuration.' }
];

const availableAmenities = [
  { id: 1, label: 'WiFi', icon: 'pi pi-wifi' },
  { id: 2, label: 'Parking', icon: 'pi pi-car' },
  { id: 3, label: 'Kitchen', icon: 'pi pi-apple' },
  { id: 4, label: 'TV', icon: 'pi pi-desktop' },
  { id: 5, label: 'Air Con', icon: 'pi pi-box' },
  { id: 6, label: 'Pool', icon: 'pi pi-water' },
  { id: 7, label: 'Gym', icon: 'pi pi-user' },
  { id: 8, label: 'Laundry', icon: 'pi pi-refresh' },
  { id: 9, label: 'Workspace', icon: 'pi pi-briefcase' },
  { id: 10, label: 'Backyard', icon: 'pi pi-sun' }
];

const initialForm = {
  title: '',
  description: '',
  address: '',
  city: '',
  price_per_night: 0,
  capacity: 1,
  bedrooms: 1,
  bathrooms: 1,
  amenities: [],
  image_url: ''
};

const form = reactive({ ...initialForm });

onMounted(async () => {
  await apartmentsStore.fetchMyApartments();
});

const averageCityPrice = computed(() => {
  if (!form.city) return 0;
  // Calculate avg from store or use default
  const cityApts = apartmentsStore.apartments.filter(a => a.city.toLowerCase() === form.city.toLowerCase());
  if (cityApts.length === 0) return 150; 
  const sum = cityApts.reduce((acc, a) => acc + Number(a.price_per_night), 0);
  return Math.round(sum / cityApts.length);
});

const priceComparisonLabel = computed(() => {
  const diff = form.price_per_night - averageCityPrice.value;
  if (Math.abs(diff) < 10) return 'perfectly aligned with market trends';
  return diff > 0 ? 'above average (Premium)' : 'highly competitive';
});

const canContinue = computed(() => {
  if (currentStep.value === 1) return form.title && form.description;
  if (currentStep.value === 2) return form.address && form.city;
  return true;
});

const nextStep = () => {
  // Touch all fields for the current step so validation shows immediately
  if (currentStep.value === 1) {
    touchedFields.title = true;
    touchedFields.description = true;
  } else if (currentStep.value === 2) {
    touchedFields.address = true;
    touchedFields.city = true;
  }
  if (canContinue.value && currentStep.value < 4) currentStep.value++;
};
const prevStep = () => { if (currentStep.value > 1) currentStep.value--; };

const openAvailability = (apt) => {
  selectedAptForAvailability.value = apt;
  showAvailabilityModal.value = true;
};

const openCreateModal = () => {
  editingId.value = null;
  currentStep.value = 1;
  showSuccess.value = false;
  // Reset all touched-field flags
  Object.keys(touchedFields).forEach(k => touchedFields[k] = false);
  Object.assign(form, initialForm);
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  showSuccess.value = false;
};

const onDialogHide = () => {
  showSuccess.value = false;
};

const addAnother = () => {
  showSuccess.value = false;
  currentStep.value = 1;
  Object.keys(touchedFields).forEach(k => touchedFields[k] = false);
  Object.assign(form, initialForm);
};

const isAmenitySelected = (label) => {
  return form.amenities.includes(label);
};

const toggleAmenity = (label) => {
  if (form.amenities.includes(label)) {
    form.amenities = form.amenities.filter(s => s !== label);
  } else {
    form.amenities.push(label);
  }
};

const startEdit = (apt) => {
  editingId.value = apt.id;
  currentStep.value = 1;
  Object.assign(form, {
    ...apt,
    price_per_night: Number(apt.price_per_night),
    amenities: Array.isArray(apt.amenities) ? [...apt.amenities] : []
  });
  showModal.value = true;
};

const handleGalleryUpload = async (event) => {
  const file = event.files[0];
  try {
    const { url } = await uploadImage(file);
    form.image_url = url;
  } catch (err) {
    console.error('Gallery upload failed', err);
  }
};

const submitForm = async () => {
  try {
    if (editingId.value) {
      await apartmentsStore.updateApartment(editingId.value, { ...form });
      await apartmentsStore.fetchMyApartments();
      closeModal();
    } else {
      const created = await apartmentsStore.createApartment({ ...form });
      await apartmentsStore.fetchMyApartments();
      // Show success overlay instead of cold close
      publishedTitle.value = created.title || form.title;
      showSuccess.value = true;
    }
  } catch (err) {
    console.error('Failed to submit apartment', err);
  }
};

const confirmDelete = (event, id) => {
  confirm.require({
    target: event.currentTarget,
    message: 'Are you sure you want to delete this listing?',
    icon: 'pi pi-exclamation-triangle',
    acceptClass: 'p-button-danger',
    accept: async () => {
      await apartmentsStore.deleteApartment(id);
      await apartmentsStore.fetchMyApartments();
    }
  });
};

const formatCurrency = (v) => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(v);
};

const truncateText = (text, length) => {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '...' : text;
};
</script>

<style scoped>
.owner-apartments-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.stat-card {
  transition: all 0.3s;
}

.stat-card:hover {
  border-color: var(--primary-color) !important;
  transform: translateY(-2px);
}

/* Header & Stats */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
}

.title-area h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  letter-spacing: -1px;
}

/* Grid & Cards */
.listings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 2.5rem;
}

.apt-card {
  border-radius: 20px !important;
  overflow: hidden;
  border: 1px solid var(--surface-border) !important;
  background: var(--surface-card) !important;
}

.apt-image-wrapper {
  position: relative;
  height: 220px;
}

.apt-image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.price-badge {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(8px);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1.1rem;
}

.apt-title {
  font-size: 1.3rem;
  font-weight: 800;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--text-color);
}

/* Advisor Panel */
.market-advisor {
  transition: all 0.3s;
}

.market-advisor:hover {
  transform: translateX(5px);
}

.advisor-icon {
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
}

/* Wizard Styling */
:deep(.studio-wizard) {
  width: 1100px;
  max-width: 95vw;
}

:deep(.p-dialog-content) {
  padding: 0 !important;
  overflow: hidden;
}

.wizard-container {
  display: flex;
  height: 700px;
  max-height: 80vh;
}

.wizard-sidebar {
  width: 260px;
}

.step-item {
  color: #94a3b8;
  transition: all 0.3s;
}

.step-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid #e2e8f0;
  font-size: 0.85rem;
  font-weight: 700;
}

.step-item.active {
  color: var(--primary-color);
}

.step-item.active .step-circle {
  border-color: var(--primary-color);
  background: var(--primary-color);
  color: white;
}

.step-item.completed {
  color: #10b981;
}

.step-item.completed .step-circle {
  border-color: #10b981;
  background: #10b981;
  color: white;
}

.amenity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
}

.amenity-item:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.amenity-item.selected {
  background: #eff6ff !important;
  border-color: #3b82f6 !important;
  color: #3b82f6 !important;
}

/* Animations */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Transitions for dark mode */
.dark .wizard-sidebar {
  border-color: #334155 !important;
}

.dark .wizard-preview {
  background: #0f172a !important;
  border-color: #334155 !important;
}

.dark .step-circle {
  border-color: #334155;
}

.dark .amenity-item:hover {
  background: #1e293b;
}

.dark .amenity-item.selected {
  background: #1e293b !important;
}

.dark .market-advisor {
  background: rgba(30, 41, 59, 0.4);
  border-color: rgba(99, 102, 241, 0.2);
}

/* ─── Publish Success Overlay ─────────────────────── */
.success-overlay {
  height: 700px;
  max-height: 80vh;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 60%);
  text-align: center;
}

.success-burst {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.burst-ring {
  position: absolute;
  border-radius: 50%;
  border: 3px solid #22c55e;
  animation: burst-expand 1.2s ease-out forwards;
  opacity: 0;
}

.ring-1 { width: 120px; height: 120px; animation-delay: 0s; }
.ring-2 { width: 160px; height: 160px; animation-delay: 0.15s; border-color: #86efac; }
.ring-3 { width: 200px; height: 200px; animation-delay: 0.3s; border-color: #bbf7d0; }

@keyframes burst-expand {
  0%   { transform: scale(0.3); opacity: 0.9; }
  100% { transform: scale(1.3); opacity: 0; }
}

.success-icon-wrap {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 30px rgba(34, 197, 94, 0.4);
  animation: icon-pop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s both;
  z-index: 1;
}

.success-check {
  font-size: 2rem;
  color: white;
}

@keyframes icon-pop {
  0%   { transform: scale(0); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
</style>

