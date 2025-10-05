import { defineStore } from 'pinia';
import { ref } from 'vue';
import { dashboardAPI } from '@/api/dashboard';

export const useDashboardStore = defineStore('dashboard', () => {
  const ownerOverview = ref(null);
  const payouts = ref([]);
  const loading = ref(false);
  const error = ref(null);

  // Mock data for development
  const mockOwnerOverview = {
    owner_id: 1,
    total_revenue: 12500,
    monthly_revenue: 3200,
    total_bookings: 45,
    occupancy_rate: 0.78,
    average_rating: 4.5,
    active_apartments: 3,
    pending_bookings: 2,
    upcoming_bookings: 5
  };

  const mockPayouts = [
    {
      id: 1,
      amount: 1200,
      status: 'completed',
      date: '2024-01-15',
      description: 'Payout for December bookings'
    },
    {
      id: 2,
      amount: 1500,
      status: 'pending',
      date: '2024-02-01',
      description: 'Payout for January bookings'
    },
    {
      id: 3,
      amount: 1100,
      status: 'completed',
      date: '2023-12-01',
      description: 'Payout for November bookings'
    }
  ];

  async function fetchOwnerOverview(ownerId) {
    console.log('🔄 Fetching owner overview for:', ownerId);
    loading.value = true;
    error.value = null;
    
    try {
      // TODO: Replace with actual API call
      // const response = await dashboardApi.getOwnerOverview(ownerId);
      // ownerOverview.value = response.data;
      
      await new Promise(resolve => setTimeout(resolve, 800));
      ownerOverview.value = mockOwnerOverview;
      console.log('✅ Owner overview loaded:', ownerOverview.value);
      return mockOwnerOverview;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch owner overview';
      console.error('❌ Error fetching owner overview:', error.value);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchOwnerPayouts(ownerId) {
    console.log('🔄 Fetching payouts for:', ownerId);
    loading.value = true;
    error.value = null;
    
    try {
      // TODO: Replace with actual API call
      // const response = await dashboardApi.getOwnerPayouts(ownerId);
      // payouts.value = response.data;
      
      await new Promise(resolve => setTimeout(resolve, 600));
      payouts.value = mockPayouts;
      console.log('✅ Payouts loaded:', payouts.value);
      return mockPayouts;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch payouts';
      console.error('❌ Error fetching payouts:', error.value);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function requestPayout(ownerId, payoutData) {
    console.log('🔄 Requesting payout for:', ownerId, payoutData);
    loading.value = true;
    error.value = null;
    
    try {
      // TODO: Replace with actual API call
      // const response = await dashboardApi.requestPayout(ownerId, payoutData);
      
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Create new payout request
      const newPayout = {
        id: Date.now(),
        amount: payoutData.amount,
        status: 'pending',
        date: new Date().toISOString().split('T')[0],
        description: payoutData.description || 'Payout request'
      };
      
      payouts.value.unshift(newPayout);
      console.log('✅ Payout requested:', newPayout);
      return newPayout;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to request payout';
      console.error('❌ Error requesting payout:', error.value);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    // State
    ownerOverview,
    payouts,
    loading,
    error,
    
    // Actions
    fetchOwnerOverview,
    fetchOwnerPayouts,
    requestPayout
  };
});