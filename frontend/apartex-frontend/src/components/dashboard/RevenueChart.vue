<template>
  <div class="bg-white rounded shadow p-4">
    <h3 class="font-medium mb-2">Monthly Revenue</h3>
    <div v-if="!hasData" class="text-gray-500">No revenue data</div>
    <div v-else class="w-full overflow-x-auto">
      <svg :width="width" :height="height">
        <g v-for="(v, i) in data.values" :key="i">
          <rect
            :x="i * (barWidth + gap)"
            :y="height - (v / maxVal) * chartHeight"
            :width="barWidth"
            :height="(v / maxVal) * chartHeight"
            fill="#1f6feb"
          />
          <text :x="i * (barWidth + gap) + barWidth/2" :y="height - 4" font-size="10" text-anchor="middle">{{ data.labels[i] }}</text>
        </g>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({
  data: {
    type: Object,
    default: () => ({ labels: [], values: [] }),
  },
});

const width = 600;
const height = 160;
const gap = 6;
const barWidth = 24;
const chartHeight = 110;

const maxVal = computed(() => {
  const vals = props.data.values || [];
  return vals.length ? Math.max(...vals) : 1;
});
const hasData = computed(() => (props.data.values || []).length > 0);
</script>

<style scoped>
svg { width: 100%; height: auto; }
</style>
