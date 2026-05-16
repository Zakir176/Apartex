<template>
  <div class="ax-container py-8 fadein animation-duration-500">
    <!-- Page Header -->
    <div class="flex flex-column md:flex-row md:align-items-end justify-content-between mb-8 gap-4">
      <div>
        <h1 class="text-5xl font-bold text-900 mb-2">My Reservations</h1>
        <p class="text-500 font-medium text-lg m-0">Track and manage all your upcoming and past stays</p>
      </div>
      <div class="flex gap-2 align-items-center">
        <SelectButton v-model="activeFilter" :options="filterOptions" optionLabel="label" optionValue="value" class="filter-select" />
      </div>
    </div>

    <!-- Stats Row -->
    <div class="grid mb-6" v-if="!bookingsStore.loading && bookings.length > 0">
      <div class="col-6 md:col-3 p-2">
        <div class="stat-card">
          <div class="stat-icon bg-blue-50"><i class="pi pi-calendar text-blue-500"></i></div>
          <div class="stat-value">{{ stats.total }}</div>
          <div class="stat-label">Total Trips</div>
        </div>
      </div>
      <div class="col-6 md:col-3 p-2">
        <div class="stat-card">
          <div class="stat-icon bg-green-50"><i class="pi pi-check-circle text-green-500"></i></div>
          <div class="stat-value">{{ stats.upcoming }}</div>
          <div class="stat-label">Upcoming</div>
        </div>
      </div>
      <div class="col-6 md:col-3 p-2">
        <div class="stat-card">
          <div class="stat-icon bg-purple-50"><i class="pi pi-history text-purple-500"></i></div>
          <div class="stat-value">{{ stats.completed }}</div>
          <div class="stat-label">Completed</div>
        </div>
      </div>
      <div class="col-6 md:col-3 p-2">
        <div class="stat-card">
          <div class="stat-icon bg-orange-50"><i class="pi pi-wallet text-orange-500"></i></div>
          <div class="stat-value">${{ stats.totalSpent }}</div>
          <div class="stat-label">Total Spent</div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="bookingsStore.loading" class="flex flex-column gap-4 mt-4">
      <Skeleton v-for="i in 3" :key="i" width="100%" height="160px" class="border-round-xl" />
    </div>

    <!-- Error State -->
    <div v-else-if="bookingsStore.error" class="empty-state-card">
      <i class="pi pi-exclamation-triangle text-5xl mb-4" style="color: var(--surface-300)"></i>
      <h3 class="text-xl font-bold text-900 mb-2">Something went wrong</h3>
      <p class="text-500 font-medium mb-4">{{ bookingsStore.error }}</p>
      <button @click="loadBookings" class="ax-button">
        <i class="pi pi-refresh"></i><span>Try Again</span>
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredBookings.length === 0 && bookings.length === 0" class="empty-state-card">
      <div class="empty-icon-circle mb-5">
        <i class="pi pi-calendar text-4xl" style="color: var(--surface-300)"></i>
      </div>
      <h3 class="text-2xl font-bold text-900 mb-2">No reservations yet</h3>
      <p class="text-500 font-medium mb-5">Your journey starts here — explore premium stays and book your first experience.</p>
      <router-link to="/apartments" class="ax-button" style="text-decoration: none">
        <i class="pi pi-search"></i><span>Discover Properties</span>
      </router-link>
    </div>

    <!-- No results for filter -->
    <div v-else-if="filteredBookings.length === 0" class="empty-state-card">
      <i class="pi pi-filter-slash text-4xl mb-4" style="color: var(--surface-300)"></i>
      <h3 class="text-xl font-bold text-900 mb-2">No {{ activeFilter }} bookings</h3>
      <p class="text-500 font-medium">Try selecting a different filter above.</p>
    </div>

    <!-- Bookings List -->
    <div v-else class="flex flex-column gap-4">
      <div
        v-for="booking in filteredBookings"
        :key="booking.id"
        class="booking-card"
        :class="{'card-upcoming': isUpcoming(booking), 'card-completed': isCompleted(booking), 'card-cancelled': booking.status === 'cancelled'}"
      >
        <div class="booking-card-inner">
          <!-- Left: Image + Info -->
          <div class="booking-main">
            <div class="booking-thumbnail">
              <img
                :src="booking.apartment?.image_url || 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=300&q=80'"
                :alt="booking.apartment?.title || 'Apartment'"
              >
              <div class="status-pill" :class="booking.status">
                <i :class="statusIcon(booking.status)"></i>
                {{ booking.status }}
              </div>
            </div>

            <div class="booking-info">
              <h3 class="booking-title">{{ booking.apartment?.title || 'Premium Stay' }}</h3>
              <div class="booking-location">
                <i class="pi pi-map-marker"></i>
                <span>{{ booking.apartment?.city || 'Zambia' }}</span>
              </div>

              <div class="booking-dates-row">
                <div class="date-block">
                  <span class="date-label">Check-in</span>
                  <span class="date-value">{{ formatDate(booking.checkin_date) }}</span>
                </div>
                <div class="date-arrow">
                  <i class="pi pi-arrow-right"></i>
                </div>
                <div class="date-block">
                  <span class="date-label">Check-out</span>
                  <span class="date-value">{{ formatDate(booking.checkout_date) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Price + Actions -->
          <div class="booking-actions-col">
            <div class="booking-price">
              <span class="price-label">Total</span>
              <span class="price-value">${{ booking.total_price }}</span>
            </div>
            <div class="booking-guests">
              <i class="pi pi-users"></i>
              <span>{{ booking.guests }} guest{{ booking.guests > 1 ? 's' : '' }}</span>
            </div>

            <div class="action-buttons">
              <button
                v-if="canCancel(booking)"
                @click="handleCancel(booking.id)"
                :disabled="cancellingId === booking.id"
                class="btn-action btn-cancel-action"
              >
                <i class="pi pi-times"></i>
                {{ cancellingId === booking.id ? 'Cancelling...' : 'Cancel' }}
              </button>
              <button
                v-if="canComplete(booking)"
                @click="handleComplete(booking.id)"
                class="btn-action btn-complete-action"
              >
                <i class="pi pi-check"></i>
                Complete Stay
              </button>
              <router-link
                v-if="booking.status === 'confirmed'"
                :to="`/apartments/${booking.apartment_id}`"
                class="btn-action btn-view-action"
              >
                <i class="pi pi-eye"></i>
                View Property
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cancel Confirmation Dialog -->
    <Dialog v-model:visible="showCancelDialog" modal header="Cancel Reservation" :style="{ width: '420px' }">
      <div class="py-2">
        <div class="flex align-items-center gap-3 mb-4">
          <div class="w-3rem h-3rem border-round-xl bg-red-50 flex align-items-center justify-content-center">
            <i class="pi pi-exclamation-triangle text-red-500 text-xl"></i>
          </div>
          <div>
            <p class="font-bold text-900 m-0">Are you sure?</p>
            <p class="text-500 text-sm m-0 mt-1">This action cannot be undone.</p>
          </div>
        </div>
        <p class="text-600 text-sm line-height-3">Your reservation will be cancelled and the dates will become available for others. Any applicable refund will be processed according to the cancellation policy.</p>
      </div>
      <template #footer>
        <div class="flex gap-2 justify-content-end">
          <Button label="Keep Booking" @click="showCancelDialog = false" class="p-button-text p-button-secondary font-bold" />
          <Button label="Cancel Reservation" icon="pi pi-times" @click="confirmCancel" :loading="cancellingId !== null" class="p-button-danger font-bold" />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '@/stores/auth';
import { useLoyaltyStore } from '@/stores/loyalty';

// PrimeVue components
import SelectButton from 'primevue/selectbutton';
import Skeleton from 'primevue/skeleton';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

const bookingsStore = useBookingsStore();
const authStore = useAuthStore();
const loyaltyStore = useLoyaltyStore();

const cancellingId = ref(null);
const showCancelDialog = ref(false);
const pendingCancelId = ref(null);
const activeFilter = ref('all');

const filterOptions = [
  { label: 'All', value: 'all' },
  { label: 'Upcoming', value: 'upcoming' },
  { label: 'Completed', value: 'completed' },
  { label: 'Cancelled', value: 'cancelled' }
];

const bookings = computed(() => bookingsStore.bookings);

const stats = computed(() => {
  const all = bookings.value;
  return {
    total: all.length,
    upcoming: all.filter(b => isUpcoming(b)).length,
    completed: all.filter(b => b.status === 'completed').length,
    totalSpent: all
      .filter(b => b.status !== 'cancelled')
      .reduce((sum, b) => sum + (b.total_price || 0), 0)
      .toLocaleString()
  };
});

const filteredBookings = computed(() => {
  if (activeFilter.value === 'all') return bookings.value;
  if (activeFilter.value === 'upcoming') return bookings.value.filter(b => isUpcoming(b));
  if (activeFilter.value === 'completed') return bookings.value.filter(b => b.status === 'completed');
  if (activeFilter.value === 'cancelled') return bookings.value.filter(b => b.status === 'cancelled');
  return bookings.value;
});

const formatDate = (dateString) => {
  if (!dateString) return '—';
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric'
  });
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

const statusIcon = (status) => {
  const icons = {
    confirmed: 'pi pi-check-circle',
    completed: 'pi pi-verified',
    cancelled: 'pi pi-times-circle'
  };
  return icons[status] || 'pi pi-info-circle';
};

const handleCancel = (bookingId) => {
  pendingCancelId.value = bookingId;
  showCancelDialog.value = true;
};

const confirmCancel = async () => {
  cancellingId.value = pendingCancelId.value;
  try {
    await bookingsStore.cancelBooking(pendingCancelId.value);
  } catch (error) {
    console.error('Failed to cancel booking:', error);
  } finally {
    cancellingId.value = null;
    showCancelDialog.value = false;
    pendingCancelId.value = null;
  }
};

const handleComplete = async (bookingId) => {
  try {
    await loyaltyStore.completeBooking(bookingId);
    await bookingsStore.fetchUserBookings(authStore.user.id);
  } catch (error) {
    console.error('Failed to complete booking:', error);
  }
};

const loadBookings = async () => {
  if (authStore.user) {
    await bookingsStore.fetchUserBookings(authStore.user.id);
  }
};

onMounted(loadBookings);
</script>

<style scoped>
/* Stats cards */
.stat-card {
  background: var(--surface-0);
  border: 1px solid var(--surface-100);
  border-radius: 1rem;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: var(--transition);
}

.stat-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.stat-icon {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: var(--surface-900);
  letter-spacing: -0.025em;
}

.stat-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--surface-400);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Empty state */
.empty-state-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 5rem 2rem;
  background: var(--surface-0);
  border: 1px solid var(--surface-100);
  border-radius: 1.5rem;
  margin-top: 1rem;
}

