<template>
  <div class="page-container">
    <h2>Owner Bookings</h2>

    <div class="filters">
      <label>
        Status
        <select v-model="status">
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="confirmed">Confirmed</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </label>
    </div>

    <div v-if="loading">Loading...</div>
    <div v-else>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Apartment</th>
            <th>Check-in</th>
            <th>Check-out</th>
            <th>Guests</th>
            <th>Total</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in filteredBookings" :key="b.id">
            <td>{{ b.id }}</td>
            <td>{{ b.apartment_id }}</td>
            <td>{{ b.check_in }}</td>
            <td>{{ b.check_out }}</td>
            <td>{{ b.guests }}</td>
            <td>${{ Number(b.total_price).toFixed(2) }}</td>
            <td><span :class="['badge', b.status]">{{ b.status }}</span></td>
          </tr>
        </tbody>
      </table>
      <div v-if="bookings.length === 0">No bookings found.</div>
    </div>
  </div>
  
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import api from '@/api/index';
import { useAuthStore } from '@/stores/auth';

const auth = useAuthStore();
const bookings = ref([]);
const loading = ref(false);
const status = ref('');

const filteredBookings = computed(() => {
  if (!status.value) return bookings.value;
  return bookings.value.filter(b => b.status === status.value);
});

async function loadBookings() {
  if (!auth.user?.id) return;
  loading.value = true;
  try {
    const resp = await api.get(`/bookings/owner/${auth.user.id}/bookings`);
    bookings.value = resp.data;
  } finally {
    loading.value = false;
  }
}

onMounted(loadBookings);
</script>

<style scoped>
.page-container { padding: 24px; }
h2 { margin-bottom: 12px; }
.filters { margin-bottom: 12px; }
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { border: 1px solid #e5e7eb; padding: 8px; text-align: left; }
.badge { padding: 2px 8px; border-radius: 9999px; text-transform: capitalize; }
.badge.confirmed { background: #dcfce7; color: #166534; }
.badge.pending { background: #fef9c3; color: #854d0e; }
.badge.completed { background: #dbeafe; color: #1e40af; }
.badge.cancelled { background: #fee2e2; color: #991b1b; }
</style>

