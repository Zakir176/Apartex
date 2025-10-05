<template>
  <div class="loyalty-view">
    <div class="loyalty-header">
      <h1>Loyalty Program</h1>
      <p>Earn points on every booking and unlock amazing rewards!</p>
    </div>

    <!-- Loyalty Status Section -->
    <section class="loyalty-status-section">
      <h2>Your Loyalty Status</h2>
      <div v-if="loyaltyStore.loading" class="loading">Loading loyalty status...</div>
      <div v-else-if="loyaltyStore.error" class="error">
        {{ loyaltyStore.error }}
      </div>
      <div v-else-if="loyaltyStatus" class="status-card">
        <div class="tier-display">
          <div class="current-tier">
            <h3>Current Tier</h3>
            <div class="tier-badge" :class="loyaltyStatus.current_tier?.toLowerCase()">
              {{ loyaltyStatus.current_tier }}
            </div>
            <p class="points">{{ loyaltyStatus.points }} points</p>
          </div>

          <div class="progress-section">
            <div class="progress-header">
              <span>Progress to {{ loyaltyStatus.next_tier }}</span>
              <span>{{ progressPercentage }}%</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :class="loyaltyStatus.current_tier?.toLowerCase()"
                :style="{ width: progressPercentage + '%' }"
              ></div>
            </div>
            <div class="progress-text">
              {{ loyaltyStatus.points }} / {{ loyaltyStatus.points_required }} points
            </div>
          </div>

          <div class="next-tier">
            <h3>Next Tier: {{ loyaltyStatus.next_tier }}</h3>
            <p>Unlocks at {{ loyaltyStatus.points_required }} points</p>
            <p class="points-needed">
              {{ loyaltyStatus.points_required - loyaltyStatus.points }} points to go
            </p>
          </div>
        </div>
      </div>
      <div v-else class="no-data">
        <p>Unable to load loyalty status</p>
      </div>
    </section>

    <!-- Available Rewards Section -->
    <section class="rewards-section">
      <h2>Available Rewards</h2>
      
      <div v-if="loadingRewards" class="loading">Loading available rewards...</div>
      <div v-else class="rewards-grid">
        <div 
          v-for="reward in availableRewards" 
          :key="reward.id"
          class="reward-card"
          :class="{ 'redeemable': isRewardRedeemable(reward) }"
        >
          <div class="reward-header">
            <h3>{{ reward.name }}</h3>
            <span class="points-cost">{{ reward.points_required }} points</span>
          </div>
          
          <p class="reward-description">{{ reward.description }}</p>
          
          <div class="reward-actions">
            <button 
              v-if="isRewardRedeemable(reward)"
              @click="redeemReward(reward)"
              :disabled="redeemingId === reward.id"
              class="btn-redeem"
            >
              {{ redeemingId === reward.id ? 'Redeeming...' : 'Redeem' }}
            </button>
            <button v-else disabled class="btn-locked">
              Need {{ reward.points_required - (loyaltyStatus?.points || 0) }} more points
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- User's Rewards Section -->
    <section class="my-rewards-section">
      <h2>My Rewards</h2>
      
      <div v-if="userRewardsLoading" class="loading">Loading your rewards...</div>
      <div v-else-if="userRewardsError" class="error">
        {{ userRewardsError }}
      </div>
      <div v-else-if="userRewards.length === 0" class="no-rewards">
        <p>You haven't redeemed any rewards yet.</p>
        <p>Start booking to earn points and unlock rewards!</p>
      </div>
      <div v-else class="rewards-list">
        <div 
          v-for="reward in userRewards" 
          :key="reward.id"
          class="user-reward-card"
          :class="{ 'used': reward.used }"
        >
          <div class="reward-info">
            <h3>{{ reward.name }}</h3>
            <p class="reward-description">{{ reward.description }}</p>
            <div class="reward-meta">
              <span class="redeemed-date">Redeemed: {{ formatDate(reward.redeemed_at) }}</span>
              <span v-if="reward.used" class="used-badge">Used</span>
              <span v-else class="active-badge">Active</span>
            </div>
          </div>
          <div class="reward-code" v-if="!reward.used">
            <strong>Code:</strong> {{ reward.redemption_code }}
          </div>
        </div>
      </div>
    </section>

    <!-- Loyalty Tiers Info -->
    <section class="tiers-info-section">
      <h2>Loyalty Tiers</h2>
      <div v-if="loyaltyTiersLoading" class="loading">Loading tiers info...</div>
      <div v-else-if="loyaltyTiers.length === 0" class="no-data">
        <p>No loyalty tiers information available</p>
      </div>
      <div v-else class="tiers-grid">
        <div 
          v-for="tier in loyaltyTiers" 
          :key="tier.name"
          class="tier-info-card"
          :class="{
            'current': tier.name === loyaltyStatus?.current_tier,
            'next': tier.name === loyaltyStatus?.next_tier
          }"
        >
          <div class="tier-header">
            <h3>{{ tier.name }}</h3>
            <div class="tier-badge-small" :class="tier.name.toLowerCase()">
              {{ tier.name }}
            </div>
          </div>
          <div class="tier-requirements">
            <p><strong>Required Points:</strong> {{ tier.required_points }}</p>
            <p><strong>Benefits:</strong></p>
            <ul class="benefits-list">
              <li v-for="benefit in tier.benefits" :key="benefit">
                {{ benefit }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useLoyaltyStore } from '../stores/loyalty';
