<template>
  <div class="max-w-[1200px] mx-auto px-6 py-8">
    <div class="flex flex-col md:flex-row justify-between items-center mb-10 gap-4">
      <div>
        <h1 class="text-4xl font-extrabold text-slate-800 mb-2">Guest Bookings</h1>
        <p class="text-slate-500 font-medium text-lg m-0">Monitor and manage guest reservations across all properties</p>
      </div>
      <div>
        <button 
          @click="loadBookings" 
          class="px-4 py-2 rounded-full border border-surface-border text-sm font-bold text-slate-600 hover:bg-slate-50 transition-colors inline-flex items-center gap-2"
          :disabled="bookingsStore.loading"
        >
          <i class="pi pi-refresh" :class="{ 'pi-spin': bookingsStore.loading }"></i>
          Refresh List
        </button>
      </div>
    </div>

    <!-- Bookings Table -->
    <div class="card-base overflow-hidden">
      <DataTable 
        v-model:filters="filters"
        :value="bookingsStore.bookings" 
        paginator 
        :rows="10" 
        dataKey="id"
        filterDisplay="menu"
        :loading="bookingsStore.loading"
        :globalFilterFields="['id', 'apartment_id', 'status']"
        responsiveLayout="scroll"
        class="border-none"
      >
        <template #header>
          <div class="flex flex-col md:flex-row justify-between items-center gap-4 p-2 bg-white">
            <span class="relative w-full md:w-auto">
              <i class="pi pi-search absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"></i>
              <InputText v-model="filters['global'].value" placeholder="Search bookings..." class="input-base !pl-10 !py-2 !text-sm w-full md:w-72" />
            </span>
            <div class="w-full md:w-auto">
              <Dropdown 
                v-model="filters['status'].value" 
                :options="statuses" 
                placeholder="Filter by Status" 
                class="w-full md:w-48"
                :showClear="true"
              />
            </div>
          </div>
        </template>

        <template #empty>
          <div class="p-8 text-center text-slate-500 font-medium">No bookings found.</div>
        </template>
        
        <Column field="id" header="ID" sortable style="min-width: 5rem"></Column>
        
        <Column field="apartment_id" header="Apartment" sortable>
          <template #body="slotProps">
            <div class="flex items-center gap-2 font-bold text-slate-700">
              <div class="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
                <i class="pi pi-home text-sm"></i>
              </div>
              <span>Listing #{{ slotProps.data.apartment_id }}</span>
            </div>
          </template>
        </Column>

        <Column field="check_in" header="Check-in" sortable>
          <template #body="slotProps">
            <span class="font-medium text-slate-600">{{ formatDate(slotProps.data.check_in) }}</span>
          </template>
        </Column>

        <Column field="check_out" header="Check-out" sortable>
          <template #body="slotProps">
            <span class="font-medium text-slate-600">{{ formatDate(slotProps.data.check_out) }}</span>
          </template>
        </Column>

        <Column field="guests" header="Guests" sortable align="center">
          <template #body="slotProps">
            <div class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 border border-surface-border rounded-md text-xs font-bold text-slate-600">
              <i class="pi pi-users text-slate-400"></i>
              {{ slotProps.data.guests }}
            </div>
          </template>
        </Column>

        <Column field="total_price" header="Total" sortable>
          <template #body="slotProps">
            <span class="font-extrabold text-slate-800 tracking-tight">{{ formatCurrency(slotProps.data.total_price) }}</span>
          </template>
        </Column>

        <Column field="status" header="Status" sortable>
          <template #body="slotProps">
            <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" class="text-[10px] font-bold uppercase tracking-wider" />
          </template>
        </Column>

        <Column header="Actions" align="right">
          <template #body="slotProps">
            <button 
              v-if="slotProps.data.status === 'confirmed'"
              @click="bookingsStore.completeBooking(slotProps.data.id)"
              class="px-3 py-1.5 bg-green-50 text-green-600 hover:bg-green-100 rounded-md text-xs font-bold transition-colors inline-flex items-center gap-1.5"
            >
              <i class="pi pi-check"></i> Complete
            </button>
            <span v-else class="text-slate-400 text-xs font-medium italic">No actions</span>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '@/stores/auth';
import { FilterMatchMode } from 'primevue/api';

// PrimeVue components
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';

const auth = useAuthStore();
const bookingsStore = useBookingsStore();

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  status: { value: null, matchMode: FilterMatchMode.EQUALS }
});

const statuses = [
  'pending', 'confirmed', 'completed', 'cancelled'
];

async function loadBookings() {
  if (!auth.user?.id) return;
  await bookingsStore.fetchOwnerBookings(auth.user.id);
}

onMounted(loadBookings);

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
