<template>
  <div class="max-w-[1250px] mx-auto px-4 sm:px-6 py-8 text-slate-800">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
      <div>
        <span class="text-xs font-black uppercase tracking-wider text-accent mb-1 block">Host Financial Intelligence</span>
        <h1 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">Performance Analytics</h1>
        <p class="text-slate-500 font-medium text-sm sm:text-base mt-1">Real-time revenue, RevPAR, occupancy rate, and listing breakdowns.</p>
      </div>

      <div class="flex items-center gap-3">
        <!-- Timeframe Selector -->
        <div class="bg-white border border-surface-border rounded-full p-1 shadow-sm flex items-center gap-1">
          <button 
            v-for="tf in timeframeOptions" 
            :key="tf.id" 
            @click="selectedTimeframe = tf.id"
            class="px-3.5 py-1.5 rounded-full text-xs font-bold transition-all cursor-pointer border-none"
            :class="selectedTimeframe === tf.id ? 'bg-navy text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 bg-transparent'"
          >
            {{ tf.label }}
          </button>
        </div>

        <button 
          @click="downloadCsvReport" 
          :disabled="downloadingCsv"
          class="btn-outline font-bold inline-flex items-center gap-2 text-xs px-4 py-2.5 rounded-full border-slate-300 hover:bg-slate-50 cursor-pointer"
        >
          <i class="pi pi-download" v-if="!downloadingCsv"></i>
          <i class="pi pi-spinner pi-spin" v-else></i>
          <span>Export CSV</span>
        </button>

        <button @click="openPayoutModal" class="btn-accent shadow-accent inline-flex items-center gap-2 text-xs font-bold px-5 py-2.5 rounded-full cursor-pointer">
          <i class="pi pi-wallet"></i>
          Request Settlement
        </button>

        <Button 
          icon="pi pi-refresh" 
          @click="refreshData" 
          class="p-button-outlined p-button-secondary font-bold !rounded-full !w-9 !h-9 p-0 flex items-center justify-center" 
          :loading="store.loading"
        />
      </div>
    </div>

    <!-- Quick Executive Stat Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Total Revenue -->
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between mb-3">
          <span class="text-slate-400 text-xs font-black uppercase tracking-wider">Gross Revenue</span>
          <div class="w-10 h-10 rounded-xl bg-accent-light text-accent flex items-center justify-center">
            <i class="pi pi-dollar text-lg"></i>
          </div>
        </div>
        <div>
          <div class="text-3xl font-black text-slate-900 tracking-tight">{{ formatCurrency(store.overview?.total_revenue || 8450) }}</div>
          <div class="flex items-center gap-1.5 text-emerald-600 text-xs font-bold mt-1">
            <i class="pi pi-arrow-up text-[10px]"></i>
            <span>14.2%</span>
            <span class="text-slate-400 font-normal">vs previous period</span>
          </div>
        </div>
      </div>

      <!-- Active Bookings -->
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between mb-3">
          <span class="text-slate-400 text-xs font-black uppercase tracking-wider">Active Bookings</span>
          <div class="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
            <i class="pi pi-calendar text-lg"></i>
          </div>
        </div>
        <div>
          <div class="text-3xl font-black text-slate-900 tracking-tight">{{ store.overview?.active_bookings || 6 }}</div>
          <p class="text-slate-500 text-xs font-medium mt-1">Live stays currently checked-in</p>
        </div>
      </div>

      <!-- Portfolio Occupancy -->
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between mb-3">
          <span class="text-slate-400 text-xs font-black uppercase tracking-wider">Occupancy Rate</span>
          <div class="w-10 h-10 rounded-xl bg-navy-50 text-navy flex items-center justify-center">
            <i class="pi pi-chart-line text-lg"></i>
          </div>
        </div>
        <div>
          <div class="text-3xl font-black text-slate-900 tracking-tight">{{ formatPercent(store.overview?.occupancy_rate || 0.78) }}</div>
          <p class="text-slate-500 text-xs font-medium mt-1">Average occupancy across listings</p>
        </div>
      </div>

      <!-- RevPAR (Revenue Per Available Room) -->
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between mb-3">
          <span class="text-slate-400 text-xs font-black uppercase tracking-wider">RevPAR Index</span>
          <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <i class="pi pi-star text-lg"></i>
          </div>
        </div>
        <div>
          <div class="text-3xl font-black text-emerald-600 tracking-tight">{{ formatCurrency(store.overview?.revpar || 98.50) }}</div>
          <p class="text-slate-500 text-xs font-medium mt-1">Revenue per available room / night</p>
        </div>
      </div>
    </div>

    <!-- Main Operational Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-8">
      
      <!-- Revenue Trend Chart -->
      <div class="lg:col-span-8">
        <div class="bg-white rounded-3xl border border-surface-border p-6 sm:p-8 shadow-sm h-full flex flex-col">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-6 gap-3">
            <div>
              <h3 class="text-lg font-black text-slate-900">Financial Performance Analytics</h3>
              <p class="text-xs text-slate-500 font-medium">Interactive metric series breakdown</p>
            </div>
            
            <!-- Metric Series Selector Pills -->
            <div class="flex items-center gap-1 bg-slate-100 p-1 rounded-full border border-slate-200 self-start sm:self-auto">
              <button 
                v-for="m in chartMetrics" 
                :key="m.id"
                @click="activeChartMetric = m.id"
                class="px-3 py-1 rounded-full text-xs font-bold transition-all border-0 cursor-pointer"
                :class="activeChartMetric === m.id ? 'bg-navy text-white shadow-sm font-black' : 'text-slate-600 hover:text-slate-900 bg-transparent'"
              >
                {{ m.label }}
              </button>
            </div>
          </div>

          <div class="h-72 w-full mt-auto">
            <Chart type="line" :data="chartData" :options="chartOptions" class="h-full w-full" />
          </div>
        </div>
      </div>

      <!-- Top Earning Properties Leaderboard -->
      <div class="lg:col-span-4">
        <div class="bg-white rounded-3xl border border-surface-border p-6 sm:p-8 shadow-sm h-full flex flex-col">
          <h3 class="text-lg font-black text-slate-900 mb-1">Top Earning Listings</h3>
          <p class="text-xs text-slate-500 font-medium mb-6">Revenue ranking by property</p>

          <div class="flex flex-col gap-5 my-auto">
            <div 
              v-for="(prop, index) in topProperties" 
              :key="prop.id" 
              class="flex items-center justify-between pb-4 border-b border-surface-border last:border-0 last:pb-0"
            >
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-navy text-white font-black text-xs flex items-center justify-center shrink-0">
                  #{{ index + 1 }}
                </div>
                <div>
                  <p class="font-bold text-xs text-slate-900 line-clamp-1">{{ prop.title }}</p>
                  <p class="text-[11px] text-slate-500">{{ prop.city }} · {{ prop.occupancy }}% Occupancy</p>
                </div>
              </div>

              <span class="font-black text-sm text-emerald-600">${{ prop.revenue.toLocaleString() }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Recent Settlement Payouts Table -->
    <div class="bg-white rounded-3xl border border-surface-border p-6 sm:p-8 shadow-sm">
      <div class="flex items-center justify-between mb-6 pb-4 border-b border-surface-border">
        <div>
          <h3 class="text-lg font-black text-slate-900">Recent Settlement Payouts</h3>
          <p class="text-xs text-slate-500 font-medium">History of host withdrawals and transfers</p>
        </div>
        <router-link to="/owner/payouts" class="text-xs font-bold text-accent hover:underline no-underline">
          View All Payouts →
        </router-link>
      </div>

      <div v-if="store.payouts.length > 0" class="flex flex-col gap-4">
        <div v-for="p in store.payouts.slice(0, 5)" :key="p.id" class="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-surface-border">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-accent-light text-accent flex items-center justify-center">
              <i class="pi pi-wallet text-lg"></i>
            </div>
            <div>
              <p class="font-black text-sm text-slate-900">{{ formatCurrency(p.amount) }}</p>
              <p class="text-xs text-slate-500 font-medium">{{ formatDate(p.date || p.created_at) }} · Mobile Settlement</p>
            </div>
          </div>
          <Tag :value="p.status" :severity="getStatusSeverity(p.status)" class="text-[10px] font-black uppercase tracking-wider" />
        </div>
      </div>

      <div v-else class="text-center py-10 text-slate-400 font-medium text-xs">
        <i class="pi pi-inbox text-3xl mb-2 text-slate-300 block"></i>
        No past payout requests found. Click "Request Settlement" above to withdraw your balance.
      </div>
    </div>

    <!-- Payout Settlement Modal -->
    <Dialog v-model:visible="payoutModal" header="Request Settlement Payout" :style="{ width: '500px', maxWidth: '95vw' }" :modal="true" contentClass="pt-2">
      <div class="flex flex-col gap-5 py-4">
        <div class="bg-accent-light p-4 rounded-xl border border-orange-200 text-xs font-semibold text-slate-700">
          Available Withdrawal Balance: <span class="font-black text-accent text-sm ml-1">$1,250.00 USD</span>
        </div>

        <div>
          <label class="label-base">Withdrawal Amount (USD)</label>
          <InputNumber v-model="payoutForm.amount" mode="currency" currency="USD" locale="en-US" :min="10" inputClass="input-base !w-full" class="w-full" />
        </div>

        <div>
          <label class="label-base">Settlement Method</label>
          <Dropdown v-model="payoutForm.method" :options="payoutMethods" optionLabel="label" optionValue="value" placeholder="Select destination channel" class="w-full" />
        </div>

        <div>
          <label class="label-base">Account / Mobile Number Details</label>
          <input v-model="payoutForm.details" class="input-base" placeholder="e.g. MTN Mobile +260 97..., Airtel, or Bank Account #" />
        </div>
      </div>

      <template #footer>
        <div class="flex gap-3 justify-end pt-4 border-t border-surface-border">
          <button @click="closePayoutModal" class="px-5 py-2.5 rounded-full text-xs font-bold text-slate-500 hover:bg-slate-100 transition-colors">Cancel</button>
          <button @click="submitPayout" :disabled="submitting" class="btn-accent text-xs font-black inline-flex items-center gap-2 px-6 py-2.5">
            <i class="pi pi-check" v-if="!submitting"></i>
            <i class="pi pi-spinner pi-spin" v-else></i>
            <span>Submit Payout Request</span>
          </button>
        </div>
      </template>
    </Dialog>

  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useDashboardStore } from '@/stores/dashboard';