import { useAuthStore } from '../stores/auth';

const loyaltyStore = useLoyaltyStore();
const authStore = useAuthStore();

const redeemingId = ref(null);
const userRewardsLoading = ref(false);
const userRewardsError = ref('');
const loyaltyTiersLoading = ref(false);
const loadingRewards = ref(false);

// Computed properties
const loyaltyStatus = computed(() => loyaltyStore.loyaltyStatus);
const userRewards = computed(() => loyaltyStore.userRewards || []);
const loyaltyTiers = computed(() => loyaltyStore.loyaltyTiers || []);
const availableRewards = computed(() => loyaltyStore.availableRewards || []);

const progressPercentage = computed(() => {
  if (!loyaltyStatus.value) return 0;
  const progress = (loyaltyStatus.value.points / loyaltyStatus.value.points_required) * 100;
  return Math.min(Math.round(progress), 100);
});

const isRewardRedeemable = (reward) => {
  return loyaltyStatus.value && loyaltyStatus.value.points >= reward.points_required;
};

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown date';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

// Data loading functions
const loadLoyaltyData = async () => {
  if (!authStore.user) {
    console.log('⚠️ No user logged in, using default user ID');
    // Use a default user ID for development
    await loyaltyStore.fetchLoyaltyStatus(1);
    return;
  }

  try {
    console.log('🔄 Loading loyalty data for user:', authStore.user.id);
    await loyaltyStore.fetchLoyaltyStatus(authStore.user.id);
  } catch (error) {
    console.error('❌ Failed to load loyalty data:', error);
  }
};

const loadUserRewards = async () => {
  userRewardsLoading.value = true;
  userRewardsError.value = '';
  
  if (!authStore.user) {
    console.log('⚠️ No user logged in, using default user ID for rewards');
    // Use a default user ID for development
    await loyaltyStore.fetchUserRewards(1);
    userRewardsLoading.value = false;
    return;
  }

  try {
    console.log('🔄 Loading user rewards for user:', authStore.user.id);
    await loyaltyStore.fetchUserRewards(authStore.user.id);
  } catch (error) {
    userRewardsError.value = 'Failed to load your rewards';
    console.error('❌ Error loading user rewards:', error);
  } finally {
    userRewardsLoading.value = false;
  }
};

const loadLoyaltyTiers = async () => {
  loyaltyTiersLoading.value = true;
  try {
    console.log('🔄 Loading loyalty tiers');
    await loyaltyStore.fetchLoyaltyTiers();
  } catch (error) {
    console.error('❌ Error loading loyalty tiers:', error);
  } finally {
    loyaltyTiersLoading.value = false;
  }
};

const loadAvailableRewards = async () => {
  loadingRewards.value = true;
  try {
    console.log('🔄 Loading available rewards');
    await loyaltyStore.fetchAvailableRewards();
  } catch (error) {
    console.error('❌ Error loading available rewards:', error);
  } finally {
    loadingRewards.value = false;
  }
};

const redeemReward = async (reward) => {
  if (!authStore.user) {
    alert('Please log in to redeem rewards');
    return;
  }

  if (!confirm(`Redeem ${reward.name} for ${reward.points_required} points?`)) return;

  redeemingId.value = reward.id;
  try {
    await loyaltyStore.redeemReward({
      reward_id: reward.id,
      user_id: authStore.user?.id || 1
    });
    
    // Refresh data after redemption
    await Promise.all([
      loadLoyaltyData(),
      loadUserRewards()
    ]);
    
    alert('🎉 Reward redeemed successfully! Check "My Rewards" for your redemption code.');
  } catch (error) {
    console.error('❌ Redemption failed:', error);
    alert('Failed to redeem reward. Please try again.');
  } finally {
    redeemingId.value = null;
  }
};

