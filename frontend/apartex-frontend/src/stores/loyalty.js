import { defineStore } from 'pinia';
import { ref } from 'vue';
import { loyaltyAPI } from '@/api/loyalty';

export const useLoyaltyStore = defineStore('loyalty', () => {
  const loyaltyStatus = ref(null);
  const userRewards = ref([]);
  const availableRewards = ref([]);
  const loyaltyTiers = ref([]);
  const loading = ref(false);
  const error = ref(null);

  // Enhanced mock data - ensure these are properly defined
  const mockUserRewards = [
    {
      id: 1,
      name: '10% Discount',
      description: 'Get 10% off your next booking',
      redeemed_at: '2024-01-15',
      used: false,
      redemption_code: 'DISC10-ABC123'
    },
    {
      id: 2,
      name: 'Early Check-in',
      description: 'Early check-in at 1 PM',
      redeemed_at: '2024-02-01',
      used: true,
      redemption_code: 'EARLY-XYZ789'
    }
  ];

  const mockAvailableRewards = [
    {
      id: 1,
      name: '10% Discount',
      description: 'Get 10% off your next booking',
      points_required: 500,
      type: 'discount'
    },
    {
      id: 2,
      name: 'Free Night',
      description: 'One free night at any standard apartment',
      points_required: 1000,
      type: 'free_night'
    },
    {
      id: 3,
      name: 'Luxury Upgrade',
      description: 'Free upgrade to a luxury apartment on your next stay',
      points_required: 1500,
      type: 'upgrade'
    },
    {
      id: 4,
      name: 'Weekend Getaway',
      description: 'Two free nights at a premium apartment',
      points_required: 2500,
      type: 'free_stay'
    }
  ];

  // Simple mock functions that always work
  async function fetchLoyaltyStatus(userId) {

    loading.value = true;
    error.value = null;
    try {
      const response = await loyaltyAPI.getLoyaltyStatus(userId);
      const data = response.data;
      
      let nextTier = 'Maximum Tier';
      let bookingsRequired = 0;
      
      if (data.loyalty_tier === 'bronze') {
        nextTier = 'Silver';
        bookingsRequired = 3;
      } else if (data.loyalty_tier === 'silver') {
        nextTier = 'Gold';
        bookingsRequired = 10;
      }
      
      loyaltyStatus.value = {
        current_tier: data.loyalty_tier,
        points: data.loyalty_points,
        total_bookings: data.total_bookings,
        bookings_required: bookingsRequired,
        next_tier: nextTier,
        bookings_needed: Math.max(0, bookingsRequired - data.total_bookings)
      };
      

      return loyaltyStatus.value;
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
      const response = await loyaltyAPI.getLoyaltyRewards(userId);
      userRewards.value = response.data.map(reward => ({
        id: reward.id,
        name: reward.reward_type === 'percentage_discount' ? `${reward.reward_value}% Discount` : 'Free Night',
        description: reward.reward_type === 'percentage_discount' ? `Get ${reward.reward_value}% off your next booking` : 'One free night at any standard apartment',
        redeemed_at: reward.earned_at,
        used: reward.status === 'used',
        redemption_code: `CODE-${reward.reward_type === 'percentage_discount' ? 'DISC' : 'FREE'}-${reward.id}`
      }));

      return userRewards.value;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch user rewards';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchLoyaltyTiers() {

    loading.value = true;
    error.value = null;
    try {
      const response = await loyaltyAPI.getLoyaltyTiers();
      loyaltyTiers.value = response.data.tiers;

      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch loyalty tiers';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchAvailableRewards() {

    
    // Fallback to mock data synchronously instead of hallucinated setTimeout delay
    // Note: The backend /tiers endpoint provides reward frequencies instead of a 'catalog'.
    availableRewards.value = mockAvailableRewards;

    return mockAvailableRewards;
  }

  async function redeemReward(rewardData) {

    loading.value = true;
    error.value = null;
    
    try {
      // In a real flow, the user would select a booking to apply the reward to.
      // We pass the data to the API. If booking_id is missing, it will throw a 422/400.
      const response = await loyaltyAPI.redeemReward(rewardData.reward_id, rewardData.booking_id);
      
      // Refresh user rewards after redemption
      if (loyaltyStatus.value) {
        await fetchUserRewards(loyaltyStatus.value.user_id || rewardData.user_id);
      }
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
      const response = await loyaltyAPI.completeBooking(bookingId);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to complete booking';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    // State
    loyaltyStatus,
    userRewards,
    availableRewards,
    loyaltyTiers,
    loading,
    error,
    
    // Actions
    fetchLoyaltyStatus,
    fetchUserRewards,
    fetchLoyaltyTiers,
    fetchAvailableRewards,
    redeemReward,
    completeBooking
  };
});