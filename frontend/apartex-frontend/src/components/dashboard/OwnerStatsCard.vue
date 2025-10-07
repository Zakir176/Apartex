<template>
  <div class="p-4 bg-white rounded shadow">
    <div class="text-sm text-gray-500">{{ title }}</div>
    <div class="text-2xl font-semibold mt-2">{{ value }}</div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
});
</script>

<style scoped>
</style>
