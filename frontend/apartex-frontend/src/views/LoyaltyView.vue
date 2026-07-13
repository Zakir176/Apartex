<template>
  <div class="max-w-[1200px] mx-auto px-6 py-12">
    <!-- Header -->
    <div class="text-center mb-16 max-w-2xl mx-auto">
      <div class="w-16 h-16 bg-orange-50 text-accent rounded-full flex items-center justify-center mx-auto mb-6">
        <i class="pi pi-star-fill text-3xl"></i>
      </div>
      <h1 class="text-4xl md:text-5xl font-black text-slate-800 mb-4 tracking-tight">Apartex Elite</h1>
      <p class="text-lg text-slate-500 font-medium">Earn points on every booking and unlock exclusive premium rewards tailored for our best guests.</p>
    </div>

    <!-- Status Section -->
    <div class="mb-16">
      <div v-if="loyaltyStore.loading" class="flex justify-center py-10"><i class="pi pi-spinner pi-spin text-3xl text-accent"></i></div>
      <div v-else-if="loyaltyStore.error" class="card-base p-6 text-center text-red-500 font-bold bg-red-50 border-red-100">{{ loyaltyStore.error }}</div>
      
      <div v-else-if="loyaltyStatus" class="rounded-3xl p-8 md:p-12 text-white shadow-xl relative overflow-hidden" 
           :class="getTierGradient(loyaltyStatus.current_tier)">
        <!-- Decorative bg elements -->
        <div class="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 rounded-full bg-white opacity-10 blur-3xl"></div>
        
        <div class="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-10 items-center">
          
          <!-- Current Tier -->
          <div class="text-center md:text-left flex flex-col items-center md:items-start">
            <span class="text-white/80 font-bold uppercase tracking-widest text-xs mb-2">Current Status</span>
            <div class="px-5 py-2 rounded-full bg-white/20 backdrop-blur-md border border-white/30 text-white font-extrabold text-xl mb-4 uppercase tracking-wider inline-block">
              {{ loyaltyStatus.current_tier }}
            </div>
            <div class="text-5xl font-black tracking-tight flex items-baseline gap-2">
              {{ loyaltyStatus.points }} <span class="text-xl text-white/80 font-bold">pts</span>
            </div>
          </div>

          <!-- Progress -->
          <div v-if="loyaltyStatus.bookings_required > 0" class="md:col-span-1">
            <div class="flex justify-between items-center mb-3 text-sm font-bold">
              <span class="text-white/90">Progress to {{ loyaltyStatus.next_tier }}</span>
              <span class="text-white">{{ progressPercentage }}%</span>
            </div>
            <div class="w-full h-3 bg-white/20 rounded-full overflow-hidden backdrop-blur-sm border border-white/10 mb-3">
              <div class="h-full bg-white rounded-full transition-all duration-1000 ease-out" :style="{ width: progressPercentage + '%' }"></div>
            </div>
            <div class="text-center text-sm font-medium text-white/80">
              {{ loyaltyStatus.total_bookings }} / {{ loyaltyStatus.bookings_required }} bookings completed
            </div>
          </div>
          <div v-else class="md:col-span-1 text-center">
            <div class="w-16 h-16 mx-auto bg-white/20 rounded-full flex items-center justify-center mb-3">
              <i class="pi pi-check text-3xl text-white"></i>
            </div>
            <p class="font-bold text-lg">Maximum Tier Reached!</p>
          </div>

          <!-- Next Tier Info -->
          <div v-if="loyaltyStatus.bookings_required > 0" class="text-center md:text-right flex flex-col items-center md:items-end">
            <span class="text-white/80 font-bold uppercase tracking-widest text-xs mb-2">Next Milestone</span>
            <h3 class="text-2xl font-extrabold mb-1">{{ loyaltyStatus.next_tier }}</h3>
            <p class="text-sm text-white/90 font-medium mb-3">Unlocks at {{ loyaltyStatus.bookings_required }} bookings</p>
            <div class="px-4 py-1.5 rounded-lg bg-black/20 text-sm font-bold backdrop-blur-md">
              {{ loyaltyStatus.bookings_needed }} booking(s) to go
            </div>
          </div>

        </div>
      </div>
      <div v-else class="card-base p-10 text-center text-slate-500 font-medium">Unable to load loyalty status</div>
    </div>

    <!-- Referral Section -->
    <div class="mb-16" v-if="authStore.user?.referral_code">
      <div class="card-base p-8 md:p-10 bg-gradient-to-r from-slate-800 to-slate-900 text-white relative overflow-hidden">
        <div class="absolute top-0 right-0 opacity-10 transform translate-x-1/4 -translate-y-1/4">
          <i class="pi pi-users text-[10rem]"></i>
        </div>
        <div class="relative z-10 flex flex-col md:flex-row gap-8 items-center justify-between">
          <div>
            <h2 class="text-2xl font-black mb-2 flex items-center gap-3">
              <i class="pi pi-gift text-accent"></i> Refer a Friend
            </h2>
            <p class="text-slate-300 font-medium max-w-md">
              Share your unique referral code with friends. When they sign up, you'll instantly receive <span class="text-accent font-bold">500 Bonus Points</span>!
            </p>
          </div>
          <div class="w-full md:w-auto bg-slate-950/50 border border-slate-700/50 rounded-xl p-4 flex flex-col gap-2">
            <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">Your Code</span>
            <div class="flex items-center gap-4">
              <span class="font-mono text-2xl font-black text-white tracking-widest">{{ authStore.user.referral_code }}</span>
              <button @click="copyReferralCode" class="w-10 h-10 rounded-lg bg-accent text-white flex items-center justify-center hover:bg-orange-600 transition-colors shadow-lg" title="Copy Code">
                <i :class="copied ? 'pi pi-check' : 'pi pi-copy'"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tiers Info -->
    <div class="mb-16">
      <h2 class="text-2xl font-black text-slate-800 mb-6">Program Tiers</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="tier in loyaltyTiers" :key="tier.name" 
             class="card-base p-6 flex flex-col relative border-2 transition-colors duration-300"
             :class="tier.name === loyaltyStatus?.current_tier ? 'border-accent' : 'border-transparent'">
          
          <div v-if="tier.name === loyaltyStatus?.current_tier" class="absolute -top-3 -right-3 bg-accent text-white w-8 h-8 rounded-full flex items-center justify-center shadow-md">
            <i class="pi pi-check text-xs font-bold"></i>
          </div>

          <div class="px-4 py-1.5 rounded-full inline-block text-xs font-black uppercase tracking-wider mb-4 w-max"
               :class="getTierBadgeClasses(tier.name)">
            {{ tier.name }}
          </div>
          
          <div class="text-sm font-bold text-slate-500 mb-4 pb-4 border-b border-surface-border">
            {{ tier.min_bookings }}{{ tier.max_bookings ? ' - ' + tier.max_bookings : '+' }} bookings
          </div>
          
          <ul class="flex flex-col gap-3 flex-grow">
            <li v-for="benefit in tier.benefits" :key="benefit" class="flex items-start gap-2 text-sm font-medium text-slate-700">
              <i class="pi pi-check-circle text-accent mt-0.5"></i>
              <span>{{ benefit }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Available Rewards -->
    <div class="mb-16">
      <h2 class="text-2xl font-black text-slate-800 mb-6">Redeem Rewards</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="reward in availableRewards" :key="reward.id" class="card-base p-6 flex flex-col justify-between group">
          <div>
            <div class="flex justify-between items-start mb-4">
              <h3 class="text-lg font-bold text-slate-800 pr-2">{{ reward.name }}</h3>
              <span class="px-3 py-1 bg-slate-100 text-slate-700 rounded-lg text-xs font-black tracking-wider flex-shrink-0">
                {{ reward.points_required }} PTS
              </span>
            </div>
            <p class="text-slate-500 text-sm font-medium mb-6 leading-relaxed">{{ reward.description }}</p>
          </div>
          
          <button 
            v-if="isRewardRedeemable(reward)"
            @click="redeemReward(reward)"
            :disabled="redeemingId === reward.id"
            class="btn-accent w-full justify-center transition-transform active:scale-95"
          >
            <i class="pi pi-spinner pi-spin" v-if="redeemingId === reward.id"></i>
            <span v-else>Redeem Now</span>
          </button>
          <button v-else disabled class="w-full px-5 py-3 rounded-full text-sm font-bold bg-slate-100 text-slate-400 cursor-not-allowed">
            Need {{ reward.points_required - (loyaltyStatus?.points || 0) }} more points
          </button>
        </div>
      </div>
    </div>

    <!-- My Rewards -->
    <div>
      <h2 class="text-2xl font-black text-slate-800 mb-6">My Redeemed Rewards</h2>
      
      <div v-if="userRewards.length === 0" class="card-base p-10 text-center flex flex-col items-center">
        <div class="w-16 h-16 rounded-full bg-slate-50 flex items-center justify-center mb-4 text-slate-300">
          <i class="pi pi-gift text-2xl"></i>
        </div>
        <p class="text-slate-500 font-bold mb-1">No rewards redeemed yet</p>
        <p class="text-sm font-medium text-slate-400">Save up your points and claim your first prize!</p>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="reward in userRewards" :key="reward.id" class="card-base p-5 flex flex-col justify-between border-l-4"
             :class="reward.used ? 'border-l-slate-300 opacity-60' : 'border-l-green-500'">
          <div class="flex justify-between items-start mb-3">
            <div>
              <h3 class="text-base font-bold text-slate-800 mb-1">{{ reward.name }}</h3>
              <p class="text-xs font-medium text-slate-500">Redeemed: {{ formatDate(reward.redeemed_at) }}</p>
            </div>
            <span v-if="reward.used" class="px-2 py-1 bg-slate-100 text-slate-500 rounded text-[10px] font-bold uppercase tracking-wider">Used</span>
            <span v-else class="px-2 py-1 bg-green-50 text-green-600 rounded text-[10px] font-bold uppercase tracking-wider">Active</span>
          </div>
          
          <div v-if="!reward.used" class="mt-4 p-3 bg-slate-50 border border-surface-border rounded-lg flex justify-between items-center">
            <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Promo Code</span>
            <span class="font-mono font-bold text-slate-800 tracking-wider">{{ reward.redemption_code }}</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useLoyaltyStore } from '../stores/loyalty';