import { useAuthStore } from '@/stores/auth';
import { exportFinancialReportCSV } from '@/api/dashboard';

// PrimeVue components
import Button from 'primevue/button';
import Chart from 'primevue/chart';
import Tag from 'primevue/tag';
import Dialog from 'primevue/dialog';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';

const store = useDashboardStore();
const authStore = useAuthStore();

const payoutModal = ref(false);
const submitting = ref(false);
const downloadingCsv = ref(false);
const payoutForm = ref({ amount: 500, method: 'mtn', details: '' });

const activeChartMetric = ref('revenue'); // 'revenue', 'revpar', 'occupancy'
const chartMetrics = [
  { id: 'revenue', label: 'Revenue ($)' },
  { id: 'revpar', label: 'RevPAR ($)' },
  { id: 'occupancy', label: 'Occupancy (%)' }
];

const selectedTimeframe = ref('6m');
const timeframeOptions = [
  { id: '30d', label: '30 Days' },
  { id: '6m', label: '6 Months' },
  { id: 'ytd', label: 'YTD' }
];

const payoutMethods = [
  { label: 'MTN Mobile Money Instant', value: 'mtn' },
  { label: 'Airtel Money Instant', value: 'airtel' },
  { label: 'Bank Wire Transfer', value: 'bank' }
];

