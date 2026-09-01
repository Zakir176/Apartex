<template>
  <div class="max-w-[1250px] mx-auto px-4 sm:px-6 py-8 min-h-screen">
    <!-- PAGE HEADER -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
      <div>
        <span class="text-xs font-black uppercase tracking-widest text-accent mb-1 block">Guest Portal</span>
        <h1 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">My Reservations</h1>
        <p class="text-slate-500 font-medium text-xs sm:text-sm mt-1">Track and manage all your upcoming and past stay reservations across Zambia.</p>
      </div>

      <!-- Filter Tabs -->
      <div class="flex items-center gap-1.5 bg-white p-1 rounded-full border border-slate-200 shadow-2xs self-start md:self-auto overflow-x-auto">
        <button
          v-for="opt in filterOptions"
          :key="opt.value"
          @click="activeFilter = opt.value"
          class="px-4 py-2 rounded-full text-xs font-black transition-all cursor-pointer border-0 whitespace-nowrap"
          :class="activeFilter === opt.value ? 'bg-slate-900 text-white shadow-xs' : 'text-slate-500 hover:text-slate-900 bg-transparent'"
        >
          {{ opt.label }}
        </button>
      </div>
    </div>

    <!-- STATS ROW -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8" v-if="!bookingsStore.loading && bookings.length > 0">
      <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-xs">
        <span class="block text-slate-400 text-[10px] sm:text-xs font-black uppercase tracking-wider mb-1">Total Reservations</span>
        <span class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">{{ stats.total }}</span>
        <p class="text-[11px] text-slate-500 font-medium mt-0.5">Lifetime bookings</p>
      </div>

      <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-xs">
        <span class="block text-slate-400 text-[10px] sm:text-xs font-black uppercase tracking-wider mb-1">Upcoming Stays</span>
        <span class="text-2xl sm:text-3xl font-black text-accent tracking-tight">{{ stats.upcoming }}</span>
        <p class="text-[11px] text-slate-500 font-medium mt-0.5">Ready for check-in</p>
      </div>

      <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-xs">
        <span class="block text-slate-400 text-[10px] sm:text-xs font-black uppercase tracking-wider mb-1">Completed Trips</span>
        <span class="text-2xl sm:text-3xl font-black text-emerald-600 tracking-tight">{{ stats.completed }}</span>
        <p class="text-[11px] text-emerald-600 font-bold mt-0.5">Verified experiences</p>
      </div>

      <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-xs">
        <span class="block text-slate-400 text-[10px] sm:text-xs font-black uppercase tracking-wider mb-1">Total Spent</span>
        <span class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">{{ formattedTotalSpent }}</span>
        <p class="text-[11px] text-slate-500 font-medium mt-0.5">Across all stays</p>
      </div>
    </div>

    <!-- LOADING STATE -->
    <div v-if="bookingsStore.loading" class="flex flex-col gap-4">
      <Skeleton v-for="i in 3" :key="i" width="100%" height="140px" class="rounded-2xl" />
    </div>

    <!-- ERROR STATE -->
    <div v-else-if="bookingsStore.error" class="bg-white border border-slate-200 rounded-3xl p-12 text-center max-w-md mx-auto my-8 shadow-sm">
      <i class="pi pi-exclamation-triangle text-4xl text-rose-500 mb-3"></i>
      <h3 class="text-lg font-black text-slate-900 mb-1">Unable to Load Reservations</h3>
      <p class="text-xs text-slate-500 mb-6 font-medium">{{ bookingsStore.error }}</p>
      <button @click="loadBookings" class="btn-accent px-6 py-2.5 rounded-full text-xs font-black inline-flex items-center gap-2">
        <i class="pi pi-refresh"></i><span>Try Again</span>
      </button>
    </div>

    <!-- EMPTY STATE -->
    <div v-else-if="filteredBookings.length === 0 && bookings.length === 0" class="bg-white border border-slate-200 rounded-3xl p-12 text-center max-w-md mx-auto my-8 shadow-sm">
      <div class="w-16 h-16 rounded-full bg-orange-50 text-accent flex items-center justify-center text-2xl mx-auto mb-4 border border-orange-100">
        <i class="pi pi-calendar"></i>
      </div>
      <h3 class="text-xl font-black text-slate-900 mb-2">No Reservations Yet</h3>
      <p class="text-xs text-slate-500 mb-6 font-medium leading-relaxed">Your journey begins here. Explore luxury stays and book your first stay.</p>
      <router-link to="/apartments" class="btn-accent px-6 py-3 rounded-full text-xs font-black inline-flex items-center gap-2 no-underline">
        <i class="pi pi-search"></i><span>Explore Stays</span>
      </router-link>
    </div>

    <!-- NO RESULTS FOR FILTER -->
    <div v-else-if="filteredBookings.length === 0" class="bg-white border border-slate-200 rounded-3xl p-12 text-center max-w-md mx-auto my-8 shadow-sm">
      <i class="pi pi-filter-slash text-3xl text-slate-300 mb-3"></i>
      <h3 class="text-lg font-black text-slate-900 mb-1">No {{ activeFilter }} reservations</h3>
      <p class="text-xs text-slate-500 font-medium">Select a different tab filter to view your stays.</p>
    </div>

    <!-- BOOKINGS LIST -->
    <div v-else class="flex flex-col gap-4">
      <div
        v-for="booking in filteredBookings"
        :key="booking.id"
        class="bg-white border border-slate-200/90 rounded-3xl p-5 sm:p-6 shadow-xs hover:shadow-md transition-all flex flex-col md:flex-row justify-between gap-6"
      >
        <!-- Left: Image & Info -->
        <div class="flex flex-col sm:flex-row gap-5 flex-1 min-w-0">
          <div class="relative w-full sm:w-44 h-40 sm:h-32 rounded-2xl overflow-hidden bg-slate-100 shrink-0">
            <img
              :src="booking.apartment?.image_url || 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=400&q=80'"
              :alt="booking.apartment?.title || 'Apartment'"
              class="w-full h-full object-cover"
            />
            <div class="absolute top-2.5 left-2.5 px-2.5 py-1 rounded-full text-[10px] font-black uppercase tracking-wider backdrop-blur-md text-white shadow-xs"
                 :class="booking.status === 'confirmed' ? 'bg-emerald-600/90' : booking.status === 'completed' ? 'bg-slate-900/90' : 'bg-rose-500/90'">
              <i :class="statusIcon(booking.status)" class="text-[9px] mr-1"></i>
              {{ booking.status }}
            </div>
          </div>

          <div class="flex flex-col justify-between min-w-0">
            <div>
              <div class="flex items-center gap-1 text-accent text-[10px] font-black uppercase tracking-widest mb-1">
                <i class="pi pi-map-marker text-[10px]"></i>
                {{ booking.apartment?.city || 'Zambia' }}
              </div>
              <h3 class="text-base sm:text-lg font-black text-slate-900 m-0 truncate" :title="booking.apartment?.title">
                {{ booking.apartment?.title || 'Luxury Stay' }}
              </h3>
            </div>

            <!-- Dates strip -->
            <div class="flex items-center gap-4 mt-3 bg-slate-50 p-3 rounded-2xl border border-slate-100">
              <div>
                <span class="block text-[10px] font-black text-slate-400 uppercase tracking-wider">Check-in</span>
                <span class="text-xs font-black text-slate-800">{{ formatDate(booking.check_in) }}</span>
              </div>
              <i class="pi pi-arrow-right text-slate-300 text-xs"></i>
              <div>
                <span class="block text-[10px] font-black text-slate-400 uppercase tracking-wider">Check-out</span>
                <span class="text-xs font-black text-slate-800">{{ formatDate(booking.check_out) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Pricing & Actions -->
        <div class="flex flex-row md:flex-col items-center md:items-end justify-between md:justify-between border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0 md:pl-6 min-w-[170px]">
          <div class="flex flex-col md:items-end">
            <span class="text-[10px] font-black text-slate-400 uppercase tracking-wider">Total Cost</span>
            <span class="text-2xl font-black text-slate-900 tracking-tight">{{ currencyStore.formatPrice(booking.total_price || 0) }}</span>
            <span class="text-[11px] font-bold text-slate-500">{{ booking.guests || 1 }} guest(s)</span>
          </div>

          <div class="flex items-center gap-2 mt-2">
            <button
              v-if="canCancel(booking)"
              @click="handleCancel(booking.id)"
              :disabled="cancellingId === booking.id"
              class="px-3.5 py-2 rounded-full text-xs font-black text-rose-600 bg-rose-50 border border-rose-100 hover:bg-rose-100 transition-colors cursor-pointer"
            >
              {{ cancellingId === booking.id ? 'Cancelling...' : 'Cancel' }}
            </button>
            
            <button
              v-if="canComplete(booking)"
              @click="handleComplete(booking.id)"
              class="px-3.5 py-2 rounded-full text-xs font-black text-emerald-700 bg-emerald-50 border border-emerald-100 hover:bg-emerald-100 transition-colors cursor-pointer"
            >
              Complete Stay
            </button>

            <router-link
              v-if="booking.apartment_id"
              :to="`/apartments/${booking.apartment_id}`"
              class="px-3.5 py-2 rounded-full text-xs font-black text-slate-700 bg-slate-100 hover:bg-slate-200 transition-colors no-underline inline-flex items-center gap-1"
            >
              <span>Details</span> <i class="pi pi-arrow-right text-[10px]"></i>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- CANCEL DIALOG -->
    <Dialog v-model:visible="showCancelDialog" modal header="Cancel Reservation" :style="{ width: '420px', maxWidth: '95vw' }">
      <div class="py-2 flex flex-col gap-3">
        <p class="text-xs font-bold text-slate-700 m-0">Are you sure you want to cancel this reservation?</p>
        <p class="text-xs text-slate-500 font-medium leading-relaxed m-0">Your reservation will be released back to the stay directory. Any eligible refund will be returned to your payment method.</p>
      </div>
      <template #footer>
        <div class="flex gap-2 justify-end pt-3 border-t border-slate-100">
          <button @click="showCancelDialog = false" class="px-4 py-2 rounded-full text-xs font-bold text-slate-500 hover:bg-slate-100 border-0 bg-transparent cursor-pointer">
            Keep Booking
          </button>
          <button @click="confirmCancel" :disabled="cancellingId !== null" class="px-5 py-2 rounded-full text-xs font-black text-white bg-rose-600 hover:bg-rose-700 transition-colors border-0 cursor-pointer">
            {{ cancellingId !== null ? 'Cancelling...' : 'Confirm Cancel' }}
          </button>
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
import { useCurrencyStore } from '@/stores/currency';

import Skeleton from 'primevue/skeleton';
import Dialog from 'primevue/dialog';

const bookingsStore = useBookingsStore();
const authStore = useAuthStore();
const loyaltyStore = useLoyaltyStore();
const currencyStore = useCurrencyStore();

const cancellingId = ref(null);
const showCancelDialog = ref(false);
const pendingCancelId = ref(null);
const activeFilter = ref('all');

const filterOptions = [
  { label: 'All Trips', value: 'all' },
  { label: 'Upcoming', value: 'upcoming' },
  { label: 'Completed', value: 'completed' },
  { label: 'Cancelled', value: 'cancelled' }
];

const bookings = computed(() => bookingsStore.bookings);

const stats = computed(() => {
  const all = bookings.value;
  const totalSpentVal = all
    .filter(b => b.status !== 'cancelled')
    .reduce((sum, b) => sum + Number(b.total_price || 0), 0);

  return {
    total: all.length,
    upcoming: all.filter(b => isUpcoming(b)).length,
    completed: all.filter(b => b.status === 'completed').length,
    totalSpentVal
  };
});

const formattedTotalSpent = computed(() => {
  return currencyStore.formatPrice(stats.value.totalSpentVal || 0);
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