import { useAuthStore } from '../stores/auth';

const loyaltyStore = useLoyaltyStore();
const authStore = useAuthStore();

const redeemingId = ref(null);
const copied = ref(false);

const copyReferralCode = () => {
  if (!authStore.user?.referral_code) return;
  navigator.clipboard.writeText(authStore.user.referral_code);
  copied.value = true;
  setTimeout(() => { copied.value = false; }, 2000);
};

const loyaltyStatus = computed(() => loyaltyStore.loyaltyStatus);
const userRewards = computed(() => loyaltyStore.userRewards || []);
const loyaltyTiers = computed(() => loyaltyStore.loyaltyTiers || []);
const availableRewards = computed(() => loyaltyStore.availableRewards || []);

const progressPercentage = computed(() => {
  if (!loyaltyStatus.value) return 0;
  const current = loyaltyStatus.value.total_bookings;
  const required = loyaltyStatus.value.bookings_required;
  if (!required) return 100;
  return Math.min(Math.round((current / required) * 100), 100);
});

const isRewardRedeemable = (reward) => {
  return loyaltyStatus.value && loyaltyStatus.value.points >= reward.points_required;
};

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown date';
  return new Date(dateString).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
};

const getTierGradient = (tier) => {
  switch(tier?.toLowerCase()) {
    case 'bronze': return 'bg-gradient-to-br from-amber-700 to-orange-900';
    case 'silver': return 'bg-gradient-to-br from-slate-400 to-slate-600';
    case 'gold': return 'bg-gradient-to-br from-yellow-400 to-yellow-600';
    case 'platinum': return 'bg-gradient-to-br from-slate-700 to-slate-900';
    default: return 'bg-gradient-to-br from-accent to-orange-600';
  }
};

