<template>
  <div class="min-h-screen bg-slate-50 py-12 px-6">
    <div class="max-w-[1000px] mx-auto">
      
      <!-- Processing State -->
      <div v-if="loading" class="card-base max-w-lg mx-auto p-12 text-center flex flex-col items-center justify-center">
        <ProgressSpinner style="width: 80px; height: 80px" strokeWidth="4" animationDuration=".5s" class="mb-6" />
        <h2 class="text-3xl font-extrabold text-slate-800 mb-2">Processing Payment</h2>
        <p class="text-slate-500 font-medium">Please do not close this window or click back.</p>
      </div>

      <!-- Success State -->
      <div v-else-if="success" class="card-base max-w-lg mx-auto p-12 text-center flex flex-col items-center justify-center animate-fade-in">
        <div class="w-24 h-24 rounded-full bg-green-50 text-green-500 flex items-center justify-center mb-6 shadow-sm border border-green-100">
          <i class="pi pi-check text-5xl font-bold"></i>
        </div>
        <h2 class="text-3xl font-extrabold text-slate-800 mb-3 tracking-tight">Booking Confirmed!</h2>
        <p class="text-slate-600 font-medium mb-2 leading-relaxed">
          Your payment was successful and <strong>{{ route.query.title }}</strong> is officially locked in for you.
        </p>
        <p class="text-slate-400 text-sm mb-8">A confirmation summary has been added to your account.</p>
        
        <div class="flex flex-col w-full gap-3">
          <button @click="router.push('/bookings')" class="btn-accent shadow-accent w-full text-center justify-center">
            View My Bookings
          </button>
          <button @click="router.push('/apartments')" class="px-5 py-3 rounded-full text-sm font-bold text-slate-600 hover:bg-slate-100 transition-colors w-full text-center">
            Discover More Stays
          </button>
        </div>
      </div>

      <!-- Checkout Form -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-5 gap-8">
        
        <!-- Payment Details (Left) -->
        <div class="lg:col-span-3 flex flex-col gap-6">
          <div class="flex items-center gap-3 mb-2">
            <button @click="router.back()" class="w-10 h-10 rounded-full border border-surface-border bg-white text-slate-600 hover:bg-slate-50 flex items-center justify-center transition-colors">
              <i class="pi pi-arrow-left"></i>
            </button>
            <h1 class="text-3xl font-extrabold text-slate-800">Checkout</h1>
          </div>

          <div class="card-base p-6">
            <h2 class="text-xl font-bold text-slate-800 mb-6">Payment Details</h2>
            
            <div class="bg-blue-50 border border-blue-100 rounded-xl p-4 flex gap-3 items-start mb-8">
              <i class="pi pi-shield text-blue-500 mt-0.5 text-lg"></i>
              <div>
                <p class="text-sm font-bold text-blue-900 mb-1">Simulated Environment</p>
                <p class="text-xs font-medium text-blue-700 m-0 leading-relaxed">This is a demo payment gateway. No real charges will be made to your card.</p>
              </div>
            </div>

            <div class="flex flex-col gap-5">
              <div>
                <label class="label-base">Name on Card</label>
                <input v-model="form.name" class="input-base" placeholder="John Doe" />
              </div>

              <div>
                <label class="label-base">Card Number</label>
                <InputMask v-model="form.cardNumber" mask="9999-9999-9999-9999" placeholder="0000-0000-0000-0000" class="input-base w-full" />
              </div>

              <div class="grid grid-cols-2 gap-5">
                <div>
                  <label class="label-base">Expiry Date</label>
                  <InputMask v-model="form.expiry" mask="99/99" placeholder="MM/YY" class="input-base w-full" />
                </div>
                <div>
                  <label class="label-base">CVV</label>
                  <InputMask v-model="form.cvv" mask="999" placeholder="123" class="input-base w-full" />
                </div>
              </div>
            </div>

            <div v-if="bookingError" class="mt-6 p-4 rounded-xl bg-red-50 border border-red-100 flex items-start gap-3">
              <i class="pi pi-exclamation-circle text-red-500 mt-0.5"></i>
              <p class="text-sm font-medium text-red-700 m-0">{{ bookingError }}</p>
            </div>

            <button 
              @click="processPayment" 
              :disabled="!isFormValid"
              class="btn-accent shadow-accent w-full justify-center mt-8 gap-2 text-base py-4"
              :class="{ 'opacity-50 cursor-not-allowed': !isFormValid }"
            >
              <i class="pi pi-lock"></i>
              Confirm & Pay ${{ finalTotal.toFixed(2) }}
            </button>
          </div>
        </div>

        <!-- Booking Summary (Right) -->
        <div class="lg:col-span-2">
          <div class="card-base p-6 sticky top-24">
            <h3 class="text-lg font-bold text-slate-800 mb-6">Booking Summary</h3>
            
            <div class="bg-slate-50 border border-surface-border rounded-xl p-4 mb-6">
              <p class="font-extrabold text-slate-800 text-lg m-0 mb-1 leading-tight">{{ route.query.title }}</p>
              <p class="text-sm font-medium text-slate-500 m-0 flex items-center gap-1.5"><i class="pi pi-map-marker text-xs"></i> {{ route.query.city || 'Zambia' }}</p>
            </div>
            
            <div class="flex flex-col gap-4 mb-6 pb-6 border-b border-surface-border">
              <div class="flex justify-between items-center text-sm">
                <span class="text-slate-500 font-medium">Check-in</span>
                <span class="font-bold text-slate-800">{{ route.query.check_in }}</span>
              </div>
              <div class="flex justify-between items-center text-sm">
                <span class="text-slate-500 font-medium">Check-out</span>
                <span class="font-bold text-slate-800">{{ route.query.check_out }}</span>
              </div>
              <div class="flex justify-between items-center text-sm">
                <span class="text-slate-500 font-medium">Guests</span>
                <span class="font-bold text-slate-800">{{ route.query.guests }}</span>
              </div>
              <div class="flex justify-between items-center text-sm">
                <span class="text-slate-500 font-medium">Nights</span>
                <span class="font-bold text-slate-800">{{ route.query.nights }}</span>
              </div>
            </div>

            <!-- Loyalty Points -->
            <div class="mb-6 pb-6 border-b border-surface-border" v-if="authStore.user?.loyalty_points > 0">
              <div class="flex justify-between items-center mb-2">
                <span class="font-bold text-slate-800 flex items-center gap-2"><i class="pi pi-star-fill text-accent"></i> Apply Points</span>
                <span class="text-xs font-bold bg-amber-100 text-amber-800 px-2 py-1 rounded-md">{{ authStore.user.loyalty_points }} Available</span>
              </div>
              <p class="text-xs text-slate-500 mb-3 font-medium">100 points = $1.00</p>
              
              <div class="flex gap-3">
                <input type="number" v-model.number="pointsApplied" min="0" :max="maxPointsToApply" class="input-base flex-1 py-2 text-sm" placeholder="0" />
                <button @click="pointsApplied = maxPointsToApply" class="px-3 py-1 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold hover:bg-slate-200 transition-colors">Max</button>
              </div>
              <p v-if="pointsApplied > 0" class="text-green-600 text-sm font-bold mt-2 text-right">-${{ pointsDiscount.toFixed(2) }}</p>
            </div>
            
            <div class="flex justify-between items-center">
              <span class="text-lg font-bold text-slate-800">Total</span>
              <span class="text-2xl font-black text-slate-900 tracking-tight">${{ finalTotal.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '@/stores/auth';

import InputMask from 'primevue/inputmask';
import ProgressSpinner from 'primevue/progressspinner';

const router = useRouter();
const route = useRoute();
const bookingsStore = useBookingsStore();
const authStore = useAuthStore();

const loading = ref(false);
const success = ref(false);
const bookingError = ref('');

const pointsApplied = ref(0);

const baseTotal = computed(() => parseFloat(route.query.total) || 0);
const maxPointsToApply = computed(() => {
  if (!authStore.user) return 0;
  // User cannot apply more points than they have, OR more points than the cost of the booking
  const maxForTotal = Math.floor(baseTotal.value * 100);
  return Math.min(authStore.user.loyalty_points, maxForTotal);
});
const pointsDiscount = computed(() => (pointsApplied.value || 0) / 100);
const finalTotal = computed(() => Math.max(0, baseTotal.value - pointsDiscount.value));

const form = ref({
    name: '',
    cardNumber: '',
    expiry: '',
    cvv: ''
});

const isFormValid = computed(() => {
    return form.value.name.length > 3 && 
           form.value.cardNumber && form.value.cardNumber.replace(/_|-/g, '').length === 16 &&
           form.value.expiry && form.value.expiry.replace(/_|\//g, '').length === 4 &&
           form.value.cvv && form.value.cvv.replace(/_/g, '').length === 3;
});

const processPayment = () => {
    if (!isFormValid.value) return;

    loading.value = true;
    bookingError.value = '';
    
    setTimeout(async () => {
        try {
            const bookingData = {
                apartment_id: parseInt(route.query.apartment_id),
                check_in: route.query.check_in,
                check_out: route.query.check_out,
                guests: parseInt(route.query.guests),
                points_applied: pointsApplied.value || 0
            };
            await bookingsStore.createBooking(bookingData);
            loading.value = false;
            success.value = true;
        } catch (e) {
            loading.value = false;
            bookingError.value = e.response?.data?.detail || 'Booking failed. The dates may no longer be available.';
        }
    }, 2500);
};
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}

:deep(.p-inputmask) {
  border: none;
  background: transparent;
  padding: 0;
  box-shadow: none;
  color: inherit;
  font-family: inherit;
  font-size: inherit;
  outline: none;
  width: 100%;
}
</style>
