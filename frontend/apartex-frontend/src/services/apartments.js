// src/services/apartments.js
import api from './api'

export default {
  getFeatured() {
    return api.get('/apartments/featured')
  },
  
  getAll() {
    return api.get('/apartments')
  },
  
  getById(id) {
    return api.get(`/apartments/${id}`)
  },
  
  search(filters) {
    return api.get('/apartments/search', { params: filters })
  },
  
  createReview(apartmentId, reviewData) {
    return api.post(`/apartments/${apartmentId}/reviews`, reviewData)
  }
}