.empty-icon-circle {
  width: 5rem;
  height: 5rem;
  border-radius: 50%;
  background: var(--surface-50);
  border: 1px solid var(--surface-100);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Booking card */
.booking-card {
  background: var(--surface-0);
  border: 1px solid var(--surface-100);
  border-radius: 1.25rem;
  overflow: hidden;
  transition: var(--transition);
}

.booking-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
  border-color: var(--surface-200);
}

.booking-card.card-upcoming {
  border-left: 4px solid #22c55e;
}

.booking-card.card-completed {
  border-left: 4px solid var(--surface-300);
}

.booking-card.card-cancelled {
  border-left: 4px solid #ef4444;
  opacity: 0.7;
}

.booking-card.card-cancelled:hover {
  opacity: 0.85;
}

.booking-card-inner {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  padding: 1.5rem;
}

/* Left section */
.booking-main {
  display: flex;
  gap: 1.5rem;
  flex: 1;
  min-width: 0;
}

.booking-thumbnail {
  position: relative;
  width: 140px;
  min-width: 140px;
  height: 120px;
  border-radius: 1rem;
  overflow: hidden;
  flex-shrink: 0;
}

.booking-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.status-pill {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.625rem;
  border-radius: 999px;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: capitalize;
  backdrop-filter: blur(8px);
}

