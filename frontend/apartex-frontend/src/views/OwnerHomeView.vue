<template>
  <section class="p-6">
    <h1 class="text-2xl font-semibold mb-4">Owner Home</h1>
    <p class="mb-4">Welcome to your owner portal. Use the dashboard to manage apartments, monitor bookings, and payouts.</p>
    <div class="flex gap-3">
      <router-link class="btn btn-primary" to="/dashboard">Go to Dashboard</router-link>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.btn { padding: 0.5rem 1rem; border-radius: 0.375rem; background: #e5e7eb; }
.btn-primary { background: #1f6feb; color: white; }
</style>
