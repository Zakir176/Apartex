// src/stores/apartments.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apartmentService from '@/services/apartments'

export const useApartmentStore = defineStore('apartments', () => {
  const apartments = ref([])
  const featuredApartments = ref([])
  const currentApartment = ref(null)
  const isLoading = ref(false)
  const filters = ref({
    minPrice: '',
    maxPrice: '',
    guests: '',
    bedrooms: '',
    amenities: []
  })

  const getApartmentById = (id) => {
    return apartments.value.find(apt => apt.id === parseInt(id))
  }

  const loadFeaturedApartments = async () => {
    isLoading.value = true
    try {
      const response = await apartmentService.getFeatured()
      featuredApartments.value = response.data
    } catch (error) {
      console.error('Error loading featured apartments:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const loadAllApartments = async () => {
    isLoading.value = true
    try {
      const response = await apartmentService.getAll()
      apartments.value = response.data
    } catch (error) {
      console.error('Error loading apartments:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const loadApartmentDetail = async (id) => {
    isLoading.value = true
    try {
      const response = await apartmentService.getById(id)
      currentApartment.value = response.data
    } catch (error) {
      console.error('Error loading apartment details:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const searchApartments = async (searchParams) => {
    isLoading.value = true
    try {
      const response = await apartmentService.search(searchParams)
      apartments.value = response.data
    } catch (error) {
      console.error('Error searching apartments:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  return {
    apartments,
    featuredApartments,
    currentApartment,
    isLoading,
    filters,
    getApartmentById,
    loadFeaturedApartments,
    loadAllApartments,
    loadApartmentDetail,
    searchApartments
  }
})