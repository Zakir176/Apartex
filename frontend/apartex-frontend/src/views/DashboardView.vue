<!-- src/views/DashboardView.vue -->
<template>
  <div class="dashboard-page">
    <div class="container">
      <!-- Header -->
      <header class="dashboard-header">
        <div class="welcome-section">
          <h1>Welcome back, Sarah! 👋</h1>
          <p>Here's what's happening with your bookings today.</p>
        </div>
        <div class="header-actions">
          <button class="action-btn primary">Book New Stay</button>
          <div class="user-menu">
            <div class="user-avatar">S</div>
          </div>
        </div>
      </header>

      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon upcoming">📅</div>
          <div class="stat-info">
            <h3>2</h3>
            <p>Upcoming Stays</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon completed">✅</div>
          <div class="stat-info">
            <h3>12</h3>
            <p>Completed Trips</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon loyalty">⭐</div>
          <div class="stat-info">
            <h3>850</h3>
            <p>Loyalty Points</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon savings">💰</div>
          <div class="stat-info">
            <h3>$240</h3>
            <p>Total Savings</p>
          </div>
        </div>
      </div>

      <div class="dashboard-content">
        <!-- Upcoming Bookings -->
        <section class="dashboard-section">
          <div class="section-header">
            <h2>Upcoming Bookings</h2>
            <router-link to="/bookings" class="view-all">View All</router-link>
          </div>
          <div class="bookings-list">
            <div v-for="booking in upcomingBookings" :key="booking.id" class="booking-card">
              <img :src="booking.image" :alt="booking.title" class="booking-image">
              <div class="booking-info">
                <h3>{{ booking.title }}</h3>
                <p class="location">{{ booking.location }}</p>
                <div class="booking-dates">
                  <span>{{ booking.checkIn }} - {{ booking.checkOut }}</span>
                </div>
                <div class="booking-status upcoming">Upcoming</div>
              </div>
              <div class="booking-actions">
                <button class="action-btn outline">View Details</button>
                <button class="action-btn text">Cancel</button>
              </div>
            </div>
          </div>
        </section>

        <!-- Recent Activity -->
        <section class="dashboard-section">
          <div class="section-header">
            <h2>Recent Activity</h2>
          </div>
          <div class="activity-list">
            <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
              <div class="activity-icon" :class="activity.type">{{ activity.icon }}</div>
              <div class="activity-content">
                <p>{{ activity.message }}</p>
                <span class="activity-time">{{ activity.time }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Quick Actions -->
        <section class="dashboard-section">
          <div class="section-header">
            <h2>Quick Actions</h2>
          </div>
          <div class="quick-actions">
            <router-link to="/apartments" class="quick-action">
              <div class="action-icon">🔍</div>
              <span>Search Apartments</span>
            </router-link>
            <router-link to="/bookings" class="quick-action">
              <div class="action-icon">📋</div>
              <span>My Bookings</span>
            </router-link>
            <router-link to="/loyalty" class="quick-action">
              <div class="action-icon">⭐</div>
              <span>Loyalty Rewards</span>
            </router-link>
            <a href="#" class="quick-action">
              <div class="action-icon">👤</div>
              <span>Profile Settings</span>
            </a>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardView',
  data() {
    return {
      upcomingBookings: [
        {
          id: 1,
          title: "Beachfront Condo",
          location: "Miami, FL",
          checkIn: "Nov 15, 2024",
          checkOut: "Nov 20, 2024",
          image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=300"
        },
        {
          id: 2,
          title: "Mountain View Cabin",
          location: "Denver, CO",
          checkIn: "Dec 5, 2024",
          checkOut: "Dec 10, 2024",
          image: "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=300"
        }
      ],
      recentActivity: [
        {
          id: 1,
          type: 'booking',
          icon: '🏠',
          message: 'You booked Mountain View Cabin for December',
          time: '2 days ago'
        },
        {
          id: 2,
          type: 'loyalty',
          icon: '⭐',
          message: 'Earned 150 loyalty points for your recent stay',
          time: '1 week ago'
        },
        {
          id: 3,
          type: 'payment',
          icon: '💳',
          message: 'Payment completed for Beachfront Condo',
          time: '2 weeks ago'
        }
      ]
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: #f7fafc;
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.welcome-section h1 {
  color: #2d3748;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.welcome-section p {
  color: #718096;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
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

.action-btn.text {
  background: transparent;
  color: #718096;
  border: none;
}

.action-btn.text:hover {
  color: #2d3748;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid #e2e8f0;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.stat-icon.upcoming {
  background: #fed7d7;
  color: #c53030;
}

.stat-icon.completed {
  background: #c6f6d5;
  color: #276749;
}

.stat-icon.loyalty {
  background: #fefcbf;
  color: #d69e2e;
}

.stat-icon.savings {
  background: #bee3f8;
  color: #2c5aa0;
}

.stat-info h3 {
  font-size: 2rem;
  color: #2d3748;
  margin: 0;
}

.stat-info p {
  color: #718096;
  margin: 0;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.dashboard-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  color: #2d3748;
  margin: 0;
  font-size: 1.5rem;
}

.view-all {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
}

.view-all:hover {
  text-decoration: underline;
}

.bookings-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.booking-card {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  transition: all 0.3s;
}

.booking-card:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.booking-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}

.booking-info {
  flex: 1;
}

.booking-info h3 {
  margin: 0 0 0.25rem 0;
  color: #2d3748;
  font-size: 1.1rem;
}

.location {
  color: #718096;
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
}

.booking-dates {
  color: #4a5568;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.booking-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.booking-status.upcoming {
  background: #fed7d7;
  color: #c53030;
}

.booking-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  justify-content: center;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}

.activity-icon.booking {
  background: #bee3f8;
  color: #2c5aa0;
}

.activity-icon.loyalty {
  background: #fefcbf;
  color: #d69e2e;
}

.activity-icon.payment {
  background: #c6f6d5;
  color: #276749;
}

.activity-content p {
  margin: 0 0 0.25rem 0;
  color: #2d3748;
}

.activity-time {
  color: #718096;
  font-size: 0.8rem;
}

.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.quick-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem 1rem;
  background: #f7fafc;
  border-radius: 8px;
  text-decoration: none;
  color: #4a5568;
  transition: all 0.3s;
  text-align: center;
}

.quick-action:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
}

.action-icon {
  font-size: 1.5rem;
}

.quick-action span {
  font-weight: 600;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 968px) {
  .dashboard-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .booking-card {
    flex-direction: column;
  }
  
  .booking-image {
    width: 100%;
    height: 120px;
  }
  
  .quick-actions {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-page {
    padding: 1rem 0;
  }
  
  .container {
    padding: 0 0.5rem;
  }
}
</style>