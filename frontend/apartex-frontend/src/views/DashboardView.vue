<template>
  <div class="dashboard-container">
    <div class="header-section">
      <div class="title-area">
        <h1>Owner Dashboard</h1>
        <p class="subtitle">Overview of your properties and performance</p>
      </div>
      <div class="action-area">
        <Button 
          label="Request Payout" 
          icon="pi pi-wallet" 
          @click="openPayoutModal" 
          class="p-button-raised p-button-primary" 
        />
        <Button 
          icon="pi pi-refresh" 
          @click="refreshData" 
          class="p-button-text p-button-secondary ml-2" 
          :loading="store.loading"
        />
      </div>
    </div>

    <!-- Stats Overview -->
    <div class="stats-grid">
      <Card class="stat-card revenue">
        <template #title>
          <div class="stat-header">
            <span>Total Revenue</span>
            <i class="pi pi-dollar"></i>
          </div>
        </template>
        <template #content>
          <div class="stat-value">{{ formatCurrency(store.overview?.total_revenue) }}</div>
          <div class="stat-footer text-green-500">
            <i class="pi pi-arrow-up"></i>
            <span>+12.5% from last month</span>
          </div>
        </template>
      </Card>

      <Card class="stat-card bookings">
        <template #title>
          <div class="stat-header">
            <span>Active Bookings</span>
            <i class="pi pi-calendar"></i>
          </div>
        </template>
        <template #content>
          <div class="stat-value">{{ store.overview?.active_bookings || 0 }}</div>
          <div class="stat-footer text-blue-500">
            <span>Current active stays</span>
          </div>
        </template>
      </Card>

      <Card class="stat-card occupancy">
        <template #title>
          <div class="stat-header">
            <span>Occupancy Rate</span>
            <i class="pi pi-percentage"></i>
          </div>
        </template>
        <template #content>
          <div class="stat-value">{{ formatPercent(store.overview?.occupancy_rate) }}</div>
          <div class="stat-footer text-orange-500">
            <span>Average across all listings</span>
          </div>
        </template>
      </Card>
    </div>

    <!-- Main Content Grid -->
    <div class="main-grid">
      <!-- Revenue Chart -->
      <Card class="chart-card">
        <template #title>Revenue Trends</template>
        <template #content>
          <Chart type="line" :data="chartData" :options="chartOptions" class="h-20rem" />
        </template>
      </Card>

      <!-- Payout History -->
      <Card class="payout-card">
        <template #title>Recent Payouts</template>
        <template #content>
          <DataTable :value="store.payouts" paginator :rows="5" responsiveLayout="scroll" class="p-datatable-sm">
            <template #empty>No payout history found.</template>
            <Column field="date" header="Date">
              <template #body="slotProps">
                {{ formatDate(slotProps.data.date || slotProps.data.created_at) }}
              </template>
            </Column>
            <Column field="amount" header="Amount">
              <template #body="slotProps">
                {{ formatCurrency(slotProps.data.amount) }}
              </template>
            </Column>
            <Column field="status" header="Status">
              <template #body="slotProps">
                <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </div>

    <!-- Apartment Management -->
    <div class="mt-6">
      <Card class="apartments-card">
        <template #title>Your Listings</template>
        <template #content>
          <DataTable :value="store.overview?.apartments || []" responsiveLayout="scroll">
            <template #empty>You haven't listed any apartments yet.</template>
            <Column field="title" header="Apartment"></Column>
            <Column field="city" header="Location"></Column>
            <Column field="price_per_night" header="Price">
              <template #body="slotProps">
                {{ formatCurrency(slotProps.data.price_per_night) }}/night
              </template>
            </Column>
            <Column header="Actions">
              <template #body="slotProps">
                <Button icon="pi pi-pencil" class="p-button-text p-button-info" />
                <Button icon="pi pi-trash" class="p-button-text p-button-danger" />
              </template>
            </Column>
          </DataTable>
        </template>
      </Card>
    </div>

    <!-- Payout Dialog -->
    <Dialog v-model:visible="payoutModal" header="Request Payout" :style="{ width: '450px' }" :modal="true" class="p-fluid">
      <div class="field mb-4">
        <label for="amount" class="block font-bold mb-2">Amount (ZMW)</label>
        <InputNumber id="amount" v-model="payoutForm.amount" mode="currency" currency="ZMW" locale="en-ZM" :min="0" />
      </div>

      <div class="field mb-4">
        <label for="method" class="block font-bold mb-2">Payment Method</label>
        <Dropdown id="method" v-model="payoutForm.method" :options="payoutMethods" optionLabel="label" optionValue="value" placeholder="Select a method" />
      </div>

      <div class="field mb-4">
        <label for="details" class="block font-bold mb-2">Transfer Details</label>
        <InputText id="details" v-model="payoutForm.details" placeholder="Bank Account / Mobile Number" />
      </div>

      <template #footer>
        <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closePayoutModal" />
        <Button label="Submit Request" icon="pi pi-check" class="p-button-primary" @click="submitPayout" :loading="submitting" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useDashboardStore } from '@/stores/dashboard';

