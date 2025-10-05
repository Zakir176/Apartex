<template>
  <div class="bookings-view">
    <h1>My Bookings</h1>
    
    <div v-if="bookingsStore.loading" class="loading">Loading bookings...</div>
    <div v-else-if="bookingsStore.error" class="error">
      {{ bookingsStore.error }}
    </div>
    <div v-else-if="bookings.length === 0" class="no-bookings">
      <p>You don't have any bookings yet.</p>
      <router-link to="/" class="btn-primary">Browse Apartments</router-link>
    </div>
    <div v-else class="bookings-list">
      <div 
        v-for="booking in bookings" 
        :key="booking.id" 
        class="booking-card"
        :class="{'upcoming': isUpcoming(booking), 'completed': isCompleted(booking)}"
      >
        <div class="booking-header">
          <h3>{{ booking.apartment?.title }}</h3>
          <span class="booking-status" :class="booking.status">
            {{ booking.status }}
          </span>
        </div>
        
        <div class="booking-details">
          <div class="detail">
            <strong>Check-in:</strong> {{ formatDate(booking.checkin_date) }}
          </div>
          <div class="detail">
            <strong>Check-out:</strong> {{ formatDate(booking.checkout_date) }}
          </div>
          <div class="detail">
            <strong>Guests:</strong> {{ booking.guests }}
          </div>
          <div class="detail">
            <strong>Total:</strong> ${{ booking.total_price }}
          </div>
        </div>
        
        <div class="booking-actions">
          <button 
            v-if="canCancel(booking)" 
            @click="cancelBooking(booking.id)" 
            class="btn-cancel"
            :disabled="cancellingId === booking.id"
          >
            {{ cancellingId === booking.id ? 'Cancelling...' : 'Cancel' }}
          </button>
          <button 
            v-if="canComplete(booking)" 
            @click="completeBooking(booking.id)" 
            class="btn-complete"
          >
            Mark Complete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '../stores/auth';
import { useLoyaltyStore } from '@/stores/loyalty';

const bookingsStore = useBookingsStore();
const authStore = useAuthStore();
const loyaltyStore = useLoyaltyStore();

const cancellingId = ref(null);

const bookings = computed(() => bookingsStore.bookings);

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

const isUpcoming = (booking) => {
  return new Date(booking.checkin_date) > new Date() && booking.status === 'confirmed';
};

const isCompleted = (booking) => {
  return booking.status === 'completed';
};

const canCancel = (booking) => {
  return booking.status === 'confirmed' && new Date(booking.checkin_date) > new Date();
};

const canComplete = (booking) => {
  return booking.status === 'confirmed' && new Date(booking.checkout_date) < new Date();
};

const cancelBooking = async (bookingId) => {
  if (!confirm('Are you sure you want to cancel this booking?')) return;
  
  cancellingId.value = bookingId;
  try {
    await bookingsStore.cancelBooking(bookingId);
  } catch (error) {
    console.error('Failed to cancel booking:', error);
  } finally {
    cancellingId.value = null;
  }
};

const completeBooking = async (bookingId) => {
  try {
    await loyaltyStore.completeBooking(bookingId);
    // Refresh bookings to update status
    await bookingsStore.fetchUserBookings(authStore.user.id);
  } catch (error) {
    console.error('Failed to complete booking:', error);
  }
};

onMounted(async () => {
  if (authStore.user) {
    await bookingsStore.fetchUserBookings(authStore.user.id);
  }
});
</script>

<style scoped>
.bookings-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
}

.no-bookings {
  text-align: center;
  padding: 3rem;
}

.btn-primary {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  margin-top: 1rem;
}

.booking-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  background: white;
}

.booking-card.upcoming {
  border-left: 4px solid #28a745;
}

.booking-card.completed {
  border-left: 4px solid #6c757d;
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.booking-header h3 {
  margin: 0;
  color: #333;
}

.booking-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}

.booking-status.confirmed {
  background-color: #d4edda;
  color: #155724;
}

.booking-status.completed {
  background-color: #e2e3e5;
  color: #383d41;
}

.booking-status.cancelled {
  background-color: #f8d7da;
  color: #721c24;
}

.booking-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.booking-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-cancel, .btn-complete {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-cancel {
  background-color: #dc3545;
  color: white;
}

.btn-cancel:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.btn-complete {
  background-color: #28a745;
  color: white;
}

.btn-complete:hover {
  background-color: #218838;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
}
</style>