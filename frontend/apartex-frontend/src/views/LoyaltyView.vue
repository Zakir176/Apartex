<!-- src/views/LoyaltyView.vue -->
<template>
  <div class="loyalty-page">
    <div class="container">
      <!-- Header -->
      <header class="page-header">
        <h1>Loyalty Rewards</h1>
        <p>Earn points, get rewards, and enjoy exclusive benefits</p>
      </header>

      <!-- Points Overview -->
      <div class="points-overview">
        <div class="points-card">
          <div class="points-display">
            <div class="points-number">{{ userPoints }}</div>
            <div class="points-label">Total Points</div>
          </div>
          <div class="points-progress">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: progressPercentage + '%' }"
              ></div>
            </div>
            <div class="progress-labels">
              <span>0</span>
              <span>Next tier: {{ nextTier.pointsRequired - userPoints }} points</span>
              <span>{{ nextTier.pointsRequired }}</span>
            </div>
          </div>
        </div>

        <div class="benefits-card">
          <h3>Current Tier: {{ currentTier.name }}</h3>
          <div class="benefits-list">
            <div 
              v-for="benefit in currentTier.benefits" 
              :key="benefit"
              class="benefit-item"
            >
              <span class="benefit-icon">✅</span>
              <span>{{ benefit }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- How It Works -->
      <section class="how-it-works">
        <h2>How It Works</h2>
        <div class="steps-grid">
          <div class="step-card">
            <div class="step-number">1</div>
            <h3>Book Stays</h3>
            <p>Earn 10 points for every dollar spent on apartment bookings</p>
          </div>
          <div class="step-card">
            <div class="step-number">2</div>
            <h3>Write Reviews</h3>
            <p>Get 50 bonus points for each review you write after your stay</p>
          </div>
          <div class="step-card">
            <div class="step-number">3</div>
            <h3>Redeem Rewards</h3>
            <p>Use your points for discounts, free nights, and exclusive perks</p>
          </div>
        </div>
      </section>

      <!-- Rewards Catalog -->
      <section class="rewards-section">
        <div class="section-header">
          <h2>Available Rewards</h2>
          <div class="tier-filter">
            <button 
              v-for="tier in tiers" 
              :key="tier.id"
              :class="['tier-btn', { active: activeTierFilter === tier.id }]"
              @click="activeTierFilter = tier.id"
            >
              {{ tier.name }}
            </button>
          </div>
        </div>

        <div class="rewards-grid">
          <div 
            v-for="reward in filteredRewards" 
            :key="reward.id"
            :class="['reward-card', { unavailable: userPoints < reward.pointsCost }]"
          >
            <div class="reward-image">
              <img :src="reward.image" :alt="reward.name">
              <div class="reward-cost">{{ reward.pointsCost }} pts</div>
            </div>
            <div class="reward-info">
              <h3>{{ reward.name }}</h3>
              <p>{{ reward.description }}</p>
              <div class="reward-tier">{{ reward.tier }}</div>
            </div>
            <div class="reward-actions">
              <button 
                class="redeem-btn"
                :disabled="userPoints < reward.pointsCost"
                @click="redeemReward(reward)"
              >
                {{ userPoints >= reward.pointsCost ? 'Redeem Now' : 'Need More Points' }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Recent Activity -->
      <section class="activity-section">
        <h2>Points History</h2>
        <div class="activity-list">
          <div 
            v-for="activity in pointsActivity" 
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-icon" :class="activity.type">
              {{ activity.type === 'earned' ? '➕' : '➖' }}
            </div>
            <div class="activity-details">
              <p class="activity-description">{{ activity.description }}</p>
              <span class="activity-date">{{ activity.date }}</span>
            </div>
            <div class="activity-points" :class="activity.type">
              {{ activity.type === 'earned' ? '+' : '-' }}{{ activity.points }}
            </div>
          </div>
        </div>
      </section>

      <!-- Tier Comparison -->
      <section class="tiers-section">
        <h2>Membership Tiers</h2>
        <div class="tiers-comparison">
          <div 
            v-for="tier in tiers" 
            :key="tier.id"
            :class="['tier-card', { current: tier.id === currentTier.id }]"
          >
            <div class="tier-header">
              <h3>{{ tier.name }}</h3>
              <div class="tier-points">{{ tier.pointsRequired }} points</div>
            </div>
            <div class="tier-benefits">
              <div 
                v-for="benefit in tier.benefits" 
                :key="benefit"
                class="tier-benefit"
              >
                <span class="benefit-check">✅</span>
                <span>{{ benefit }}</span>
              </div>
            </div>
            <div class="tier-status" v-if="tier.id === currentTier.id">
              Current Tier
            </div>
            <div class="tier-status upcoming" v-else-if="tier.pointsRequired > userPoints">
              {{ tier.pointsRequired - userPoints }} points to go
            </div>
            <div class="tier-status achieved" v-else>
              Achieved
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoyaltyView',
  data() {
    return {
      userPoints: 1250,
      activeTierFilter: 'all',
      tiers: [
        {
          id: 'bronze',
          name: 'Bronze',
          pointsRequired: 0,
          benefits: [
            '10 points per $1 spent',
            'Basic customer support',
            'Email newsletters'
          ]
        },
        {
          id: 'silver',
          name: 'Silver',
          pointsRequired: 1000,
          benefits: [
            '12 points per $1 spent',
            'Priority customer support',
            'Early access to deals',
            'Free cancellation'
          ]
        },
        {
          id: 'gold',
          name: 'Gold',
          pointsRequired: 2500,
          benefits: [
            '15 points per $1 spent',
            '24/7 VIP support',
            'Exclusive discounts',
            'Free upgrades when available',
            'Welcome gift on arrival'
          ]
        },
        {
          id: 'platinum',
          name: 'Platinum',
          pointsRequired: 5000,
          benefits: [
            '20 points per $1 spent',
            'Personal travel consultant',
            'Complimentary services',
            'Guaranteed best rates',
            'Luxury experience packages'
          ]
        }
      ],
      rewards: [
        {
          id: 1,
          name: '$25 Travel Credit',
          description: 'Use on your next apartment booking',
          pointsCost: 500,
          tier: 'Bronze+',
          image: 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=300'
        },
        {
          id: 2,
          name: '1 Free Night',
          description: 'Complimentary night at select properties',
          pointsCost: 1000,
          tier: 'Silver+',
          image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=300'
        },
        {
          id: 3,
          name: 'Priority Upgrade',
          description: 'Room upgrade on your next stay',
          pointsCost: 750,
          tier: 'Silver+',
          image: 'https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=300'
        },
        {
          id: 4,
          name: 'Luxury Experience',
          description: 'Curated local experience package',
          pointsCost: 2000,
          tier: 'Gold+',
          image: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=300'
        },
        {
          id: 5,
          name: 'Weekend Getaway',
          description: '2-night stay at premium property',
          pointsCost: 3000,
          tier: 'Gold+',
          image: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=300'
        },
        {
          id: 6,
          name: 'VIP Concierge',
          description: 'Personal travel planning service',
          pointsCost: 5000,
          tier: 'Platinum',
          image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=300'
        }
      ],
      pointsActivity: [
        {
          id: 1,
          type: 'earned',
          points: 150,
          description: 'Stay at Mountain View Cabin',
          date: 'Nov 5, 2024'
        },
        {
          id: 2,
          type: 'earned',
          points: 50,
          description: 'Review bonus',
          date: 'Nov 3, 2024'
        },
        {
          id: 3,
          type: 'earned',
          points: 1200,
          description: 'Stay at Beachfront Condo',
          date: 'Oct 20, 2024'
        },
        {
          id: 4,
          type: 'earned',
          points: 100,
          description: 'Welcome bonus',
          date: 'Aug 15, 2024'
        }
      ]
    }
  },
  computed: {
    currentTier() {
      // Find the highest tier the user qualifies for
      const qualifiedTiers = this.tiers.filter(tier => this.userPoints >= tier.pointsRequired)
      return qualifiedTiers[qualifiedTiers.length - 1] || this.tiers[0]
    },
    nextTier() {
      const currentIndex = this.tiers.findIndex(tier => tier.id === this.currentTier.id)
      return this.tiers[currentIndex + 1] || this.tiers[this.tiers.length - 1]
    },
    progressPercentage() {
      if (this.nextTier) {
        const progress = (this.userPoints / this.nextTier.pointsRequired) * 100
        return Math.min(progress, 100)
      }
      return 100
    },
    filteredRewards() {
      if (this.activeTierFilter === 'all') {
        return this.rewards
      }
      return this.rewards.filter(reward => 
        reward.tier.toLowerCase().includes(this.activeTierFilter)
      )
    }
  },
  methods: {
    redeemReward(reward) {
      if (this.userPoints >= reward.pointsCost) {
        if (confirm(`Redeem ${reward.name} for ${reward.pointsCost} points?`)) {
          this.userPoints -= reward.pointsCost
          alert(`Success! You've redeemed ${reward.name}. Your new points balance is ${this.userPoints}.`)
        }
      }
    }
  }
}
</script>

<style scoped>
.loyalty-page {
  min-height: 100vh;
  background: #f7fafc;
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
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

.points-overview {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 3rem;
}

.points-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  text-align: center;
}

.points-display {
  margin-bottom: 2rem;
}

.points-number {
  font-size: 4rem;
  font-weight: bold;
  color: #667eea;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.points-label {
  color: #718096;
  font-size: 1.1rem;
  font-weight: 600;
}

.points-progress {
  space-y: 0.75rem;
}

.progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  color: #718096;
  font-size: 0.8rem;
}

