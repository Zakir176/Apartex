import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useLoyaltyStore = defineStore('loyalty', () => {
  const loyaltyStatus = ref(null);
  const userRewards = ref([]);
  const availableRewards = ref([]);
  const loyaltyTiers = ref([]);
  const loading = ref(false);
  const error = ref(null);

  // Enhanced mock data - ensure these are properly defined
  const mockLoyaltyStatus = {
    user_id: 1,
    current_tier: 'Gold',
    points: 1250,
    next_tier: 'Platinum',
    points_required: 2000
  };

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

  const mockLoyaltyTiers = [
    {
      name: 'Bronze',
      required_points: 0,
      benefits: [
        'Earn 1 point per $1 spent',
        'Basic customer support',
        'Standard booking options'
      ]
    },
    {
      name: 'Silver',
      required_points: 500,
      benefits: [
        'Earn 1.25 points per $1 spent',
        'Priority customer support',
        'Early check-in/late checkout',
        'Free cancellation up to 48 hours'
      ]
    },
    {
      name: 'Gold',
      required_points: 1000,
      benefits: [
        'Earn 1.5 points per $1 spent',
        '24/7 VIP support',
        'Free room upgrades when available',
        'Welcome gift on arrival',
        'Dedicated booking specialist'
      ]
    },
    {
      name: 'Platinum',
      required_points: 2000,
      benefits: [
        'Earn 2 points per $1 spent',
        'Dedicated concierge service',
        'Complimentary airport transfer',
        'Exclusive member events',
        'Suite upgrades when available',
        'Late checkout until 4 PM'
      ]
    }
  ];

  // Simple mock functions that always work
  async function fetchLoyaltyStatus(userId) {
    console.log('🔄 Fetching loyalty status for user:', userId);
    loading.value = true;
    error.value = null;
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Always return mock data
    loyaltyStatus.value = mockLoyaltyStatus;
    console.log('✅ Loyalty status set:', loyaltyStatus.value);
    loading.value = false;
    return mockLoyaltyStatus;
  }

  async function fetchUserRewards(userId) {
    console.log('🔄 Fetching user rewards for user:', userId);
    loading.value = true;
    error.value = null;
    
    await new Promise(resolve => setTimeout(resolve, 600));
    
    userRewards.value = mockUserRewards;
    console.log('✅ User rewards set:', userRewards.value);
    loading.value = false;
    return mockUserRewards;
  }

  async function fetchLoyaltyTiers() {
    console.log('🔄 Fetching loyalty tiers');
    loading.value = true;
    error.value = null;
    
    await new Promise(resolve => setTimeout(resolve, 500));
    
    loyaltyTiers.value = mockLoyaltyTiers;
    console.log('✅ Loyalty tiers set:', loyaltyTiers.value);
    loading.value = false;
    return mockLoyaltyTiers;
  }

  async function fetchAvailableRewards() {
    console.log('🔄 Fetching available rewards');
    
    await new Promise(resolve => setTimeout(resolve, 400));
    
    availableRewards.value = mockAvailableRewards;
    console.log('✅ Available rewards set:', availableRewards.value);
    return mockAvailableRewards;
  }

  async function redeemReward(rewardData) {
    console.log('🔄 Redeeming reward:', rewardData);
    loading.value = true;
    error.value = null;
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Create new reward
    const newReward = {
      id: Date.now(),
      name: mockAvailableRewards.find(r => r.id === rewardData.reward_id)?.name || 'Reward',
      description: mockAvailableRewards.find(r => r.id === rewardData.reward_id)?.description || '',
      redeemed_at: new Date().toISOString().split('T')[0],
      used: false,
      redemption_code: `CODE-${Math.random().toString(36).substr(2, 8).toUpperCase()}`
    };
    
    userRewards.value.unshift(newReward);
    console.log('✅ Reward redeemed:', newReward);
    loading.value = false;
    return newReward;
  }

  async function completeBooking(bookingId) {
    console.log('🔄 Completing booking:', bookingId);
    loading.value = true;
    error.value = null;
    
    await new Promise(resolve => setTimeout(resolve, 500));
    
    loading.value = false;
    return { success: true, points_earned: 100 };
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