// src/api/loyalty.js
import api from './index'

export const loyaltyAPI = {
  getLoyaltyStatus(userId) {
    return api.get(`/loyalty/users/${userId}/status`)
  },
  
  getLoyaltyRewards(userId) {
    return api.get(`/loyalty/users/${userId}/rewards`)
  },
  
  redeemReward(rewardId, bookingId) {
    return api.post('/loyalty/rewards/redeem', { reward_id: rewardId, booking_id: bookingId })
  },

  getLoyaltyTiers() {
    return api.get('/loyalty/tiers');
  },

  completeBooking(bookingId) {
    return api.put(`/loyalty/bookings/${bookingId}/complete`);
  }
}

export default loyaltyAPI