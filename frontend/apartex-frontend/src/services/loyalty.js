// src/services/loyalty.js
import api from './api'

export default {
  getPoints() {
    return api.get('/loyalty/points')
  },
  
  getRewards() {
    return api.get('/loyalty/rewards')
  },
  
  redeemReward(rewardId) {
    return api.post('/loyalty/redeem', { reward_id: rewardId })
  },
  
  getHistory() {
    return api.get('/loyalty/history')
  }
}