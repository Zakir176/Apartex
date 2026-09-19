<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-white to-emerald-50/30 flex flex-col items-center justify-center px-4 py-12">

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center gap-4 text-slate-400">
      <div class="w-16 h-16 rounded-full border-4 border-accent/20 border-t-accent animate-spin"></div>
      <p class="text-sm font-semibold tracking-wide">Verifying booking...</p>
    </div>

    <!-- Error / Not Found -->
    <div v-else-if="error" class="w-full max-w-md bg-white rounded-3xl border border-red-100 shadow-xl p-10 text-center">
      <div class="w-16 h-16 rounded-full bg-red-50 border border-red-100 flex items-center justify-center mx-auto mb-5">
        <i class="pi pi-times-circle text-3xl text-red-400"></i>
      </div>
      <h1 class="text-xl font-black text-slate-900 mb-2">Booking Not Found</h1>
      <p class="text-sm text-slate-500 font-medium leading-relaxed mb-6">{{ error }}</p>
      <a href="/" class="btn-accent px-6 py-2.5 rounded-full text-xs font-black inline-flex items-center gap-2 no-underline">
        <i class="pi pi-home text-xs"></i> Go to Apartex
      </a>
    </div>

    <!-- Success Card -->
    <div v-else-if="booking" class="w-full max-w-lg">

      <!-- Apartex Brand Header -->
      <div class="text-center mb-6">
        <span class="text-xs font-black uppercase tracking-[0.2em] text-accent">Apartex · Official Booking Verification</span>
      </div>

      <div class="bg-white rounded-3xl border border-slate-100 shadow-2xl overflow-hidden print:shadow-none print:rounded-none">

        <!-- Green Header Banner -->
        <div class="bg-[#0A6640] px-8 py-7 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-48 h-48 bg-white/5 rounded-full translate-x-16 -translate-y-16 pointer-events-none"></div>
          <div class="absolute bottom-0 left-0 w-32 h-32 bg-white/5 rounded-full -translate-x-10 translate-y-10 pointer-events-none"></div>

          <div class="flex items-start justify-between relative z-10">
            <div>
              <p class="text-white/60 text-[11px] font-semibold uppercase tracking-widest mb-1">Booking Reference</p>
              <p class="text-white text-2xl font-black tracking-wide">{{ booking.reference }}</p>
            </div>
            <!-- Status Badge -->
            <span
              class="px-3 py-1.5 rounded-full text-[10px] font-black uppercase tracking-wider flex items-center gap-1.5"
              :class="statusStyle.badge"
            >
              <span class="w-1.5 h-1.5 rounded-full" :class="statusStyle.dot"></span>
              {{ booking.status }}
            </span>
          </div>

          <div class="mt-5 relative z-10">
            <p class="text-white text-lg font-black leading-tight">{{ booking.property_name }}</p>
            <p class="text-white/60 text-xs font-medium mt-0.5 flex items-center gap-1">
              <i class="pi pi-map-marker text-[10px]"></i>{{ booking.property_city || 'Zambia' }}
            </p>
          </div>

          <!-- Walk-in badge if applicable -->
          <div v-if="booking.is_walk_in" class="mt-4 inline-flex items-center gap-1.5 bg-white/10 border border-white/20 px-3 py-1 rounded-full relative z-10">
            <i class="pi pi-desktop text-white text-[10px]"></i>
            <span class="text-white text-[10px] font-semibold">Walk-in Booking</span>
          </div>
        </div>

        <!-- Body -->
        <div class="p-8">

          <!-- Stay Dates Card -->
          <div class="bg-slate-50 border border-slate-200/80 rounded-2xl p-5 mb-6">
            <div class="flex items-stretch gap-4">
              <div class="flex-1">
                <p class="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1.5">Check-in</p>
                <p class="text-sm font-black text-slate-900">{{ formatDate(booking.check_in) }}</p>
                <p class="text-[11px] text-slate-400 font-medium mt-0.5">{{ formatDayName(booking.check_in) }}</p>
              </div>

              <div class="flex flex-col items-center justify-center gap-1 px-2">
                <div class="h-px w-8 bg-slate-200"></div>
                <span class="text-[10px] font-black text-slate-400 bg-white border border-slate-200 rounded-full px-2 py-0.5 whitespace-nowrap">
                  {{ nightsCount }} night{{ nightsCount !== 1 ? 's' : '' }}
                </span>
                <div class="h-px w-8 bg-slate-200"></div>
              </div>

              <div class="flex-1 text-right">
                <p class="text-[10px] font-black uppercase tracking-widest text-slate-400 mb-1.5">Check-out</p>
                <p class="text-sm font-black text-slate-900">{{ formatDate(booking.check_out) }}</p>
                <p class="text-[11px] text-slate-400 font-medium mt-0.5">{{ formatDayName(booking.check_out) }}</p>
              </div>
            </div>
          </div>

          <!-- Booking Details Grid -->
          <div class="grid grid-cols-2 gap-3 mb-6">
            <div class="bg-slate-50 rounded-xl p-3.5">
              <p class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-1">Guests</p>
              <p class="text-sm font-black text-slate-900 flex items-center gap-1.5">
                <i class="pi pi-users text-accent text-xs"></i>
                {{ booking.guests }} guest{{ booking.guests !== 1 ? 's' : '' }}
              </p>
            </div>
            <div class="bg-slate-50 rounded-xl p-3.5">
              <p class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-1">Booking Type</p>
              <p class="text-sm font-black text-slate-900 flex items-center gap-1.5">
                <i class="pi pi-tag text-accent text-xs"></i>
                {{ booking.is_walk_in ? 'Walk-in' : 'Online' }}
              </p>
            </div>
            <div class="bg-slate-50 rounded-xl p-3.5">
              <p class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-1">Booking ID</p>
              <p class="text-xs font-black text-slate-700 font-mono">#{{ booking.booking_id }}</p>
            </div>
            <div class="bg-slate-50 rounded-xl p-3.5">
              <p class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-1">Created</p>
              <p class="text-xs font-black text-slate-700">{{ formatDate(booking.created_at) }}</p>
            </div>
          </div>

          <!-- Confirmed checkmark strip -->
          <div
            class="flex items-center gap-3 rounded-xl px-4 py-3 mb-6 border"
            :class="statusStyle.strip"
          >
            <i class="pi text-lg shrink-0" :class="statusStyle.icon"></i>
            <div>
              <p class="text-sm font-black" :class="statusStyle.textDark">{{ statusMessage }}</p>
              <p class="text-xs font-medium mt-0.5" :class="statusStyle.textLight">Verified by Apartex Platform</p>
            </div>
          </div>

          <!-- Footer -->
          <div class="text-center pt-2 border-t border-slate-100">
            <p class="text-[11px] text-slate-400 leading-relaxed">
              <span class="font-black text-[#0A6640]">apartex.vercel.app</span>
              &nbsp;·&nbsp; Official booking verification. Present this screen at check-in.
            </p>
          </div>
        </div>
      </div>

      <!-- Print button (hidden in print) -->
      <div class="mt-5 flex justify-center gap-3 print:hidden">
        <button @click="handlePrint" class="px-5 py-2.5 rounded-full border border-slate-300 bg-white text-slate-700 text-xs font-bold hover:bg-slate-50 transition-colors inline-flex items-center gap-2 shadow-sm cursor-pointer">
          <i class="pi pi-print text-xs"></i> Print / Save PDF
        </button>
        <a href="/apartments" class="px-5 py-2.5 rounded-full bg-[#0A6640] text-white text-xs font-bold hover:bg-emerald-800 transition-colors inline-flex items-center gap-2 shadow-sm no-underline">
          <i class="pi pi-home text-xs"></i> Browse Stays
        </a>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const booking = ref(null);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  const id = route.params.id;
  try {
    // Use plain fetch — this endpoint is public (no auth required).
    // Avoids the apiClient auth interceptor redirecting to /login.
    const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';
    const res = await fetch(`${API_BASE}/bookings/verify/${id}`);
    if (res.status === 404) {
      error.value = `No booking found with ID #${id}. The QR code may be outdated or the booking may have been removed.`;
    } else if (!res.ok) {
      error.value = 'Unable to verify this booking right now. Please try again or contact Apartex support.';
    } else {
      booking.value = await res.json();
    }
  } catch {
    error.value = 'Unable to verify this booking right now. Please try again or contact Apartex support.';
  } finally {
    loading.value = false;
  }
});

