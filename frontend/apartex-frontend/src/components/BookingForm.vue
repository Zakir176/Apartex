<template>
  <div class="booking-form">
    <h3>Book This Apartment</h3>
    <form @submit.prevent="handleBooking">
      <div class="form-group">
        <label for="checkin">Check-in Date</label>
        <input
          id="checkin"
          v-model="form.checkin_date"
          type="date"
          required
          :min="today"
        />
      </div>

      <div class="form-group">
        <label for="checkout">Check-out Date</label>
        <input
          id="checkout"
          v-model="form.checkout_date"
          type="date"
          required
          :min="minCheckoutDate"
        />
      </div>

      <div class="form-group">
        <label for="guests">Number of Guests</label>
        <select id="guests" v-model="form.guests" required>
          <option v-for="n in apartment.max_guests" :key="n" :value="n">
            {{ n }} {{ n === 1 ? 'guest' : 'guests' }}
          </option>
        </select>
      </div>

      <div class="price-summary">
        <div class="price-item">
          <span>${{ apartment.price_per_night }} x {{ nights }} nights</span>
          <span>${{ subtotal }}</span>
        </div>
        <div class="price-item">
          <span>Service fee</span>
          <span>${{ serviceFee }}</span>
        </div>
        <div class="price-total">
          <span>Total</span>
          <span>${{ total }}</span>
        </div>
      </div>

      <button 
        type="submit" 
        :disabled="loading || !nights" 
        class="btn-book"
      >
        {{ loading ? 'Booking...' : 'Book Now' }}
      </button>

      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({
  apartment: {
    type: Object,
    required: true
  }
});

const router = useRouter();
const bookingsStore = useBookingsStore();
const authStore = useAuthStore();

const form = ref({
  checkin_date: '',
  checkout_date: '',
  guests: 1
});

const loading = ref(false);
const error = ref('');

const today = computed(() => new Date().toISOString().split('T')[0]);
const minCheckoutDate = computed(() => {
  if (!form.value.checkin_date) return today.value;
  const nextDay = new Date(form.value.checkin_date);
  nextDay.setDate(nextDay.getDate() + 1);
  return nextDay.toISOString().split('T')[0];
});

const nights = computed(() => {
  if (!form.value.checkin_date || !form.value.checkout_date) return 0;
  const checkin = new Date(form.value.checkin_date);
  const checkout = new Date(form.value.checkout_date);
  const diff = checkout.getTime() - checkin.getTime();
  return Math.ceil(diff / (1000 * 3600 * 24));
});

const subtotal = computed(() => (props.apartment.price_per_night * nights.value).toFixed(2));
const serviceFee = computed(() => (subtotal.value * 0.1).toFixed(2));
const total = computed(() => (parseFloat(subtotal.value) + parseFloat(serviceFee.value)).toFixed(2));

watch(() => form.value.checkin_date, () => {
  if (form.value.checkout_date && form.value.checkout_date <= form.value.checkin_date) {
    form.value.checkout_date = minCheckoutDate.value;
  }
});

const handleBooking = async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }

  loading.value = true;
  error.value = '';

  try {
    const bookingData = {
      apartment_id: props.apartment.id,
      ...form.value
    };

    await bookingsStore.createBooking(bookingData);
    router.push('/bookings');
  } catch (err) {
    error.value = err.response?.data?.detail || 'Booking failed';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.booking-form {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.booking-form h3 {
  margin: 0 0 1.5rem 0;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.price-summary {
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.price-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.price-total {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid #ddd;
  font-weight: bold;
}

.btn-book {
  width: 100%;
  padding: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
}

.btn-book:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 1rem;
}
</style>