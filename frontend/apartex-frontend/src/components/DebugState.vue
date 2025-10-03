<!-- src/components/DebugState.vue -->
<template>
  <div class="debug-state" style="background: #f3f4f6; padding: 1rem; margin: 1rem 0; border-radius: 0.5rem;">
    <h3>Debug Information:</h3>
    <p><strong>Apartments array length:</strong> {{ apartments.length }}</p>
    <p><strong>Loading state:</strong> {{ loading }}</p>
    <p><strong>Apartments data:</strong></p>
    <pre>{{ JSON.stringify(apartments, null, 2) }}</pre>
  </div>
</template>

<script>
export default {
  name: 'DebugState',
  props: {
    apartments: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>