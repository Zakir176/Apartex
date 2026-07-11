<template>
  <div class="max-w-[1200px] mx-auto px-6 py-8">
    <div class="flex flex-col md:flex-row justify-between items-center mb-10 gap-4">
      <div>
        <h1 class="text-4xl font-extrabold text-slate-800 mb-2">Finance & Payouts</h1>
        <p class="text-slate-500 font-medium text-lg m-0">Track your earnings and manage withdrawal requests</p>
      </div>
      <div>
        <button 
          @click="handleRequestPayout" 
          :disabled="loading" 
          class="btn-accent shadow-accent inline-flex items-center gap-2"
        >
          <i class="pi pi-wallet" v-if="!loading"></i>
          <i class="pi pi-spinner pi-spin" v-else></i>
          Request New Payout
        </button>
      </div>
    </div>

    <!-- Payout Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
      <div class="card-base p-6 flex flex-col justify-between">
        <div class="flex justify-between items-center mb-4">
          <span class="text-slate-500 text-xs font-bold uppercase tracking-wider">Pending Balance</span>
          <div class="w-10 h-10 rounded-xl bg-orange-50 flex items-center justify-center">
            <i class="pi pi-clock text-accent text-lg"></i>
          </div>
        </div>
        <div class="text-4xl font-extrabold text-slate-800 tracking-tight">{{ formatCurrency(pendingBalance) }}</div>
      </div>
      
      <div class="card-base p-6 flex flex-col justify-between">
        <div class="flex justify-between items-center mb-4">
          <span class="text-slate-500 text-xs font-bold uppercase tracking-wider">Total Withdrawn</span>
          <div class="w-10 h-10 rounded-xl bg-green-50 flex items-center justify-center">
            <i class="pi pi-check-circle text-green-600 text-lg"></i>
          </div>
        </div>
        <div class="text-4xl font-extrabold text-green-600 tracking-tight">{{ formatCurrency(totalWithdrawn) }}</div>
      </div>
    </div>

    <!-- Payout History Table -->
    <div class="card-base overflow-hidden">
      <div class="p-6 border-b border-surface-border">
        <h3 class="text-lg font-bold text-slate-800">Transaction History</h3>
      </div>
      
      <DataTable 
        :value="payouts" 
        paginator 
        :rows="10" 
        :loading="loading"
        responsiveLayout="scroll"
        class="border-none"
      >
        <template #empty>
          <div class="p-8 text-center text-slate-500 font-medium">No payout history found.</div>
        </template>
        
        <Column field="id" header="Transaction ID" sortable></Column>
        
        <Column field="amount" header="Amount" sortable>
          <template #body="slotProps">
            <span class="font-extrabold text-lg text-slate-800 tracking-tight">{{ formatCurrency(slotProps.data.amount) }}</span>
          </template>
        </Column>

        <Column field="status" header="Status" sortable>
          <template #body="slotProps">
            <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" class="text-[10px] font-bold uppercase tracking-wider" />
          </template>
        </Column>

        <Column field="period" header="Coverage Period">
          <template #body="slotProps">
            <div class="flex items-center gap-2 text-sm font-medium text-slate-600">
              <i class="pi pi-calendar-minus text-slate-400"></i>
              <span>{{ formatDate(slotProps.data.period_start) }}</span>
              <i class="pi pi-arrow-right text-[10px] text-slate-300"></i>
              <span>{{ formatDate(slotProps.data.period_end) }}</span>
            </div>
          </template>
        </Column>

        <Column field="created_at" header="Requested Date" sortable>
          <template #body="slotProps">
            <span class="text-sm font-medium text-slate-600">{{ formatDate(slotProps.data.created_at) }}</span>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { fetchOwnerPayouts, requestPayout } from '@/api/dashboard';

// PrimeVue components
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';

const auth = useAuthStore();
const payouts = ref([]);
const loading = ref(false);

const pendingBalance = ref(450.00); // Mocked for now

const totalWithdrawn = computed(() => {
  return payouts.value
    .filter(p => p.status === 'completed' || p.status === 'transferred')
    .reduce((acc, p) => acc + Number(p.amount), 0);
});

async function loadPayouts() {
  if (!auth.user?.id) return;
  loading.value = true;
  try {
    const data = await fetchOwnerPayouts(auth.user.id);
    payouts.value = data;
  } finally {
    loading.value = false;
  }
}

async function handleRequestPayout() {
  if (!auth.user?.id) return;
  loading.value = true;
  try {
    await requestPayout(auth.user.id, {});
    await loadPayouts();
  } finally {
    loading.value = false;
  }
}

onMounted(loadPayouts);

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const formatCurrency = (v) => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(v);
};

const getStatusSeverity = (status) => {
  switch (status?.toLowerCase()) {
    case 'completed': 
    case 'transferred': return 'success';
    case 'pending': return 'warning';
    case 'failed': return 'danger';
    default: return 'info';
  }
};
</script>
