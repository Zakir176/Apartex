<template>
  <div class="max-w-[1250px] mx-auto px-4 sm:px-6 py-8 text-slate-800">
    <!-- Header -->
    <div class="flex flex-col md:flex-row justify-between items-center mb-8 gap-4">
      <div>
        <span class="text-xs font-black uppercase tracking-wider text-accent mb-1 block">Host Settlement Portal</span>
        <h1 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">Finance & Payouts</h1>
        <p class="text-slate-500 font-medium text-sm sm:text-base mt-1">Track guest payouts, manage withdrawal channels, and request fast settlements.</p>
      </div>

      <div>
        <button 
          @click="openModal" 
          :disabled="loading" 
          class="btn-accent shadow-accent font-black text-xs px-6 py-3 rounded-full inline-flex items-center gap-2"
        >
          <i class="pi pi-wallet" v-if="!loading"></i>
          <i class="pi pi-spinner pi-spin" v-else></i>
          <span>Request Instant Payout</span>
        </button>
      </div>
    </div>

    <!-- Payout Statistics -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex justify-between items-center mb-3">
          <span class="text-slate-400 text-xs font-black uppercase tracking-wider">Available Balance</span>
          <div class="w-10 h-10 rounded-xl bg-accent-light text-accent flex items-center justify-center">
            <i class="pi pi-wallet text-lg"></i>
          </div>
        </div>
        <div class="text-3xl font-black text-slate-900 tracking-tight">$1,250.00</div>
        <p class="text-xs text-slate-500 font-medium mt-1">Ready for immediate withdrawal</p>
      </div>

      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex justify-between items-center mb-3">
          <span class="text-slate-400 text-xs font-black uppercase tracking-wider">Pending Settlement</span>
          <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
            <i class="pi pi-clock text-lg"></i>
          </div>
        </div>
        <div class="text-3xl font-black text-amber-500 tracking-tight">$450.00</div>
        <p class="text-xs text-slate-500 font-medium mt-1">Held during guest stays</p>
      </div>
      
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex justify-between items-center mb-3">
          <span class="text-slate-400 text-xs font-black uppercase tracking-wider">Total Transferred</span>
          <div class="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
            <i class="pi pi-check-circle text-lg"></i>
          </div>
        </div>
        <div class="text-3xl font-black text-emerald-600 tracking-tight">{{ formatCurrency(totalWithdrawn) }}</div>
        <p class="text-xs text-slate-500 font-medium mt-1">Lifetime payout volume</p>
      </div>
    </div>

    <!-- Supported Withdrawal Channels -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-2xl p-5 border border-surface-border shadow-sm flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-amber-400 text-slate-900 font-black text-xs flex items-center justify-center shrink-0">
          MTN
        </div>
        <div>
          <h4 class="font-black text-xs text-slate-900">MTN Mobile Money</h4>
          <p class="text-[11px] text-slate-500 font-medium mt-0.5">Instant local currency transfer across Zambia.</p>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-5 border border-surface-border shadow-sm flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-rose-600 text-white font-black text-xs flex items-center justify-center shrink-0">
          AIRTEL
        </div>
        <div>
          <h4 class="font-black text-xs text-slate-900">Airtel Money</h4>
          <p class="text-[11px] text-slate-500 font-medium mt-0.5">0% fee instant mobile wallet settlement.</p>
        </div>
      </div>

      <div class="bg-white rounded-2xl p-5 border border-surface-border shadow-sm flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-navy text-white font-black text-xs flex items-center justify-center shrink-0">
          BANK
        </div>
        <div>
          <h4 class="font-black text-xs text-slate-900">Bank Transfer</h4>
          <p class="text-[11px] text-slate-500 font-medium mt-0.5">Standard SWIFT / EFT bank deposit.</p>
        </div>
      </div>
    </div>

    <!-- Payout History Table -->
    <div class="bg-white rounded-3xl border border-surface-border overflow-hidden shadow-sm">
      <div class="p-6 border-b border-surface-border flex items-center justify-between">
        <h3 class="text-base font-black text-slate-900">Transaction & Payout History</h3>
        <span class="text-xs text-slate-400 font-bold">Updated Live</span>
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
          <div class="p-12 text-center text-slate-500 font-medium text-xs">
            <i class="pi pi-inbox text-3xl mb-2 text-slate-300 block"></i>
            No payout history recorded yet.
          </div>
        </template>
        
        <Column field="id" header="Transaction ID" sortable>
          <template #body="slotProps">
            <span class="font-mono text-xs font-black text-slate-700">#TXN-{{ slotProps.data.id }}</span>
          </template>
        </Column>

        <Column field="amount" header="Amount" sortable>
          <template #body="slotProps">
            <span class="font-black text-sm text-slate-900 tracking-tight">{{ formatCurrency(slotProps.data.amount) }}</span>
          </template>
        </Column>

        <Column field="status" header="Status" sortable>
          <template #body="slotProps">
            <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" class="text-[10px] font-black uppercase tracking-wider" />
          </template>
        </Column>

        <Column field="created_at" header="Requested Date" sortable>
          <template #body="slotProps">
            <span class="text-xs font-semibold text-slate-600">{{ formatDate(slotProps.data.created_at) }}</span>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Request Modal -->
    <Dialog v-model:visible="showModal" header="Request Instant Settlement" :style="{ width: '450px', maxWidth: '95vw' }" :modal="true" contentClass="pt-2">
      <div class="flex flex-col gap-4 py-3">
        <div>
          <label class="label-base">Withdrawal Amount ($ USD)</label>
          <input v-model.number="amount" type="number" class="input-base" placeholder="Enter amount..." />
        </div>
        <div>
          <label class="label-base">Channel / Phone Number</label>
          <input v-model="details" type="text" class="input-base" placeholder="e.g. MTN Mobile +260 97..." />
        </div>
      </div>
      <template #footer>
        <div class="flex gap-2 justify-end pt-3">
          <button @click="showModal = false" class="px-4 py-2 rounded-full text-xs font-bold text-slate-500">Cancel</button>
          <button @click="handleRequestPayout" class="btn-accent text-xs font-black px-5 py-2 rounded-full">Submit Request</button>
        </div>
      </template>
    </Dialog>

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
import Dialog from 'primevue/dialog';

const auth = useAuthStore();
const payouts = ref([]);
const loading = ref(false);
const showModal = ref(false);
const amount = ref(500);
const details = ref('');

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

function openModal() {
  showModal.value = true;
}

async function handleRequestPayout() {
  if (!auth.user?.id) return;
  loading.value = true;
  try {
    await requestPayout(auth.user.id, { amount: amount.value, details: details.value });
    showModal.value = false;
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
