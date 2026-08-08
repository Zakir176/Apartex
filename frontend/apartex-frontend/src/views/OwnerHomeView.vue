<template>
  <div class="max-w-[1250px] mx-auto px-4 sm:px-6 py-8 text-slate-800">
    
    <!-- Executive Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
      <div>
        <div class="flex items-center gap-2 mb-1">
          <span class="px-3 py-1 rounded-full bg-accent-light text-accent text-xs font-black uppercase tracking-wider">
            Host Ecosystem Hub
          </span>
          <span class="text-slate-400 text-xs">• Verified Host Account</span>
        </div>
        <h1 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
          Welcome back, {{ authStore.user?.full_name || 'Property Host' }}!
        </h1>
        <p class="text-slate-500 font-medium text-sm sm:text-base mt-1">
          Overview of your portfolio performance, guest reservations, and payout readiness across Zambia.
        </p>
      </div>

      <div class="flex items-center gap-3 flex-wrap">
        <button
          @click="showWalkInModal = true"
          class="flex items-center gap-2 px-6 py-3 rounded-full border-2 border-accent text-accent text-sm font-black hover:bg-accent-subtle transition-colors duration-150 cursor-pointer"
        >
          <i class="pi pi-user-plus"></i>
          <span>Walk-in Booking</span>
        </button>
        <button
          @click="router.push('/owner/apartments')"
          class="btn-accent shadow-accent text-sm font-black px-6 py-3 rounded-full flex items-center gap-2 no-underline cursor-pointer"
        >
          <i class="pi pi-plus-circle"></i>
          <span>Add New Property</span>
        </button>
      </div>
    </div>

    <!-- Executive KPI Summary Strip -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <!-- Total Revenue -->
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between mb-4">
          <span class="text-xs font-black text-slate-400 uppercase tracking-wider">Gross Earnings</span>
          <div class="w-10 h-10 rounded-xl bg-accent-light text-accent flex items-center justify-center">
            <i class="pi pi-wallet text-lg"></i>
          </div>
        </div>
        <div>
          <p class="text-3xl font-black text-slate-900 tracking-tight animate-number-reveal">${{ animatedEarnings.toLocaleString() }}</p>
          <p class="text-xs font-bold text-emerald-600 flex items-center gap-1 mt-1">
            <i class="pi pi-arrow-up text-[10px]"></i> +14.2% <span class="text-slate-400 font-normal">vs last month</span>
          </p>
        </div>
      </div>

      <!-- Active Listings -->
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between mb-4">
          <span class="text-xs font-black text-slate-400 uppercase tracking-wider">Active Properties</span>
          <div class="w-10 h-10 rounded-xl bg-navy-50 text-navy flex items-center justify-center">
            <i class="pi pi-building text-lg"></i>
          </div>
        </div>
        <div>
          <p class="text-3xl font-black text-slate-900 tracking-tight">{{ apartmentsStore.apartments.length || 3 }}</p>
          <p class="text-xs text-slate-500 font-semibold mt-1">All listings active & verified</p>
        </div>
      </div>

      <!-- Occupancy Rate -->
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between mb-4">
          <span class="text-xs font-black text-slate-400 uppercase tracking-wider">Occupancy Rate</span>
          <div class="w-10 h-10 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
            <i class="pi pi-chart-line text-lg"></i>
          </div>
        </div>
        <div>
          <p class="text-3xl font-black text-slate-900 tracking-tight">78%</p>
          <p class="text-xs font-bold text-emerald-600 flex items-center gap-1 mt-1">
            <i class="pi pi-arrow-up text-[10px]"></i> +5% <span class="text-slate-400 font-normal">above city average</span>
          </p>
        </div>
      </div>

      <!-- Pending Reservations -->
      <div class="bg-white rounded-2xl p-6 border border-surface-border shadow-sm flex flex-col justify-between">
        <div class="flex items-center justify-between mb-4">
          <span class="text-xs font-black text-slate-400 uppercase tracking-wider">Pending Approvals</span>
          <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
            <i class="pi pi-clock text-lg"></i>
          </div>
        </div>
        <div>
          <p class="text-3xl font-black text-amber-500 tracking-tight animate-number-reveal" style="animation-delay: 0.2s">{{ animatedPending }}</p>
          <p class="text-xs text-slate-500 font-semibold mt-1">Requires host action</p>
        </div>
      </div>
    </div>

    <!-- Quick Action Launchpad -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
      <div @click="router.push('/owner/apartments')" class="bg-white p-6 rounded-2xl border border-surface-border shadow-sm hover:shadow-md hover:-translate-y-1 transition-all cursor-pointer group">
        <div class="w-12 h-12 rounded-xl bg-accent-light text-accent flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
          <i class="pi pi-plus-circle text-xl"></i>
        </div>
        <h3 class="text-base font-black text-slate-900 group-hover:text-accent transition-colors">List New Property</h3>
        <p class="text-xs text-slate-500 font-medium mt-1 leading-relaxed">Add a new penthouse, suite or villa to your portfolio.</p>
      </div>

      <div @click="router.push('/dashboard')" class="bg-white p-6 rounded-2xl border border-surface-border shadow-sm hover:shadow-md hover:-translate-y-1 transition-all cursor-pointer group">
        <div class="w-12 h-12 rounded-xl bg-navy-50 text-navy flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
          <i class="pi pi-chart-bar text-xl"></i>
        </div>
        <h3 class="text-base font-black text-slate-900 group-hover:text-accent transition-colors">View Analytics</h3>
        <p class="text-xs text-slate-500 font-medium mt-1 leading-relaxed">Analyze revenue per available room (RevPAR) & trends.</p>
      </div>

      <div @click="router.push('/owner/bookings')" class="bg-white p-6 rounded-2xl border border-surface-border shadow-sm hover:shadow-md hover:-translate-y-1 transition-all cursor-pointer group">
        <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
          <i class="pi pi-calendar-check text-xl"></i>
        </div>
        <h3 class="text-base font-black text-slate-900 group-hover:text-accent transition-colors">Manage Reservations</h3>
        <p class="text-xs text-slate-500 font-medium mt-1 leading-relaxed">Review guest details, check-in dates & stay status.</p>
      </div>

      <div @click="router.push('/owner/payouts')" class="bg-white p-6 rounded-2xl border border-surface-border shadow-sm hover:shadow-md hover:-translate-y-1 transition-all cursor-pointer group">
        <div class="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
          <i class="pi pi-mobile text-xl"></i>
        </div>
        <h3 class="text-base font-black text-slate-900 group-hover:text-accent transition-colors">Withdraw Earnings</h3>
        <p class="text-xs text-slate-500 font-medium mt-1 leading-relaxed">Instant payouts via MTN, Airtel Money, or Bank Transfer.</p>
      </div>
    </div>

    <!-- Main Operational Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      
      <!-- Left Column: Upcoming Check-Ins & Pending Approvals -->
      <div class="lg:col-span-8 flex flex-col gap-8">
        
        <!-- Upcoming Guest Stay Schedule -->
        <div class="bg-white rounded-3xl border border-surface-border p-6 sm:p-8 shadow-sm">
          <div class="flex items-center justify-between mb-6 pb-4 border-b border-surface-border">
            <div>
              <h3 class="text-lg font-black text-slate-900">Upcoming Guest Check-Ins</h3>
              <p class="text-xs text-slate-500 font-medium mt-0.5">Scheduled check-ins over the next 7 days</p>
            </div>
            <router-link to="/owner/bookings" class="text-xs font-bold text-accent hover:underline no-underline">
              View All Bookings →
            </router-link>
          </div>

          <div class="flex flex-col gap-4">
            <div 
              v-for="booking in upcomingCheckIns" 
              :key="booking.id"
              class="p-4 rounded-2xl border border-surface-border bg-slate-50 hover:bg-white transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-full bg-navy text-white font-black text-sm flex items-center justify-center shrink-0">
                  {{ booking.guestInitials }}
                </div>
                <div>
                  <p class="font-black text-sm text-slate-900">{{ booking.guestName }}</p>
                  <p class="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                    <i class="pi pi-home text-[10px]"></i> {{ booking.propertyName }}
                  </p>
                </div>
              </div>

              <div class="flex items-center justify-between sm:justify-end gap-6 text-xs">
                <div>
                  <p class="text-slate-400 font-semibold uppercase text-[10px]">Check-in Date</p>
                  <p class="font-bold text-slate-800">{{ booking.checkInDate }}</p>
                </div>
                <div>
                  <p class="text-slate-400 font-semibold uppercase text-[10px]">Payout Value</p>
                  <p class="font-black text-emerald-600">${{ booking.totalPrice }}</p>
                </div>
                <span class="px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider" :class="booking.statusClass">
                  {{ booking.status }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Host Optimization Advice & News -->
        <div class="bg-gradient-to-br from-slate-900 via-navy-700 to-slate-900 rounded-3xl p-8 text-white shadow-xl relative overflow-hidden">
          <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="max-w-xl">
              <span class="text-[10px] font-black uppercase tracking-widest text-accent mb-2 block">Host Growth Insight</span>
              <h3 class="text-2xl font-black text-white">Enable Instant Booking & Mobile Money Payouts</h3>
              <p class="text-xs text-slate-300 leading-relaxed mt-2">
                Listings with instant confirmation and MTN/Airtel settlement options receive up to 45% more direct reservations from business travelers in Zambia.
              </p>
            </div>
            <button @click="router.push('/owner/apartments')" class="btn-accent font-black text-xs px-6 py-3 rounded-full shrink-0 shadow-accent">
              Optimize Listings
            </button>
          </div>
        </div>

      </div>

      <!-- Right Column: Host Quality Score & Quick Settlement -->
      <div class="lg:col-span-4 flex flex-col gap-8">
        
        <!-- Host Health & Rating Card -->
        <div class="bg-white rounded-3xl border border-surface-border p-7 shadow-sm">
          <h3 class="text-base font-black text-slate-900 mb-4 flex items-center justify-between">
            <span>Host Performance Score</span>
            <span class="text-xs font-black text-emerald-600 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">SUPERHOST</span>
          </h3>

          <div class="flex items-baseline gap-2 mb-6">
            <span class="text-4xl font-black text-slate-900">4.96</span>
            <span class="text-xs font-bold text-amber-500 flex items-center gap-1">
              <i class="pi pi-star-fill text-xs"></i> 100% Verified Rating
            </span>
          </div>

          <div class="flex flex-col gap-4 border-t border-surface-border pt-4 text-xs font-semibold">
            <div>
              <div class="flex justify-between text-slate-600 mb-1">
                <span>Response Rate</span>
                <span class="font-extrabold text-slate-900">99.4%</span>
              </div>
              <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full w-[99%]"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-600 mb-1">
                <span>Booking Acceptance</span>
                <span class="font-extrabold text-slate-900">96.8%</span>
              </div>
              <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-accent rounded-full w-[96%]"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-slate-600 mb-1">
                <span>Cleanliness Rating</span>
                <span class="font-extrabold text-slate-900">5.0 / 5.0</span>
              </div>
              <div class="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full w-[100%]"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Payout Readiness Card -->
        <div class="bg-white rounded-3xl border border-surface-border p-7 shadow-sm">
          <span class="text-xs font-black text-slate-400 uppercase tracking-wider block mb-1">Ready for Withdrawal</span>
          <p class="text-3xl font-black text-slate-900">${{ availablePayout.toLocaleString() }} <span class="text-xs font-normal text-slate-400">USD</span></p>
          <p class="text-xs text-slate-500 font-medium mt-1">Available for immediate transfer via Mobile Money or Bank.</p>

          <button @click="router.push('/owner/payouts')" class="w-full mt-6 bg-navy text-white text-center font-bold text-xs py-3 rounded-xl block no-underline hover:bg-slate-800 transition-colors">
            Request Payout Now
          </button>
        </div>

      </div>

    </div>

    <!-- Walk-in Booking Modal -->
    <WalkInBookingModal
      :show="showWalkInModal"
      :ownerProperties="ownerProperties"
      @close="showWalkInModal = false"
      @booked="onWalkInBooked"
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useApartmentsStore } from '@/stores/apartments';
import { useBookingsStore } from '@/stores/bookings';
import { useDashboardStore } from '@/stores/dashboard';
import { useCountUp } from '@/composables/useCountUp';
import WalkInBookingModal from '@/components/WalkInBookingModal.vue';

