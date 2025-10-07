// src/stores/dashboard.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { fetchOwnerOverview, fetchOwnerPayouts, requestPayout } from '@/api/dashboard';
import { useAuthStore } from './auth'; // assumes this exists

export const useDashboardStore = defineStore('dashboard', () => {
  const auth = useAuthStore();

  const overview = ref(null);
  const payouts = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const lastFetched = ref(null);

  async function loadOverview() {
    if (!auth.user || !auth.user.id) return;
    loading.value = true;
    error.value = null;
    try {
      const data = await fetchOwnerOverview(auth.user.id);
      overview.value = data;
      lastFetched.value = new Date();
    } catch (err) {
      console.error('Failed to load overview', err);
      error.value = err;
    } finally {
      loading.value = false;
    }
  }

  async function loadPayouts() {
    if (!auth.user || !auth.user.id) return;
    loading.value = true;
    error.value = null;
    try {
      payouts.value = await fetchOwnerPayouts(auth.user.id);
    } catch (err) {
      console.error('Failed to load payouts', err);
      error.value = err;
    } finally {
      loading.value = false;
    }
  }

  async function submitPayoutRequest(payload) {
    if (!auth.user || !auth.user.id) throw new Error('Not authenticated');
    loading.value = true;
    try {
      const resp = await requestPayout(auth.user.id, payload);
      // refresh payouts
      await loadPayouts();
      return resp;
    } catch (err) {
      console.error('Payout request failed', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    overview,
    payouts,
    loading,
    error,
    lastFetched,
    loadOverview,
    loadPayouts,
    submitPayoutRequest,
  };
});
