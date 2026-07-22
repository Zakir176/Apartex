<template>
  <div class="max-w-[1250px] mx-auto px-4 sm:px-6 py-8 text-slate-800">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
      <div>
        <span class="text-xs font-black uppercase tracking-wider text-accent mb-1 block">Reservations Hub</span>
        <h1 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">Guest Bookings</h1>
        <p class="text-slate-500 font-medium text-sm sm:text-base mt-1">Review, approve, and manage guest stay schedules across all your properties.</p>
      </div>

      <div class="flex items-center gap-3">
        <button 
          @click="loadBookings" 
          class="px-4 py-2.5 rounded-full border border-surface-border text-xs font-black text-slate-600 bg-white hover:bg-slate-50 transition-colors inline-flex items-center gap-2 shadow-sm cursor-pointer"
          :disabled="bookingsStore.loading"
        >
          <i class="pi pi-refresh text-xs" :class="{ 'pi-spin': bookingsStore.loading }"></i>
          <span>Refresh Bookings</span>
        </button>
      </div>
    </div>

    <!-- Filter Tabs Strip -->
    <div class="flex flex-wrap items-center gap-2 mb-6 bg-white p-1.5 rounded-2xl border border-surface-border shadow-sm">
      <button 
        v-for="tab in filterTabs" 
        :key="tab.id"
        @click="activeStatusFilter = tab.id"
        class="px-4 py-2 rounded-xl text-xs font-black transition-all cursor-pointer border-none"
        :class="activeStatusFilter === tab.id ? 'bg-navy text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 bg-transparent'"
      >
        {{ tab.label }}
        <span class="ml-1 px-1.5 py-0.5 rounded-full text-[10px]" :class="activeStatusFilter === tab.id ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-500'">
          {{ getTabCount(tab.id) }}
        </span>
      </button>
    </div>

    <!-- Bookings Table -->
    <div class="bg-white rounded-3xl border border-surface-border overflow-hidden shadow-sm">
      <DataTable 
        :value="filteredBookings" 
        paginator 
        :rows="10" 
        dataKey="id"
        :loading="bookingsStore.loading"
        responsiveLayout="scroll"
        class="border-none"
      >
        <template #empty>
          <div class="p-12 text-center text-slate-500 font-medium text-xs">
            <i class="pi pi-calendar-times text-3xl mb-2 text-slate-300 block"></i>
            No bookings found under this category filter.
          </div>
        </template>
        
        <Column field="id" header="Booking ID" sortable style="min-width: 6rem">
          <template #body="slotProps">
            <span class="font-mono text-xs font-black text-slate-700">#BK-{{ slotProps.data.id }}</span>
          </template>
        </Column>

        <Column field="apartment_id" header="Property" sortable>
          <template #body="slotProps">
            <div class="flex items-center gap-2 font-black text-xs text-slate-800">
              <div class="w-8 h-8 rounded-lg bg-accent-light text-accent flex items-center justify-center shrink-0">
                <i class="pi pi-home text-xs"></i>
              </div>
              <span>Listing #{{ slotProps.data.apartment_id }}</span>
            </div>
          </template>
        </Column>

        <Column field="check_in" header="Stay Dates" sortable>
          <template #body="slotProps">
            <div class="flex flex-col text-xs font-semibold text-slate-700">
              <span class="font-bold">{{ formatDate(slotProps.data.check_in) }}</span>
              <span class="text-[10px] text-slate-400">to {{ formatDate(slotProps.data.check_out) }}</span>
            </div>
          </template>
        </Column>

        <Column field="guests" header="Guests" sortable align="center">
          <template #body="slotProps">
            <div class="inline-flex items-center gap-1 px-2.5 py-1 bg-slate-50 border border-surface-border rounded-lg text-xs font-black text-slate-600">
              <i class="pi pi-users text-slate-400 text-xs"></i>
              {{ slotProps.data.guests || 1 }}
            </div>
          </template>
        </Column>

        <Column field="total_price" header="Total Price" sortable>
          <template #body="slotProps">
            <span class="font-black text-sm text-emerald-600 tracking-tight">{{ formatCurrency(slotProps.data.total_price) }}</span>
          </template>
        </Column>

        <Column field="status" header="Status" sortable>
          <template #body="slotProps">
            <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" class="text-[10px] font-black uppercase tracking-wider" />
          </template>
        </Column>

        <Column header="Actions" align="right">
          <template #body="slotProps">
            <div class="flex items-center justify-end gap-2">
              <button 
                v-if="slotProps.data.status === 'pending'"
                @click="approveBooking(slotProps.data.id)"
                class="px-3 py-1.5 bg-emerald-50 text-emerald-700 hover:bg-emerald-100 rounded-lg text-xs font-black transition-colors inline-flex items-center gap-1 border border-emerald-200"
              >
                <i class="pi pi-check text-[10px]"></i> Approve
              </button>

              <button 
                v-if="slotProps.data.status === 'confirmed'"
                @click="bookingsStore.completeBooking(slotProps.data.id)"
                class="px-3 py-1.5 bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-lg text-xs font-black transition-colors inline-flex items-center gap-1 border border-blue-200"
              >
                <i class="pi pi-check-circle text-[10px]"></i> Complete
              </button>

              <button 
                @click="openGuestModal(slotProps.data)"
                class="px-3 py-1.5 bg-slate-100 text-slate-700 hover:bg-slate-200 rounded-lg text-xs font-bold transition-colors inline-flex items-center gap-1"
              >
                <i class="pi pi-eye text-[10px]"></i> Details
              </button>
            </div>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Booking Details Dialog -->
    <Dialog v-model:visible="guestModal" header="Reservation & Guest Details" :style="{ width: '480px', maxWidth: '95vw' }" :modal="true" contentClass="pt-2">
      <div v-if="selectedBooking" class="flex flex-col gap-4 py-3 text-xs text-slate-700 font-semibold">
        <div class="bg-slate-50 p-4 rounded-2xl border border-surface-border">
          <p class="text-[10px] font-black uppercase text-slate-400">Reservation Reference</p>
          <p class="text-sm font-black text-slate-900 mt-0.5">#BK-{{ selectedBooking.id }}</p>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <p class="text-[10px] font-black uppercase text-slate-400">Check-in Date</p>
            <p class="font-bold text-slate-900 mt-0.5">{{ formatDate(selectedBooking.check_in) }}</p>
          </div>
          <div>
            <p class="text-[10px] font-black uppercase text-slate-400">Check-out Date</p>
            <p class="font-bold text-slate-900 mt-0.5">{{ formatDate(selectedBooking.check_out) }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <p class="text-[10px] font-black uppercase text-slate-400">Guests</p>
            <p class="font-bold text-slate-900 mt-0.5">{{ selectedBooking.guests || 1 }} Guests</p>
          </div>
          <div>
            <p class="text-[10px] font-black uppercase text-slate-400">Total Price</p>
            <p class="font-black text-emerald-600 text-sm mt-0.5">{{ formatCurrency(selectedBooking.total_price) }}</p>
          </div>
        </div>

        <div class="border-t border-surface-border pt-3">
          <p class="text-[10px] font-black uppercase text-slate-400 mb-2">Host Concierge Contact</p>
          <div class="flex items-center gap-2 p-3 bg-accent-light rounded-xl border border-orange-200">
            <i class="pi pi-phone text-accent"></i>
            <span>Guest support concierge ready for check-in coordination.</span>
          </div>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '@/stores/auth';

// PrimeVue components
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';

const auth = useAuthStore();
const bookingsStore = useBookingsStore();

const activeStatusFilter = ref('all');
const guestModal = ref(false);
const selectedBooking = ref(null);

const filterTabs = [
  { id: 'all', label: 'All Bookings' },
  { id: 'pending', label: 'Pending Approval' },
  { id: 'confirmed', label: 'Confirmed' },
  { id: 'completed', label: 'Completed' },
  { id: 'cancelled', label: 'Cancelled' }
];

async function loadBookings() {
  if (!auth.user?.id) return;
  await bookingsStore.fetchOwnerBookings(auth.user.id);
}

onMounted(loadBookings);

const filteredBookings = computed(() => {
  if (activeStatusFilter.value === 'all') return bookingsStore.bookings;
  return bookingsStore.bookings.filter(b => b.status?.toLowerCase() === activeStatusFilter.value);
});

function getTabCount(statusId) {
  if (statusId === 'all') return bookingsStore.bookings.length;
  return bookingsStore.bookings.filter(b => b.status?.toLowerCase() === statusId).length;
}

function openGuestModal(booking) {
  selectedBooking.value = booking;
  guestModal.value = true;
}

async function approveBooking(id) {
  try {
    const booking = bookingsStore.bookings.find(b => b.id === id);
    if (booking) booking.status = 'confirmed';
  } catch (e) {}
}

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const formatCurrency = (v) => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(v);
};

const getStatusSeverity = (status) => {
  switch (status?.toLowerCase()) {
    case 'confirmed': return 'success';
    case 'pending': return 'warning';
    case 'completed': return 'info';
    case 'cancelled': return 'danger';
    default: return 'secondary';
  }
};
</script>
