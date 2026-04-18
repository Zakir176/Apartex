<template>
  <Card class="booking-card shadow-lg border-round-xl overflow-hidden">
    <template #content>
      <!-- Price Header -->
      <div class="price-header mb-4">
        <span class="text-3xl font-bold">${{ apartment.price_per_night }}</span>
        <span class="text-gray-600 ml-1">/ night</span>
      </div>

      <!-- Form Inputs -->
      <div class="booking-inputs p-fluid">
        <div class="field mb-4">
          <label class="font-bold text-sm block mb-2 uppercase text-gray-500">Dates</label>
          <Calendar 
            v-model="dates" 
            selectionMode="range" 
            :minDate="minDate" 
            placeholder="Select date range"
            iconDisplay="input"
            showIcon
            class="custom-calendar"
            :manualInput="false"
          />
        </div>

        <div class="field mb-5">
          <label class="font-bold text-sm block mb-2 uppercase text-gray-500">Guests</label>
          <Dropdown 
            v-model="form.guests" 
            :options="guestOptions" 
            placeholder="Select guests"
            class="w-full"
          />
        </div>

        <Button 
          label="Reserve — Proceed to Checkout" 
          icon="pi pi-lock"
          :loading="loading" 
          @click="handleBooking" 
          class="p-button-primary p-button-lg w-full font-bold py-3"
          :disabled="!isValidRange || !form.guests"
        />
        
        <p class="text-center text-sm text-gray-500 mt-3"><i class="pi pi-shield mr-1"></i>Secure checkout — You won't be charged yet</p>
      </div>

      <!-- Price Breakdown -->
      <div v-if="isValidRange" class="price-breakdown mt-5 fadein animation-duration-300">
        <div class="flex justify-content-between mb-3 text-gray-700">
          <span>${{ apartment.price_per_night }} x {{ nights }} nights</span>
          <span>${{ subtotal }}</span>
        </div>
        <div class="flex justify-content-between mb-3 text-gray-700">
          <span>Cleaning fee</span>
          <span>$45.00</span>
        </div>
        <div class="flex justify-content-between mb-4 text-gray-700">
          <span>Apartex service fee</span>
          <span>${{ serviceFee }}</span>
        </div>
        
        <Divider />
        
        <div class="flex justify-content-between mt-4 font-bold text-xl text-gray-900">
          <span>Total</span>
          <span>${{ total }}</span>
        </div>
      </div>

      <Message v-if="error" severity="error" class="mt-3">{{ error }}</Message>
    </template>
  </Card>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '../stores/auth';

// PrimeVue components
import Card from 'primevue/card';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import Message from 'primevue/message';
import Divider from 'primevue/divider';

const props = defineProps({
  apartment: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const bookingsStore = useBookingsStore();
const authStore = useAuthStore();

const dates = ref(null);
const minDate = ref(new Date());
const form = ref({
  guests: 1
});

const guestOptions = computed(() => {
  const options = [];
  for (let i = 1; i <= (props.apartment.max_guests || 4); i++) {
    options.push({ label: `${i} ${i === 1 ? 'guest' : 'guests'}`, value: i });
  }
  return options;
});

const loading = ref(false);
const error = ref('');

const isValidRange = computed(() => {
  return dates.value && dates.value[0] && dates.value[1];
});

const nights = computed(() => {
  if (!isValidRange.value) return 0;
  const diff = dates.value[1].getTime() - dates.value[0].getTime();
  return Math.ceil(diff / (1000 * 3600 * 24));
});

const subtotal = computed(() => (props.apartment.price_per_night * nights.value).toFixed(2));
const cleaningFee = 45;
const serviceFee = computed(() => (parseFloat(subtotal.value) * 0.12).toFixed(2));
const total = computed(() => {
  return (parseFloat(subtotal.value) + cleaningFee + parseFloat(serviceFee.value)).toFixed(2);
});

const handleBooking = () => {
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }

  if (!isValidRange.value) return;

  // Navigate to checkout with booking details as query params instead of directly creating
  router.push({
    path: '/checkout',
    query: {
      apartment_id: props.apartment.id,
      check_in: dates.value[0].toISOString().split('T')[0],
      check_out: dates.value[1].toISOString().split('T')[0],
      guests: form.value.guests?.value || form.value.guests,
      total: total.value,
      nights: nights.value,
      title: props.apartment.title
    }
  });
};
</script>

<style scoped>
.booking-card {
  border: 1px solid #f1f5f9;
  border-radius: 1.5rem !important;
}

:deep(.p-card-body) {
  padding: 1.5rem !important;
}

.custom-calendar :deep(.p-inputtext) {
  border-radius: 8px;
  padding: 0.75rem;
}

.price-header {
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 1rem;
}

.p-button-lg {
  border-radius: 12px !important;
}
</style>