<template>
  <div class="location-picker">
    <div class="flex gap-2 mb-3">
      <div class="flex-1">
        <label class="ax-label">Latitude</label>
        <InputNumber v-model="lat" :minFractionDigits="6" :maxFractionDigits="8" inputClass="ax-input" @input="updateFromInputs" />
      </div>
      <div class="flex-1">
        <label class="ax-label">Longitude</label>
        <InputNumber v-model="lng" :minFractionDigits="6" :maxFractionDigits="8" inputClass="ax-input" @input="updateFromInputs" />
      </div>
      <div class="flex align-items-end">
        <Button icon="pi pi-search-plus" label="Geocode" @click="geocodeAddress" :loading="loading" class="p-button-outlined" v-tooltip="'Find coordinates from address'" />
      </div>
    </div>

    <div class="map-wrapper border-round-xl overflow-hidden shadow-2 relative" style="height: 300px; width: 100%; z-index: 1;">
      <l-map ref="map" :zoom="13" :center="center" :use-global-leaflet="false" @click="handleMapClick">
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          layer-type="base"
          name="OpenStreetMap"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        ></l-tile-layer>
        <l-marker v-if="lat && lng" :lat-lng="[lat, lng]"></l-marker>
      </l-map>
      <div class="map-overlay-hint">
        <span class="text-xs font-bold text-white uppercase tracking-widest">Click map to pin exact location</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import 'leaflet/dist/leaflet.css';
import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import axios from 'axios';

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({ lat: null, lng: null })
  },
  address: String,
  city: String
});

const emit = defineEmits(['update:modelValue']);

const lat = ref(props.modelValue.lat);
const lng = ref(props.modelValue.lng);
const center = ref([lat.value || -15.3875, lng.value || 28.3228]);
const loading = ref(false);

const cityCoordinates = {
  'Lusaka': [-15.3875, 28.3228],
  'Livingstone': [-16.8561, 25.8528],
  'Ndola': [-12.9686, 28.6366],
  'Kitwe': [-12.8167, 28.2000],
};

watch(() => props.modelValue, (newVal) => {
  lat.value = newVal.lat;
  lng.value = newVal.lng;
  if (lat.value && lng.value) {
    center.value = [lat.value, lng.value];
  }
}, { deep: true });

const handleMapClick = (event) => {
  lat.value = event.latlng.lat;
  lng.value = event.latlng.lng;
  emitUpdate();
};

const updateFromInputs = () => {
  if (lat.value && lng.value) {
    center.value = [lat.value, lng.value];
  }
  emitUpdate();
};

const emitUpdate = () => {
  emit('update:modelValue', { lat: lat.value, lng: lng.value });
};

const geocodeAddress = async () => {
  if (!props.city) return;
  
  loading.value = true;
  try {
    const query = `${props.address || ''} ${props.city}, Zambia`.trim();
    const response = await axios.get(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`);
    
    if (response.data && response.data.length > 0) {
      const result = response.data[0];
      lat.value = parseFloat(result.lat);
      lng.value = parseFloat(result.lon);
      center.value = [lat.value, lng.value];
      emitUpdate();
    } else {
      // Fallback to city
      if (cityCoordinates[props.city]) {
        lat.value = cityCoordinates[props.city][0];
        lng.value = cityCoordinates[props.city][1];
        center.value = [lat.value, lng.value];
        emitUpdate();
      }
    }
  } catch (error) {
    console.error('Geocoding failed', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (!lat.value && !lng.value && props.city) {
    if (cityCoordinates[props.city]) {
      center.value = cityCoordinates[props.city];
    }
  }
});
</script>

<style scoped>
.map-overlay-hint {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.6);
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  z-index: 2;
  pointer-events: none;
}
</style>
