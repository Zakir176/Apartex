import apiClient from './index.js';

export const availabilityApi = {
  /**
   * Get all blocked dates for an apartment (public).
   * @param {number} apartmentId
   */
  getBlockedDates(apartmentId) {
    return apiClient.get(`/availability/${apartmentId}`);
  },

  /**
   * Block a date range for an apartment (owner only).
   * @param {{ apartment_id, start_date, end_date, reason }} payload
   */
  blockDateRange(payload) {
    return apiClient.post('/availability/block', payload);
  },

  /**
   * Unblock a specific blocked date entry (owner only).
   * @param {number} blockId
   */
  unblockDate(blockId) {
    return apiClient.delete(`/availability/${blockId}`);
  }
};
