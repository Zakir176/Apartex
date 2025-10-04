import apiClient from './index';

export const dashboardApi = {
  getOwnerOverview(ownerId) {
    return apiClient.get(`/dashboard/owners/${ownerId}/overview`);
  },

  getOwnerPayouts(ownerId) {
    return apiClient.get(`/dashboard/owners/${ownerId}/payouts`);
  },

  requestPayout(ownerId, payoutData) {
    return apiClient.post(`/dashboard/owners/${ownerId}/payouts/request`, payoutData);
  }
};