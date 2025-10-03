<!-- src/views/BookingsView.vue -->
<template>
  <div class="bookings-page">
    <div class="container">
      <!-- Header -->
      <header class="page-header">
        <h1>My Bookings</h1>
        <p>Manage your upcoming and past stays</p>
      </header>

      <!-- Booking Tabs -->
      <div class="booking-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab-btn', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.label }} ({{ getBookingsCount(tab.id) }})
        </button>
      </div>

      <!-- Bookings List -->
      <div class="bookings-content">
        <div v-if="filteredBookings.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <h3>No {{ activeTab }} bookings</h3>
          <p v-if="activeTab === 'upcoming'">
            You don't have any upcoming stays. <router-link to="/apartments">Browse apartments</router-link> to book your next trip!
          </p>
          <p v-else>
            You haven't completed any stays yet.
          </p>
        </div>

        <div v-else class="bookings-list">
          <div 
            v-for="booking in filteredBookings" 
            :key="booking.id"
            :class="['booking-card', booking.status]"
          >
            <div class="booking-main">
              <img :src="booking.image" :alt="booking.title" class="booking-image">
              <div class="booking-details">
                <div class="booking-header">
                  <h3>{{ booking.title }}</h3>
                  <div class="booking-status" :class="booking.status">
                    {{ formatStatus(booking.status) }}
                  </div>
                </div>
                <p class="location">{{ booking.location }}</p>
                
                <div class="booking-dates">
                  <div class="date-group">
                    <strong>Check-in</strong>
                    <span>{{ formatDate(booking.checkIn) }}</span>
                  </div>
                  <div class="date-group">
                    <strong>Check-out</strong>
                    <span>{{ formatDate(booking.checkOut) }}</span>
                  </div>
                </div>

                <div class="booking-info">
                  <div class="info-item">
                    <span class="icon">👥</span>
                    <span>{{ booking.guests }} guest{{ booking.guests !== 1 ? 's' : '' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="icon">🛏️</span>
                    <span>{{ booking.bedrooms }} bedroom{{ booking.bedrooms !== 1 ? 's' : '' }}</span>
                  </div>
                  <div class="info-item">
                    <span class="icon">💰</span>
                    <span>${{ booking.totalPrice }} total</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="booking-actions">
              <button 
                v-if="booking.status === 'upcoming'" 
                class="action-btn danger"
                @click="cancelBooking(booking)"
              >
                Cancel Booking
              </button>
              <button 
                v-if="booking.status === 'upcoming'" 
                class="action-btn primary"
                @click="viewBookingDetails(booking)"
              >
                View Details
              </button>
              <button 
                v-if="booking.status === 'completed'" 
                class="action-btn outline"
                @click="writeReview(booking)"
              >
                Write Review
              </button>
              <button 
                v-if="booking.status === 'completed'" 
                class="action-btn text"
                @click="viewBookingDetails(booking)"
              >
                View Receipt
              </button>
              <button 
                v-if="booking.status === 'cancelled'" 
                class="action-btn text"
                @click="rebook(booking)"
              >
                Rebook
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Booking Stats -->
      <div class="booking-stats">
        <div class="stat-card">
          <div class="stat-icon">📅</div>
          <div class="stat-content">
            <h3>{{ stats.totalBookings }}</h3>
            <p>Total Bookings</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-content">
            <h3>{{ stats.pointsEarned }}</h3>
            <p>Points Earned</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">💰</div>
          <div class="stat-content">
            <h3>${{ stats.totalSpent }}</h3>
            <p>Total Spent</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BookingsView',
  data() {
    return {
      activeTab: 'upcoming',
      tabs: [
        { id: 'upcoming', label: 'Upcoming' },
        { id: 'completed', label: 'Completed' },
        { id: 'cancelled', label: 'Cancelled' }
      ],
      bookings: [
        {
          id: 1,
          title: "Beachfront Condo",
          location: "Miami, FL",
          checkIn: "2024-11-15",
          checkOut: "2024-11-20",
          guests: 4,
          bedrooms: 3,
          totalPrice: 1200,
          status: "upcoming",
          image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
          bookingDate: "2024-10-01",
          confirmationCode: "APT20241115MIAMI"
        },
        {
          id: 2,
          title: "Mountain View Cabin",
          location: "Denver, CO",
          checkIn: "2024-12-05",
          checkOut: "2024-12-10",
          guests: 4,
          bedrooms: 2,
          totalPrice: 900,
          status: "upcoming",
          image: "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400",
          bookingDate: "2024-10-15",
          confirmationCode: "APT20241205DENVER"
        },
        {
          id: 3,
          title: "Luxury Downtown Apartment",
          location: "New York, NY",
          checkIn: "2024-08-10",
          checkOut: "2024-08-15",
          guests: 2,
          bedrooms: 1,
          totalPrice: 750,
          status: "completed",
          image: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400",
          bookingDate: "2024-07-20",
          confirmationCode: "APT20240810NYC"
        },
        {
          id: 4,
          title: "City Center Studio",
          location: "Chicago, IL",
          checkIn: "2024-09-01",
          checkOut: "2024-09-03",
          guests: 2,
          bedrooms: 1,
          totalPrice: 300,
          status: "cancelled",
          image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400",
          bookingDate: "2024-08-15",
          confirmationCode: "APT20240901CHICAGO"
        }
      ],
      stats: {
        totalBookings: 8,
        pointsEarned: 1250,
        totalSpent: 3150
      }
    }
  },
  computed: {
    filteredBookings() {
      return this.bookings.filter(booking => booking.status === this.activeTab)
    }
  },
  methods: {
    getBookingsCount(status) {
      return this.bookings.filter(booking => booking.status === status).length
    },
    formatStatus(status) {
      const statusMap = {
        upcoming: 'Upcoming',
        completed: 'Completed',
        cancelled: 'Cancelled'
      }
      return statusMap[status] || status
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { 
        weekday: 'short', 
        month: 'short', 
        day: 'numeric',
        year: 'numeric'
      })
    },
    cancelBooking(booking) {
      if (confirm(`Are you sure you want to cancel your booking at ${booking.title}?`)) {
        // In real app, this would call an API
        booking.status = 'cancelled'
        alert('Booking cancelled successfully.')
      }
    },
    viewBookingDetails(booking) {
      alert(`Booking Details:\n\nProperty: ${booking.title}\nConfirmation: ${booking.confirmationCode}\nCheck-in: ${this.formatDate(booking.checkIn)}\nCheck-out: ${this.formatDate(booking.checkOut)}\nTotal: $${booking.totalPrice}`)
    },
    writeReview(booking) {
      alert(`Write a review for ${booking.title}`)
    },
    rebook(booking) {
      this.$router.push('/apartments')
    }
  }
}
</script>

