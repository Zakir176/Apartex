<template>
  <div class="max-w-[1200px] mx-auto px-6 py-8">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
      <div>
        <h1 class="text-4xl font-extrabold text-slate-800 mb-2">Performance Analytics</h1>
        <p class="text-slate-500 font-medium text-lg">Real-time overview of your property portfolio and earnings</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="openPayoutModal" class="btn-accent shadow-accent inline-flex items-center gap-2">
          <i class="pi pi-wallet"></i>
          Request Payout
        </button>
        <Button 
          icon="pi pi-refresh" 
          @click="refreshData" 
          class="p-button-outlined p-button-secondary font-bold !rounded-full !w-10 !h-10 p-0 flex items-center justify-center" 
          v-tooltip.bottom="'Sync Data'"
          :loading="store.loading"
        />
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <!-- Total Revenue -->
      <div class="card-base p-6 flex flex-col justify-between h-full">
        <div class="flex items-center justify-between mb-4">
          <span class="text-slate-500 text-xs font-bold uppercase tracking-wider">Total Revenue</span>
          <div class="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center">
            <i class="pi pi-dollar text-blue-500 text-lg"></i>
          </div>
        </div>
        <div>
          <div class="text-4xl font-extrabold text-slate-800 tracking-tight mb-2">{{ formatCurrency(store.overview?.total_revenue) }}</div>
          <div class="flex items-center gap-2 text-green-600 text-sm font-bold">
            <i class="pi pi-arrow-up text-xs"></i>
            <span>12.5%</span>
            <span class="text-slate-500 font-medium">vs last month</span>
          </div>
        </div>
      </div>

      <!-- Active Bookings -->
      <div class="card-base p-6 flex flex-col justify-between h-full">
        <div class="flex items-center justify-between mb-4">
          <span class="text-slate-500 text-xs font-bold uppercase tracking-wider">Active Bookings</span>
          <div class="w-10 h-10 rounded-xl bg-purple-50 flex items-center justify-center">
            <i class="pi pi-calendar text-purple-500 text-lg"></i>
          </div>
        </div>
        <div>
          <div class="text-4xl font-extrabold text-slate-800 tracking-tight mb-2">{{ store.overview?.active_bookings || 0 }}</div>
          <p class="text-slate-500 text-sm font-medium m-0">Live stays at your properties</p>
        </div>
      </div>

      <!-- Portfolio Health -->
      <div class="card-base p-6 flex flex-col justify-between h-full">
        <div class="flex items-center justify-between mb-4">
          <span class="text-slate-500 text-xs font-bold uppercase tracking-wider">Portfolio Health</span>
          <div class="w-10 h-10 rounded-xl bg-orange-50 flex items-center justify-center">
            <i class="pi pi-chart-line text-orange-500 text-lg"></i>
          </div>
        </div>
        <div>
          <div class="text-4xl font-extrabold text-slate-800 tracking-tight mb-2">{{ formatPercent(store.overview?.occupancy_rate) }}</div>
          <p class="text-slate-500 text-sm font-medium m-0">Average occupancy across listings</p>
        </div>
      </div>
    </div>

    <!-- Secondary Insights -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Main Chart -->
      <div class="lg:col-span-2">
        <div class="card-base p-6 h-full">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-slate-800">Revenue Trends</h3>
            <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">Last 6 Months</span>
          </div>
          <div class="h-64">
            <Chart type="line" :data="chartData" :options="chartOptions" class="h-full w-full" />
          </div>
        </div>
      </div>

      <!-- Recent Activity / Payouts -->
      <div class="lg:col-span-1">
        <div class="card-base p-6 h-full">
          <h3 class="text-xl font-bold text-slate-800 mb-6">Recent Payouts</h3>
          
          <div v-if="store.payouts.length > 0" class="flex flex-col gap-5">
            <div v-for="p in store.payouts.slice(0, 5)" :key="p.id" class="flex items-center justify-between pb-4 border-b border-surface-border last:border-0 last:pb-0">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center">
                  <i class="pi pi-arrow-down-left text-slate-400"></i>
                </div>
                <div>
                  <div class="font-extrabold text-slate-800 text-sm mb-0.5">{{ formatCurrency(p.amount) }}</div>
                  <div class="text-xs font-medium text-slate-500">{{ formatDate(p.date || p.created_at) }}</div>
                </div>
              </div>
              <Tag :value="p.status" :severity="getStatusSeverity(p.status)" class="text-[10px] font-bold uppercase tracking-wider" />
            </div>
          </div>
          
          <div v-else class="flex flex-col items-center justify-center py-10 text-center">
            <div class="w-16 h-16 rounded-full bg-slate-50 flex items-center justify-center mb-4">
              <i class="pi pi-inbox text-2xl text-slate-300"></i>
            </div>
            <p class="text-slate-500 text-sm font-medium">No payout history found</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Payout Request Dialog -->
    <Dialog v-model:visible="payoutModal" header="Request Funds" :style="{ width: '450px' }" :modal="true" :breakpoints="{'640px': '90vw'}" contentClass="pt-2">
      <div class="flex flex-col gap-5 py-4">
        <div>
          <label class="label-base">Withdrawal Amount (USD)</label>
          <InputNumber v-model="payoutForm.amount" mode="currency" currency="USD" locale="en-US" :min="0" inputClass="input-base !w-full" class="w-full" />
        </div>

        <div>
          <label class="label-base">Transfer Method</label>
          <Dropdown v-model="payoutForm.method" :options="payoutMethods" optionLabel="label" optionValue="value" placeholder="Select destination" class="w-full" />
        </div>

        <div>
          <label class="label-base">Account Details</label>
          <input v-model="payoutForm.details" class="input-base" placeholder="SWIFT / IBAN / Account Number" />
        </div>
      </div>

      <template #footer>
        <div class="flex gap-3 justify-end pt-4 border-t border-surface-border">
          <button @click="closePayoutModal" class="px-5 py-2.5 rounded-full text-sm font-bold text-slate-500 hover:bg-slate-100 transition-colors">Cancel</button>
          <button @click="submitPayout" :disabled="submitting" class="btn-accent inline-flex items-center gap-2">
            <i class="pi pi-check" v-if="!submitting"></i>
            <i class="pi pi-spinner pi-spin" v-else></i>
            <span>Confirm Request</span>
          </button>
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
        borderColor: '#E8621A',
        borderWidth: 3,
        pointRadius: 4,
        pointBackgroundColor: '#fff',
        pointBorderWidth: 2,
        tension: 0.4,
        backgroundColor: 'rgba(232, 98, 26, 0.05)'
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
      backgroundColor: '#1E293B',
      padding: 12,
      bodyFont: { weight: 'bold' },
      cornerRadius: 8
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#F1EFE9', drawBorder: false },
      ticks: { color: '#94A3B8', font: { weight: 600 } }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#94A3B8', font: { weight: 600 } }
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
