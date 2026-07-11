<template>
  <div class="max-w-[1400px] mx-auto px-6 py-8 min-h-screen">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
      <div>
        <h1 class="text-4xl font-extrabold text-slate-800 mb-2 m-0">My Reservations</h1>
        <p class="text-slate-500 font-medium text-lg m-0">Track and manage all your upcoming and past stays</p>
      </div>
      <div class="flex gap-2 items-center">
        <SelectButton v-model="activeFilter" :options="filterOptions" optionLabel="label" optionValue="value" class="[&_.p-button]:rounded-lg" />
      </div>
    </div>

    <!-- Stats Row -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8" v-if="!bookingsStore.loading && bookings.length > 0">
      <div class="bg-white border border-surface-border rounded-2xl p-5 flex flex-col gap-2 transition-all duration-250 hover:shadow-md hover:-translate-y-1">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center bg-blue-50 text-blue-500 text-sm mb-1"><i class="pi pi-calendar"></i></div>
        <div class="text-2xl font-extrabold text-slate-800 tracking-tight">{{ stats.total }}</div>
        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Total Trips</div>
      </div>
      <div class="bg-white border border-surface-border rounded-2xl p-5 flex flex-col gap-2 transition-all duration-250 hover:shadow-md hover:-translate-y-1">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center bg-green-50 text-green-500 text-sm mb-1"><i class="pi pi-check-circle"></i></div>
        <div class="text-2xl font-extrabold text-slate-800 tracking-tight">{{ stats.upcoming }}</div>
        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Upcoming</div>
      </div>
      <div class="bg-white border border-surface-border rounded-2xl p-5 flex flex-col gap-2 transition-all duration-250 hover:shadow-md hover:-translate-y-1">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center bg-slate-50 text-slate-500 text-sm mb-1"><i class="pi pi-history"></i></div>
        <div class="text-2xl font-extrabold text-slate-800 tracking-tight">{{ stats.completed }}</div>
        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Completed</div>
      </div>
      <div class="bg-white border border-surface-border rounded-2xl p-5 flex flex-col gap-2 transition-all duration-250 hover:shadow-md hover:-translate-y-1">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center bg-orange-50 text-orange-500 text-sm mb-1"><i class="pi pi-wallet"></i></div>
        <div class="text-2xl font-extrabold text-slate-800 tracking-tight">${{ stats.totalSpent }}</div>
        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Total Spent</div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="bookingsStore.loading" class="flex flex-col gap-4 mt-4">
      <Skeleton v-for="i in 3" :key="i" width="100%" height="160px" class="border-round-xl" />
    </div>

    <!-- Error State -->
    <div v-else-if="bookingsStore.error" class="flex flex-col items-center justify-center text-center py-20 px-8 bg-white border border-surface-border rounded-3xl mt-4">
      <i class="pi pi-exclamation-triangle text-5xl mb-4 text-slate-300"></i>
      <h3 class="text-xl font-bold text-slate-800 mb-2">Something went wrong</h3>
      <p class="text-slate-500 font-medium mb-6">{{ bookingsStore.error }}</p>
      <button @click="loadBookings" class="btn-accent inline-flex items-center gap-2">
        <i class="pi pi-refresh"></i><span>Try Again</span>
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredBookings.length === 0 && bookings.length === 0" class="flex flex-col items-center justify-center text-center py-20 px-8 bg-white border border-surface-border rounded-3xl mt-4">
      <div class="w-20 h-20 rounded-full bg-slate-50 border border-surface-border flex items-center justify-center mb-6">
        <i class="pi pi-calendar text-4xl text-slate-300"></i>
      </div>
      <h3 class="text-2xl font-bold text-slate-800 mb-2">No reservations yet</h3>
      <p class="text-slate-500 font-medium mb-8">Your journey starts here — explore premium stays and book your first experience.</p>
      <router-link to="/apartments" class="btn-accent inline-flex items-center gap-2 no-underline">
        <i class="pi pi-search"></i><span>Discover Properties</span>
      </router-link>
    </div>

    <!-- No results for filter -->
    <div v-else-if="filteredBookings.length === 0" class="flex flex-col items-center justify-center text-center py-20 px-8 bg-white border border-surface-border rounded-3xl mt-4">
      <i class="pi pi-filter-slash text-4xl mb-4 text-slate-300"></i>
      <h3 class="text-xl font-bold text-slate-800 mb-2">No {{ activeFilter }} bookings</h3>
      <p class="text-slate-500 font-medium">Try selecting a different filter above.</p>
    </div>

    <!-- Bookings List -->
    <div v-else class="flex flex-col gap-4">
      <div
        v-for="booking in filteredBookings"
        :key="booking.id"
        class="bg-white border border-surface-border rounded-2xl overflow-hidden transition-all duration-250 hover:shadow-lg hover:-translate-y-1 hover:border-surface-border-strong relative"
        :class="{
          'border-l-[4px] border-l-green-500': isUpcoming(booking), 
          'border-l-[4px] border-l-slate-400': isCompleted(booking), 
          'border-l-[4px] border-l-red-500 opacity-70 hover:opacity-90': booking.status === 'cancelled'
        }"
      >
        <div class="flex flex-col md:flex-row justify-between gap-6 p-6">
          <!-- Left: Image + Info -->
          <div class="flex flex-col md:flex-row gap-6 flex-1 min-w-0">
            <div class="relative w-full md:w-[160px] h-[160px] md:h-[120px] rounded-xl overflow-hidden shrink-0">
              <img
                :src="booking.apartment?.image_url || 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=300&q=80'"
                :alt="booking.apartment?.title || 'Apartment'"
                class="w-full h-full object-cover"
              >
              <div class="absolute top-2 left-2 flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-bold capitalize backdrop-blur-md text-white"
                   :class="booking.status === 'confirmed' ? 'bg-green-500/90' : booking.status === 'completed' ? 'bg-slate-500/90' : 'bg-red-500/90'">
                <i :class="statusIcon(booking.status)" class="text-[10px]"></i>
                {{ booking.status }}
              </div>
            </div>

            <div class="flex flex-col justify-center gap-2 min-w-0">
              <h3 class="text-lg font-extrabold text-slate-800 m-0 truncate">{{ booking.apartment?.title || 'Premium Stay' }}</h3>
              <div class="flex items-center gap-1.5 text-sm font-semibold text-slate-500">
                <i class="pi pi-map-marker text-accent text-xs"></i>
                <span>{{ booking.apartment?.city || 'Zambia' }}</span>
              </div>

              <div class="flex items-center gap-4 mt-2">
                <div class="flex flex-col">
                  <span class="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Check-in</span>
                  <span class="text-sm font-bold text-slate-700">{{ formatDate(booking.check_in) }}</span>
                </div>
                <i class="pi pi-arrow-right text-slate-300 text-xs mt-3"></i>
                <div class="flex flex-col">
                  <span class="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">Check-out</span>
                  <span class="text-sm font-bold text-slate-700">{{ formatDate(booking.check_out) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Price + Actions -->
          <div class="flex flex-row md:flex-col items-center md:items-end justify-between md:justify-between gap-4 md:gap-2 min-w-[150px] flex-wrap">
            <div class="flex flex-col md:items-end">
              <span class="text-[10px] font-bold uppercase tracking-widest text-slate-400">Total</span>
              <span class="text-2xl font-extrabold text-slate-800 tracking-tight">${{ booking.total_price }}</span>
              <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-500 mt-1">
                <i class="pi pi-users text-[10px]"></i>
                <span>{{ booking.guests }} guest{{ booking.guests > 1 ? 's' : '' }}</span>
              </div>
            </div>

            <div class="flex gap-2 flex-wrap md:justify-end w-full md:w-auto mt-2 md:mt-0">
              <button
                v-if="canCancel(booking)"
                @click="handleCancel(booking.id)"
                :disabled="cancellingId === booking.id"
                class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-bold transition-all duration-150 border bg-red-50 text-red-600 border-red-200 hover:bg-red-100 hover:-translate-y-px disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <i class="pi pi-times"></i>
                {{ cancellingId === booking.id ? 'Cancelling...' : 'Cancel' }}
              </button>
              <button
                v-if="canComplete(booking)"
                @click="handleComplete(booking.id)"
                class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-bold transition-all duration-150 border bg-green-50 text-green-600 border-green-200 hover:bg-green-100 hover:-translate-y-px"
              >
                <i class="pi pi-check"></i>
                Complete Stay
              </button>
              <router-link
                v-if="booking.status === 'confirmed'"
                :to="`/apartments/${booking.apartment_id}`"
                class="inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-bold transition-all duration-150 border bg-slate-50 text-slate-600 border-surface-border hover:bg-slate-100 hover:text-slate-900 hover:-translate-y-px no-underline"
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
            <p class="font-bold text-slate-800 m-0">Are you sure?</p>
            <p class="text-slate-500 text-sm m-0 mt-1">This action cannot be undone.</p>
          </div>
        </div>
        <p class="text-slate-600 text-sm leading-relaxed">Your reservation will be cancelled and the dates will become available for others. Any applicable refund will be processed according to the cancellation policy.</p>
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
  return new Date(booking.check_in) > new Date() && booking.status === 'confirmed';
};

const isCompleted = (booking) => {
  return booking.status === 'completed';
};

const canCancel = (booking) => {
  return booking.status === 'confirmed' && new Date(booking.check_in) > new Date();
};

const canComplete = (booking) => {
  return booking.status === 'confirmed' && new Date(booking.check_out) < new Date();
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