<style scoped>
.bookings-page {
  min-height: 100vh;
  background: #f7fafc;
  padding: 2rem 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 1rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2d3748;
  margin-bottom: 0.5rem;
  font-size: 2.5rem;
}

.page-header p {
  color: #718096;
  font-size: 1.1rem;
}

.booking-tabs {
  display: flex;
  background: white;
  border-radius: 12px;
  padding: 0.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.tab-btn {
  flex: 1;
  padding: 0.75rem 1rem;
  border: none;
  background: transparent;
  color: #718096;
  font-weight: 600;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
}

.tab-btn.active {
  background: #667eea;
  color: white;
}

.tab-btn:hover:not(.active) {
  background: #f7fafc;
  color: #4a5568;
}

.bookings-content {
  margin-bottom: 3rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #718096;
  max-width: 400px;
  margin: 0 auto;
}

.empty-state a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.empty-state a:hover {
  text-decoration: underline;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.booking-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition: all 0.3s;
}

.booking-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.booking-card.cancelled {
  opacity: 0.7;
  background: #f7fafc;
}

.booking-main {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.booking-image {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}

.booking-details {
  flex: 1;
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.booking-header h3 {
  color: #2d3748;
  margin: 0;
  font-size: 1.25rem;
}

.booking-status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.booking-status.upcoming {
  background: #fed7d7;
  color: #c53030;
}

.booking-status.completed {
  background: #c6f6d5;
  color: #276749;
}

.booking-status.cancelled {
  background: #e2e8f0;
  color: #4a5568;
}

.location {
  color: #718096;
  margin: 0 0 1rem 0;
  font-size: 0.95rem;
}

.booking-dates {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f7fafc;
  border-radius: 8px;
}

.date-group {
  display: flex;
  flex-direction: column;
}

.date-group strong {
  color: #4a5568;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.date-group span {
  color: #2d3748;
  font-weight: 600;
}

.booking-info {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a5568;
  font-size: 0.9rem;
}

.booking-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
  font-size: 0.9rem;
}

.action-btn.primary {
  background: #667eea;
  color: white;
}

.action-btn.primary:hover {
  background: #5a6fd8;
}

.action-btn.outline {
  background: transparent;
  border: 1px solid #667eea;
  color: #667eea;
}

.action-btn.outline:hover {
  background: #667eea;
  color: white;
}

.action-btn.danger {
  background: #fed7d7;
  color: #c53030;
  border: 1px solid #fed7d7;
}

.action-btn.danger:hover {
  background: #feb2b2;
}

.action-btn.text {
  background: transparent;
  color: #718096;
  border: none;
}

.action-btn.text:hover {
  color: #2d3748;
  background: #f7fafc;
}

.booking-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: #bee3f8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-content h3 {
  font-size: 1.75rem;
  color: #2d3748;
  margin: 0 0 0.25rem 0;
}

.stat-content p {
  color: #718096;
  margin: 0;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .booking-main {
    flex-direction: column;
  }
  
  .booking-image {
    width: 100%;
    height: 200px;
  }
  
  .booking-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .booking-dates {
    grid-template-columns: 1fr;
  }
  
  .booking-actions {
    justify-content: flex-start;
  }
  
  .booking-tabs {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .bookings-page {
    padding: 1rem 0;
  }
  
  .container {
    padding: 0 0.5rem;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .booking-info {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .booking-stats {
    grid-template-columns: 1fr;
  }
}
</style>