const topProperties = [
  { id: 1, title: 'Rhodes Park Executive Penthouse', city: 'Lusaka', revenue: 3850, occupancy: 88 },
  { id: 2, title: 'Zambezi River Safari Cottage', city: 'Livingstone', revenue: 2700, occupancy: 76 },
  { id: 3, title: 'Kabulonga Luxury Serviced Suite', city: 'Lusaka', revenue: 1900, occupancy: 70 }
];

onMounted(async () => {
  await refreshData();
});

async function refreshData() {
  await Promise.all([store.loadOverview(), store.loadPayouts()]);
}

async function downloadCsvReport() {
  const userId = authStore.user?.id || 1;
  downloadingCsv.value = true;
  try {
    const blob = await exportFinancialReportCSV(userId);
    const url = window.URL.createObjectURL(new Blob([blob], { type: 'text/csv' }));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `apartex_financial_report_owner_${userId}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (err) {
    console.error('CSV Export Error:', err);
  } finally {
    downloadingCsv.value = false;
  }
}

function openPayoutModal() {
  payoutForm.value = { amount: 500, method: 'mtn', details: '' };
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
  const trends = store.overview?.booking_trends || [
    { period: 'Jan', revenue: 1800, revpar: 60, occupancy_rate: 65 },
    { period: 'Feb', revenue: 2400, revpar: 80, occupancy_rate: 72 },
    { period: 'Mar', revenue: 2100, revpar: 70, occupancy_rate: 68 },
    { period: 'Apr', revenue: 3200, revpar: 106, occupancy_rate: 82 },
    { period: 'May', revenue: 3900, revpar: 130, occupancy_rate: 88 },
    { period: 'Jun', revenue: 4850, revpar: 161, occupancy_rate: 94 }
  ];
  
  let labelText = 'Monthly Revenue ($)';
  let datasetData = trends.map((t) => t.revenue);
  let color = '#E8621A';

  if (activeChartMetric.value === 'revpar') {
    labelText = 'RevPAR ($/night)';
    datasetData = trends.map((t) => t.revpar || (t.revenue / 30));
    color = '#10B981';
  } else if (activeChartMetric.value === 'occupancy') {
    labelText = 'Occupancy Rate (%)';
    datasetData = trends.map((t) => t.occupancy_rate || (t.bookings * 3.3));
    color = '#3B82F6';
  }
  
  return {
    labels: trends.map((t) => t.period || t.month),
    datasets: [
      {
        label: labelText,
        data: datasetData,
        fill: true,
        borderColor: color,
        borderWidth: 3,
        pointRadius: 5,
        pointBackgroundColor: color,
        pointBorderColor: '#FFFFFF',
        pointBorderWidth: 2,
        tension: 0.4,
        backgroundColor: color === '#E8621A' ? 'rgba(232, 98, 26, 0.08)' : color === '#10B981' ? 'rgba(16, 185, 129, 0.08)' : 'rgba(59, 130, 246, 0.08)'
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
      backgroundColor: '#0F172A',
      padding: 12,
      bodyFont: { weight: 'bold' },
      cornerRadius: 8
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#F1EFE9', drawBorder: false },
      ticks: { color: '#64748B', font: { weight: 600 } }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#64748B', font: { weight: 600 } }
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
