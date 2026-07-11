// src/api/dashboard.js
import api from './index'; // your axios instance

export async function fetchOwnerOverview(ownerId) {
  const resp = await api.get(`/dashboard/owners/${ownerId}/overview`);
  return resp.data;
}

export async function fetchOwnerPayouts(ownerId) {
  const resp = await api.get(`/dashboard/owners/${ownerId}/payouts`);
  return resp.data;
}

export async function requestPayout(ownerId, payload) {
  // payload: { amount: number, method: 'bank'|'momo', details: {...} }
  const resp = await api.post(`/dashboard/owners/${ownerId}/payouts/request`, payload);
  return resp.data;
}
