<template>
  <div class="ax-container py-8">
    <!-- Page Header -->
    <div class="flex flex-column md:flex-row md:align-items-center justify-content-between mb-8 gap-4">
      <div>
        <h1 class="text-5xl font-bold text-900 mb-2">Performance Analytics</h1>
        <p class="text-500 font-medium text-lg">Real-time overview of your property portfolio and earnings</p>
      </div>
      <div class="flex gap-2">
        <button @click="openPayoutModal" class="ax-button shadow-lg">
          <i class="pi pi-wallet mr-2"></i>
          Request Payout
        </button>
        <Button 
          icon="pi pi-refresh" 
          @click="refreshData" 
          class="p-button-outlined p-button-secondary font-bold" 
          v-tooltip.bottom="'Sync Data'"
          :loading="store.loading"
        />
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="grid mb-8">
      <div class="col-12 md:col-4 p-3">
        <div class="surface-0 p-5 border-round-xl border-1 border-100 shadow-soft h-full">
          <div class="flex align-items-center justify-content-between mb-4">
            <span class="text-500 text-xs font-bold uppercase tracking-wider">Total Revenue</span>
            <div class="w-2rem h-2rem border-circle bg-blue-50 flex align-items-center justify-content-center">
              <i class="pi pi-dollar text-blue-500"></i>
            </div>
          </div>
          <div class="text-4xl font-bold text-900 mb-2">{{ formatCurrency(store.overview?.total_revenue) }}</div>
          <div class="flex align-items-center gap-2 text-green-600 text-sm font-bold">
            <i class="pi pi-arrow-up"></i>
            <span>12.5%</span>
            <span class="text-500 font-normal">vs last month</span>
          </div>
        </div>
      </div>

      <div class="col-12 md:col-4 p-3">
        <div class="surface-0 p-5 border-round-xl border-1 border-100 shadow-soft h-full">
          <div class="flex align-items-center justify-content-between mb-4">
            <span class="text-500 text-xs font-bold uppercase tracking-wider">Active Bookings</span>
            <div class="w-2rem h-2rem border-circle bg-purple-50 flex align-items-center justify-content-center">
              <i class="pi pi-calendar text-purple-500"></i>
            </div>
          </div>
          <div class="text-4xl font-bold text-900 mb-2">{{ store.overview?.active_bookings || 0 }}</div>
          <p class="text-500 text-sm font-medium m-0">Live stays at your properties</p>
        </div>
      </div>

      <div class="col-12 md:col-4 p-3">
        <div class="surface-0 p-5 border-round-xl border-1 border-100 shadow-soft h-full">
          <div class="flex align-items-center justify-content-between mb-4">
            <span class="text-500 text-xs font-bold uppercase tracking-wider">Portfolio Health</span>
            <div class="w-2rem h-2rem border-circle bg-orange-50 flex align-items-center justify-content-center">
              <i class="pi pi-chart-line text-orange-500"></i>
            </div>
          </div>
          <div class="text-4xl font-bold text-900 mb-2">{{ formatPercent(store.overview?.occupancy_rate) }}</div>
          <p class="text-500 text-sm font-medium m-0">Average occupancy across listings</p>
        </div>
      </div>
    </div>

    <!-- Secondary Insights -->
    <div class="grid">
      <!-- Main Chart -->
      <div class="col-12 lg:col-8 p-3">
        <div class="surface-0 p-5 border-round-xl border-1 border-100 shadow-soft h-full">
          <div class="flex align-items-center justify-content-between mb-6">
            <h3 class="text-xl font-bold text-900">Revenue Trends</h3>
            <span class="text-xs font-bold text-500 uppercase tracking-widest">Last 6 Months</span>
          </div>
          <Chart type="line" :data="chartData" :options="chartOptions" class="h-20rem" />
        </div>
      </div>

      <!-- Recent Activity / Payouts -->
      <div class="col-12 lg:col-4 p-3">
        <div class="surface-0 p-5 border-round-xl border-1 border-100 shadow-soft h-full">
          <h3 class="text-xl font-bold text-900 mb-6">Recent Payouts</h3>
          
          <div v-if="store.payouts.length > 0" class="flex flex-column gap-4">
            <div v-for="p in store.payouts.slice(0, 5)" :key="p.id" class="flex align-items-center justify-content-between">
              <div class="flex align-items-center gap-3">
                <div class="w-2rem h-2rem border-round-lg surface-100 flex align-items-center justify-content-center">
                  <i class="pi pi-arrow-down-left text-sm"></i>
                </div>
                <div>
                  <div class="font-bold text-900 text-sm">{{ formatCurrency(p.amount) }}</div>
                  <div class="text-xs text-500">{{ formatDate(p.date || p.created_at) }}</div>
                </div>
              </div>
              <Tag :value="p.status" :severity="getStatusSeverity(p.status)" class="text-xs font-bold uppercase" />
            </div>
          </div>
          
          <div v-else class="flex flex-column align-items-center justify-content-center py-8 text-center">
            <i class="pi pi-inbox text-3xl text-200 mb-3"></i>
            <p class="text-500 text-sm font-medium">No payout history</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Payout Request Dialog -->
    <Dialog v-model:visible="payoutModal" header="Request Funds" :style="{ width: '450px' }" :modal="true" class="studio-payout-modal">
      <div class="p-fluid py-2">
        <div class="ax-field-group">
          <label class="ax-label">Withdrawal Amount (USD)</label>
          <InputNumber v-model="payoutForm.amount" mode="currency" currency="USD" locale="en-US" :min="0" inputClass="ax-input" />
        </div>

        <div class="ax-field-group">
          <label class="ax-label">Transfer Method</label>
          <Dropdown v-model="payoutForm.method" :options="payoutMethods" optionLabel="label" optionValue="value" placeholder="Select destination" />
        </div>

        <div class="ax-field-group mb-0">
          <label class="ax-label">Account Details</label>
          <input v-model="payoutForm.details" class="ax-input" placeholder="SWIFT / IBAN / Account Number" />
        </div>
      </div>

      <template #footer>
        <div class="flex gap-2 justify-content-end pt-4">
          <Button label="Cancel" @click="closePayoutModal" class="p-button-text p-button-secondary font-bold" />
          <Button label="Confirm Request" icon="pi pi-check" @click="submitPayout" :loading="submitting" class="p-button-primary font-bold px-4" />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useDashboardStore } from '@/stores/dashboard';

