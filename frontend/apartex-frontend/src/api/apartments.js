import apiClient from './index';

export const apartmentsApi = {
  getApartments(params = {}) {
    return apiClient.get('/apartments/', { params });
  },

  getApartmentById(apartmentId) {
    return apiClient.get(`/apartments/${apartmentId}`);
  },

  createApartment(apartmentData) {
    return apiClient.post('/apartments/', apartmentData);
  },

  updateApartment(apartmentId, apartmentData) {
    return apiClient.put(`/apartments/${apartmentId}`, apartmentData);
  },

  deleteApartment(apartmentId) {
    return apiClient.delete(`/apartments/${apartmentId}`);
  }
};