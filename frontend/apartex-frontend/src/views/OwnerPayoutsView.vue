<template>
  <div class="page-container">
    <h2>Payouts</h2>

    <div class="actions">
      <button class="btn" :disabled="loading" @click="handleRequestPayout">{{ loading ? 'Requesting...' : 'Request Payout' }}</button>
    </div>

    <h3>History</h3>
    <div v-if="loading">Loading...</div>
    <table v-else class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Amount</th>
          <th>Status</th>
          <th>Period</th>
          <th>Created</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in payouts" :key="p.id">
          <td>{{ p.id }}</td>
          <td>${{ Number(p.amount).toFixed(2) }}</td>
          <td>{{ p.status }}</td>
          <td>{{ p.period_start }} → {{ p.period_end }}</td>
          <td>{{ p.created_at }}</td>
        </tr>
      </tbody>
    </table>
    <div v-if="!loading && payouts.length === 0">No payouts yet.</div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { fetchOwnerPayouts, requestPayout } from '@/api/dashboard';

const auth = useAuthStore();
const payouts = ref([]);
const loading = ref(false);

async function loadPayouts() {
  if (!auth.user?.id) return;
  loading.value = true;
  try {
    payouts.value = await fetchOwnerPayouts(auth.user.id);
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
</script>

<style scoped>
.page-container { padding: 24px; }
h2 { margin-bottom: 12px; }
.actions { margin-bottom: 12px; }
.btn { padding: 8px 14px; background: #2563eb; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { border: 1px solid #e5e7eb; padding: 8px; text-align: left; }
</style>

