import apiClient from './index';

export const loyaltyApi = {
  getUserLoyaltyStatus(userId) {
    return apiClient.get(`/loyalty/users/${userId}/status`);
  },

  getUserRewards(userId) {
    return apiClient.get(`/loyalty/users/${userId}/rewards`);
  },

  redeemReward(rewardData) {
    return apiClient.post('/loyalty/rewards/redeem', rewardData);
  },

  completeBooking(bookingId) {
    return apiClient.put(`/loyalty/bookings/${bookingId}/complete`);
  },

  getLoyaltyTiers() {
    return apiClient.get('/loyalty/tiers');
  }
};