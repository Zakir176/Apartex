<template>
  <div class="dashboard-view">
    <div class="dashboard-header">
      <h1>Owner Dashboard</h1>
      <p>Manage your apartments and track your earnings</p>
    </div>

    <!-- Overview Stats -->
    <section class="overview-section">
      <h2>Overview</h2>
      <div v-if="dashboardStore.loading" class="loading">Loading dashboard data...</div>
      <div v-else-if="dashboardStore.error" class="error">
        {{ dashboardStore.error }}
      </div>
      <div v-else-if="overview" class="stats-grid">
        <div class="stat-card revenue">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <h3>Total Revenue</h3>
            <p class="stat-value">${{ overview.total_revenue?.toLocaleString() }}</p>
            <p class="stat-trend">+${{ overview.monthly_revenue?.toLocaleString() }} this month</p>
          </div>
        </div>

        <div class="stat-card bookings">
          <div class="stat-icon">📅</div>
          <div class="stat-info">
            <h3>Total Bookings</h3>
            <p class="stat-value">{{ overview.total_bookings }}</p>
            <p class="stat-trend">{{ overview.upcoming_bookings }} upcoming</p>
          </div>
        </div>

        <div class="stat-card occupancy">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <h3>Occupancy Rate</h3>
            <p class="stat-value">{{ (overview.occupancy_rate * 100).toFixed(1) }}%</p>
            <p class="stat-trend">Industry avg: 65%</p>
          </div>
        </div>

        <div class="stat-card rating">
          <div class="stat-icon">⭐</div>
          <div class="stat-info">
            <h3>Average Rating</h3>
            <p class="stat-value">{{ overview.average_rating }}/5</p>
            <p class="stat-trend">Based on {{ overview.total_bookings }} reviews</p>
          </div>
        </div>

        <div class="stat-card apartments">
          <div class="stat-icon">🏠</div>
          <div class="stat-info">
            <h3>Active Apartments</h3>
            <p class="stat-value">{{ overview.active_apartments }}</p>
            <p class="stat-trend">{{ overview.pending_bookings }} pending bookings</p>
          </div>
        </div>

        <div class="stat-card performance">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <h3>Performance</h3>
            <p class="stat-value">Excellent</p>
            <p class="stat-trend">+15% vs last month</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Quick Actions -->
    <section class="actions-section">
      <h2>Quick Actions</h2>
      <div class="actions-grid">
        <button @click="navigateToApartments" class="action-btn">
          <span class="action-icon">🏠</span>
          <span>Manage Apartments</span>
        </button>
        <button @click="showPayoutModal = true" class="action-btn">
          <span class="action-icon">💰</span>
          <span>Request Payout</span>
        </button>
        <button @click="navigateToBookings" class="action-btn">
          <span class="action-icon">📅</span>
          <span>View Bookings</span>
        </button>
        <button @click="showAddApartment = true" class="action-btn">
          <span class="action-icon">➕</span>
          <span>Add New Apartment</span>
        </button>
      </div>
    </section>

    <!-- Payouts Section -->
    <section class="payouts-section">
      <div class="section-header">
        <h2>Recent Payouts</h2>
        <button @click="showPayoutModal = true" class="btn-primary">
          Request Payout
        </button>
      </div>

      <div v-if="dashboardStore.loading" class="loading">Loading payouts...</div>
      <div v-else-if="payouts.length === 0" class="no-data">
        <p>No payout history found.</p>
      </div>
      <div v-else class="payouts-list">
        <div v-for="payout in payouts" :key="payout.id" class="payout-card">
          <div class="payout-info">
            <h3>${{ payout.amount.toLocaleString() }}</h3>
            <p class="payout-description">{{ payout.description }}</p>
            <p class="payout-date">{{ formatDate(payout.date) }}</p>
          </div>
          <div class="payout-status" :class="payout.status">
            {{ payout.status }}
          </div>
        </div>
      </div>
    </section>

    <!-- Payout Request Modal -->
    <div v-if="showPayoutModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Request Payout</h2>
          <button @click="showPayoutModal = false" class="btn-close">&times;</button>
        </div>

        <form @submit.prevent="handlePayoutRequest" class="payout-form">
          <div class="form-group">
            <label for="amount">Amount</label>
            <input
              id="amount"
              v-model="payoutForm.amount"
              type="number"
              required
              placeholder="Enter amount"
              min="1"
            />
          </div>

          <div class="form-group">
            <label for="description">Description</label>
            <textarea
              id="description"
              v-model="payoutForm.description"
              rows="3"
              placeholder="Optional description for this payout request"
            ></textarea>
          </div>

          <div class="balance-info">
            <p><strong>Available Balance:</strong> ${{ availableBalance.toLocaleString() }}</p>
            <p v-if="payoutForm.amount > availableBalance" class="error-text">
              Amount exceeds available balance
            </p>
          </div>

          <div class="form-actions">
            <button
              type="button"
              @click="showPayoutModal = false"
              class="btn-cancel"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="requestingPayout || payoutForm.amount > availableBalance"
              class="btn-submit"
            >
              {{ requestingPayout ? 'Processing...' : 'Request Payout' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useDashboardStore } from '../stores/dashboard';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const dashboardStore = useDashboardStore();
const authStore = useAuthStore();

const showPayoutModal = ref(false);
const showAddApartment = ref(false);
const requestingPayout = ref(false);

const payoutForm = ref({
  amount: '',
  description: ''
});

const overview = computed(() => dashboardStore.ownerOverview);
const payouts = computed(() => dashboardStore.payouts);

const availableBalance = computed(() => {
  return overview.value ? overview.value.monthly_revenue : 0;
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const navigateToApartments = () => {
  router.push('/apartments');
};

const navigateToBookings = () => {
  router.push('/bookings');
};

const handlePayoutRequest = async () => {
  if (!authStore.user) return;

  requestingPayout.value = true;
  try {
    await dashboardStore.requestPayout(authStore.user.id, {
      amount: parseFloat(payoutForm.value.amount),
      description: payoutForm.value.description
    });

    // Reset form and close modal
    payoutForm.value = { amount: '', description: '' };
    showPayoutModal.value = false;
    
    alert('Payout request submitted successfully!');
  } catch (error) {
    console.error('Payout request failed:', error);
    alert('Failed to submit payout request. Please try again.');
  } finally {
    requestingPayout.value = false;
  }
};

const loadDashboardData = async () => {
  if (!authStore.user) {
    console.log('⚠️ No user logged in, using default owner ID');
    // Use default ID for development
    await Promise.all([
      dashboardStore.fetchOwnerOverview(1),
      dashboardStore.fetchOwnerPayouts(1)
    ]);
    return;
  }

  try {
    console.log('🔄 Loading dashboard data for user:', authStore.user.id);
    await Promise.all([
      dashboardStore.fetchOwnerOverview(authStore.user.id),
      dashboardStore.fetchOwnerPayouts(authStore.user.id)
    ]);
  } catch (error) {
    console.error('❌ Failed to load dashboard data:', error);
  }
};

onMounted(async () => {
  console.log('🚀 DashboardView mounted - Starting data load...');
  await loadDashboardData();
});
</script>

<style scoped>
.dashboard-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.dashboard-header p {
  font-size: 1.2rem;
  color: #666;
}

.overview-section, .actions-section, .payouts-section {
  margin-bottom: 3rem;
}

.overview-section h2, .actions-section h2, .payouts-section h2 {
  margin-bottom: 1.5rem;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card.revenue {
  border-left: 4px solid #28a745;
}

.stat-card.bookings {
  border-left: 4px solid #007bff;
}

.stat-card.occupancy {
  border-left: 4px solid #ffc107;
}

.stat-card.rating {
  border-left: 4px solid #6f42c1;
}

.stat-card.apartments {
  border-left: 4px solid #fd7e14;
}

.stat-card.performance {
  border-left: 4px solid #20c997;
}

.stat-icon {
  font-size: 2.5rem;
  width: 60px;
  text-align: center;
}

.stat-info h3 {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
  font-weight: normal;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  margin: 0 0 0.25rem 0;
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
}

.stat-trend {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

/* Quick Actions */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
  font-weight: 500;
}

.action-btn:hover {
  border-color: #007bff;
  background: #f8f9fa;
  transform: translateY(-2px);
}

.action-icon {
  font-size: 2rem;
}

/* Payouts Section */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.payouts-list {
  display: grid;
  gap: 1rem;
}

.payout-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  transition: box-shadow 0.2s;
}

.payout-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.payout-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.5rem;
}

.payout-description {
  margin: 0 0 0.5rem 0;
  color: #666;
}

.payout-date {
  margin: 0;
  color: #999;
  font-size: 0.9rem;
}

.payout-status {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}

.payout-status.completed {
  background-color: #d4edda;
  color: #155724;
}

.payout-status.pending {
  background-color: #fff3cd;
  color: #856404;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.btn-close:hover {
  color: #333;
}

.payout-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus, .form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

.balance-info {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.error-text {
  color: #dc3545;
  margin: 0.5rem 0 0 0;
  font-size: 0.9rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-cancel, .btn-submit {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background-color: #545b62;
}

.btn-submit {
  background-color: #007bff;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background-color: #0056b3;
}

.btn-submit:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

/* Loading and Error States */
.loading, .error, .no-data {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}

.error {
  color: #dc3545;
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
}

.no-data {
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-view {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .payout-card {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .actions-grid {
    grid-template-columns: 1fr 1fr;
  }

  .modal-content {
    width: 95%;
    margin: 1rem;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>