const getTierBadgeClasses = (tier) => {
  switch(tier?.toLowerCase()) {
    case 'bronze': return 'bg-amber-100 text-amber-800';
    case 'silver': return 'bg-slate-200 text-slate-700';
    case 'gold': return 'bg-yellow-100 text-yellow-800';
    case 'platinum': return 'bg-slate-800 text-white';
    default: return 'bg-blue-100 text-blue-800';
  }
};

const redeemReward = async (reward) => {
  if (!authStore.user) return;
  if (!confirm(`Redeem ${reward.name} for ${reward.points_required} points?`)) return;

  redeemingId.value = reward.id;
  try {
    await loyaltyStore.redeemReward({ reward_id: reward.id, user_id: authStore.user.id });
    await Promise.all([
      loyaltyStore.fetchLoyaltyStatus(authStore.user.id),
      loyaltyStore.fetchUserRewards(authStore.user.id)
    ]);
  } catch (error) {
    console.error(error);
  } finally {
    redeemingId.value = null;
  }
};

onMounted(async () => {
  if (authStore.user) {
    await Promise.all([
      loyaltyStore.fetchLoyaltyStatus(authStore.user.id),
      loyaltyStore.fetchUserRewards(authStore.user.id),
      loyaltyStore.fetchLoyaltyTiers(),
      loyaltyStore.fetchAvailableRewards()
    ]);
  }
});
</script>