// Initialize on mount
onMounted(async () => {
  console.log('🚀 LoyaltyView mounted - Starting data load...');
  
  // Load all data in parallel
  await Promise.all([
    loadLoyaltyData(),
    loadUserRewards(),
    loadLoyaltyTiers(),
    loadAvailableRewards()
  ]);
  
  console.log('✅ All data loaded:', {
    loyaltyStatus: loyaltyStore.loyaltyStatus,
    userRewards: loyaltyStore.userRewards,
    loyaltyTiers: loyaltyStore.loyaltyTiers,
    availableRewards: loyaltyStore.availableRewards
  });
});
</script>

<style scoped>
/* Keep all the same CSS styles from the previous version */
/* They are comprehensive and work well */

.loyalty-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.loyalty-header {
  text-align: center;
  margin-bottom: 3rem;
}

.loyalty-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.loyalty-header p {
  font-size: 1.2rem;
  color: #666;
}

/* Status Section */
.status-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 3rem;
}

.tier-display {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 2rem;
  align-items: center;
}

.current-tier {
  text-align: center;
}

.current-tier h3 {
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.tier-badge {
  display: inline-block;
  padding: 0.5rem 1.5rem;
  border-radius: 25px;
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.tier-badge.bronze { background: #cd7f32; }
.tier-badge.silver { background: #c0c0c0; color: #333; }
.tier-badge.gold { background: #ffd700; color: #333; }
.tier-badge.platinum { background: #e5e4e2; color: #333; }

.points {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
}

.progress-section {
  text-align: center;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.progress-bar {
  height: 12px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.5s ease;
}

.progress-fill.bronze { background: #cd7f32; }
.progress-fill.silver { background: #c0c0c0; }
.progress-fill.gold { background: #ffd700; }
.progress-fill.platinum { background: #e5e4e2; }

.progress-text {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  opacity: 0.9;
}

.next-tier {
  text-align: center;
}

.next-tier h3 {
  margin-bottom: 0.5rem;
}

.points-needed {
  font-weight: bold;
  color: #ffd700;
}

/* Rewards Section */
.rewards-section, .my-rewards-section, .tiers-info-section {
  margin-bottom: 3rem;
}

.rewards-section h2, .my-rewards-section h2, .tiers-info-section h2 {
  margin-bottom: 1.5rem;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.rewards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.reward-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  transition: all 0.3s ease;
}

.reward-card.redeemable {
  border-color: #28a745;
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.1);
}

.reward-card.redeemable:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.15);
}

.reward-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.reward-header h3 {
  margin: 0;
  color: #333;
}

.points-cost {
  background: #007bff;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.reward-description {
  color: #666;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.reward-actions {
  text-align: center;
}

.btn-redeem, .btn-locked {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-redeem {
  background-color: #28a745;
  color: white;
}

.btn-redeem:hover:not(:disabled) {
  background-color: #218838;
}

.btn-redeem:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.btn-locked {
  background-color: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}

/* My Rewards Section */
.rewards-list {
  display: grid;
  gap: 1rem;
}

.user-reward-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-reward-card.used {
  opacity: 0.6;
  background: #f8f9fa;
}

.reward-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.reward-meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.redeemed-date {
  color: #666;
}

.used-badge, .active-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: bold;
}

.used-badge {
  background: #6c757d;
  color: white;
}

.active-badge {
  background: #28a745;
  color: white;
}

.reward-code {
  background: #f8f9fa;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-family: monospace;
}

/* Tiers Info Section */
.tiers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.tier-info-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  background: white;
  transition: all 0.3s ease;
}

.tier-info-card.current {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
}

.tier-info-card.next {
  border-color: #28a745;
}

.tier-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.tier-header h3 {
  margin: 0;
  color: #333;
}

.tier-badge-small {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.tier-badge-small.bronze { background: #cd7f32; color: white; }
.tier-badge-small.silver { background: #c0c0c0; color: #333; }
.tier-badge-small.gold { background: #ffd700; color: #333; }
.tier-badge-small.platinum { background: #e5e4e2; color: #333; }

.benefits-list {
  margin: 0;
  padding-left: 1.2rem;
}

.benefits-list li {
  margin-bottom: 0.25rem;
  color: #555;
}

/* Loading and Error States */
.loading, .error {
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

.no-rewards, .no-data {
  text-align: center;
  padding: 3rem;
  color: #666;
  background: #f8f9fa;
  border-radius: 8px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .loyalty-view {
    padding: 1rem;
  }

  .tier-display {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    text-align: center;
  }

  .user-reward-card {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .rewards-grid, .tiers-grid {
    grid-template-columns: 1fr;
  }

  .loyalty-header h1 {
    font-size: 2rem;
  }
}
</style>