.benefits-card {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.benefits-card h3 {
  color: #2d3748;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.benefits-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #4a5568;
}

.benefit-icon {
  font-size: 1.1rem;
}

.how-it-works {
  margin-bottom: 4rem;
}

.how-it-works h2 {
  text-align: center;
  color: #2d3748;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.step-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  text-align: center;
  transition: transform 0.3s;
}

.step-card:hover {
  transform: translateY(-5px);
}

.step-number {
  width: 50px;
  height: 50px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 1rem;
}

.step-card h3 {
  color: #2d3748;
  margin-bottom: 1rem;
}

.step-card p {
  color: #718096;
  line-height: 1.6;
}

.rewards-section {
  margin-bottom: 4rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h2 {
  color: #2d3748;
  margin: 0;
  font-size: 2rem;
}

.tier-filter {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tier-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #cbd5e0;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  font-weight: 600;
}

.tier-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.tier-btn:hover:not(.active) {
  border-color: #667eea;
  color: #667eea;
}

.rewards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.reward-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition: all 0.3s;
}

.reward-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.reward-card.unavailable {
  opacity: 0.6;
}

.reward-image {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.reward-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.reward-cost {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: bold;
  color: #667eea;
  font-size: 0.9rem;
}

.reward-info {
  padding: 1.5rem;
}

.reward-info h3 {
  color: #2d3748;
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
}

.reward-info p {
  color: #718096;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.reward-tier {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f7fafc;
  color: #4a5568;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.reward-actions {
  padding: 0 1.5rem 1.5rem;
}

.redeem-btn {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.redeem-btn:hover:not(:disabled) {
  background: #5a6fd8;
}

.redeem-btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

.activity-section {
  margin-bottom: 4rem;
}

.activity-section h2 {
  color: #2d3748;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.activity-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.activity-icon.earned {
  background: #c6f6d5;
  color: #276749;
}

.activity-icon.redeemed {
  background: #fed7d7;
  color: #c53030;
}

.activity-details {
  flex: 1;
}

.activity-description {
  color: #2d3748;
  margin: 0 0 0.25rem 0;
  font-weight: 500;
}

.activity-date {
  color: #718096;
  font-size: 0.8rem;
}

.activity-points {
  font-weight: bold;
  font-size: 1.1rem;
}

.activity-points.earned {
  color: #276749;
}

.activity-points.redeemed {
  color: #c53030;
}

.tiers-section {
  margin-bottom: 2rem;
}

.tiers-section h2 {
  text-align: center;
  color: #2d3748;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.tiers-comparison {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.tier-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  text-align: center;
  transition: all 0.3s;
  position: relative;
}

.tier-card.current {
  border-color: #667eea;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
  transform: scale(1.05);
}

.tier-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.tier-header h3 {
  color: #2d3748;
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
}

.tier-points {
  color: #667eea;
  font-weight: bold;
  font-size: 1.1rem;
}

.tier-benefits {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  text-align: left;
}

.tier-benefit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a5568;
  font-size: 0.9rem;
}

.benefit-check {
  color: #48bb78;
  font-size: 0.8rem;
}

.tier-status {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  background: #c6f6d5;
  color: #276749;
}

.tier-status.upcoming {
  background: #fefcbf;
  color: #d69e2e;
}

.tier-status.achieved {
  background: #bee3f8;
  color: #2c5aa0;
}

/* Responsive Design */
@media (max-width: 968px) {
  .points-overview {
    grid-template-columns: 1fr;
  }
  
  .tiers-comparison {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .tiers-comparison {
    grid-template-columns: 1fr;
  }
  
  .tier-card.current {
    transform: none;
  }
  
  .steps-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .loyalty-page {
    padding: 1rem 0;
  }
  
  .container {
    padding: 0 0.5rem;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .points-number {
    font-size: 3rem;
  }
  
  .rewards-grid {
    grid-template-columns: 1fr;
  }
  
  .activity-item {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .activity-details {
    text-align: center;
  }
}
</style>