// src/stores/bookings.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import bookingService from '@/services/bookings'

export const useBookingStore = defineStore('bookings', () => {
  const bookings = ref([])
  const currentBooking = ref(null)
  const isLoading = ref(false)

  const loadBookings = async () => {
    isLoading.value = true
    try {
      const response = await bookingService.getUserBookings()
      bookings.value = response.data
    } catch (error) {
      console.error('Error loading bookings:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const createBooking = async (bookingData) => {
    isLoading.value = true
    try {
      const response = await bookingService.create(bookingData)
      bookings.value.push(response.data)
      return response
    } catch (error) {
      console.error('Error creating booking:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const cancelBooking = async (bookingId) => {
    isLoading.value = true
    try {
      await bookingService.cancel(bookingId)
      const index = bookings.value.findIndex(b => b.id === bookingId)
      if (index !== -1) {
        bookings.value[index].status = 'cancelled'
      }
    } catch (error) {
      console.error('Error cancelling booking:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const getBookingById = async (id) => {
    isLoading.value = true
    try {
      const response = await bookingService.getById(id)
      currentBooking.value = response.data
    } catch (error) {
      console.error('Error loading booking details:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  return {
    bookings,
    currentBooking,
    isLoading,
    loadBookings,
    createBooking,
    cancelBooking,
    getBookingById
  }
})