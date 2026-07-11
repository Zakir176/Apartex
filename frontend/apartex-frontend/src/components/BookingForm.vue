<template>
  <div class="surface-0 p-4 border-round-xl border-1 border-200 shadow-4">
    <!-- Pricing -->
    <div class="flex align-items-baseline gap-2 mb-4">
      <span class="text-3xl font-bold text-900">${{ apartment.price_per_night }}</span>
      <span class="text-500 font-medium">/ night</span>
    </div>

    <!-- Controls Stack -->
    <div class="flex flex-column gap-3 mb-4">
      <div class="ax-field-group mb-0">
        <label class="ax-label">Dates</label>
        <Calendar 
          v-model="dates" 
          selectionMode="range" 
          :minDate="minDate" 
          placeholder="Check-in — Check-out"
          iconDisplay="input"
          inputClass="ax-input"
          :manualInput="false"
          :disabledDates="disabledDates"
        />
      </div>

      <div class="ax-field-group mb-0">
        <label class="ax-label">Guests</label>
        <Dropdown 
          v-model="form.guests" 
          :options="guestOptions" 
          optionLabel="label"
          optionValue="value"
          placeholder="Number of guests"
          class="w-full"
          inputClass="font-medium"
        />
      </div>
    </div>

    <!-- Action -->
    <button 
      class="ax-button w-full mb-3 shadow-lg" 
      :disabled="isOverlapping || loading"
      @click="handleBooking"
    >
      <i class="pi pi-bolt mr-2"></i>
      {{ isValidRange ? 'Reserve Property' : 'Check Availability' }}
    </button>

    <p class="text-center text-xs text-500 font-medium mb-4">Secure hold — you won't be charged yet</p>

    <!-- Price Breakdown -->
    <Transition name="fade">
      <div v-if="isValidRange" class="pt-4 border-top-1 border-100 flex flex-column gap-3">
        <div class="flex justify-content-between text-sm">
          <span class="text-600 underline">${{ apartment.price_per_night }} x {{ nights }} nights</span>
          <span class="font-bold text-900">${{ subtotal }}</span>
        </div>
        <div class="flex justify-content-between text-sm">
          <span class="text-600 underline">Cleaning fee</span>
          <span class="font-bold text-900">$45.00</span>
        </div>
        <div class="flex justify-content-between text-sm">
          <span class="text-600 underline">Service fee</span>
          <span class="font-bold text-900">${{ serviceFee }}</span>
        </div>
        
        <div class="surface-50 p-3 border-round-lg flex justify-content-between align-items-center mt-2">
          <span class="font-bold text-900">Total</span>
          <span class="text-xl font-black text-900">${{ total }}</span>
        </div>
      </div>
    </Transition>

    <Transition name="fade">
      <div v-if="isOverlapping" class="mt-4 p-3 bg-red-50 text-red-600 border-round-lg text-xs font-bold flex align-items-center gap-2">
        <i class="pi pi-exclamation-circle"></i>
        <span>Dates are unavailable.</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '../stores/auth';
import { availabilityApi } from '@/api/availability.js';

// PrimeVue components
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import Message from 'primevue/message';

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
  for (let i = 1; i <= (props.apartment.capacity || 4); i++) {
    options.push({ label: `${i} ${i === 1 ? 'Guest' : 'Guests'}`, value: i });
  }
  return options;
});

const loading = ref(false);
const error = ref('');
const blockedDatesRes = ref([]);

const disabledDates = computed(() => {
  return blockedDatesRes.value.map(bd => new Date(bd.blocked_date + 'T00:00:00'));
});

const isOverlapping = computed(() => {
  if (!isValidRange.value) return false;
  const start = dates.value[0];
  const end = dates.value[1];
  let current = new Date(start);
  while (current <= end) {
    const curStr = current.toISOString().split('T')[0];
    if (blockedDatesRes.value.some(bd => bd.blocked_date === curStr)) return true;
    current.setDate(current.getDate() + 1);
  }
  return false;
});

onMounted(async () => {
  try {
    const res = await availabilityApi.getBlockedDates(props.apartment.id);
    blockedDatesRes.value = res.data;
  } catch (e) {
    console.error('Failed to load blocked dates', e);
  }
});

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

  if (!isValidRange.value) {
    // Scroll to dates if not selected
    return;
  }

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
/* Styling removed */
</style>