.status-pill.confirmed {
  background: rgba(34, 197, 94, 0.9);
  color: #fff;
}

.status-pill.completed {
  background: rgba(100, 116, 139, 0.85);
  color: #fff;
}

.status-pill.cancelled {
  background: rgba(239, 68, 68, 0.85);
  color: #fff;
}

.status-pill i {
  font-size: 0.625rem;
}

.booking-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.5rem;
  min-width: 0;
}

.booking-title {
  font-size: 1.125rem;
  font-weight: 800;
  color: var(--surface-900);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.booking-location {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--surface-400);
}

.booking-location i {
  color: var(--primary-500);
  font-size: 0.75rem;
}

.booking-dates-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.25rem;
}

.date-block {
  display: flex;
  flex-direction: column;
}

.date-label {
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--surface-400);
}

.date-value {
  font-size: 0.8125rem;
  font-weight: 700;
  color: var(--surface-700);
}

.date-arrow {
  color: var(--surface-300);
  font-size: 0.75rem;
  margin-top: 0.625rem;
}

/* Right section */
.booking-actions-col {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
  gap: 0.5rem;
  min-width: 150px;
}

.booking-price {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.price-label {
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--surface-400);
}

.price-value {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--surface-900);
  letter-spacing: -0.025em;
}

.booking-guests {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--surface-400);
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  border-radius: 0.625rem;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition);
  border: 1px solid transparent;
  text-decoration: none;
}

.btn-cancel-action {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}

.btn-cancel-action:hover:not(:disabled) {
  background: #fee2e2;
  transform: translateY(-1px);
}

.btn-cancel-action:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-complete-action {
  background: #f0fdf4;
  color: #16a34a;
  border-color: #bbf7d0;
}

.btn-complete-action:hover {
  background: #dcfce7;
  transform: translateY(-1px);
}

.btn-view-action {
  background: var(--surface-50);
  color: var(--surface-600);
  border-color: var(--surface-200);
}

.btn-view-action:hover {
  background: var(--surface-100);
  color: var(--surface-900);
  transform: translateY(-1px);
}

/* Filter override */
.filter-select :deep(.p-selectbutton) {
  border-radius: 0.75rem;
}

/* Responsive */
@media (max-width: 768px) {
  .booking-card-inner {
    flex-direction: column;
    gap: 1rem;
  }

  .booking-main {
    flex-direction: column;
  }

  .booking-thumbnail {
    width: 100%;
    height: 160px;
  }

  .booking-actions-col {
    flex-direction: row;
    align-items: center;
    flex-wrap: wrap;
    min-width: 0;
  }

  .booking-price {
    align-items: flex-start;
  }

  .action-buttons {
    justify-content: flex-start;
  }

  .stat-value {
    font-size: 1.375rem;
  }
}
</style>