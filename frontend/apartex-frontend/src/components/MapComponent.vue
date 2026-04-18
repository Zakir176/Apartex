<template>
  <div class="map-wrapper border-round-xl overflow-hidden shadow-2 relative" style="height: 400px; width: 100%; z-index: 1;">
    <l-map ref="map" :zoom="13" :center="mapCenter" :use-global-leaflet="false">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      ></l-tile-layer>
      <l-marker v-if="markerPosition" :lat-lng="markerPosition">
        <l-tooltip>{{ title }}</l-tooltip>
      </l-marker>
    </l-map>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue';
import 'leaflet/dist/leaflet.css';
import { LMap, LTileLayer, LMarker, LTooltip } from '@vue-leaflet/vue-leaflet';

const props = defineProps({
  city: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: "Apartment Location"
  }
});

// Very simple static mapping for cities to coordinates for simulation purposes.
// In a real app, this would use a geocoding API or exact coordinates from the backend.
const cityCoordinates = {
  'Lusaka': [-15.3875, 28.3228],
  'Livingstone': [-16.8561, 25.8528],
  'Ndola': [-12.9686, 28.6366],
  'Kitwe': [-12.8167, 28.2000],
};

const mapCenter = computed(() => {
  return cityCoordinates[props.city] || [-15.3875, 28.3228]; // Default to Lusaka
});

const markerPosition = computed(() => {
   // Add a tiny random offset to make it look realistic if multiple apartments are in same city
   const exactLat = mapCenter.value[0] + (Math.random() - 0.5) * 0.05;
   const exactLng = mapCenter.value[1] + (Math.random() - 0.5) * 0.05;
   return [exactLat, exactLng];
});
</script>

<style scoped>
.map-wrapper {
  background: #f8fafc;
}

/* Fix leaflet icon path issues in Vue/Vite */
:deep(.leaflet-pane) {
  z-index: 1;
}
:deep(.leaflet-top),
:deep(.leaflet-bottom) {
  z-index: 2;
}
</style>
