<template>
  <div class="min-h-screen bg-[#F8F7F4] text-slate-900 overflow-x-hidden selection:bg-accent selection:text-white">
    <!-- HERO SECTION -->
    <header class="bg-slate-950 text-white relative pt-16 pb-24 lg:pt-24 lg:pb-32 overflow-hidden border-b border-slate-800">
      <div class="absolute top-1/4 left-10 w-80 h-80 bg-accent/20 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
      <div class="absolute bottom-10 right-10 w-96 h-96 bg-emerald-500/15 rounded-full blur-3xl pointer-events-none"></div>

      <div class="max-w-[1280px] mx-auto px-4 sm:px-6 relative z-10 text-center">
        <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900 border border-slate-700 text-xs font-black text-amber-400 mb-6">
          <i class="pi pi-bolt"></i>
          <span>0% Booking Commissions · Flat Subscription Model</span>
        </div>

        <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-[1.08] mb-6 text-white">
          Maximize Your Property Revenue in Zambia<br class="hidden sm:block" />
          <span class="text-gradient">With Zero Booking Commissions</span>
        </h1>

        <p class="text-base sm:text-xl text-slate-300 font-medium max-w-3xl mx-auto leading-relaxed mb-10">
          Replace 18%+ legacy OTA commissions with a simple fixed monthly subscription. Receive 100% of guest payouts directly into your Mobile Money or Bank account.
        </p>

        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <router-link 
            to="/register?role=owner" 
            class="btn-accent text-base sm:text-lg font-black px-9 py-4 rounded-full shadow-accent hover:scale-105 transition-transform no-underline w-full sm:w-auto flex items-center justify-center gap-2"
          >
            <span>Register Your Property</span>
            <i class="pi pi-arrow-right text-sm"></i>
          </router-link>
          <button 
            @click="scrollToCalculator"
            class="px-8 py-4 rounded-full bg-slate-900 border border-slate-700 text-white font-bold text-base hover:bg-slate-800 transition-colors w-full sm:w-auto cursor-pointer"
          >
            Calculate Earnings
          </button>
        </div>
      </div>
    </header>

    <!-- INTERACTIVE EARNINGS CALCULATOR SECTION -->
    <section id="earnings-calculator" class="max-w-[1280px] mx-auto px-4 sm:px-6 py-20">
      <div class="text-center max-w-3xl mx-auto mb-12">
        <span class="section-tag">Profit Projection</span>
        <h2 class="text-3xl sm:text-5xl font-black tracking-tight text-slate-900">
          Interactive Host Earnings Calculator
        </h2>
        <p class="text-slate-600 text-base sm:text-lg mt-3 font-medium">
          Estimate your monthly income and see how much 0% commission saves you every year.
        </p>
      </div>

      <div class="max-w-5xl mx-auto bg-gradient-to-b from-slate-900 to-navy-950 text-white border border-slate-800 rounded-3xl p-6 sm:p-10 shadow-2xl relative overflow-hidden">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <!-- Controls -->
          <div class="lg:col-span-7 space-y-6 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                  <i class="pi pi-building text-accent"></i> Number of Properties / Units
                </label>
                <span class="text-sm font-black text-amber-400 bg-amber-400/10 px-3 py-1 rounded-full border border-amber-400/20">
                  {{ calcUnits }} {{ calcUnits === 1 ? 'Unit' : 'Units' }}
                </span>
              </div>
              <input type="range" min="1" max="20" v-model.number="calcUnits" class="w-full accent-accent cursor-pointer h-2 bg-slate-700 rounded-lg" />
              <div class="flex justify-between text-[11px] text-slate-500 font-bold mt-1">
                <span>1 Unit</span>
                <span>10 Units</span>
                <span>20 Units</span>
              </div>
            </div>

            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                  <i class="pi pi-dollar text-emerald-400"></i> Average Nightly Rate
                </label>
                <span class="text-sm font-black text-emerald-400 bg-emerald-400/10 px-3 py-1 rounded-full border border-emerald-400/20">
                  {{ currencyStore.formatPrice(calcNightlyRate) }} / night
                </span>
              </div>
              <input type="range" min="30" max="500" step="10" v-model.number="calcNightlyRate" class="w-full accent-accent cursor-pointer h-2 bg-slate-700 rounded-lg" />
              <div class="flex justify-between text-[11px] text-slate-500 font-bold mt-1">
                <span>$30</span>
                <span>$250</span>
                <span>$500</span>
              </div>
            </div>

            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                  <i class="pi pi-chart-line text-blue-400"></i> Estimated Occupancy
                </label>
                <span class="text-sm font-black text-blue-400 bg-blue-400/10 px-3 py-1 rounded-full border border-blue-400/20">
                  {{ calcOccupancy }}% (~{{ Math.round(30 * (calcOccupancy / 100)) }} nights/mo)
                </span>
              </div>
              <input type="range" min="30" max="90" step="5" v-model.number="calcOccupancy" class="w-full accent-accent cursor-pointer h-2 bg-slate-700 rounded-lg" />
              <div class="flex justify-between text-[11px] text-slate-500 font-bold mt-1">
                <span>30% Low</span>
                <span>65% Average</span>
                <span>90% High</span>
              </div>
            </div>
          </div>

          <!-- Display -->
          <div class="lg:col-span-5 flex flex-col gap-4">
            <div class="bg-slate-900/80 p-5 rounded-2xl border border-slate-800">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400 block">Est. Gross Monthly Revenue</span>
              <p class="text-3xl font-black text-white mt-1">{{ currencyStore.formatPrice(grossMonthly) }} <span class="text-xs text-slate-400 font-medium">/ mo</span></p>
            </div>

            <div class="bg-slate-950 p-4 rounded-2xl border border-slate-800 text-xs space-y-2">
              <div class="flex justify-between text-red-400 font-bold">
                <span>18% Legacy OTA Fees Lost:</span>
                <span>-{{ currencyStore.formatPrice(annualOtaLoss) }} / yr</span>
              </div>
              <div class="flex justify-between text-emerald-400 font-bold pt-2 border-t border-slate-800">
                <span>Apartex Flat Subscription:</span>
                <span>{{ currencyStore.formatPrice(planCostAnnual) }} / yr</span>
              </div>
            </div>

            <div class="bg-gradient-to-r from-emerald-950 via-slate-900 to-emerald-950 p-5 rounded-2xl border border-emerald-500/40 text-center">
              <span class="text-xs font-black uppercase tracking-widest text-emerald-400 block mb-1">Your Net Annual Savings</span>
              <p class="text-3xl sm:text-4xl font-black text-emerald-400">+{{ currencyStore.formatPrice(netSavings) }}</p>
              <p class="text-xs text-slate-300 mt-1 font-medium">Money kept directly in your bank or MoMo wallet!</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- HOST SUBSCRIPTION TIERS -->
    <section class="bg-white border-y border-surface-border py-20">
      <div class="max-w-[1280px] mx-auto px-4 sm:px-6">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <span class="section-tag">Transparent Subscriptions</span>
          <h2 class="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight">Choose Your Host Plan</h2>
          <p class="text-slate-600 text-base mt-2 font-medium">No hidden fees, no percentage cuts, upgrade or cancel anytime.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div 
            v-for="plan in plans" 
            :key="plan.name"
            class="rounded-3xl p-8 border flex flex-col justify-between transition-all duration-300 relative"
            :class="plan.popular ? 'bg-slate-900 text-white border-white/20 shadow-sm scale-105' : 'bg-white text-slate-900 border-surface-border shadow-sm'"
          >
            <div v-if="plan.popular" class="absolute -top-4 left-1/2 -translate-x-1/2 bg-accent text-white text-xs font-black uppercase tracking-widest px-4 py-1.5 rounded-full shadow-md">
              Most Popular
            </div>

            <div>
              <span class="text-xs font-black uppercase tracking-widest text-accent block mb-2">{{ plan.bestFor }}</span>
              <h3 class="text-2xl font-black mb-2">{{ plan.name }}</h3>
              <p class="text-xs font-medium opacity-70 mb-6 min-h-[36px]">{{ plan.description }}</p>

              <div class="mb-6 pb-6 border-b border-slate-200/40">
                <span class="text-4xl font-black">{{ currencyStore.formatPrice(plan.monthly) }}</span>
                <span class="text-xs font-bold opacity-60"> / month</span>
              </div>

              <div class="space-y-3 mb-8 text-xs font-medium">
                <div v-for="feat in plan.features" :key="feat" class="flex items-center gap-2.5">
                  <i class="pi pi-check-circle text-emerald-500 text-sm"></i>
                  <span>{{ feat }}</span>
                </div>
              </div>
            </div>

            <router-link to="/register?role=owner" class="w-full btn-accent font-black py-4 px-6 rounded-2xl text-center no-underline block text-sm">
              Get Started with {{ plan.name }}
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER CTA -->
    <footer class="bg-slate-950 text-white py-16">
      <div class="max-w-[1280px] mx-auto px-4 sm:px-6 text-center">
        <h2 class="text-3xl sm:text-4xl font-black mb-4">Ready to Start Earning More?</h2>
        <p class="text-slate-400 max-w-xl mx-auto mb-8 text-sm">Join top executive hosts and property owners across Lusaka, Livingstone, Ndola, and Solwezi.</p>
        <router-link to="/register?role=owner" class="btn-accent text-base font-black px-9 py-4 rounded-full no-underline inline-block">
          Become a Host Today
        </router-link>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useCurrencyStore } from '@/stores/currency';

