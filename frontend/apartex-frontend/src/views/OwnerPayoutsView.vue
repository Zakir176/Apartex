<template>
  <div class="owner-payouts-container">
    <div class="header-section">
      <div class="title-area">
        <h1>Finance & Payouts</h1>
        <p class="subtitle">Track your earnings and manage withdrawal requests</p>
      </div>
      <div class="action-area">
        <Button 
          label="Request New Payout" 
          icon="pi pi-wallet" 
          @click="handleRequestPayout" 
          :loading="loading" 
          class="p-button-raised p-button-primary" 
        />
      </div>
    </div>

    <!-- Payout Statistics (Mocked/Static for now) -->
    <div class="stats-grid mb-6">
      <Card class="stat-item">
        <template #content>
          <div class="stat-label">Pending Balance</div>
          <div class="stat-value">{{ formatCurrency(pendingBalance) }}</div>
        </template>
      </Card>
      <Card class="stat-item">
        <template #content>
          <div class="stat-label">Total Withdrawn</div>
          <div class="stat-value text-green-600">{{ formatCurrency(totalWithdrawn) }}</div>
        </template>
      </Card>
    </div>

    <!-- Payout History Table -->
    <Card class="table-card">
      <template #title>Transaction History</template>
      <template #content>
        <DataTable 
          :value="payouts" 
          paginator 
          :rows="10" 
          :loading="loading"
          responsiveLayout="scroll"
          class="p-datatable-sm"
        >
          <template #empty>No payout history found.</template>
          
          <Column field="id" header="Transaction ID" sortable></Column>
          
          <Column field="amount" header="Amount" sortable>
            <template #body="slotProps">
              <span class="font-bold text-lg text-primary">{{ formatCurrency(slotProps.data.amount) }}</span>
            </template>
          </Column>

          <Column field="status" header="Status" sortable>
            <template #body="slotProps">
              <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
            </template>
          </Column>

          <Column field="period" header="Coverage Period">
            <template #body="slotProps">
              <div class="flex align-items-center gap-2">
                <i class="pi pi-calendar-minus opacity-50"></i>
                <span>{{ formatDate(slotProps.data.period_start) }}</span>
                <i class="pi pi-arrow-right text-xs opacity-50"></i>
                <span>{{ formatDate(slotProps.data.period_end) }}</span>
              </div>
            </template>
          </Column>

          <Column field="created_at" header="Requested Date" sortable>
            <template #body="slotProps">
              {{ formatDate(slotProps.data.created_at) }}
            </template>
          </Column>
        </DataTable>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { fetchOwnerPayouts, requestPayout } from '@/api/dashboard';

// PrimeVue components
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';
import Card from 'primevue/card';

const auth = useAuthStore();
const payouts = ref([]);
const loading = ref(false);

const pendingBalance = ref(450.00); // Mocked for now, in a real app this would come from an API

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
    // In a real app, we'd fire a toast here
  } finally {
    loading.value = false;
  }
}

onMounted(loadPayouts);

const formatDate = (dateString) => {
  if (!dateString) return '-';
  return new Date(dateString).toLocaleDateString();
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

<style scoped>
.owner-payouts-container {
  max-width: 1200px;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.stat-item {
  border-radius: 12px;
  background: white;
  border: 1px solid #f1f5f9;
}

.stat-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #718096;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 800;
  color: #1a202c;
}

.table-card {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style>

