<template>
  <div class="owner-bookings-container">
    <div class="header-section">
      <div class="title-area">
        <h1>Guest Bookings</h1>
        <p class="subtitle">Monitor and manage guest reservations across all properties</p>
      </div>
      <div class="action-area">
        <Button 
          icon="pi pi-refresh" 
          @click="loadBookings" 
          class="p-button-text p-button-secondary" 
          :loading="bookingsStore.loading"
        />
      </div>
    </div>

    <!-- Bookings Table -->
    <Card class="table-card">
      <template #content>
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
          class="p-datatable-sm"
        >
          <template #header>
            <div class="flex justify-content-between align-items-center">
              <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText v-model="filters['global'].value" placeholder="Search bookings..." />
              </span>
              <div class="flex gap-2">
                <Dropdown 
                  v-model="filters['status'].value" 
                  :options="statuses" 
                  placeholder="Filter by Status" 
                  class="p-column-filter"
                  style="min-width: 12rem"
                  :showClear="true"
                />
              </div>
            </div>
          </template>

          <template #empty>No bookings found.</template>
          
          <Column field="id" header="ID" sortable style="min-width: 5rem"></Column>
          
          <Column field="apartment_id" header="Apartment" sortable>
            <template #body="slotProps">
              <div class="flex align-items-center">
                <i class="pi pi-home mr-2 text-primary"></i>
                <span>Listing #{{ slotProps.data.apartment_id }}</span>
              </div>
            </template>
          </Column>

          <Column field="check_in" header="Check-in" sortable>
            <template #body="slotProps">
              {{ formatDate(slotProps.data.check_in) }}
            </template>
          </Column>

          <Column field="check_out" header="Check-out" sortable>
            <template #body="slotProps">
              {{ formatDate(slotProps.data.check_out) }}
            </template>
          </Column>

          <Column field="guests" header="Guests" sortable style="text-align: center">
            <template #body="slotProps">
              <i class="pi pi-users mr-1"></i>
              {{ slotProps.data.guests }}
            </template>
          </Column>

          <Column field="total_price" header="Total" sortable>
            <template #body="slotProps">
              <span class="font-bold text-lg">{{ formatCurrency(slotProps.data.total_price) }}</span>
            </template>
          </Column>

          <Column field="status" header="Status" sortable>
            <template #body="slotProps">
              <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
            </template>
          </Column>

          <Column header="Actions" style="min-width: 8rem">
            <template #body="slotProps">
              <Button 
                v-if="slotProps.data.status === 'confirmed'"
                icon="pi pi-check" 
                label="Complete" 
                class="p-button-success p-button-sm p-button-text" 
                @click="bookingsStore.completeBooking(slotProps.data.id)"
              />
              <span v-else class="text-gray-400 text-xs italic">No actions available</span>
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useBookingsStore } from '@/stores/bookings';
import { useAuthStore } from '@/stores/auth';
import { FilterMatchMode } from 'primevue/api';

// PrimeVue components
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import InputText from 'primevue/inputtext';
import Card from 'primevue/card';
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
  return new Date(dateString).toLocaleDateString();
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

<style scoped>
.owner-bookings-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
}

.title-area h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.subtitle {
  color: #718096;
}

.table-card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

:deep(.p-datatable .p-datatable-header) {
  background: white;
  padding: 1rem;
}

:deep(.p-inputtext) {
  border-radius: 8px;
}
</style>
