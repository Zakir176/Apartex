import apiClient from './index';

export const apartmentsApi = {
  getApartments(params = {}) {
    const cleanParams = {};
    if (params && typeof params === 'object') {
      for (const [key, val] of Object.entries(params)) {
        if (val !== null && val !== undefined && val !== '' && !Number.isNaN(val)) {
          cleanParams[key] = val;
        }
      }
    }
    return apiClient.get('/apartments/', { params: cleanParams });
  },

  getApartmentById(apartmentId) {
    if (!apartmentId) return Promise.reject(new Error('Apartment ID is required'));
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
  },

  getMyApartments() {
    return apiClient.get('/apartments/me');
  },

  getRoomsForProperty(propertyId) {
    if (!propertyId) return Promise.reject(new Error('Property ID is required'));
    return apiClient.get(`/rooms/property/${propertyId}`);
  }
};