const nightsCount = computed(() => {
  if (!booking.value?.check_in || !booking.value?.check_out) return 0;
  const diff = new Date(booking.value.check_out) - new Date(booking.value.check_in);
  return Math.max(0, Math.round(diff / (1000 * 60 * 60 * 24)));
});

const statusStyle = computed(() => {
  const s = booking.value?.status?.toLowerCase();
  if (s === 'confirmed') return {
    badge: 'bg-emerald-500/20 text-emerald-300',
    dot: 'bg-emerald-400',
    strip: 'bg-emerald-50 border-emerald-200',
    icon: 'pi-check-circle text-emerald-500',
    textDark: 'text-emerald-800',
    textLight: 'text-emerald-600',
  };
  if (s === 'completed') return {
    badge: 'bg-blue-500/20 text-blue-300',
    dot: 'bg-blue-400',
    strip: 'bg-blue-50 border-blue-200',
    icon: 'pi-star-fill text-blue-500',
    textDark: 'text-blue-800',
    textLight: 'text-blue-600',
  };
  if (s === 'cancelled') return {
    badge: 'bg-red-500/20 text-red-300',
    dot: 'bg-red-400',
    strip: 'bg-red-50 border-red-200',
    icon: 'pi-times-circle text-red-500',
    textDark: 'text-red-800',
    textLight: 'text-red-600',
  };
  // pending / default
  return {
    badge: 'bg-amber-500/20 text-amber-300',
    dot: 'bg-amber-400',
    strip: 'bg-amber-50 border-amber-200',
    icon: 'pi-clock text-amber-500',
    textDark: 'text-amber-800',
    textLight: 'text-amber-600',
  };
});

const statusMessage = computed(() => {
  const s = booking.value?.status?.toLowerCase();
  if (s === 'confirmed') return 'Booking Confirmed — Valid for check-in';
  if (s === 'completed') return 'Stay Completed — Thank you for your visit';
  if (s === 'cancelled') return 'Booking Cancelled — No longer valid';
  return 'Booking Pending — Awaiting confirmation';
});

const formatDate = (dateStr) => {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' });
};

const formatDayName = (dateStr) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-US', { weekday: 'long' });
};

function handlePrint() {
  globalThis.window.print();
}
</script>

<style scoped>
@media print {
  body { background: white; }
  .print\:hidden { display: none !important; }
  .print\:shadow-none { box-shadow: none !important; }
  .print\:rounded-none { border-radius: 0 !important; }
}
</style>
