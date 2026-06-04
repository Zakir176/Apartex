import apiClient from './index.js';

export const reviewsApi = {
  /**
   * Fetch all reviews for a specific apartment.
   * @param {number} apartmentId
   */
  getApartmentReviews(apartmentId) {
    return apiClient.get(`/reviews/apartment/${apartmentId}`);
  },

  /**
   * Create a new review for an apartment.
   * @param {{ apartment_id: number, rating: number, comment: string, image_urls: string[] }} payload
   */
  createReview(payload) {
    return apiClient.post('/reviews/', payload);
  }
};
