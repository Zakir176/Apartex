<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 font-sans antialiased pb-16">
    
    <!-- 1. Hero Section & Integrated Search Bar -->
    <section class="relative bg-slate-900 text-white pt-12 pb-20 px-4 sm:px-6 lg:px-8 overflow-hidden rounded-b-[2.5rem] shadow-2xl">
      <!-- Decorative Backdrop Effects -->
      <div class="absolute inset-0 opacity-20 bg-[radial-gradient(#f97316_1px,transparent_1px)] [background-size:24px_24px]"></div>

      <div class="max-w-5xl mx-auto relative z-10 text-center">
        <!-- Trust Badge -->
        <span class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 border border-white/20 backdrop-blur-md text-orange-300 text-xs font-black uppercase tracking-widest mb-6 shadow-sm">
          <i class="pi pi-shield text-xs"></i> Premier Stay & Accommodation Network
        </span>

        <!-- Hero Headline -->
        <h1 class="text-3xl sm:text-5xl lg:text-6xl font-black text-white tracking-tight leading-tight mb-4">
          Find Your Perfect Stay Across <br class="hidden sm:inline" />
          <span class="bg-gradient-to-r from-orange-400 via-amber-300 to-yellow-400 bg-clip-text text-transparent">
            Zambia & Beyond
          </span>
        </h1>
        
        <p class="text-sm sm:text-lg text-slate-300 max-w-2xl mx-auto font-medium leading-relaxed mb-10">
          Book verified luxury apartments, boutique hotels, and lodges with zero hidden fees. Instant Mobile Money & card payments.
        </p>

        <!-- Integrated Search Bar Pill -->
        <div class="bg-white/95 backdrop-blur-2xl p-3 sm:p-4 rounded-3xl sm:rounded-full shadow-2xl border border-white/40 max-w-4xl mx-auto text-slate-900 grid grid-cols-1 sm:grid-cols-12 gap-3 items-center">
          
          <!-- Destination Input -->
          <div class="sm:col-span-4 text-left px-3 py-1 sm:border-r border-slate-200">
            <label class="block text-[10px] font-black uppercase tracking-widest text-slate-400 mb-0.5">Destination</label>
            <div class="flex items-center gap-2">
              <i class="pi pi-map-marker text-accent text-sm"></i>
              <input
                type="text"
                v-model="searchLocation"
                placeholder="Lusaka, Livingstone, Ndola..."
                class="w-full bg-transparent text-xs font-bold text-slate-800 focus:outline-none placeholder:text-slate-400"
              />
            </div>
          </div>

          <!-- Accommodation Type -->
          <div class="sm:col-span-3 text-left px-3 py-1 sm:border-r border-slate-200">
            <label class="block text-[10px] font-black uppercase tracking-widest text-slate-400 mb-0.5">Stay Type</label>
            <select
              v-model="searchType"
              class="w-full bg-transparent text-xs font-bold text-slate-800 focus:outline-none cursor-pointer border-0 p-0"
            >
              <option value="">All Stays</option>
              <option value="apartment">Apartments</option>
              <option value="hotel">Hotels</option>
              <option value="lodge">Lodges</option>
            </select>
          </div>

          <!-- Guests Selector -->
          <div class="sm:col-span-3 text-left px-3 py-1">
            <label class="block text-[10px] font-black uppercase tracking-widest text-slate-400 mb-0.5">Guests</label>
            <div class="flex items-center gap-2">
              <i class="pi pi-users text-slate-400 text-sm"></i>
              <select
                v-model.number="searchGuests"
                class="w-full bg-transparent text-xs font-bold text-slate-800 focus:outline-none cursor-pointer border-0 p-0"
              >
                <option :value="1">1 Guest</option>
                <option :value="2">2 Guests</option>
                <option :value="4">4+ Guests</option>
              </select>
            </div>
          </div>

          <!-- Search CTA Button -->
          <div class="sm:col-span-2">
            <button
              @click="executeSearch"
              class="w-full btn-accent py-3.5 px-4 rounded-2xl sm:rounded-full text-xs font-black tracking-wider uppercase hover:scale-105 transition-all flex items-center justify-center gap-1.5 cursor-pointer border-0"
            >
              <i class="pi pi-search text-xs"></i>
              <span>Search</span>
            </button>
          </div>

        </div>
      </div>
    </section>

    <!-- Main Homepage Flow Container -->
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 space-y-20 mt-16">
      
      <!-- 3. Featured Properties Preview Section -->
      <section>
        <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
          <div>
            <span class="text-xs font-black text-accent uppercase tracking-widest bg-orange-50 px-3 py-1 rounded-full border border-orange-100">Handpicked Stays</span>
            <h2 class="text-2xl sm:text-4xl font-black text-slate-900 mt-2">Featured Accommodations</h2>
          </div>
          <router-link to="/apartments" class="text-xs font-black text-accent hover:text-accent-hover flex items-center gap-1.5 no-underline group">
            <span>Explore All Stays ({{ featuredApartments.length }})</span>
            <i class="pi pi-arrow-right text-xs group-hover:translate-x-1 transition-transform"></i>
          </router-link>
        </div>

        <div v-if="apartmentsStore.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="n in 4" :key="n" class="bg-white rounded-2xl p-4 border border-slate-200 animate-pulse space-y-3">
            <div class="h-44 bg-slate-200 rounded-xl"></div>
            <div class="h-4 bg-slate-200 rounded w-3/4"></div>
            <div class="h-4 bg-slate-200 rounded w-1/2"></div>
          </div>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <ApartmentCard
            v-for="apt in displayedFeatured"
            :key="apt.id"
            :apartment="apt"
            :isWishlisted="isWishlisted(apt.id)"
            @toggle-wishlist="handleWishlistToggle"
          />
        </div>
      </section>

      <!-- 4. Why Choose Apartex Section -->
      <section id="why-apartex" class="bg-white border border-slate-200/80 rounded-3xl p-6 sm:p-12 shadow-xl">
        <div class="text-center max-w-2xl mx-auto mb-12">
          <span class="text-xs font-black text-blue-600 uppercase tracking-widest bg-blue-50 px-3 py-1 rounded-full border border-blue-100">Platform Excellence</span>
          <h2 class="text-2xl sm:text-4xl font-black text-slate-900 mt-3 mb-2">Why Choose Apartex?</h2>
          <p class="text-sm text-slate-600 font-medium">Designed for seamless travel and property management across Zambia.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="flex flex-col items-start p-6 bg-slate-50 rounded-2xl border border-slate-100">
            <div class="w-12 h-12 rounded-2xl bg-orange-100 text-accent flex items-center justify-center text-xl font-black mb-4">
              <i class="pi pi-check-circle"></i>
            </div>
            <h3 class="text-base font-black text-slate-900 mb-2">Verified Listings & Real Photos</h3>
            <p class="text-xs text-slate-600 font-medium leading-relaxed">Every property on Apartex undergoes strict verification to guarantee accurate descriptions, amenities, and location accuracy.</p>
          </div>

          <div class="flex flex-col items-start p-6 bg-slate-50 rounded-2xl border border-slate-100">
            <div class="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-600 flex items-center justify-center text-xl font-black mb-4">
              <i class="pi pi-mobile"></i>
            </div>
            <h3 class="text-base font-black text-slate-900 mb-2">Instant Mobile Money Payments</h3>
            <p class="text-xs text-slate-600 font-medium leading-relaxed">Pay seamlessly using MTN Mobile Money, Airtel Money, Zamtel, or credit cards with zero booking markups.</p>
          </div>

          <div class="flex flex-col items-start p-6 bg-slate-50 rounded-2xl border border-slate-100">
            <div class="w-12 h-12 rounded-2xl bg-purple-100 text-purple-600 flex items-center justify-center text-xl font-black mb-4">
              <i class="pi pi-shield"></i>
            </div>
            <h3 class="text-base font-black text-slate-900 mb-2">24/7 Guest & Host Protection</h3>
            <p class="text-xs text-slate-600 font-medium leading-relaxed">Enjoy peace of mind with 100% refund coverage for cancellations and dedicated concierge support.</p>
          </div>
        </div>
      </section>

      <!-- 5. Popular Destinations Grid Section -->
      <section id="destinations">
        <div class="flex items-center justify-between mb-8">
          <div>
            <span class="text-xs font-black text-emerald-600 uppercase tracking-widest bg-emerald-50 px-3 py-1 rounded-full border border-emerald-100">Zambian Hubs</span>
            <h2 class="text-2xl sm:text-4xl font-black text-slate-900 mt-2">Popular Destinations</h2>
          </div>
          <router-link to="/apartments" class="text-xs font-black text-accent hover:text-accent-hover flex items-center gap-1.5 no-underline">
            <span>View All</span>
            <i class="pi pi-arrow-right text-xs"></i>
          </router-link>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
          <div
            v-for="dest in popularDestinations"
            :key="dest.name"
            @click="filterByCity(dest.name)"
            class="relative rounded-3xl overflow-hidden aspect-[4/5] cursor-pointer group shadow-md hover:shadow-2xl transition-all duration-300"
          >
            <img :src="dest.image" :alt="dest.name" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700">
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/85 via-slate-900/30 to-transparent"></div>
            
            <div class="absolute bottom-4 left-4 right-4 text-white">
              <h3 class="text-lg font-black text-white mb-0.5 tracking-tight">{{ dest.name }}</h3>
              <p class="text-[11px] font-bold text-orange-300 uppercase tracking-wider">{{ dest.stays }} Verified Stays</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 6. Become a Host & Earnings Estimator Preview -->
      <section id="host-calculator" class="bg-navy text-white rounded-3xl p-6 sm:p-12 shadow-2xl relative overflow-hidden">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
          <div class="lg:col-span-7 space-y-4">
            <span class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/20 border border-accent/30 text-accent text-xs font-black uppercase tracking-widest">
              <i class="pi pi-calculator text-xs"></i> Host Calculator
            </span>
            <h2 class="text-2xl sm:text-4xl font-black text-white leading-tight">
              Turn Your Property Into <br />
              <span class="text-orange-400">Monthly Revenue</span>
            </h2>
            <p class="text-xs sm:text-sm text-slate-200 font-medium leading-relaxed max-w-xl">
              Got an apartment, hotel, or lodge? List for free on Apartex and reach thousands of guests with direct Mobile Money payouts.
            </p>

            <div class="pt-4 flex flex-wrap gap-4">
              <router-link to="/host" class="btn-accent text-xs font-black px-6 py-3.5 rounded-full no-underline inline-flex items-center gap-2">
                <span>Use Full Calculator</span>
                <i class="pi pi-arrow-right text-xs"></i>
              </router-link>
              <router-link to="/register?role=owner" class="px-6 py-3.5 rounded-full border border-white/20 hover:bg-white/10 text-white font-bold text-xs no-underline">
                List Property
              </router-link>
            </div>
          </div>

          <div class="lg:col-span-5 bg-white/10 border border-white/15 rounded-3xl p-6 text-center space-y-4">
            <span class="text-[10px] font-black uppercase tracking-widest text-slate-200">Estimated Monthly Earnings</span>
            <div class="text-3xl sm:text-4xl font-black text-white">
              {{ currencyStore.formatPrice(1450) }}
            </div>
            <p class="text-xs text-slate-200 font-medium">Based on 2 units at $80/night & 18 days occupancy/month.</p>
            <div class="h-px bg-white/10 my-2"></div>
            <div class="text-[11px] font-bold text-emerald-400 flex items-center justify-center gap-1.5">
              <i class="pi pi-check-circle"></i>
              <span class="text-emerald-300">Instant Payouts to MTN & Airtel Money</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 7. Guest Testimonials Section -->
      <section>
        <div class="text-center max-w-2xl mx-auto mb-10">
          <span class="text-xs font-black text-purple-600 uppercase tracking-widest bg-purple-50 px-3 py-1 rounded-full border border-purple-100">Guest Feedback</span>
          <h2 class="text-2xl sm:text-4xl font-black text-slate-900 mt-2">Loved by Travelers</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div v-for="t in testimonials" :key="t.author" class="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm flex flex-col justify-between">
            <div class="space-y-3">
              <div class="flex text-amber-400 text-xs">
                <i v-for="s in 5" :key="s" class="pi pi-star-fill"></i>
              </div>
              <p class="text-xs text-slate-700 font-medium leading-relaxed italic">"{{ t.quote }}"</p>
            </div>
            <div class="mt-6 pt-4 border-t border-slate-100 flex items-center gap-3">
              <div class="w-9 h-9 rounded-full bg-navy text-white font-black text-xs flex items-center justify-center uppercase">
                {{ t.author.charAt(0) }}
              </div>
              <div>
                <h4 class="text-xs font-black text-slate-900">{{ t.author }}</h4>
                <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">{{ t.location }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 8. FAQ Accordion Section -->
      <section id="faq" class="bg-white border border-slate-200/80 rounded-3xl p-6 sm:p-12 shadow-xl">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between mb-8 gap-4">
          <div>
            <span class="text-xs font-black text-accent uppercase tracking-widest bg-orange-50 px-3 py-1 rounded-full border border-orange-100">Common Questions</span>
            <h2 class="text-2xl sm:text-4xl font-black text-slate-900 mt-2">Frequently Asked Questions</h2>
          </div>
          <router-link to="/help" class="text-xs font-black text-accent hover:text-accent-hover flex items-center gap-1.5 no-underline">
            <span>View Help Center</span>
            <i class="pi pi-arrow-right text-xs"></i>
          </router-link>
        </div>

        <div class="space-y-3">
          <div
            v-for="(faq, idx) in previewFaqs"
            :key="idx"
            class="border border-slate-100 rounded-2xl overflow-hidden"
          >
            <button
              @click="openFaq = openFaq === idx ? null : idx"
              class="w-full text-left p-5 flex items-center justify-between font-extrabold text-sm text-slate-800 hover:text-accent transition-colors bg-transparent border-0 cursor-pointer"
            >
              <span>{{ faq.q }}</span>
              <i :class="openFaq === idx ? 'pi pi-chevron-up text-accent' : 'pi pi-chevron-down text-slate-400'" class="text-xs"></i>
            </button>
            <div v-show="openFaq === idx" class="px-5 pb-5 pt-1 text-xs text-slate-600 font-medium leading-relaxed border-t border-slate-50 bg-slate-50/50">
              {{ faq.a }}
            </div>
          </div>
        </div>
      </section>

    </div>

    <!-- 9. Comprehensive Footer -->
    <footer class="mt-24 border-t border-slate-200 bg-white pt-16 pb-12 text-slate-600">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
        <div class="col-span-2 space-y-4">
          <router-link to="/" class="flex items-center gap-2 text-xl font-black text-navy no-underline">
            <img src="/logo.svg" alt="Apartex Logo" class="w-8 h-8 rounded-xl shadow-sm" />
            <span class="tracking-wider text-slate-900 font-black text-base">APARTEX</span>
          </router-link>
          <p class="text-xs text-slate-500 font-medium max-w-sm leading-relaxed">
            Zambia's premier online accommodation platform for apartments, boutique hotels, and lodges. Enjoy direct Mobile Money payouts and zero hidden booking markups.
          </p>
        </div>

        <div>
          <h4 class="text-xs font-black uppercase tracking-wider text-slate-900 mb-4">For Guests</h4>
          <ul class="space-y-2.5 text-xs font-bold list-none p-0 m-0">
            <li><router-link to="/apartments" class="text-slate-600 hover:text-accent no-underline">Browse Stays</router-link></li>
            <li><router-link to="/apartments?type=hotel" class="text-slate-600 hover:text-accent no-underline">Hotels in Lusaka</router-link></li>
            <li><router-link to="/apartments?type=lodge" class="text-slate-600 hover:text-accent no-underline">Livingstone Lodges</router-link></li>
            <li><router-link to="/help" class="text-slate-600 hover:text-accent no-underline">Guest FAQs</router-link></li>
          </ul>
        </div>

        <div>
          <h4 class="text-xs font-black uppercase tracking-wider text-slate-900 mb-4">For Hosts</h4>
          <ul class="space-y-2.5 text-xs font-bold list-none p-0 m-0">
            <li><router-link to="/host" class="text-slate-600 hover:text-accent no-underline">Become a Host</router-link></li>
            <li><router-link to="/host#host-calculator" class="text-slate-600 hover:text-accent no-underline">Earnings Calculator</router-link></li>
            <li><router-link to="/register?role=owner" class="text-slate-600 hover:text-accent no-underline">List Property</router-link></li>
            <li><router-link to="/owner/login" class="text-slate-600 hover:text-accent no-underline">Host Login</router-link></li>
          </ul>
        </div>

        <div>
          <h4 class="text-xs font-black uppercase tracking-wider text-slate-900 mb-4">Company</h4>
          <ul class="space-y-2.5 text-xs font-bold list-none p-0 m-0">
            <li><router-link to="/help" class="text-slate-600 hover:text-accent no-underline">About Us</router-link></li>
            <li><router-link to="/help" class="text-slate-600 hover:text-accent no-underline">Trust & Safety</router-link></li>
            <li><router-link to="/help" class="text-slate-600 hover:text-accent no-underline">Help Center</router-link></li>
            <li><a href="mailto:support@apartex.com" class="text-slate-600 hover:text-accent no-underline">Contact Support</a></li>
          </ul>
        </div>
      </div>

      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-slate-100 pt-6 flex flex-col sm:flex-row items-center justify-between text-xs font-bold text-slate-400 gap-4">
        <p>© 2026 Apartex Technologies Inc. All rights reserved.</p>
        <div class="flex items-center gap-4">
          <span>MTN Mobile Money</span>
          <span>•</span>
          <span>Airtel Money</span>
          <span>•</span>
          <span>Visa / Mastercard</span>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import { useWishlistStore } from '@/stores/wishlist';
