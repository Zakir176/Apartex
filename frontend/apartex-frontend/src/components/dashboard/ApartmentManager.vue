<template>
  <div class="bg-white rounded shadow p-4 mb-4">
    <h3 class="font-medium mb-3">Your Apartments</h3>
    <div v-if="!apartments || apartments.length === 0" class="text-gray-500">No apartments yet.</div>
    <ul>
      <li v-for="a in apartments" :key="a.id" class="py-2 border-t flex justify-between items-center">
        <div>
          <div class="font-semibold">{{ a.name }}</div>
          <div class="text-sm text-gray-500">{{ a.location?.city || a.location?.address || '—' }}</div>
        </div>
        <div class="flex gap-2">
          <button class="text-sm">Edit</button>
          <button class="text-sm text-red-600">Remove</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  apartments: {
    type: Array,
    default: () => [],
  },
});
</script>