const router = useRouter();
const authStore = useAuthStore();
const apartmentsStore = useApartmentsStore();
const bookingsStore = useBookingsStore();
const dashboardStore = useDashboardStore();

const showWalkInModal = ref(false);
const ownerProperties = ref([]);

function onWalkInBooked(booking) {
  // Refresh bookings list after a walk-in is recorded
  if (authStore.user?.id) {
    bookingsStore.fetchOwnerBookings(authStore.user.id);
  }
}

const totalEarnings = computed(() => dashboardStore.overview?.revenue_summary?.total_revenue || 0);
const availablePayout = ref(1250);
const pendingBookingsCount = computed(() => {
  return bookingsStore.ownerBookings?.filter(b => b.status === 'pending')?.length || 0;
});

const { current: animatedEarnings } = useCountUp(() => totalEarnings.value, 2000, 400);
const { current: animatedPending } = useCountUp(() => pendingBookingsCount.value, 800, 600);

const upcomingCheckIns = [
  {
    id: 101,
    guestName: 'Sharon Phiri',
    guestInitials: 'SP',
    propertyName: 'Rhodes Park Executive Penthouse',
    checkInDate: 'Jul 26, 2026',
    totalPrice: 625,
    status: 'Confirmed',
    statusClass: 'bg-emerald-50 text-emerald-700 border border-emerald-200'
  },
  {
    id: 102,
    guestName: 'Mwansa Kabwe',
    guestInitials: 'MK',
    propertyName: 'Zambezi River Cottages',
    checkInDate: 'Jul 28, 2026',
    totalPrice: 480,
    status: 'Confirmed',
    statusClass: 'bg-emerald-50 text-emerald-700 border border-emerald-200'
  },
  {
    id: 103,
    guestName: 'Daniel Zulu',
    guestInitials: 'DZ',
    propertyName: 'Kabulonga Executive Suite',
    checkInDate: 'Aug 02, 2026',
    totalPrice: 350,
    status: 'Pending',
    statusClass: 'bg-amber-50 text-amber-700 border border-amber-200'
  }
];

onMounted(async () => {
  if (apartmentsStore.apartments.length === 0) {
    await apartmentsStore.fetchApartments();
  }
  if (authStore.user?.id) {
    try { await bookingsStore.fetchOwnerBookings(authStore.user.id); } catch {}
  }
  try { await dashboardStore.loadOverview(); } catch {}
  // Load owner properties for walk-in modal
  try {
    const { apartmentsApi } = await import('@/api/apartments');
    const res = await apartmentsApi.getMyApartments();
    ownerProperties.value = res.data;
  } catch {}
});
</script>