import { useCurrencyStore } from '@/stores/currency';
import ApartmentCard from '@/components/ApartmentCard.vue';

const router = useRouter();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();
const currencyStore = useCurrencyStore();

const searchLocation = ref('');
const searchType = ref('');
const searchGuests = ref(1);

const openFaq = ref(0);

const featuredApartments = computed(() => apartmentsStore.apartments || []);
const displayedFeatured = computed(() => featuredApartments.value.slice(0, 4));

const popularDestinations = [
  { name: 'Lusaka', stays: '48+', image: 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=600&q=80' },
  { name: 'Livingstone', stays: '32+', image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80' },
  { name: 'Ndola', stays: '18+', image: 'https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=600&q=80' },
  { name: 'Solwezi', stays: '12+', image: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=600&q=80' }
];

const testimonials = [
  { quote: 'Booking our hotel room in Lusaka via Mobile Money was completely instant. No credit card hassles!', author: 'Chanda Mwansa', location: 'Lusaka' },
  { quote: 'As a lodge owner in Livingstone, Apartex allowed us to manage walk-in guests easily while receiving online bookings.', author: 'David Kasonde', location: 'Livingstone Host' },
  { quote: 'Clean, verified apartment with high-speed internet. Will definitely use Apartex for all my Zambian business trips.', author: 'Sarah Jenkins', location: 'London, UK' }
];

const previewFaqs = [
  { q: 'How do I pay for my stay on Apartex?', a: 'You can pay instantly using MTN Mobile Money, Airtel Money, Zamtel Kwacha, or credit card.' },
  { q: 'Can I view listings without creating an account?', a: 'Yes! All property listings, search filters, and host information are 100% public.' },
  { q: 'How do host payouts work for property owners?', a: 'Earnings are automatically transferred to your designated Mobile Money or bank account upon guest check-in.' }
];

onMounted(async () => {
  await apartmentsStore.fetchApartments();
});

const executeSearch = () => {
  router.push({
    path: '/apartments',
    query: {
      city: searchLocation.value,
      type: searchType.value,
      guests: searchGuests.value
    }
  });
};

const filterByCity = (cityName) => {
  router.push({
    path: '/apartments',
    query: { city: cityName }
  });
};

const isWishlisted = (apartmentId) => {
  return wishlistStore.wishlistItems.some(i => i.apartment_id === apartmentId);
};

const handleWishlistToggle = (apartmentId, newState) => {
  // Store handles state
};
</script>
