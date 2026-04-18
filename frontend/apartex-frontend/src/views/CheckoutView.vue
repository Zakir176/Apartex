<template>
  <div class="checkout-container flex justify-content-center align-items-start min-h-screen py-6 px-3">
    <!-- Processing State -->
    <Card v-if="loading" class="w-full max-w-30rem text-center p-5 shadow-6 border-round-2xl">
      <template #content>
        <ProgressSpinner style="width: 80px; height: 80px" strokeWidth="4" animationDuration=".5s" />
        <h2 class="mt-4 text-2xl font-bold text-gray-800">Processing Payment...</h2>
        <p class="text-gray-500">Please do not close this window.</p>
      </template>
    </Card>

    <!-- Success State -->
    <Card v-else-if="success" class="w-full max-w-30rem text-center p-6 shadow-6 border-round-2xl">
      <template #content>
        <div class="success-animation mb-4">
          <i class="pi pi-check-circle" style="font-size: 5rem; color: #22c55e;"></i>
        </div>
        <h2 class="text-3xl font-bold text-gray-800 mb-2">Booking Confirmed! 🎉</h2>
        <p class="text-gray-600 mb-2">Your payment was successful and <strong>{{ route.query.title }}</strong> is locked in for you.</p>
        <p class="text-gray-500 text-sm mb-5">A confirmation summary has been added to your bookings.</p>
        <Button label="View My Bookings" @click="router.push('/bookings')" class="p-button-success p-button-lg w-full font-bold" />
        <Button label="Discover More Stays" @click="router.push('/apartments')" class="p-button-text w-full mt-2" />
      </template>
    </Card>

    <!-- Checkout Form -->
    <div v-else class="checkout-grid w-full">
      <!-- Booking Summary Sidebar -->
      <Card class="summary-card shadow-3 border-round-2xl">
        <template #content>
          <h3 class="text-lg font-bold mb-4 text-gray-800">Booking Summary</h3>
          <div class="surface-100 border-round-xl p-4 mb-4">
            <p class="font-bold text-900 m-0">{{ route.query.title }}</p>
            <p class="text-sm text-gray-600 mt-1">{{ route.query.city || 'Zambia' }}</p>
          </div>
          <div class="flex justify-content-between text-sm text-gray-700 mb-2">
            <span>Check-in</span><span class="font-bold">{{ route.query.check_in }}</span>
          </div>
          <div class="flex justify-content-between text-sm text-gray-700 mb-2">
            <span>Check-out</span><span class="font-bold">{{ route.query.check_out }}</span>
          </div>
          <div class="flex justify-content-between text-sm text-gray-700 mb-2">
            <span>Guests</span><span class="font-bold">{{ route.query.guests }}</span>
          </div>
          <div class="flex justify-content-between text-sm text-gray-700 mb-4">
            <span>Nights</span><span class="font-bold">{{ route.query.nights }}</span>
          </div>
          <Divider />
          <div class="flex justify-content-between font-bold text-xl text-gray-900">
            <span>Total</span>
            <span>$&nbsp;{{ route.query.total }}</span>
          </div>
        </template>
      </Card>

      <!-- Payment Form -->
      <Card class="payment-card shadow-3 border-round-2xl">
        <template #title>
          <div class="flex align-items-center">
            <Button icon="pi pi-arrow-left" class="p-button-rounded p-button-text p-button-secondary mr-2" @click="router.back()" />
            <h2 class="m-0 text-xl">Payment Details</h2>
          </div>
        </template>
        <template #content>
          <Message severity="info" :closable="false" class="mb-5">
            <i class="pi pi-shield mr-2"></i> This is a <strong>simulated</strong> payment gateway. No real charges will be made.
          </Message>

          <div class="p-fluid">
            <div class="field mb-4">
              <label for="nameOnCard" class="font-bold text-sm text-gray-700 block mb-2">Name on Card</label>
              <InputText id="nameOnCard" v-model="form.name" placeholder="John Doe" />
            </div>

            <div class="field mb-4">
              <label for="cardNumber" class="font-bold text-sm text-gray-700 block mb-2">Card Number</label>
              <InputMask id="cardNumber" v-model="form.cardNumber" mask="9999-9999-9999-9999" placeholder="0000-0000-0000-0000" />
            </div>

            <div class="formgrid grid">
              <div class="field col mb-4">
                <label for="expiry" class="font-bold text-sm text-gray-700 block mb-2">Expiry Date</label>
                <InputMask id="expiry" v-model="form.expiry" mask="99/99" placeholder="MM/YY" />
              </div>
              <div class="field col mb-4">
                <label for="cvv" class="font-bold text-sm text-gray-700 block mb-2">CVV</label>
                <InputMask id="cvv" v-model="form.cvv" mask="999" placeholder="123" />
              </div>
            </div>
          </div>

          <Message v-if="bookingError" severity="error" class="mt-3">{{ bookingError }}</Message>

          <Button
            :label="`Confirm & Pay $${route.query.total}`"
            icon="pi pi-lock"
            @click="processPayment"
            :disabled="!isFormValid"
            class="p-button-primary p-button-lg w-full font-bold mt-3"
          />
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useBookingsStore } from '@/stores/bookings';

import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import InputMask from 'primevue/inputmask';
import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import Message from 'primevue/message';
import Divider from 'primevue/divider';

const router = useRouter();
const route = useRoute();
const bookingsStore = useBookingsStore();

const loading = ref(false);
const success = ref(false);
const bookingError = ref('');

const form = ref({
    name: '',
    cardNumber: '',
    expiry: '',
    cvv: ''
});

const isFormValid = computed(() => {
    return form.value.name.length > 3 && 
           form.value.cardNumber.replace(/_|-/g, '').length === 16 &&
           form.value.expiry.replace(/_|\//g, '').length === 4 &&
           form.value.cvv.replace(/_/g, '').length === 3;
});

const processPayment = () => {
    if (!isFormValid.value) return;

    loading.value = true;
    bookingError.value = '';
    
    // Simulate 2.5s payment processing delay, then actually create the booking
    setTimeout(async () => {
        try {
            const bookingData = {
                apartment_id: parseInt(route.query.apartment_id),
                check_in: route.query.check_in,
                check_out: route.query.check_out,
                guests: parseInt(route.query.guests)
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
.success-animation {
    animation: bounceIn 0.8s ease-out forwards;
}

@keyframes bounceIn {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); opacity: 1; }
}

.checkout-container {
    background: linear-gradient(135deg, #f8fafc 0%, #f0f4ff 100%);
    min-height: 100vh;
}

.checkout-grid {
    max-width: 900px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1.5fr;
    gap: 2rem;
    align-items: start;
}

@media (max-width: 768px) {
  .checkout-grid {
    grid-template-columns: 1fr;
  }
}
</style>