// PrimeVue components
import Card from 'primevue/card';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Chart from 'primevue/chart';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';

const store = useDashboardStore();

const payoutModal = ref(false);
const submitting = ref(false);
const payoutForm = ref({ amount: 0, method: 'bank', details: '' });

const payoutMethods = [
  { label: 'Bank Transfer', value: 'bank' },
  { label: 'Mobile Money', value: 'momo' }
];

onMounted(async () => {
  await refreshData();
});

async function refreshData() {
  await Promise.all([store.loadOverview(), store.loadPayouts()]);
}

function openPayoutModal() {
  payoutForm.value = { amount: 0, method: 'bank', details: '' };
  payoutModal.value = true;
}

function closePayoutModal() {
  payoutModal.value = false;
}

async function submitPayout() {
  if (payoutForm.value.amount <= 0) return;
  
  submitting.value = true;
  try {
    await store.submitPayoutRequest({
      amount: payoutForm.value.amount,
      method: payoutForm.value.method,
      details: payoutForm.value.details,
    });
    closePayoutModal();
  } catch (err) {
    console.error(err);
  } finally {
    submitting.value = false;
  }
}

const chartData = computed(() => {
  const monthly = store.overview?.monthly_revenue || [
    { month: 'Jan', revenue: 1200 },
    { month: 'Feb', revenue: 1900 },
    { month: 'Mar', revenue: 1500 },
    { month: 'Apr', revenue: 2100 }
  ];
  
  return {
    labels: monthly.map((m) => m.month),
    datasets: [
      {
        label: 'Monthly Revenue',
        data: monthly.map((m) => m.revenue),
        fill: true,
        borderColor: '#42A5F5',
        tension: 0.4,
        backgroundColor: 'rgba(66, 165, 245, 0.2)'
      }
    ]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: '#f0f0f0'
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
};

function formatCurrency(v) {
  if (v == null) return '$0.00';
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(v);
}

function formatPercent(p) {
  if (p == null) return '0%';
  return `${Math.round(p * 100)}%`;
}

function formatDate(dateString) {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString();
}

function getStatusSeverity(status) {
  switch (status?.toLowerCase()) {
    case 'completed': return 'success';
    case 'pending': return 'warning';
    case 'failed': return 'danger';
    default: return 'info';
  }
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
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
  margin: 0 0 0.25rem 0;
  color: #1a202c;
}

.subtitle {
  color: #718096;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1rem;
  color: #4a5568;
}

.stat-header i {
  font-size: 1.25rem;
  opacity: 0.7;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 800;
  margin: 0.5rem 0;
  color: #1a202c;
}

.stat-footer {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.85rem;
  font-weight: 600;
}

.main-grid {
  display: grid;
  grid-template-columns: 2fr 1.5fr;
  gap: 1.5rem;
}

.chart-card, .payout-card, .apartments-card {
  height: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

@media (max-width: 1024px) {
  .main-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }
}
</style>

<style scoped>
.input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
}
.btn { padding: 0.5rem 1rem; border-radius: 0.375rem; background: #e5e7eb; }
.btn-primary { background: #1f6feb; color: white; }
</style>
