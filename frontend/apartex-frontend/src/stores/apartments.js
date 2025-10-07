import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { apartmentsApi } from '../api/apartments';

export const useApartmentsStore = defineStore('apartments', () => {
  const apartments = ref([]);
  const currentApartment = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const featuredApartments = computed(() => 
    apartments.value.filter(apt => apt.featured).slice(0, 6)
  );

  async function fetchApartments(params = {}) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apartmentsApi.getApartments(params);
      apartments.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch apartments';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchApartmentById(apartmentId) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apartmentsApi.getApartmentById(apartmentId);
      currentApartment.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch apartment';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function createApartment(apartmentData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apartmentsApi.createApartment(apartmentData);
      apartments.value.push(response.data);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to create apartment';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateApartment(apartmentId, apartmentData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apartmentsApi.updateApartment(apartmentId, apartmentData);
      const idx = apartments.value.findIndex(a => a.id === apartmentId);
      if (idx !== -1) apartments.value[idx] = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update apartment';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteApartment(apartmentId) {
    loading.value = true;
    error.value = null;
    try {
      await apartmentsApi.deleteApartment(apartmentId);
      apartments.value = apartments.value.filter(a => a.id !== apartmentId);
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete apartment';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    apartments,
    currentApartment,
    loading,
    error,
    featuredApartments,
    fetchApartments,
    fetchApartmentById,
    createApartment,
    updateApartment,
    deleteApartment
  };
});