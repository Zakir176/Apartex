import { defineStore } from 'pinia';
import { ref } from 'vue';
import { loyaltyApi } from '../api/loyalty';

export const useLoyaltyStore = defineStore('loyalty', () => {
  const loyaltyStatus = ref(null);
  const availableRewards = ref([]);
  const loyaltyTiers = ref([]);
  const loading = ref(false);
  const error = ref(null);

  async function fetchLoyaltyStatus(userId) {
    loading.value = true;
    error.value = null;
    try {
      const response = await loyaltyApi.getUserLoyaltyStatus(userId);
      loyaltyStatus.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch loyalty status';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchUserRewards(userId) {
    loading.value = true;
    error.value = null;
    try {
      const response = await loyaltyApi.getUserRewards(userId);
      availableRewards.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch rewards';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchLoyaltyTiers() {
    loading.value = true;
    error.value = null;
    try {
      const response = await loyaltyApi.getLoyaltyTiers();
      loyaltyTiers.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch loyalty tiers';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function redeemReward(rewardData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await loyaltyApi.redeemReward(rewardData);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to redeem reward';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function completeBooking(bookingId) {
    loading.value = true;
    error.value = null;
    try {
      const response = await loyaltyApi.completeBooking(bookingId);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to complete booking';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    loyaltyStatus,
    availableRewards,
    loyaltyTiers,
    loading,
    error,
    fetchLoyaltyStatus,
    fetchUserRewards,
    fetchLoyaltyTiers,
    redeemReward,
    completeBooking
  };
});