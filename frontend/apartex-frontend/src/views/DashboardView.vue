<!-- src/views/DashboardView.vue -->
<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="text-gray-600 mt-2">Welcome back, {{ userStore.user?.email }}</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#D63384]"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p class="text-red-800 font-medium">Failed to load dashboard data</p>
        <button 
          @click="loadDashboardData"
          class="mt-4 bg-[#D63384] text-white px-4 py-2 rounded-lg hover:bg-[#C12B74]"
        >
          Try Again
        </button>
      </div>

      <!-- Owner Dashboard -->
      <div v-else-if="userStore.user?.role === 'owner'" class="space-y-6">
        <!-- Overview Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Total Revenue -->
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="p-2 bg-[#FFE5E5] rounded-lg">
                <svg class="w-6 h-6 text-[#D63384]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Revenue</p>
                <p class="text-2xl font-bold text-gray-900">${{ ownerOverview?.total_revenue || 0 }}</p>
              </div>
            </div>
          </div>

          <!-- Occupancy Rate -->
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="p-2 bg-[#FFE5E5] rounded-lg">
                <svg class="w-6 h-6 text-[#D63384]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Occupancy Rate</p>
                <p class="text-2xl font-bold text-gray-900">{{ ownerOverview?.occupancy_rate || 0 }}%</p>
              </div>
            </div>
          </div>

          <!-- Active Bookings -->
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="p-2 bg-[#FFE5E5] rounded-lg">
                <svg class="w-6 h-6 text-[#D63384]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Active Bookings</p>
                <p class="text-2xl font-bold text-gray-900">{{ ownerOverview?.active_bookings || 0 }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Payouts Section -->
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200">
            <div class="flex justify-between items-center">
              <h2 class="text-lg font-medium text-gray-900">Payouts</h2>
              <button 
                @click="requestPayout"
                :disabled="payoutLoading"
                class="bg-[#D63384] text-white px-4 py-2 rounded-lg hover:bg-[#C12B74] disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ payoutLoading ? 'Processing...' : 'Request Payout' }}
              </button>
            </div>
          </div>
          <div class="p-6">
            <div v-if="payouts.length === 0" class="text-center text-gray-500 py-8">
              <p>No payout history available</p>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="payout in payouts" 
                :key="payout.id"
                class="flex justify-between items-center p-4 border border-gray-200 rounded-lg"
              >
                <div>
                  <p class="font-medium text-gray-900">${{ payout.amount }}</p>
                  <p class="text-sm text-gray-600">{{ formatDate(payout.created_at) }}</p>
                </div>
                <span 
                  :class="{
                    'bg-green-100 text-green-800': payout.status === 'completed',
                    'bg-yellow-100 text-yellow-800': payout.status === 'pending',
                    'bg-red-100 text-red-800': payout.status === 'failed'
                  }"
                  class="px-3 py-1 rounded-full text-xs font-medium capitalize"
                >
                  {{ payout.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Renter Dashboard -->
      <div v-else class="space-y-6">
        <!-- Loyalty Summary -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-4">Loyalty Status</h2>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-2xl font-bold text-[#D63384]">{{ loyaltyStatus?.tier || 'Bronze' }}</p>
              <p class="text-gray-600">{{ loyaltyStatus?.points || 0 }} points</p>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-600">Next Tier: {{ getNextTier(loyaltyStatus?.points) }}</p>
              <div class="w-32 bg-gray-200 rounded-full h-2 mt-2">
                <div 
                  class="bg-[#FFB84D] h-2 rounded-full" 
                  :style="{ width: getTierProgress(loyaltyStatus?.points) + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Bookings -->
        <div class="bg-white rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-gray-900">Recent Bookings</h2>
          </div>
          <div class="p-6">
            <div v-if="renterBookings.length === 0" class="text-center text-gray-500 py-8">
              <p>No bookings found</p>
              <router-link 
                to="/apartments" 
                class="text-[#D63384] hover:text-[#C12B74] mt-2 inline-block"
              >
                Browse Apartments
              </router-link>
            </div>
            <div v-else class="space-y-4">
              <div 
                v-for="booking in renterBookings" 
                :key="booking.id"
                class="flex justify-between items-center p-4 border border-gray-200 rounded-lg"
              >
                <div>
                  <p class="font-medium text-gray-900">{{ booking.apartment?.title || 'Apartment' }}</p>
                  <p class="text-sm text-gray-600">
                    {{ formatDate(booking.check_in) }} - {{ formatDate(booking.check_out) }}
                  </p>
                </div>
                <span 
                  :class="{
                    'bg-green-100 text-green-800': booking.status === 'confirmed',
                    'bg-yellow-100 text-yellow-800': booking.status === 'pending',
                    'bg-red-100 text-red-800': booking.status === 'cancelled'
                  }"
                  class="px-3 py-1 rounded-full text-xs font-medium capitalize"
                >
                  {{ booking.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useBookingsStore } from '@/stores/bookings'
import dashboardAPI from '@/api/dashboard'
import loyaltyAPI from '@/api/loyalty'

const userStore = useAuthStore()
const bookingsStore = useBookingsStore()

const loading = ref(true)
const payoutLoading = ref(false)
const error = ref(false)
const ownerOverview = ref(null)
const payouts = ref([])
const loyaltyStatus = ref(null)
const renterBookings = ref([])

onMounted(async () => {
  await loadDashboardData()
})

async function loadDashboardData() {
  try {
    loading.value = true
    error.value = false
    
    if (userStore.user?.role === 'owner') {
      // Load owner data
      const [overviewResponse, payoutsResponse] = await Promise.all([
        dashboardAPI.getOwnerOverview(userStore.user.id),
        dashboardAPI.getOwnerPayouts(userStore.user.id)
      ])
      
      ownerOverview.value = overviewResponse.data
      payouts.value = payoutsResponse.data
    } else {
      // Load renter data
      const [loyaltyResponse] = await Promise.all([
        loyaltyAPI.getLoyaltyStatus(userStore.user.id),
        // Use the existing fetchUserBookings method from the store
        bookingsStore.fetchUserBookings(userStore.user.id)
      ])
      
      loyaltyStatus.value = loyaltyResponse.data
      // Use bookingsStore.bookings instead of bookingsStore.userBookings
      renterBookings.value = bookingsStore.bookings.slice(0, 5) // Show last 5 bookings
    }
  } catch (err) {
    console.error('Error loading dashboard data:', err)
    error.value = true
  } finally {
    loading.value = false
  }
}

async function requestPayout() {
  try {
    payoutLoading.value = true
    await dashboardAPI.requestPayout(userStore.user.id)
    // Reload payouts after successful request
    const response = await dashboardAPI.getOwnerPayouts(userStore.user.id)
    payouts.value = response.data
    // TODO: Add success toast
  } catch (err) {
    console.error('Error requesting payout:', err)
    // TODO: Add error toast
  } finally {
    payoutLoading.value = false
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

function getNextTier(points = 0) {
  if (points < 1000) return 'Silver (1,000 points)'
  if (points < 2500) return 'Gold (2,500 points)'
  if (points < 5000) return 'Platinum (5,000 points)'
  return 'Maximum Tier'
}

function getTierProgress(points = 0) {
  if (points < 1000) return (points / 1000) * 100
  if (points < 2500) return ((points - 1000) / 1500) * 100
  if (points < 5000) return ((points - 2500) / 2500) * 100
  return 100
}
</script>