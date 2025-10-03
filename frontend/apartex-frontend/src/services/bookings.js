// src/services/bookings.js
import api from './api'

export default {
  getUserBookings() {
    return api.get('/bookings')
  },
  
  getById(id) {
    return api.get(`/bookings/${id}`)
  },
  
  create(bookingData) {
    return api.post('/bookings', bookingData)
  },
  
  cancel(id) {
    return api.put(`/bookings/${id}/cancel`)
  },
  
  update(id, bookingData) {
    return api.put(`/bookings/${id}`, bookingData)
  }
}