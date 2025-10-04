import { defineStore } from 'pinia';
import { ref } from 'vue';
import { bookingsApi } from '../api/bookings';

export const useBookingsStore = defineStore('bookings', () => {
  const bookings = ref([]);
  const currentBooking = ref(null);
  const availability = ref(null);
  const loading = ref(false);
  const error = ref(null);

  async function fetchBookings() {
    loading.value = true;
    error.value = null;
    try {
      const response = await bookingsApi.getBookings();
      bookings.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch bookings';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchUserBookings(userId) {
    loading.value = true;
    error.value = null;
    try {
      const response = await bookingsApi.getUserBookings(userId);
      bookings.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch user bookings';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function createBooking(bookingData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await bookingsApi.createBooking(bookingData);
      bookings.value.push(response.data);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to create booking';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function checkAvailability(apartmentId, dates) {
    loading.value = true;
    error.value = null;
    try {
      const response = await bookingsApi.checkAvailability(apartmentId, dates);
      availability.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to check availability';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function cancelBooking(bookingId) {
    loading.value = true;
    error.value = null;
    try {
      await bookingsApi.deleteBooking(bookingId);
      bookings.value = bookings.value.filter(booking => booking.id !== bookingId);
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to cancel booking';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    bookings,
    currentBooking,
    availability,
    loading,
    error,
    fetchBookings,
    fetchUserBookings,
    createBooking,
    checkAvailability,
    cancelBooking
  };
});