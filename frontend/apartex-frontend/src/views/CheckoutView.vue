<template>
  <div class="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-[1050px] mx-auto">
      
      <!-- PROCESSING STATE -->
      <div v-if="loading" class="bg-white rounded-3xl border border-slate-200 shadow-xl max-w-lg mx-auto p-12 text-center flex flex-col items-center justify-center my-12">
        <ProgressSpinner style="width: 70px; height: 70px" strokeWidth="4" animationDuration=".6s" class="mb-6" />
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900 mb-2">Securing Reservation...</h2>
        <p class="text-slate-500 font-medium text-xs sm:text-sm max-w-xs">Communicating with payment gateway and locking in your stay dates.</p>
      </div>

      <!-- SUCCESS / CONFIRMED STATE -->
      <div v-else-if="success" class="bg-white rounded-3xl border border-slate-200 shadow-xl max-w-xl mx-auto p-8 sm:p-12 text-center flex flex-col items-center justify-center my-8 animate-fade-in">
        <div class="w-20 h-20 rounded-full bg-emerald-50 text-emerald-500 flex items-center justify-center mb-6 shadow-sm border border-emerald-100">
          <i class="pi pi-check text-4xl font-black"></i>
        </div>

        <span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-black uppercase tracking-widest mb-3">
          Booking Confirmed & Verified
        </span>

        <h2 class="text-3xl font-black text-slate-900 mb-2 tracking-tight">Your Stay is Locked In!</h2>
        
        <div class="bg-slate-50 border border-slate-200/80 rounded-2xl p-4 my-6 w-full text-left flex flex-col gap-2">
          <div class="flex justify-between text-xs font-bold">
            <span class="text-slate-400 uppercase tracking-wider">Booking Reference</span>
            <span class="text-slate-900 font-black font-mono">#{{ bookingReference }}</span>
          </div>
          <div class="flex justify-between text-xs font-bold">
            <span class="text-slate-400 uppercase tracking-wider">Property</span>
            <span class="text-slate-900 font-bold truncate max-w-[200px]">{{ route.query.title }}</span>
          </div>
          <div class="flex justify-between text-xs font-bold">
            <span class="text-slate-400 uppercase tracking-wider">Check-in Date</span>
            <span class="text-slate-900 font-bold">{{ route.query.check_in }}</span>
          </div>
        </div>

        <p class="text-slate-500 text-xs font-medium mb-8 leading-relaxed">
          A confirmation email with check-in instructions and key passcode has been dispatched to your account.
        </p>
        
        <div class="flex flex-col sm:flex-row w-full gap-3">
          <button @click="router.push('/bookings')" class="btn-accent shadow-accent flex-1 text-center justify-center py-3 text-xs font-black">
            View My Reservations
          </button>
          <button @click="router.push('/apartments')" class="px-5 py-3 rounded-full text-xs font-bold text-slate-700 hover:bg-slate-100 transition-colors flex-1 text-center border border-slate-200">
            Explore More Stays
          </button>
        </div>
      </div>

      <!-- CHECKOUT FORM -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-5 gap-8">
        
        <!-- LEFT COLUMN: GUEST DETAILS & PAYMENT -->
        <div class="lg:col-span-3 flex flex-col gap-6">
          <div class="flex items-center gap-3">
            <button @click="router.back()" class="w-9 h-9 rounded-full border border-slate-200 bg-white text-slate-600 hover:bg-slate-100 flex items-center justify-center transition-colors cursor-pointer border-0">
              <i class="pi pi-arrow-left text-xs"></i>
            </button>
            <div>
              <span class="text-[10px] font-black text-accent uppercase tracking-widest">Step 2 of 2</span>
              <h1 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">Confirm & Reserve</h1>
            </div>
          </div>

          <!-- GUEST CONTACT FORM -->
          <div class="bg-white rounded-3xl p-6 sm:p-7 border border-slate-200 shadow-xs flex flex-col gap-4">
            <h2 class="text-base font-black text-slate-900 flex items-center gap-2">
              <i class="pi pi-user text-accent"></i> Guest Information
            </h2>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider block mb-1">Full Name</label>
                <input v-model="guestForm.fullName" type="text" placeholder="John Doe" class="input-base !py-2.5 !text-xs w-full" />
              </div>
              <div>
                <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider block mb-1">Phone Number</label>
                <input v-model="guestForm.phone" type="text" placeholder="+260 971 234 567" class="input-base !py-2.5 !text-xs w-full" />
              </div>
            </div>

            <div>
              <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider block mb-1">Special Requests / Arrival Time (Optional)</label>
              <textarea v-model="guestForm.specialRequests" rows="2" placeholder="e.g. Late check-in, quiet room preference..." class="input-base !py-2 !text-xs w-full resize-none"></textarea>
            </div>
          </div>

          <!-- PAYMENT DETAILS -->
          <div class="bg-white rounded-3xl p-6 sm:p-7 border border-slate-200 shadow-xs flex flex-col gap-5">
            <div class="flex items-center justify-between">
              <h2 class="text-base font-black text-slate-900 flex items-center gap-2">
                <i class="pi pi-credit-card text-accent"></i> Payment Method
              </h2>
              <div class="flex items-center gap-1 text-[10px] font-black text-slate-400 uppercase tracking-widest">
                <i class="pi pi-lock text-emerald-500 text-xs"></i> 256-Bit Encrypted
              </div>
            </div>
            
            <div class="bg-blue-50/80 border border-blue-100 rounded-2xl p-4 flex gap-3 items-start">
              <i class="pi pi-info-circle text-blue-500 mt-0.5 text-base"></i>
              <div>
                <p class="text-xs font-bold text-blue-900 mb-0.5">Simulated Payment Gateway</p>
                <p class="text-[11px] font-medium text-blue-700 m-0 leading-relaxed">This is a sandbox test environment. No real charges will be deducted from your account.</p>
              </div>
            </div>

            <div class="flex flex-col gap-4">
              <div>
                <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider block mb-1">Name on Card</label>
                <input v-model="form.name" class="input-base !py-2.5 !text-xs w-full" placeholder="John Doe" />
              </div>

              <div>
                <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider block mb-1">Card Number</label>
                <div class="relative">
                  <InputMask v-model="form.cardNumber" mask="9999-9999-9999-9999" placeholder="4000-0000-0000-0000" class="input-base !py-2.5 !text-xs w-full !pl-3" />
                  <i class="pi pi-credit-card absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider block mb-1">Expiry Date</label>
                  <InputMask v-model="form.expiry" mask="99/99" placeholder="MM/YY" class="input-base !py-2.5 !text-xs w-full" />
                </div>
                <div>
                  <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider block mb-1">CVV Security Code</label>
                  <InputMask v-model="form.cvv" mask="999" placeholder="123" class="input-base !py-2.5 !text-xs w-full" />
                </div>
              </div>
            </div>

            <div v-if="bookingError" class="p-4 rounded-2xl bg-rose-50 border border-rose-100 flex items-start gap-3">
              <i class="pi pi-exclamation-circle text-rose-500 mt-0.5"></i>
              <p class="text-xs font-bold text-rose-700 m-0 leading-relaxed">{{ bookingError }}</p>
            </div>

            <button 
              @click="processPayment" 
              :disabled="!isFormValid"
              class="btn-accent shadow-accent w-full justify-center mt-4 gap-2 text-xs font-black py-3.5 rounded-full cursor-pointer transition-transform active:scale-98"
              :class="{ 'opacity-50 cursor-not-allowed': !isFormValid }"
            >
              <i class="pi pi-lock text-xs"></i>
              <span>Confirm & Pay {{ formattedFinalTotal }}</span>
            </button>
          </div>
        </div>

        <!-- RIGHT COLUMN: BOOKING ORDER SUMMARY -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-3xl p-6 border border-slate-200 shadow-lg sticky top-24 flex flex-col gap-5">
            <h3 class="text-base font-black text-slate-900">Reservation Summary</h3>
            
            <div class="bg-slate-50 border border-slate-200/80 rounded-2xl p-4">
              <p class="font-black text-slate-900 text-sm m-0 mb-1 leading-snug">{{ route.query.title }}</p>
              <p v-if="route.query.room_name || route.query.room_title" class="text-xs font-bold text-accent m-0 mb-1">
                Room: {{ route.query.room_name || route.query.room_title }}
              </p>
              <p class="text-xs font-bold text-slate-500 m-0 flex items-center gap-1">
                <i class="pi pi-map-marker text-xs text-accent"></i> {{ route.query.city || 'Zambia' }}
              </p>
            </div>
            
            <div class="flex flex-col gap-3 text-xs font-bold text-slate-600 pb-4 border-b border-slate-100">
              <div class="flex justify-between items-center">
                <span class="text-slate-400 font-medium">Check-in</span>
                <span class="text-slate-900">{{ route.query.check_in }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-slate-400 font-medium">Check-out</span>
                <span class="text-slate-900">{{ route.query.check_out }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-slate-400 font-medium">Guests</span>
                <span class="text-slate-900">{{ route.query.guests || 1 }} guest(s)</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-slate-400 font-medium">Duration</span>
                <span class="text-slate-900">{{ route.query.nights }} night(s)</span>
              </div>
            </div>

            <!-- LOYALTY POINTS DISCOUNT INTEGRATION -->
            <div v-if="authStore.user?.loyalty_points > 0" class="pb-4 border-b border-slate-100">
              <div class="flex justify-between items-center mb-2">
                <span class="font-extrabold text-xs text-slate-900 flex items-center gap-1.5">
                  <i class="pi pi-star-fill text-amber-400 text-xs"></i> Apply Loyalty Points
                </span>
                <span class="text-[10px] font-black bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full">
                  {{ authStore.user.loyalty_points }} pts
                </span>
              </div>
              <p class="text-[10px] text-slate-400 font-medium mb-3">100 points = $1.00 discount</p>
              
              <div class="flex gap-2 items-center">
                <input type="number" v-model.number="pointsApplied" min="0" :max="maxPointsToApply" class="input-base !py-1.5 !text-xs flex-1" placeholder="0" />
                <button @click="pointsApplied = maxPointsToApply" class="px-3 py-1.5 bg-slate-100 text-slate-700 rounded-xl text-xs font-black hover:bg-slate-200 transition-colors border-0 cursor-pointer">
                  Max
                </button>
              </div>
              <p v-if="pointsApplied > 0" class="text-emerald-600 text-xs font-black mt-2 text-right">
                -{{ currencyStore.formatPrice(pointsDiscount) }}
              </p>
            </div>
            
            <!-- FINAL ITEMIZED TOTAL -->
            <div class="flex flex-col gap-2 pt-1">
              <div class="flex justify-between items-center text-xs text-slate-500 font-medium">
                <span>Base Nightly Rate</span>
                <span class="font-bold text-slate-700">{{ currencyStore.formatPrice(baseTotal) }}</span>
              </div>
              <div v-if="pointsDiscount > 0" class="flex justify-between items-center text-xs text-emerald-600 font-bold">
                <span>Loyalty Savings</span>
                <span>-{{ currencyStore.formatPrice(pointsDiscount) }}</span>
              </div>
              <div class="flex justify-between items-center pt-3 border-t border-slate-100">
                <span class="text-base font-black text-slate-900">Total Price</span>
                <span class="text-2xl font-black text-slate-900 tracking-tight">{{ formattedFinalTotal }}</span>
              </div>
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
import { useCurrencyStore } from '@/stores/currency';

import InputMask from 'primevue/inputmask';
import ProgressSpinner from 'primevue/progressspinner';

const router = useRouter();
const route = useRoute();
const bookingsStore = useBookingsStore();
const authStore = useAuthStore();
const currencyStore = useCurrencyStore();

const loading = ref(false);
const success = ref(false);
const bookingError = ref('');
const bookingReference = ref('');

const pointsApplied = ref(0);

const guestForm = ref({
  fullName: authStore.user?.full_name || '',
  phone: '',
  specialRequests: ''
});

const baseTotal = computed(() => parseFloat(route.query.total) || 0);

const maxPointsToApply = computed(() => {
  if (!authStore.user) return 0;
  const maxForTotal = Math.floor(baseTotal.value * 100);
  return Math.min(authStore.user.loyalty_points || 0, maxForTotal);
});

const pointsDiscount = computed(() => (pointsApplied.value || 0) / 100);
const finalTotal = computed(() => Math.max(0, baseTotal.value - pointsDiscount.value));

const formattedFinalTotal = computed(() => currencyStore.formatPrice(finalTotal.value));

const form = ref({
  name: authStore.user?.full_name || '',
  cardNumber: '',
  expiry: '',
  cvv: ''
});

const isFormValid = computed(() => {
  return form.value.name.length > 2 && 
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
        property_id: parseInt(route.query.property_id),
        room_id: route.query.room_id ? parseInt(route.query.room_id) : null,
        check_in: route.query.check_in,
        check_out: route.query.check_out,
        guests: parseInt(route.query.guests || 1),
        points_applied: pointsApplied.value || 0
      };
      await bookingsStore.createBooking(bookingData);
      bookingReference.value = 'APT-' + Math.floor(100000 + Math.random() * 900000);
      loading.value = false;
      success.value = true;
    } catch (e) {
      loading.value = false;
      bookingError.value = e.response?.data?.detail || 'Booking failed. The dates may no longer be available.';
    }
  }, 2000);
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

