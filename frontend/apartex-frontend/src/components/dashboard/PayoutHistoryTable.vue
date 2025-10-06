<template>
  <div class="bg-white rounded shadow p-4">
    <table class="w-full text-sm">
      <thead>
        <tr class="text-left text-gray-600">
          <th>Date</th>
          <th>Amount</th>
          <th>Method</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="!payouts || payouts.length === 0">
          <td colspan="4" class="py-4 text-center text-gray-500">No payouts yet</td>
        </tr>
        <tr v-for="p in payouts" :key="p.id" class="border-t">
          <td>{{ formatDate(p.created_at) }}</td>
          <td>{{ formatCurrency(p.amount) }}</td>
          <td>{{ p.method }}</td>
          <td>{{ p.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  payouts: {
    type: Array,
    default: () => [],
  },
});

function formatCurrency(v) {
  if (v == null) return '-';
  return new Intl.NumberFormat('en-ZM', { style: 'currency', currency: 'ZMW' }).format(v);
}
function formatDate(d) {
  if (!d) return '-';
  return new Date(d).toLocaleDateString();
}
</script>
