<template>
  <div class="map-wrapper border-round-xl overflow-hidden shadow-2 relative" :style="{ height: height, width: '100%', z-index: 1 }">
    <l-map ref="map" :zoom="13" :center="mapCenter" :use-global-leaflet="false">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      ></l-tile-layer>
      <l-marker 
        v-for="marker in allMarkers" 
        :key="marker.id" 
        :lat-lng="marker.position"
        @click="emit('marker-click', marker.raw)"
      >
        <l-tooltip>
          <div class="flex flex-column gap-1">
            <span class="font-bold text-900">{{ marker.title }}</span>
            <span v-if="marker.price" class="text-primary-600 font-extrabold">${{ marker.price }}/nt</span>
          </div>
        </l-tooltip>
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
    default: "Lusaka"
  },
  title: {
    type: String,
    default: "Apartment Location"
  },
  lat: {
    type: Number,
    default: null
  },
  lng: {
    type: Number,
    default: null
  },
  markers: {
    type: Array,
    default: () => []
  },
  height: {
    type: String,
    default: "400px"
  }
});

const emit = defineEmits(['marker-click']);

// Very simple static mapping for cities to coordinates as fallback
const cityCoordinates = {
  'Lusaka': [-15.3875, 28.3228],
  'Livingstone': [-16.8561, 25.8528],
  'Ndola': [-12.9686, 28.6366],
  'Kitwe': [-12.8167, 28.2000],
};

const mapCenter = computed(() => {
  if (props.lat !== null && props.lng !== null) {
    return [props.lat, props.lng];
  }
  if (props.markers.length > 0) {
    // Center on the first marker with coordinates
    const firstWithCoords = props.markers.find(m => m.latitude && m.longitude);
    if (firstWithCoords) return [firstWithCoords.latitude, firstWithCoords.longitude];
  }
  return cityCoordinates[props.city] || [-15.3875, 28.3228]; // Default to Lusaka
});

const allMarkers = computed(() => {
  if (props.markers.length > 0) {
    return props.markers
      .filter(m => m.latitude && m.longitude)
      .map(m => ({
        id: m.id,
        position: [m.latitude, m.longitude],
        title: m.title,
        price: m.price_per_night,
        raw: m
      }));
  }
  
  if (props.lat !== null && props.lng !== null) {
    return [{
      id: 'single',
      position: [props.lat, props.lng],
      title: props.title
    }];
  }

  // Fallback: Add a tiny random offset to make it look realistic if multiple apartments are in same city
  const center = cityCoordinates[props.city] || [-15.3875, 28.3228];
  const exactLat = center[0] + (Math.random() - 0.5) * 0.05;
  const exactLng = center[1] + (Math.random() - 0.5) * 0.05;
  return [{
    id: 'fallback',
    position: [exactLat, exactLng],
    title: props.title
  }];
});
</script>

<style scoped>
.map-wrapper {
  background: #f8fafc;
}

.price-tooltip {
  background: var(--surface-900);
  color: #fff;
  font-weight: 800;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  border: none;
  box-shadow: var(--shadow-sm);
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
