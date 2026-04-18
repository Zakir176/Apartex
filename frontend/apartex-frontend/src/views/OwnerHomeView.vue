<template>
  <div class="owner-home-container">
    <div class="welcome-header">
      <h1>Welcome back, {{ authStore.user?.name }}!</h1>
      <p>Efficiently manage your properties and maximize your earnings from one central hub.</p>
    </div>

    <!-- Quick Action Cards -->
    <div class="quick-actions-grid">
      <Card class="action-card" @click="router.push('/owner/apartments')">
        <template #content>
          <div class="action-icon list-apt">
            <i class="pi pi-plus-circle"></i>
          </div>
          <h3>List New Apartment</h3>
          <p>Create a beautiful listing and start reaching guests instantly.</p>
          <Button label="Add Listing" icon="pi pi-plus" class="p-button-text p-button-sm" />
        </template>
      </Card>

      <Card class="action-card" @click="router.push('/dashboard')">
        <template #content>
          <div class="action-icon analytics">
            <i class="pi pi-chart-line"></i>
          </div>
          <h3>View Performance</h3>
          <p>Analyze revenue, occupancy rates, and optimization tips.</p>
          <Button label="Open Analytics" icon="pi pi-external-link" class="p-button-text p-button-sm" />
        </template>
      </Card>

      <Card class="action-card" @click="router.push('/owner/bookings')">
        <template #content>
          <div class="action-icon bookings">
            <i class="pi pi-calendar-check"></i>
          </div>
          <h3>Manage Bookings</h3>
          <p>Review incoming requests and coordinate check-ins.</p>
          <Button label="View Bookings" icon="pi pi-arrow-right" class="p-button-text p-button-sm" />
        </template>
      </Card>
    </div>

    <!-- Getting Started / News Section -->
    <div class="info-grid mt-6">
      <Card class="info-item guide">
        <template #title>Getting Started Guide</template>
        <template #content>
          <ul class="guide-list">
            <li>
              <i class="pi pi-check-circle text-green-500"></i>
              <span>Complete your profile and payout details</span>
            </li>
            <li>
              <i class="pi pi-check-circle text-green-500"></i>
              <span>Add at least 3 high-quality photos per listing</span>
            </li>
            <li>
              <i class="pi pi-circle text-gray-400"></i>
              <span>Verify your identity to increase guest trust</span>
            </li>
            <li>
              <i class="pi pi-circle text-gray-400"></i>
              <span>Sync with external calendars to avoid overlaps</span>
            </li>
          </ul>
        </template>
      </Card>

      <Card class="info-item news">
        <template #title>What's New</template>
        <template #content>
          <div class="news-item">
            <span class="news-badge">Update</span>
            <p>New "Instant Book" feature is now available for premium members.</p>
          </div>
          <div class="news-item">
            <span class="news-badge promo">Tips</span>
            <p>Seasonal pricing trends: How to price your city stay this summer.</p>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Card from 'primevue/card'
import Button from 'primevue/button'

const router = useRouter()
const authStore = useAuthStore()
</script>

<style scoped>
.owner-home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.welcome-header {
  margin-bottom: 3.5rem;
}

.welcome-header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1a202c;
  margin-bottom: 0.75rem;
}

.welcome-header p {
  font-size: 1.15rem;
  color: #718096;
  max-width: 600px;
  line-height: 1.6;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.action-card {
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #f1f5f9;
}

.action-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: #6366f1;
}

.action-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.action-icon i {
  font-size: 1.75rem;
}

.list-apt { background-color: #e0e7ff; color: #4338ca; }
.analytics { background-color: #fef3c7; color: #b45309; }
.bookings { background-color: #d1fae5; color: #065f46; }

.action-card h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #1a202c;
}

.action-card p {
  color: #718096;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.info-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 2rem;
}

.info-item {
  border-radius: 16px;
  background: white;
}

.guide-list {
  list-style: none;
  padding: 0;
}

.guide-list li {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f8fafc;
}

.guide-list li:last-child {
  border-bottom: none;
}

.guide-list i {
  font-size: 1.25rem;
}

.news-item {
  margin-bottom: 1.5rem;
}

.news-badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  background: #eff6ff;
  color: #2563eb;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.news-badge.promo {
  background: #fdf2f8;
  color: #db2777;
}

.news-item p {
  font-size: 0.95rem;
  color: #4a5568;
  margin: 0;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