// PrimeVue components
import Button from 'primevue/button';
import Chart from 'primevue/chart';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';

const store = useDashboardStore();

const payoutModal = ref(false);
const submitting = ref(false);
const payoutForm = ref({ amount: 0, method: 'bank', details: '' });

const payoutMethods = [
  { label: 'Standard Bank Transfer', value: 'bank' },
  { label: 'Fast Settlement (Mobile)', value: 'momo' }
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
    { month: 'Apr', revenue: 2100 },
    { month: 'May', revenue: 2800 },
    { month: 'Jun', revenue: 3500 }
  ];
  
  return {
    labels: monthly.map((m) => m.month),
    datasets: [
      {
        label: 'Monthly Revenue',
        data: monthly.map((m) => m.revenue),
        fill: true,
        borderColor: '#3b82f6',
        borderWidth: 3,
        pointRadius: 4,
        pointBackgroundColor: '#fff',
        pointBorderWidth: 2,
        tension: 0.4,
        backgroundColor: 'rgba(59, 130, 246, 0.05)'
      }
    ]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#0f172a',
      padding: 12,
      bodyFont: { weight: 'bold' },
      cornerRadius: 8
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#f1f5f9', drawBorder: false },
      ticks: { color: '#94a3b8', font: { weight: 600 } }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#94a3b8', font: { weight: 600 } }
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
  return new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
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
.shadow-soft {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -2px rgba(0, 0, 0, 0.03);
}
</style>
