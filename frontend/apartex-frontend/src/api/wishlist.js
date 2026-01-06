import apiClient from './index';

export const wishlistApi = {
  getWishlist() {
    return apiClient.get('/wishlist/');
  },

  addToWishlist(apartmentId) {
    return apiClient.post('/wishlist/', { apartment_id: apartmentId });
  },

  removeFromWishlist(apartmentId) {
    return apiClient.delete(`/wishlist/${apartmentId}`);
  }
};