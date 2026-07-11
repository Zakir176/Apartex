<template>
  <div class="min-h-screen bg-[#F8F7F4]">

    <!-- HERO -->
    <header class="bg-animated-mesh border-b border-surface-border">
      <div class="max-w-content mx-auto px-6 py-20 text-center relative z-10">
        <span class="section-tag">Zambia's Accommodation Platform</span>
        <h1 class="text-5xl md:text-6xl font-black text-slate-800 tracking-tight leading-tight mb-4">
          Find Your Perfect<br class="hidden md:block" />
          <span class="text-accent">Stay in Zambia</span>
        </h1>
        <p class="text-lg text-slate-500 max-w-xl mx-auto mb-10">
          Handpicked apartments, lodges and guest houses — no hidden fees.
        </p>

        <!-- Search Bar -->
        <div class="bg-white rounded-xl shadow-xl border border-surface-border max-w-4xl mx-auto p-2 flex flex-col md:flex-row items-stretch gap-2">
          <!-- Location -->
          <div class="flex-1 flex flex-col px-4 py-2 border-b md:border-b-0 md:border-r border-surface-border">
            <label class="text-xs font-bold text-slate-400 uppercase tracking-wide mb-1">Where to?</label>
            <select v-model="selectedCity" class="bg-transparent text-sm font-semibold text-slate-700 outline-none border-none cursor-pointer">
              <option value="">Any city</option>
              <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>
          <!-- Check-in -->
          <div class="flex-1 flex flex-col px-4 py-2 border-b md:border-b-0 md:border-r border-surface-border">
            <label class="text-xs font-bold text-slate-400 uppercase tracking-wide mb-1">Check-in</label>
            <input type="date" v-model="checkInDate" :min="todayDate" class="bg-transparent text-sm font-semibold text-slate-700 outline-none border-none cursor-pointer" />
          </div>
          <!-- Check-out -->
          <div class="flex-1 flex flex-col px-4 py-2 border-b md:border-b-0 md:border-r border-surface-border">
            <label class="text-xs font-bold text-slate-400 uppercase tracking-wide mb-1">Check-out</label>
            <input type="date" v-model="checkOutDate" :min="checkInDate || todayDate" class="bg-transparent text-sm font-semibold text-slate-700 outline-none border-none cursor-pointer" />
          </div>
          <!-- Guests -->
          <div class="flex-1 flex flex-col px-4 py-2 border-b md:border-b-0 md:border-r border-surface-border">
            <label class="text-xs font-bold text-slate-400 uppercase tracking-wide mb-1">Guests</label>
            <select v-model="guestCount" class="bg-transparent text-sm font-semibold text-slate-700 outline-none border-none cursor-pointer">
              <option v-for="n in 6" :key="n" :value="n">{{ n }} Guest{{ n > 1 ? 's' : '' }}</option>
            </select>
          </div>
          <!-- Search Button -->
          <button @click="triggerSearch" class="btn-accent px-8 py-3 rounded-lg whitespace-nowrap shrink-0 text-sm">
            <i class="pi pi-search mr-2"></i> Search
          </button>
        </div>

        <!-- Trust row -->
        <div class="flex items-center justify-center gap-3 mt-6 text-sm text-slate-400 flex-wrap">
          <span class="flex items-center gap-1.5"><i class="pi pi-check-circle text-accent"></i> No booking fees</span>
          <span class="text-slate-300">·</span>
          <span class="flex items-center gap-1.5"><i class="pi pi-check-circle text-accent"></i> Verified properties</span>
          <span class="text-slate-300">·</span>
          <span class="flex items-center gap-1.5"><i class="pi pi-check-circle text-accent"></i> Instant confirmation</span>
        </div>
      </div>
    </header>

    <!-- DESTINATIONS -->
    <section class="max-w-content mx-auto px-6 py-16">
      <h2 class="section-title mb-8">Explore by City</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div
          v-for="destination in destinationList"
          :key="destination.name"
          class="relative rounded-lg overflow-hidden cursor-pointer group aspect-[4/5]"
          @click="selectTrendingCity(destination.name)"
        >
          <img :src="destination.image" :alt="destination.name" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/10 to-transparent"></div>
          <div class="absolute bottom-0 left-0 p-4">
            <h3 class="text-white font-bold text-lg leading-tight">{{ destination.name }}</h3>
            <p class="text-white/70 text-sm font-medium">{{ destination.count }} Properties</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURED STAYS -->
    <section class="max-w-content mx-auto px-6 pb-16">
      <div class="flex items-end justify-between mb-8">
        <h2 class="section-title">Featured Stays</h2>
        <router-link to="/apartments" class="text-sm font-semibold text-accent hover:text-accent-hover transition-colors duration-150 no-underline">
          View all →
        </router-link>
      </div>

      <!-- Skeleton -->
      <div v-if="apartmentsStore.loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="i in 3" :key="i" class="bg-white rounded-lg border border-surface-border overflow-hidden">
          <div class="aspect-[4/3] bg-slate-100 animate-pulse"></div>
          <div class="p-4 flex flex-col gap-3">
            <div class="h-3 bg-slate-100 rounded animate-pulse w-1/3"></div>
            <div class="h-4 bg-slate-100 rounded animate-pulse w-3/4"></div>
            <div class="h-3 bg-slate-100 rounded animate-pulse w-full"></div>
          </div>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ApartmentCard
          v-for="apartment in apartmentsStore.featuredApartments"
          :key="apartment.id"
          :apartment="apartment"
        />
      </div>

      <div v-if="!apartmentsStore.loading && apartmentsStore.featuredApartments.length === 0" class="text-center py-16 text-slate-400">
        <p class="text-4xl mb-4">🏠</p>
        <p class="font-semibold">No featured stays yet — check back soon.</p>
      </div>
    </section>

    <!-- WHY APARTEX -->
    <section class="bg-surface-alt border-y border-surface-border py-16">
      <div class="max-w-content mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="perk in perks" :key="perk.title" class="flex flex-col items-start gap-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center bg-accent-light">
              <i :class="perk.icon" class="text-accent text-xl"></i>
            </div>
            <div>
              <h3 class="font-bold text-slate-800 text-lg mb-1">{{ perk.title }}</h3>
              <p class="text-slate-500 text-sm leading-relaxed">{{ perk.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- LOYALTY TEASER -->
    <section class="max-w-content mx-auto px-6 py-16">
      <div class="bg-navy rounded-2xl p-10 md:p-16 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <!-- Text -->
        <div>
          <span class="text-xs font-bold uppercase tracking-widest text-accent mb-3 block">Apartex Club</span>
          <h2 class="text-3xl md:text-4xl font-black text-white tracking-tight mb-4">Earn Rewards With Every Stay</h2>
          <p class="text-white/60 text-base leading-relaxed mb-6">
            Every night you book earns points. Redeem them for free stays, upgrades, and cashback.
          </p>
          <ul class="flex flex-col gap-3 mb-8">
            <li class="flex items-center gap-3 text-white/80 text-sm font-medium">
              <i class="pi pi-check-circle text-accent"></i>
              Earn points on every night spent
            </li>
            <li class="flex items-center gap-3 text-white/80 text-sm font-medium">
              <i class="pi pi-check-circle text-accent"></i>
              Redeem rewards for discount bookings
            </li>
            <li class="flex items-center gap-3 text-white/80 text-sm font-medium">
              <i class="pi pi-check-circle text-accent"></i>
              Bronze → Silver → Gold tier benefits
            </li>
          </ul>
          <router-link to="/loyalty" class="inline-flex items-center gap-2 bg-accent text-white font-semibold px-6 py-3 rounded-full text-sm hover:bg-accent-hover transition-colors duration-150 no-underline">
            View Loyalty Perks <i class="pi pi-star-fill text-xs"></i>
          </router-link>
        </div>
        <!-- Loyalty Card mockup -->
        <div class="flex justify-center">
          <div class="w-full max-w-sm bg-gradient-to-br from-navy-700 to-slate-900 border border-white/10 rounded-2xl p-7 relative overflow-hidden shadow-2xl">
            <div class="absolute top-0 right-0 w-48 h-48 bg-accent/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
            <div class="relative z-10">
              <div class="flex justify-between items-start mb-8">
                <div>
                  <p class="text-white/40 text-xs font-bold uppercase tracking-widest">Apartex Club</p>
                  <p class="text-2xl font-black bg-gradient-to-r from-yellow-300 to-yellow-500 bg-clip-text text-transparent mt-1">GOLD TIER</p>
                </div>
                <span class="bg-yellow-400/10 border border-yellow-400/20 text-yellow-400 text-xs font-black px-2.5 py-1 rounded-md">VIP</span>
              </div>
              <div class="mb-6">
                <p class="text-white/40 text-xs uppercase tracking-widest mb-1">Card Holder</p>
                <p class="text-white font-bold text-lg">Demo Traveler</p>
              </div>
              <div>
                <p class="text-white/40 text-xs uppercase tracking-widest mb-1">Points Balance</p>
                <p class="text-white font-black text-2xl">4,250 <span class="text-sm font-medium text-white/50">PTS</span></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TESTIMONIALS -->
    <section class="bg-surface-alt border-t border-surface-border py-16">
      <div class="max-w-content mx-auto px-6">
        <div class="text-center mb-10">
          <span class="section-tag">Traveler Stories</span>
          <h2 class="section-title">Loved by Guests</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="review in reviews" :key="review.author" class="bg-white rounded-lg border border-surface-border p-6 shadow-sm flex flex-col gap-4">
            <div class="flex gap-0.5">
              <i v-for="s in 5" :key="s" class="pi pi-star-fill text-accent text-sm"></i>
            </div>
            <p class="text-slate-600 text-sm leading-relaxed italic flex-1">"{{ review.text }}"</p>
            <div class="flex items-center gap-3 pt-3 border-t border-surface-border">
              <div class="w-9 h-9 rounded-full bg-navy-light flex items-center justify-center text-navy font-bold text-sm shrink-0">
                {{ review.initials }}
              </div>
              <div>
                <p class="font-bold text-sm text-slate-800">{{ review.author }}</p>
                <p class="text-xs text-slate-400 flex items-center gap-1"><i class="pi pi-shield-check text-green-500"></i> Verified Guest</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-surface-border">
      <div class="max-w-content mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-4 gap-10">
        <div class="col-span-1">
          <h2 class="text-lg font-black text-navy mb-3">APARTEX</h2>
          <p class="text-sm text-slate-400 leading-relaxed mb-5">Redefining accommodation booking across Zambia with handpicked, verified properties.</p>
          <div class="flex gap-3">
            <a href="#" class="w-9 h-9 rounded-full border border-surface-border flex items-center justify-center text-slate-400 hover:border-accent hover:text-accent transition-colors duration-150"><i class="pi pi-facebook text-sm"></i></a>
            <a href="#" class="w-9 h-9 rounded-full border border-surface-border flex items-center justify-center text-slate-400 hover:border-accent hover:text-accent transition-colors duration-150"><i class="pi pi-twitter text-sm"></i></a>
            <a href="#" class="w-9 h-9 rounded-full border border-surface-border flex items-center justify-center text-slate-400 hover:border-accent hover:text-accent transition-colors duration-150"><i class="pi pi-instagram text-sm"></i></a>
          </div>
        </div>
        <div>
          <h3 class="text-xs font-bold uppercase tracking-widest text-slate-500 mb-4">Quick Links</h3>
          <ul class="flex flex-col gap-2.5">
            <li><router-link to="/" class="text-sm text-slate-500 hover:text-accent no-underline transition-colors duration-150">Home</router-link></li>
            <li><router-link to="/apartments" class="text-sm text-slate-500 hover:text-accent no-underline transition-colors duration-150">Explore Stays</router-link></li>
            <li><router-link to="/bookings" class="text-sm text-slate-500 hover:text-accent no-underline transition-colors duration-150">Reservations</router-link></li>
            <li><router-link to="/loyalty" class="text-sm text-slate-500 hover:text-accent no-underline transition-colors duration-150">Loyalty Club</router-link></li>
          </ul>
        </div>
        <div>
          <h3 class="text-xs font-bold uppercase tracking-widest text-slate-500 mb-4">Destinations</h3>
          <ul class="flex flex-col gap-2.5">
            <li><a href="#" @click.prevent="selectTrendingCity('Lusaka')" class="text-sm text-slate-500 hover:text-accent no-underline transition-colors duration-150">Lusaka</a></li>
            <li><a href="#" @click.prevent="selectTrendingCity('Livingstone')" class="text-sm text-slate-500 hover:text-accent no-underline transition-colors duration-150">Livingstone</a></li>
            <li><a href="#" @click.prevent="selectTrendingCity('Ndola')" class="text-sm text-slate-500 hover:text-accent no-underline transition-colors duration-150">Ndola</a></li>
            <li><a href="#" @click.prevent="selectTrendingCity('Kitwe')" class="text-sm text-slate-500 hover:text-accent no-underline transition-colors duration-150">Kitwe</a></li>
          </ul>
        </div>
        <div>
          <h3 class="text-xs font-bold uppercase tracking-widest text-slate-500 mb-4">Newsletter</h3>
          <p class="text-sm text-slate-400 leading-relaxed mb-4">Stay updated on premium properties and exclusive offers.</p>
          <div class="flex gap-2">
            <input type="email" placeholder="Your email" class="input-base !py-2" />
            <button class="btn-accent shrink-0">Subscribe</button>
          </div>
        </div>
      </div>
      <div class="border-t border-surface-border">
        <div class="max-w-content mx-auto px-6 py-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <p class="text-xs text-slate-400">&copy; 2026 Apartex Inc. All rights reserved.</p>
          <div class="flex gap-4">
            <a href="#" class="text-xs text-slate-400 hover:text-accent no-underline">Privacy Policy</a>
            <a href="#" class="text-xs text-slate-400 hover:text-accent no-underline">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import ApartmentCard from '@/components/ApartmentCard.vue';

const router = useRouter();
const apartmentsStore = useApartmentsStore();

// Search state
const selectedCity = ref('');
const checkInDate = ref('');
const checkOutDate = ref('');
const guestCount = ref(1);

const todayDate = new Date().toISOString().split('T')[0];

const tabs = [
  { id: 'stays', label: 'Stays', icon: 'pi pi-home' },
  { id: 'experiences', label: 'Experiences', icon: 'pi pi-compass' },
  { id: 'long-term', label: 'Monthly Stay', icon: 'pi pi-calendar' }
];
const activeTab = ref('stays');

const cities = ['Lusaka', 'Livingstone', 'Ndola', 'Kitwe'];

const destinationList = [
  { name: 'Lusaka', count: '12', image: 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=400&q=80' },
  { name: 'Livingstone', count: '8', image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=400&q=80' },
  { name: 'Ndola', count: '6', image: 'https://images.unsplash.com/photo-1449034446853-66c86144b0ad?auto=format&fit=crop&w=400&q=80' },
  { name: 'Kitwe', count: '4', image: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=400&q=80' }
];

const perks = [
  {
    title: 'Inspected Properties',
    description: 'Every apartment is hand-selected and verified for amenities, hygiene, and comfort.',
    icon: 'pi pi-shield'
  },
  {
    title: 'Zero Booking Fees',
    description: 'Direct bookings with no hidden service charges. Best price guaranteed.',
    icon: 'pi pi-wallet'
  },
  {
    title: 'VIP Loyalty Program',
    description: 'Accumulate reward points with every night stay and redeem free stays/payout benefits.',
    icon: 'pi pi-star'
  }
];

const reviews = [
  {
    text: 'Apartex completely transformed our travel experience. The luxury apartment in Lusaka was gorgeous, clean, and checked in flawlessly. Highly recommend the VIP loyalty club!',
    author: 'Sharon Phiri',
    initials: 'SP'
  },
  {
    text: 'Best booking system I have used. Clean user interface, zero unexpected fees, and outstanding support. Our riverside cottage was beyond expectations.',
    author: 'Mwansa Kabwe',
    initials: 'MK'
  },
  {
    text: 'The gold tier benefits are real. Redeeemed points for our second booking. Quick, seamless, and luxurious properties.',
    author: 'Daniel Zulu',
    initials: 'DZ'
  }
];

onMounted(async () => {
  if (apartmentsStore.apartments.length === 0) {
    await apartmentsStore.fetchApartments();
  }
});

const triggerSearch = () => {
  const query = {};
  if (selectedCity.value) query.city = selectedCity.value;
  if (guestCount.value) query.capacity = guestCount.value;
  
  router.push({
    path: '/apartments',
    query
  });
};

const selectTrendingCity = (cityName) => {
  router.push({
    path: '/apartments',
    query: { city: cityName }
  });
};

const viewApartmentDetail = (id) => {
  router.push(`/apartments/${id}`);
};
</script>