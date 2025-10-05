import apiClient from './index';

export const bookingsApi = {
  getBookings(params = {}) {
    return apiClient.get('/bookings/', { params });
  },

  getBookingById(bookingId) {
    return apiClient.get(`/bookings/${bookingId}`);
  },

  createBooking(bookingData) {
    return apiClient.post('/bookings/', bookingData);
  },

  updateBooking(bookingId, bookingData) {
    return apiClient.put(`/bookings/${bookingId}`, bookingData);
  },

  deleteBooking(bookingId) {
    return apiClient.delete(`/bookings/${bookingId}`);
  },

  checkAvailability(apartmentId, dates) {
    return apiClient.get(`/bookings/apartment/${apartmentId}/availability`, { 
      params: dates 
    });
  },

  getUserBookings(userId) {
    return apiClient.get(`/bookings/user/${userId}/bookings`);
  }
};