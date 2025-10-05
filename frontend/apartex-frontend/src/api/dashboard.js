// src/api/dashboard.js
import api from './index'

export const dashboardAPI = {
  // Owner endpoints
  getOwnerOverview(ownerId) {
    return api.get(`/dashboard/owners/${ownerId}/overview`)
  },
  
  getOwnerPayouts(ownerId) {
    return api.get(`/dashboard/owners/${ownerId}/payouts`)
  },
  
  requestPayout(ownerId) {
    return api.post(`/dashboard/owners/${ownerId}/payouts/request`)
  }
}

export default dashboardAPI