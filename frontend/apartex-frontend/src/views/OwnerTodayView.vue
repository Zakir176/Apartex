<template>
  <div class="max-w-4xl mx-auto">

    <!-- Header -->
    <div class="mb-8" v-motion :initial="{ opacity: 0, y: 16 }" :enter="{ opacity: 1, y: 0, transition: { duration: 400 } }">
      <p class="text-xs font-black uppercase tracking-widest text-accent mb-1">{{ dayName }}, {{ formattedDate }}</p>
      <h1 class="text-3xl font-black text-slate-800 tracking-tight">Today at a Glance</h1>
      <p class="text-slate-400 text-sm mt-1 font-medium">Your property activity for today</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div v-for="i in 3" :key="i" class="h-28 bg-slate-100 rounded-2xl animate-pulse"></div>
    </div>

    <!-- Stats row -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8" v-motion :initial="{ opacity: 0, y: 20 }" :enter="{ opacity: 1, y: 0, transition: { delay: 100, duration: 400 } }">
      <div class="bg-white rounded-2xl border border-surface-border p-5 flex flex-col gap-2 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center">
          <i class="pi pi-sign-in text-emerald-500 text-lg"></i>
        </div>
        <p class="text-2xl font-black text-slate-800">{{ checkIns.length }}</p>
        <p class="text-xs font-bold text-slate-400 uppercase tracking-wide">Check-ins Today</p>
      </div>
      <div class="bg-white rounded-2xl border border-surface-border p-5 flex flex-col gap-2 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center">
          <i class="pi pi-sign-out text-amber-500 text-lg"></i>
        </div>
        <p class="text-2xl font-black text-slate-800">{{ checkOuts.length }}</p>
        <p class="text-xs font-bold text-slate-400 uppercase tracking-wide">Check-outs Today</p>
      </div>
      <div class="bg-navy rounded-2xl p-5 flex flex-col gap-2 shadow-sm">
        <div class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center">
          <i class="pi pi-users text-white text-lg"></i>
        </div>
        <p class="text-2xl font-black text-white">{{ currentGuests.length }}</p>
        <p class="text-xs font-black text-white/50 uppercase tracking-wide">Current Guests</p>
      </div>
    </div>

    <!-- Check-ins section -->
    <div class="mb-8" v-motion :initial="{ opacity: 0, y: 20 }" :enter="{ opacity: 1, y: 0, transition: { delay: 200, duration: 400 } }">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
        <h2 class="text-base font-black text-slate-800">Checking In Today</h2>
        <span class="ml-auto text-xs font-black text-slate-400 bg-slate-100 px-2.5 py-1 rounded-full">{{ checkIns.length }}</span>
      </div>

      <div v-if="checkIns.length === 0" class="bg-white rounded-2xl border border-surface-border p-8 text-center">
        <i class="pi pi-check-circle text-3xl text-slate-200 mb-3 block"></i>
        <p class="text-sm font-bold text-slate-400">No check-ins today</p>
      </div>

      <div v-else class="flex flex-col gap-3">
        <div
          v-for="(booking, index) in checkIns"
          :key="booking.id"
          class="bg-white rounded-2xl border border-surface-border p-4 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow duration-200"
          v-motion
          :initial="{ opacity: 0, x: -16 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: 250 + index * 80, duration: 350 } }"
        >
          <!-- Avatar -->
          <div class="w-11 h-11 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center shrink-0">
            <span class="text-emerald-600 font-black text-sm">{{ guestInitials(booking) }}</span>
          </div>

          <!-- Details -->
          <div class="flex-1 min-w-0">
            <p class="font-bold text-slate-800 text-sm truncate">{{ guestName(booking) }}</p>
            <p class="text-xs text-slate-400 font-medium truncate">{{ propertyName(booking.property_id) }} {{ booking.room_id ? '· ' + roomName(booking.room_id) : '' }}</p>
          </div>

          <!-- Meta -->
          <div class="text-right shrink-0">
            <p class="text-xs font-black text-slate-700">{{ booking.guests }} guest{{ booking.guests !== 1 ? 's' : '' }}</p>
            <p class="text-xs text-slate-400 font-medium">Until {{ formatDate(booking.check_out) }}</p>
          </div>

          <!-- Badge -->
          <div class="shrink-0">
            <span
              class="text-[10px] font-black px-2.5 py-1 rounded-full uppercase tracking-wide"
              :class="booking.is_walk_in ? 'bg-accent/10 text-accent' : 'bg-blue-50 text-blue-600'"
            >
              {{ booking.is_walk_in ? 'Walk-in' : 'Online' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Check-outs section -->
    <div class="mb-8" v-motion :initial="{ opacity: 0, y: 20 }" :enter="{ opacity: 1, y: 0, transition: { delay: 300, duration: 400 } }">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-2.5 h-2.5 rounded-full bg-amber-400"></div>
        <h2 class="text-base font-black text-slate-800">Checking Out Today</h2>
        <span class="ml-auto text-xs font-black text-slate-400 bg-slate-100 px-2.5 py-1 rounded-full">{{ checkOuts.length }}</span>
      </div>

      <div v-if="checkOuts.length === 0" class="bg-white rounded-2xl border border-surface-border p-8 text-center">
        <i class="pi pi-calendar text-3xl text-slate-200 mb-3 block"></i>
        <p class="text-sm font-bold text-slate-400">No check-outs today</p>
      </div>

      <div v-else class="flex flex-col gap-3">
        <div
          v-for="(booking, index) in checkOuts"
          :key="booking.id"
          class="bg-white rounded-2xl border border-surface-border p-4 flex items-center gap-4 shadow-sm hover:shadow-md transition-shadow duration-200"
          v-motion
          :initial="{ opacity: 0, x: -16 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: 350 + index * 80, duration: 350 } }"
        >
          <div class="w-11 h-11 rounded-xl bg-amber-50 border border-amber-100 flex items-center justify-center shrink-0">
            <span class="text-amber-600 font-black text-sm">{{ guestInitials(booking) }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-bold text-slate-800 text-sm truncate">{{ guestName(booking) }}</p>
            <p class="text-xs text-slate-400 font-medium truncate">{{ propertyName(booking.property_id) }} {{ booking.room_id ? '· ' + roomName(booking.room_id) : '' }}</p>
          </div>
          <div class="text-right shrink-0">
            <p class="text-xs font-black text-slate-700">${{ booking.total_price }}</p>
            <p class="text-xs text-slate-400 font-medium">{{ booking.guests }} guest{{ booking.guests !== 1 ? 's' : '' }}</p>
          </div>
          <div class="shrink-0">
            <span
              class="text-[10px] font-black px-2.5 py-1 rounded-full uppercase tracking-wide"
              :class="booking.is_walk_in ? 'bg-accent/10 text-accent' : 'bg-blue-50 text-blue-600'"
            >
              {{ booking.is_walk_in ? 'Walk-in' : 'Online' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Current guests section -->
    <div v-motion :initial="{ opacity: 0, y: 20 }" :enter="{ opacity: 1, y: 0, transition: { delay: 400, duration: 400 } }">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-2.5 h-2.5 rounded-full bg-navy"></div>
        <h2 class="text-base font-black text-slate-800">Currently Staying</h2>
        <span class="ml-auto text-xs font-black text-slate-400 bg-slate-100 px-2.5 py-1 rounded-full">{{ currentGuests.length }}</span>
      </div>

      <div v-if="currentGuests.length === 0" class="bg-white rounded-2xl border border-surface-border p-8 text-center">
        <i class="pi pi-home text-3xl text-slate-200 mb-3 block"></i>
        <p class="text-sm font-bold text-slate-400">No guests currently staying</p>
      </div>

      <div v-else class="flex flex-col gap-3">
        <div
          v-for="(booking, index) in currentGuests"
          :key="booking.id"
          class="bg-navy/5 border border-navy/10 rounded-2xl p-4 flex items-center gap-4"
          v-motion
          :initial="{ opacity: 0, x: -16 }"
          :enter="{ opacity: 1, x: 0, transition: { delay: 450 + index * 80, duration: 350 } }"
        >
          <div class="w-11 h-11 rounded-xl bg-navy/10 flex items-center justify-center shrink-0">
            <span class="text-navy font-black text-sm">{{ guestInitials(booking) }}</span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-bold text-slate-800 text-sm truncate">{{ guestName(booking) }}</p>
            <p class="text-xs text-slate-400 font-medium truncate">{{ propertyName(booking.property_id) }} {{ booking.room_id ? '· ' + roomName(booking.room_id) : '' }}</p>
          </div>
          <div class="text-right shrink-0">
            <p class="text-xs font-black text-slate-700">Checks out {{ formatDate(booking.check_out) }}</p>
            <p class="text-xs text-slate-400 font-medium">{{ daysRemaining(booking.check_out) }} day{{ daysRemaining(booking.check_out) !== 1 ? 's' : '' }} left</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useBookingsStore } from '@/stores/bookings';
import { useApartmentsStore } from '@/stores/apartments';
import { bookingsApi } from '@/api/bookings';
import { apartmentsApi } from '@/api/apartments';

const authStore = useAuthStore();
const bookingsStore = useBookingsStore();

const loading = ref(true);
const allBookings = ref([]);
const properties = ref([]);
const rooms = ref([]);

const today = new Date();
const todayStr = today.toISOString().split('T')[0];

const dayName = computed(() => today.toLocaleDateString('en-US', { weekday: 'long' }));
const formattedDate = computed(() => today.toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' }));

// Today's check-ins
const checkIns = computed(() =>
  allBookings.value.filter(b =>
    b.check_in === todayStr && b.status === 'confirmed'
  )
);

// Today's check-outs
const checkOuts = computed(() =>
  allBookings.value.filter(b =>
    b.check_out === todayStr && b.status === 'confirmed'
  )
);

// Guests currently staying (checked in before today, checking out after today)
const currentGuests = computed(() =>
  allBookings.value.filter(b =>
    b.check_in < todayStr && b.check_out > todayStr && b.status === 'confirmed'
  )
);

function guestName(booking) {
  return booking.is_walk_in
    ? booking.walk_in_guest_name || 'Walk-in Guest'
    : booking.user_id ? `Guest #${booking.user_id}` : 'Online Guest';
}

function guestInitials(booking) {
  const name = guestName(booking);
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
}

function propertyName(propertyId) {
  const prop = properties.value.find(p => p.id === propertyId);
  return prop?.title || `Property #${propertyId}`;
}

function roomName(roomId) {
  const room = rooms.value.find(r => r.id === roomId);
  return room?.room_type || '';
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-US', { day: 'numeric', month: 'short' });
}

function daysRemaining(checkOut) {
  const diff = new Date(checkOut) - today;
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

onMounted(async () => {
  try {
    const ownerId = authStore.user?.id;
    if (!ownerId) return;

    const [bookingsRes, propertiesRes] = await Promise.all([
      bookingsApi.getOwnerBookings(ownerId),
      apartmentsApi.getMyApartments(),
    ]);

    allBookings.value = bookingsRes.data;
    properties.value = propertiesRes.data;

    // Load rooms for all non-apartment properties
    const nonApartmentProps = propertiesRes.data.filter(
      p => ['hotel', 'lodge', 'guest_house'].includes(p.property_type)
    );
    const roomResults = await Promise.all(
      nonApartmentProps.map(p => apartmentsApi.getRoomsForProperty(p.id).catch(() => ({ data: [] })))
    );
    rooms.value = roomResults.flatMap(r => r.data);

  } catch (err) {
    console.error('Failed to load today data:', err);
  } finally {
    loading.value = false;
  }
});
</script>