const currencyStore = useCurrencyStore();

const calcUnits = ref(2);
const calcNightlyRate = ref(100);
const calcOccupancy = ref(65);

const grossMonthly = computed(() => {
  const nights = Math.round(30 * (calcOccupancy.value / 100)) * calcUnits.value;
  return nights * calcNightlyRate.value;
});

const grossAnnual = computed(() => grossMonthly.value * 12);
const annualOtaLoss = computed(() => Math.round(grossAnnual.value * 0.18));

const planCostAnnual = computed(() => {
  if (calcUnits.value === 1) return 240;
  if (calcUnits.value <= 5) return 480;
  return 840;
});

const netSavings = computed(() => Math.max(0, annualOtaLoss.value - planCostAnnual.value));

const plans = [
  {
    name: 'Starter Host',
    bestFor: 'Single Property Owners',
    description: 'Perfect for independent hosts managing a single apartment or house.',
    monthly: 20,
    popular: false,
    features: [
      '0% Booking Commission',
      'Walk-in POS Calendar Sync',
      'MTN & Airtel MoMo Payouts',
      'Verified Guest Reviews',
      'Basic Owner Analytics'
    ]
  },
  {
    name: 'Growth Host',
    bestFor: '2–5 Properties',
    description: 'Designed for expanding property hosts across Zambian hubs.',
    monthly: 40,
    popular: true,
    features: [
      '0% Booking Commission',
      'Walk-in POS Calendar Sync',
      'MTN & Airtel MoMo Payouts',
      'Apartex Loyalty Integration',
      'Advanced Multi-Property Dashboard',
      'Priority Support'
    ]
  },
  {
    name: 'Professional Portfolio',
    bestFor: 'Lodges & Hotels',
    description: 'Commercial multi-room inventory management solution.',
    monthly: 70,
    popular: false,
    features: [
      '0% Booking Commission',
      'Unlimited Room Types',
      'Walk-in POS Calendar Sync',
      'Dedicated Account Manager',
      'Custom API & Channel Sync',
      '24/7 VIP Onboarding Support'
    ]
  }
];

const scrollToCalculator = () => {
  const el = document.getElementById('earnings-calculator');
  if (el) el.scrollIntoView({ behavior: 'smooth' });
};
</script>
