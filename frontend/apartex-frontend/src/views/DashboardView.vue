<template>
  <section class="p-6">
    <h1 class="text-2xl font-semibold mb-4">Owner Dashboard</h1>

    <div v-if="store.loading" class="py-8">
      <p>Loading dashboard…</p>
    </div>

    <div v-if="store.error" class="text-red-600">
      <p>Error loading dashboard. Check console for details.</p>
    </div>

    <div v-if="store.overview" class="grid gap-6 grid-cols-1 md:grid-cols-3 mb-6">
      <OwnerStatsCard title="Total Revenue" :value="formatCurrency(store.overview.total_revenue)" />
      <OwnerStatsCard title="Active Bookings" :value="store.overview.active_bookings" />
      <OwnerStatsCard title="Occupancy Rate" :value="formatPercent(store.overview.occupancy_rate)" />
    </div>

    <div class="grid gap-6 grid-cols-1 lg:grid-cols-2">
      <div>
        <RevenueChart :data="chartData" />
      </div>
      <div>
        <ApartmentManager :apartments="store.overview?.apartments || []" />
        <div class="mt-6">
          <h2 class="text-lg font-medium mb-2">Payouts</h2>
          <PayoutHistoryTable :payouts="store.payouts" />
          <div class="mt-4">
            <button @click="openPayoutModal" class="btn btn-primary">Request Payout</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Payout modal (simple) -->
    <div v-if="payoutModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white p-6 rounded shadow w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4">Request Payout</h3>

        <label class="block mb-2">
          <span>Amount</span>
          <input v-model.number="payoutForm.amount" type="number" class="input" />
        </label>

        <label class="block mb-2">
          <span>Method</span>
          <select v-model="payoutForm.method" class="input">
            <option value="bank">Bank Transfer</option>
            <option value="momo">Mobile Money</option>
          </select>
        </label>

        <label v-if="payoutForm.method === 'bank'" class="block mb-2">
          <span>Bank details</span>
          <input v-model="payoutForm.details" placeholder="Account number / Bank" class="input" />
        </label>

        <div class="flex justify-end gap-2 mt-4">
          <button @click="closePayoutModal" class="btn">Cancel</button>
          <button @click="submitPayout" class="btn btn-primary" :disabled="submitting">Send Request</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useDashboardStore } from '@/stores/dashboard';
import OwnerStatsCard from '@/components/dashboard/OwnerStatsCard.vue';
import RevenueChart from '@/components/dashboard/RevenueChart.vue';
import ApartmentManager from '@/components/dashboard/ApartmentManager.vue';
import PayoutHistoryTable from '@/components/dashboard/PayoutHistoryTable.vue';

const store = useDashboardStore();

const payoutModal = ref(false);
const submitting = ref(false);
const payoutForm = ref({ amount: 0, method: 'bank', details: '' });

onMounted(async () => {
  await Promise.all([store.loadOverview(), store.loadPayouts()]);
});

function openPayoutModal() {
  payoutForm.value = { amount: 0, method: 'bank', details: '' };
  payoutModal.value = true;
}

function closePayoutModal() {
  payoutModal.value = false;
}

async function submitPayout() {
  submitting.value = true;
  try {
    await store.submitPayoutRequest({
      amount: payoutForm.value.amount,
      method: payoutForm.value.method,
      details: payoutForm.value.details,
    });
    closePayoutModal();
    // optionally show toast
  } catch (err) {
    console.error(err);
    alert('Payout request failed');
  } finally {
    submitting.value = false;
  }
}

const chartData = computed(() => {
  // backend should provide monthly_revenue: [{month: '2025-09', revenue: 1000}, ...]
  const monthly = store.overview?.monthly_revenue || [];
  return {
    labels: monthly.map((m) => m.month),
    values: monthly.map((m) => m.revenue),
  };
});

function formatCurrency(v) {
  if (v == null) return '-';
  return new Intl.NumberFormat('en-ZM', { style: 'currency', currency: 'ZMW' }).format(v);
}
function formatPercent(p) {
  if (p == null) return '-';
  return `${Math.round(p * 100)}%`;
}
</script>

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
