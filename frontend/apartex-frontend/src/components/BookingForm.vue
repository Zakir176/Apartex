<template>
  <div class="bg-white border border-surface-border rounded-3xl p-6 shadow-xl">

    <!-- Price -->
    <div class="flex items-baseline gap-2 mb-5">
      <span class="text-3xl font-black text-slate-800">{{ currencyStore.formatPrice(apartment.price_per_night) }}</span>
      <span class="text-sm font-medium text-slate-400">/ night</span>
    </div>

    <!-- Fields -->
    <div class="flex flex-col gap-4 mb-5">
      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-1.5">Dates</label>
        <Calendar
          v-model="dates"
          selectionMode="range"
          :minDate="minDate"
          placeholder="Check-in — Check-out"
          iconDisplay="input"
          inputClass="w-full border border-surface-border rounded-md px-4 py-3 text-sm text-slate-800 outline-none focus:border-accent focus:ring-2 focus:ring-accent-light"
          :manualInput="false"
          :disabledDates="disabledDates"
          class="w-full"
        />
      </div>

      <div>
        <label class="block text-sm font-semibold text-slate-700 mb-1.5">Guests</label>
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

    <!-- Book Button -->
    <button
      class="w-full bg-accent hover:bg-accent-hover disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3.5 rounded-lg text-sm transition-colors duration-150 mb-2 flex items-center justify-center gap-2 shadow-accent"
      :disabled="isOverlapping || loading"
      @click="handleBooking"
    >
      <i class="pi pi-bolt"></i>
      {{ isValidRange ? 'Reserve Property' : 'Check Availability' }}
    </button>

    <p class="text-center text-xs text-slate-400 font-medium mb-4">Secure hold — you won't be charged yet</p>

    <!-- Price Breakdown -->
    <Transition name="fade">
      <div v-if="isValidRange" class="pt-4 border-t border-surface-border flex flex-col gap-3">
        <div class="flex justify-between text-sm">
          <span class="text-slate-500 underline">{{ currencyStore.formatPrice(apartment.price_per_night) }} × {{ nights }} nights</span>
          <span class="font-bold text-slate-800">{{ currencyStore.formatPrice(subtotal) }}</span>
        </div>
        <div class="flex justify-between text-sm">
          <span class="text-slate-500 underline">Cleaning fee</span>
          <span class="font-bold text-slate-800">{{ currencyStore.formatPrice(45) }}</span>
        </div>
        <div class="flex justify-between text-sm">
          <span class="text-slate-500 underline">Service fee</span>
          <span class="font-bold text-slate-800">{{ currencyStore.formatPrice(serviceFee) }}</span>
        </div>
        <div class="bg-[#F8F7F4] rounded-lg px-4 py-3 flex justify-between items-center mt-1">
          <span class="font-bold text-slate-800">Total</span>
          <span class="text-xl font-black text-slate-800">{{ currencyStore.formatPrice(total) }}</span>
        </div>
      </div>
    </Transition>

    <!-- Overlap Warning -->
    <Transition name="fade">
      <div v-if="isOverlapping" class="mt-4 bg-red-50 border border-red-200 text-red-600 rounded-lg px-4 py-3 text-xs font-bold flex items-center gap-2">
        <i class="pi pi-exclamation-circle"></i>
        <span>These dates are unavailable. Please choose different dates.</span>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '@/stores/auth';
import { useCurrencyStore } from '@/stores/currency';
import { availabilityApi } from '@/api/availability.js';

// PrimeVue components
import Calendar from 'primevue/calendar';
import Dropdown from 'primevue/dropdown';

const props = defineProps({
  apartment: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const bookingsStore = useBookingsStore();
const authStore = useAuthStore();
const currencyStore = useCurrencyStore();

const dates = ref(null);
const minDate = ref(new Date());
const form = ref({
  guests: 1
});

const formattedNightlyRate = computed(() => {
  return currencyStore.formatPrice(props.apartment.price_per_night);
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

const isValidRange = computed(() => {
  return dates.value && dates.value[0] && dates.value[1];
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
    blockedDatesRes.value = res.data || [];
  } catch (e) {
    console.error('Failed to load blocked dates', e);
  }
});

const nights = computed(() => {
  if (!isValidRange.value) return 0;
  const diff = dates.value[1].getTime() - dates.value[0].getTime();
  return Math.max(1, Math.ceil(diff / (1000 * 3600 * 24)));
});

const subtotalUSD = computed(() => props.apartment.price_per_night * nights.value);
const cleaningFeeUSD = 25;
const serviceFeeUSD = computed(() => subtotalUSD.value * 0.08);
const totalUSD = computed(() => subtotalUSD.value + cleaningFeeUSD + serviceFeeUSD.value);

const formattedSubtotal = computed(() => currencyStore.formatPrice(subtotalUSD.value));
const formattedCleaningFee = computed(() => currencyStore.formatPrice(cleaningFeeUSD));
const formattedServiceFee = computed(() => currencyStore.formatPrice(serviceFeeUSD.value));
const formattedTotal = computed(() => currencyStore.formatPrice(totalUSD.value));

const handleBooking = () => {
  if (!authStore.isAuthenticated) {
    router.push({
      path: '/login',
      query: { redirect: `/apartments/${props.apartment.id}` }
    });
    return;
  }

  if (!isValidRange.value) {
    return;
  }

  router.push({
    path: '/checkout',
    query: {
      apartment_id: props.apartment.id,
      check_in: dates.value[0].toISOString().split('T')[0],
      check_out: dates.value[1].toISOString().split('T')[0],
      guests: form.value.guests?.value || form.value.guests,
      total: totalUSD.value,
      nights: nights.value,
      title: props.apartment.title
    }
  });
};
</script>