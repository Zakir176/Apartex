<template>
  <div class="min-h-screen bg-[#F8F7F4] text-slate-900 overflow-x-hidden selection:bg-accent selection:text-white">

    <!-- HERO SECTION -->
    <header class="bg-animated-mesh relative pt-12 pb-28 lg:pt-20 lg:pb-36 overflow-hidden border-b border-surface-border">
      <!-- Floating Background Glow Orbs -->
      <div class="absolute top-1/4 left-10 w-72 h-72 bg-accent/15 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
      <div class="absolute bottom-10 right-10 w-96 h-96 bg-navy/15 rounded-full blur-3xl pointer-events-none"></div>

      <div class="max-w-content mx-auto px-4 sm:px-6 relative z-10">
        
        <!-- Live Tag Badge -->
        <div class="flex justify-center mb-8">
          <div class="inline-flex items-center gap-3 px-5 py-2.5 rounded-full bg-white/90 backdrop-blur-xl border border-surface-border shadow-sm text-xs sm:text-sm font-extrabold text-slate-800 hover:scale-105 transition-transform duration-300">
            <span class="flex h-3 w-3 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-accent"></span>
            </span>
            <span>✨ Introducing Apartex 2.0 Ecosystem</span>
            <span class="text-slate-300">|</span>
            <span class="text-accent font-black">Zero Hidden Booking Fees</span>
          </div>
        </div>

        <!-- Hero Headline & Subtitle -->
        <div class="text-center max-w-4xl mx-auto mb-12">
          <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-[1.06] mb-6 text-slate-900">
            The Luxury Ecosystem for<br class="hidden sm:block" />
            <span class="text-gradient">Accommodation Across Zambia</span>
          </h1>
          <p class="text-base sm:text-xl text-slate-600 font-medium max-w-2xl mx-auto leading-relaxed">
            Connecting discerning travelers with handpicked executive apartments, safari lodges & urban retreats. Guaranteed best prices with zero service markups.
          </p>

          <!-- Primary CTAs -->
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mt-10">
            <router-link 
              to="/register" 
              class="btn-accent text-base sm:text-lg font-black px-9 py-4 rounded-full shadow-accent hover:scale-105 transition-all duration-200 no-underline w-full sm:w-auto flex items-center justify-center gap-2"
            >
              <span>Explore & Book Stays</span>
              <i class="pi pi-arrow-right text-sm"></i>
            </router-link>

            <router-link 
              to="/register?role=owner" 
              class="btn-outline text-base sm:text-lg font-black px-9 py-4 rounded-full hover:bg-slate-50 hover:scale-105 transition-all duration-200 no-underline w-full sm:w-auto flex items-center justify-center gap-2 border-slate-300"
            >
              <i class="pi pi-building text-accent"></i>
              <span>List Your Property</span>
            </router-link>
          </div>
        </div>

        <!-- Animated Hero Showcase Card Stack -->
        <div class="max-w-5xl mx-auto relative mt-8">
          <!-- Glassmorphism Container -->
          <div class="glass-card rounded-3xl p-4 sm:p-8 shadow-2xl border border-surface-border relative z-10">
            
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              <!-- Left Preview Image -->
              <div class="lg:col-span-7 relative group overflow-hidden rounded-2xl aspect-[16/10]">
                <img 
                  src="https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80" 
                  alt="Lusaka Penthouse" 
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" 
                />
                <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-950/20 to-transparent"></div>
                
                <div class="absolute bottom-6 left-6 right-6 text-white z-10">
                  <span class="bg-accent text-white text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full inline-block mb-2">Featured Suite</span>
                  <h3 class="text-2xl font-black leading-snug">The Rhodes Park Executive Penthouse</h3>
                  <p class="text-xs text-slate-300 font-medium mt-1 flex items-center gap-2">
                    <i class="pi pi-map-marker text-accent"></i> Lusaka, Zambia · 3 Bedrooms · Solar Backup · Private Pool
                  </p>
                </div>
              </div>

              <!-- Right Floating Interactive Stats -->
              <div class="lg:col-span-5 flex flex-col gap-4">
                <div class="bg-white p-5 rounded-2xl border border-surface-border shadow-sm">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Direct Host Price</span>
                    <span class="text-xs font-extrabold text-emerald-600 bg-emerald-50 px-2.5 py-0.5 rounded-full">Save 18%</span>
                  </div>
                  <p class="text-3xl font-black text-slate-900">$125 <span class="text-xs font-medium text-slate-400">/ night</span></p>
                </div>

                <div class="bg-navy text-white p-5 rounded-2xl shadow-md">
                  <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-accent uppercase tracking-wider">Apartex Club VIP</span>
                    <i class="pi pi-star-fill text-amber-300 text-sm"></i>
                  </div>
                  <p class="text-lg font-black">+625 Loyalty Points</p>
                  <p class="text-xs text-white/70 mt-1">Earn free night vouchers & airport shuttle perks.</p>
                </div>

                <div class="bg-slate-50 p-5 rounded-2xl border border-surface-border flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full bg-emerald-100 text-emerald-700 font-black flex items-center justify-center">
                      <i class="pi pi-shield-check text-lg"></i>
                    </div>
                    <div>
                      <p class="text-xs font-bold text-slate-900">Verified Inspection</p>
                      <p class="text-[11px] text-slate-500">100% Hygiene & Wi-Fi Guarantee</p>
                    </div>
                  </div>
                  <span class="text-xs font-black text-emerald-600">PASSED</span>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- Quick Stats Counter Strip -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto mt-16 text-center">
          <div class="p-4">
            <p class="text-3xl sm:text-4xl font-black text-navy">1,200+</p>
            <p class="text-xs sm:text-sm text-slate-500 font-bold mt-1">Verified Properties</p>
          </div>
          <div class="p-4">
            <p class="text-3xl sm:text-4xl font-black text-accent">4.92 ★</p>
            <p class="text-xs sm:text-sm text-slate-500 font-bold mt-1">Guest Satisfaction</p>
          </div>
          <div class="p-4">
            <p class="text-3xl sm:text-4xl font-black text-navy">100%</p>
            <p class="text-xs sm:text-sm text-slate-500 font-bold mt-1">Direct Host Payouts</p>
          </div>
          <div class="p-4">
            <p class="text-3xl sm:text-4xl font-black text-emerald-600">24/7</p>
            <p class="text-xs sm:text-sm text-slate-500 font-bold mt-1">Local VIP Concierge</p>
          </div>
        </div>

      </div>
    </header>

    <!-- PLATFORM PILLARS & FEATURES ("WHY APARTEX") -->
    <section class="max-w-content mx-auto px-4 sm:px-6 py-24">
      <div class="text-center max-w-3xl mx-auto mb-16">
        <span class="section-tag">Redefining Hospitality</span>
        <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-slate-900">
          Why Discriminating Travelers Choose Apartex
        </h2>
        <p class="text-slate-600 text-base sm:text-lg mt-3 font-medium">
          Engineered to replace outdated booking sites with transparency, speed, and luxury security.
        </p>
      </div>

      <!-- 4 Pillars Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div 
          v-for="(pillar, idx) in pillars" 
          :key="pillar.title"
          class="bg-white rounded-3xl p-8 border border-surface-border shadow-card hover:shadow-card-hover transition-all duration-300 hover:-translate-y-2 flex flex-col justify-between group"
        >
          <div>
            <div 
              class="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl mb-6 transition-transform group-hover:scale-110"
              :class="pillar.bg"
            >
              <i :class="[pillar.icon, pillar.color]"></i>
            </div>
            <h3 class="text-xl font-black text-slate-900 mb-3 group-hover:text-accent transition-colors">
              {{ pillar.title }}
            </h3>
            <p class="text-slate-500 text-sm leading-relaxed font-medium">
              {{ pillar.description }}
            </p>
          </div>

          <div class="mt-8 pt-4 border-t border-slate-100 flex items-center text-xs font-extrabold text-accent group-hover:translate-x-2 transition-transform">
            <span>Learn More</span>
            <i class="pi pi-arrow-right ml-2 text-[10px]"></i>
          </div>
        </div>
      </div>
    </section>

    <!-- INTERACTIVE HOW IT WORKS WORKFLOW -->
    <section class="bg-white border-y border-surface-border py-24">
      <div class="max-w-content mx-auto px-4 sm:px-6">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <span class="section-tag">Seamless Journey</span>
          <h2 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">How Apartex Works in 3 Simple Steps</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 relative">
          
          <div v-for="(step, i) in steps" :key="step.number" class="flex flex-col items-center text-center p-8 bg-slate-50 rounded-3xl border border-surface-border relative group hover:bg-white hover:shadow-xl transition-all duration-300">
            <span class="w-12 h-12 rounded-full bg-accent text-white font-black text-lg flex items-center justify-center mb-6 shadow-accent group-hover:scale-110 transition-transform">
              {{ step.number }}
            </span>
            <h3 class="text-xl font-black text-slate-900 mb-3">{{ step.title }}</h3>
            <p class="text-slate-500 text-sm font-medium leading-relaxed">{{ step.description }}</p>
          </div>

        </div>
      </div>
    </section>

    <!-- COMPARISON TABLE: APARTEX VS LEGACY PLATFORMS -->
    <section class="max-w-content mx-auto px-4 sm:px-6 py-24">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <span class="section-tag">Unmatched Advantage</span>
        <h2 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">Apartex vs Legacy Booking Sites</h2>
        <p class="text-slate-500 text-sm mt-2 font-medium">See how Apartex elevates every aspect of property discovery in Zambia.</p>
      </div>

      <div class="max-w-4xl mx-auto bg-white rounded-3xl border border-surface-border shadow-xl overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse min-w-[600px]">
            <thead>
              <tr class="bg-slate-900 text-white text-xs uppercase tracking-wider">
                <th class="py-5 px-6 font-black">Platform Feature</th>
                <th class="py-5 px-6 font-black text-amber-400 bg-navy">Apartex Platform</th>
                <th class="py-5 px-6 font-semibold text-slate-400">Traditional OTA Sites</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-surface-border text-sm font-medium text-slate-700">
              <tr v-for="row in comparisonRows" :key="row.feature" class="hover:bg-slate-50 transition-colors">
                <td class="py-4 px-6 font-bold text-slate-900">{{ row.feature }}</td>
                <td class="py-4 px-6 font-black text-accent bg-accent/5 flex items-center gap-2">
                  <i class="pi pi-check-circle text-emerald-500"></i> {{ row.apartex }}
                </td>
                <td class="py-4 px-6 text-slate-400 flex items-center gap-2">
                  <i class="pi pi-times-circle text-red-400"></i> {{ row.others }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- INTERACTIVE DESTINATION HIGHLIGHTS -->
    <section class="bg-slate-950 text-white py-24 relative overflow-hidden">
      <!-- Glow background -->
      <div class="absolute -top-32 -left-32 w-96 h-96 bg-accent/20 rounded-full blur-3xl pointer-events-none"></div>

      <div class="max-w-content mx-auto px-4 sm:px-6 relative z-10">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
          <div>
            <span class="text-xs font-black uppercase tracking-widest text-accent mb-2 block">Curated Locations</span>
            <h2 class="text-3xl sm:text-4xl font-black text-white tracking-tight">Explore Zambia's Finest Regions</h2>
          </div>
          <router-link to="/register" class="btn-accent font-extrabold text-sm px-6 py-3 no-underline shadow-accent">
            View All Stays →
          </router-link>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div 
            v-for="city in cityCards" 
            :key="city.name"
            class="group relative rounded-2xl overflow-hidden aspect-[3/4] flex flex-col justify-end p-6 border border-white/10 hover:border-accent/50 transition-all duration-500 cursor-pointer shadow-2xl"
          >
            <img :src="city.image" :alt="city.name" class="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950/95 via-slate-950/40 to-transparent"></div>
            
            <div class="relative z-10">
              <span class="text-[10px] font-black uppercase tracking-widest text-amber-300 block mb-1">{{ city.label }}</span>
              <h3 class="text-2xl font-black text-white group-hover:text-accent transition-colors">{{ city.name }}</h3>
              <p class="text-xs text-white/70 mt-1 line-clamp-2">{{ city.desc }}</p>
              <div class="mt-4 pt-3 border-t border-white/15 flex items-center justify-between text-xs font-bold text-accent">
                <span>{{ city.count }} Properties</span>
                <i class="pi pi-arrow-right group-hover:translate-x-1 transition-transform text-[10px]"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TESTIMONIALS & SOCIAL PROOF -->
    <section class="max-w-content mx-auto px-4 sm:px-6 py-24">
      <div class="text-center max-w-2xl mx-auto mb-16">
        <span class="section-tag">Verified Proof</span>
        <h2 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">Trusted by Travelers & Hosts</h2>
        <div class="flex items-center justify-center gap-2 mt-3 text-amber-400">
          <i v-for="s in 5" :key="s" class="pi pi-star-fill text-sm"></i>
          <span class="text-slate-800 text-sm font-bold ml-1">4.92 / 5.0 Rating</span>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div 
          v-for="quote in testimonials" 
          :key="quote.author"
          class="bg-white rounded-3xl p-8 border border-surface-border shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
        >
          <div class="flex flex-col gap-4">
            <div class="flex items-center gap-1 text-amber-400 text-xs">
              <i v-for="s in 5" :key="s" class="pi pi-star-fill"></i>
            </div>
            <p class="text-slate-600 text-sm leading-relaxed font-medium italic">
              "{{ quote.text }}"
            </p>
          </div>

          <div class="flex items-center gap-3 pt-6 border-t border-slate-100 mt-6">
            <div class="w-10 h-10 rounded-full bg-navy text-white font-black text-sm flex items-center justify-center shrink-0">
              {{ quote.initials }}
            </div>
            <div>
              <p class="font-black text-sm text-slate-900">{{ quote.author }}</p>
              <p class="text-xs text-slate-400">{{ quote.role }} · {{ quote.city }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FINAL CALL TO ACTION BANNER -->
    <section class="max-w-content mx-auto px-4 sm:px-6 pb-24">
      <div class="bg-gradient-to-r from-navy-700 via-slate-900 to-navy-700 rounded-3xl p-10 sm:p-16 text-center text-white relative overflow-hidden shadow-2xl">
        <div class="relative z-10 max-w-3xl mx-auto">
          <span class="text-xs font-black uppercase tracking-widest text-accent mb-3 block">Start Your Journey</span>
          <h2 class="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight mb-6">
            Ready to Experience Extraordinary Stays Across Zambia?
          </h2>
          <p class="text-slate-300 text-base sm:text-lg mb-10 font-medium">
            Join thousands of satisfied guests and top property owners today.
          </p>

          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <router-link to="/register" class="btn-accent text-base font-black px-9 py-4 rounded-full shadow-accent hover:scale-105 transition-transform no-underline">
              Create Free Account
            </router-link>
            <router-link to="/register?role=owner" class="btn-outline text-base font-black px-9 py-4 rounded-full hover:scale-105 transition-transform no-underline bg-white text-slate-900 border-none">
              Register as Host
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="bg-slate-950 text-white border-t border-slate-800 py-12">
      <div class="max-w-content mx-auto px-4 sm:px-6 flex flex-col sm:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-2 text-xl font-black text-white">
          <div class="w-8 h-8 rounded-lg bg-accent text-white flex items-center justify-center text-sm">
            <i class="pi pi-building"></i>
          </div>
          APARTEX
        </div>

        <p class="text-xs text-slate-500">&copy; 2026 Apartex Ecosystem. All rights reserved. Created by Zakir Motala.</p>

        <div class="flex gap-6 text-xs text-slate-400 font-medium">
          <router-link to="/login" class="hover:text-white no-underline transition-colors">Sign In</router-link>
          <router-link to="/register" class="hover:text-white no-underline transition-colors">Sign Up</router-link>
          <router-link to="/register?role=owner" class="hover:text-white no-underline transition-colors">Become a Host</router-link>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref } from 'vue';

const pillars = [
  {
    title: 'Zero Hidden Markup',
    description: 'Direct host rates without 15-20% hidden service commissions charged by old travel portals.',
    icon: 'pi pi-wallet',
    color: 'text-accent',
    bg: 'bg-accent-light'
  },
  {
    title: 'Apartex VIP Club',
    description: 'Earn points on every stay night. Redeem for free vouchers, cashbacks, and airport shuttles.',
    icon: 'pi pi-star-fill',
    color: 'text-amber-500',
    bg: 'bg-amber-50'
  },
  {
    title: 'Inspected Comfort',
    description: 'Every property is hand-inspected for hygiene, high-speed Wi-Fi, air-con, and 24/7 security.',
    icon: 'pi pi-shield',
    color: 'text-emerald-600',
    bg: 'bg-emerald-50'
  },
  {
    title: 'Instant Mobile Money',
    description: 'Seamless instant payment via MTN Mobile Money, Airtel Money, or credit cards.',
    icon: 'pi pi-mobile',
    color: 'text-blue-600',
    bg: 'bg-blue-50'
  }
];

const steps = [
  {
    number: '1',
    title: 'Discover & Compare',
    description: 'Search verified apartments & lodges by city, amenities, capacity, and real guest ratings.'
  },
  {
    number: '2',
    title: 'Instant Booking',
    description: 'Reserve directly with zero markups using Airtel Money, MTN Mobile Money, or Credit Cards.'
  },
  {
    number: '3',
    title: 'Stay & Earn Rewards',
    description: 'Enjoy 24/7 VIP concierge support and automatically earn Apartex Club points on every stay.'
  }
];

const comparisonRows = [
  { feature: 'Service Markups & Fees', apartex: '0% Fees (Direct Pricing)', others: '12% - 20% Hidden Fees' },
  { feature: 'Loyalty Rewards Program', apartex: 'Points & Cashbacks on Every Stay', others: 'None or Weak Tier Perks' },
  { feature: 'Mobile Money Support', apartex: 'MTN & Airtel Money Instant', others: 'Credit Card Only' },
  { feature: 'Property Inspection Standard', apartex: 'Verified Hygiene & Solar Power', others: 'Unverified Self-Listings' },
  { feature: 'Local Support Concierge', apartex: '24/7 Dedicated Zambian Support', others: 'Offshore Chatbots' }
];

const cityCards = [
  { name: 'Lusaka', label: 'Capital Suites', count: 14, desc: 'High-rise executive penthouses in Kabulonga & Rhodes Park.', image: 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=600&q=80' },
  { name: 'Livingstone', label: 'Victoria Falls', count: 9, desc: 'Riverside safari lodges and eco-cottages along the Zambezi.', image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80' },
  { name: 'Ndola', label: 'Copperbelt', count: 7, desc: 'Quiet executive serviced suites for corporate travelers.', image: 'https://images.unsplash.com/photo-1449034446853-66c86144b0ad?auto=format&fit=crop&w=600&q=80' },
  { name: 'Kitwe', label: 'Commercial Hub', count: 5, desc: 'Modern serviced suites near Nkana Golf Club & Riverside.', image: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=600&q=80' }
];

const testimonials = [
  { text: 'Apartex completely changed how our company books business stays in Lusaka. Zero hidden fees and instant mobile money confirmation.', author: 'Sharon Phiri', role: 'Corporate Guest', city: 'Lusaka' },
  { text: 'Listing our Victoria Falls lodge on Apartex doubled our monthly bookings. Direct host payouts with zero hassle.', author: 'Mwansa Kabwe', role: 'Property Owner', city: 'Livingstone' },
  { text: 'The VIP Gold points benefits are real. Redeemed my points for a free weekend stay. Smooth, modern, and reliable.', author: 'Daniel Zulu', role: 'Frequent Traveler', city: 'Ndola' }
];
</script>
