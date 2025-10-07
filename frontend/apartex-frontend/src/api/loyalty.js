// src/api/loyalty.js
import api from './index'

export const loyaltyAPI = {
  getLoyaltyStatus(userId) {
    return api.get(`/loyalty/users/${userId}/status`)
  },
  
  getLoyaltyRewards(userId) {
    return api.get(`/loyalty/users/${userId}/rewards`)
  },
  
  redeemReward(rewardId) {
    return api.post('/loyalty/rewards/redeem', { reward_id: rewardId })
  }
}

export default loyaltyAPI