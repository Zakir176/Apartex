<!-- src/views/DashboardView.vue -->
<template>
  <div class="dashboard-page">
    <div class="container">
      <header class="dashboard-header">
        <div class="welcome-section">
          <h1>Welcome back, {{ authStore.user?.first_name }}! 👋</h1>
          <p>Here's what's happening with your bookings today.</p>
        </div>
      </header>

      <!-- Rest of dashboard content using real data from stores -->
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useBookingStore } from '@/stores/bookings'

export default {
  name: 'DashboardView',
  setup() {
    const authStore = useAuthStore()
    const bookingStore = useBookingStore()

    onMounted(async () => {
      try {
        await bookingStore.loadBookings()
      } catch (error) {
        console.error('Failed to load bookings:', error)
      }
    })

    return {
      authStore,
      bookingStore
    }
  }
}
</script>