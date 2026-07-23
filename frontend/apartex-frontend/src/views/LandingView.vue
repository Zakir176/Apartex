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

        <!-- INTERACTIVE LIVE HERO SEARCH BAR WIDGET -->
        <div class="max-w-4xl mx-auto mt-10 relative z-30 mb-12">
          <div class="bg-white/95 backdrop-blur-2xl border border-surface-border rounded-3xl p-4 sm:p-5 shadow-2xl ring-1 ring-slate-900/5 hover:border-accent/40 transition-all duration-300">
            
            <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
              
              <!-- Destination City Selector -->
              <div class="md:col-span-5 relative group">
                <label class="text-[10px] font-black uppercase tracking-widest text-slate-400 block px-3 pt-1">Destination City</label>
                <div class="flex items-center gap-2.5 px-3 py-2 cursor-pointer rounded-2xl hover:bg-slate-50 transition-colors">
                  <div class="w-9 h-9 rounded-xl bg-accent/10 text-accent font-black flex items-center justify-center shrink-0">
                    <i class="pi pi-map-marker text-sm"></i>
                  </div>
                  <div class="grow">
                    <select 
                      v-model="heroSearchCity"
                      class="w-full bg-transparent font-black text-sm text-slate-900 focus:outline-none cursor-pointer border-0 p-0 appearance-none"
                    >
                      <option v-for="c in heroCities" :key="c.value" :value="c.value">
                        {{ c.name }} — {{ c.label }}
                      </option>
                    </select>
                    <p class="text-[11px] text-slate-500 font-medium">Lusaka, Livingstone, Ndola, Kitwe</p>
                  </div>
                  <i class="pi pi-chevron-down text-xs text-slate-400"></i>
                </div>
              </div>

              <!-- Divider line -->
              <div class="hidden md:block w-px h-10 bg-slate-200"></div>

              <!-- Guest Capacity Selector -->
              <div class="md:col-span-4 relative">
                <label class="text-[10px] font-black uppercase tracking-widest text-slate-400 block px-3 pt-1">Guest Capacity</label>
                <div class="flex items-center justify-between px-3 py-2 rounded-2xl">
                  <div class="flex items-center gap-2.5">
                    <div class="w-9 h-9 rounded-xl bg-navy/10 text-navy font-black flex items-center justify-center shrink-0">
                      <i class="pi pi-users text-sm"></i>
                    </div>
                    <div>
                      <p class="font-black text-sm text-slate-900">{{ heroSearchGuests }} {{ heroSearchGuests === 1 ? 'Guest' : 'Guests' }}</p>
                      <p class="text-[11px] text-slate-500 font-medium">Entire suite stay</p>
                    </div>
                  </div>
                  <!-- Increment/Decrement Buttons -->
                  <div class="flex items-center gap-2 bg-slate-100 p-1 rounded-xl border border-slate-200">
                    <button 
                      @click="heroSearchGuests = Math.max(1, heroSearchGuests - 1)" 
                      class="w-7 h-7 rounded-lg bg-white text-slate-700 font-black text-xs flex items-center justify-center shadow-sm hover:bg-slate-50 border-0 cursor-pointer"
                      title="Decrease guests"
                    >-</button>
                    <span class="text-xs font-black text-slate-900 px-1">{{ heroSearchGuests }}</span>
                    <button 
                      @click="heroSearchGuests = Math.min(10, heroSearchGuests + 1)" 
                      class="w-7 h-7 rounded-lg bg-white text-slate-700 font-black text-xs flex items-center justify-center shadow-sm hover:bg-slate-50 border-0 cursor-pointer"
                      title="Increase guests"
                    >+</button>
                  </div>
                </div>
              </div>

              <!-- Search CTA Button -->
              <div class="md:col-span-3">
                <button 
                  @click="executeHeroSearch"
                  class="w-full btn-accent font-black py-4 px-6 rounded-2xl shadow-accent hover:scale-[1.03] transition-transform duration-200 flex items-center justify-center gap-2 border-0 cursor-pointer text-sm"
                >
                  <i class="pi pi-search text-sm"></i>
                  <span>Search Stays</span>
                </button>
              </div>

            </div>

            <!-- Instant Real-Time Filter Preview Bar -->
            <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between px-2 text-xs">
              <div class="flex items-center gap-2">
                <span class="inline-flex h-2.5 w-2.5 relative">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                </span>
                <span class="font-extrabold text-slate-800">
                  {{ filteredHeroProperties.length }} {{ filteredHeroProperties.length === 1 ? 'Luxury Property' : 'Luxury Properties' }}
                </span>
                <span class="text-slate-500 font-medium">available for {{ heroSearchGuests }} {{ heroSearchGuests === 1 ? 'guest' : 'guests' }} in {{ heroSearchCity === 'All' ? 'Zambia' : heroSearchCity }}</span>
              </div>

              <button 
                @click="isPreviewOpen = !isPreviewOpen"
                class="text-accent font-bold hover:underline flex items-center gap-1 bg-transparent border-0 cursor-pointer"
              >
                <span>{{ isPreviewOpen ? 'Hide Preview' : 'Instant Preview' }}</span>
                <i :class="isPreviewOpen ? 'rotate-180' : ''" class="pi pi-chevron-down text-[10px] transition-transform"></i>
              </button>
            </div>

            <!-- Instant Live Cards Preview Grid -->
            <div v-show="isPreviewOpen" class="mt-4 pt-4 border-t border-slate-100 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div 
                v-for="prop in filteredHeroProperties.slice(0, 3)" 
                :key="prop.id"
                @click="executeHeroSearch"
                class="bg-slate-50 hover:bg-white rounded-2xl p-3 border border-slate-200 hover:border-accent/40 shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer group flex flex-col justify-between"
              >
                <div class="relative rounded-xl overflow-hidden aspect-[16/10] mb-2.5">
                  <img :src="prop.image" :alt="prop.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                  <span class="absolute top-2 left-2 bg-slate-900/80 backdrop-blur-md text-white text-[10px] font-black px-2.5 py-0.5 rounded-full">
                    {{ prop.city }}
                  </span>
                  <span class="absolute top-2 right-2 bg-emerald-500 text-white text-[10px] font-black px-2 py-0.5 rounded-full flex items-center gap-1">
                    <i class="pi pi-star-fill text-[9px]"></i> {{ prop.rating }}
                  </span>
                </div>
                <div>
                  <h4 class="font-black text-xs text-slate-900 group-hover:text-accent transition-colors line-clamp-1 mb-1">{{ prop.title }}</h4>
                  <div class="flex items-center justify-between text-[11px] text-slate-500 font-medium">
                    <span>{{ prop.bedrooms }} Beds · Up to {{ prop.maxGuests }} Guests</span>
                    <span class="font-black text-slate-900 text-xs">${{ prop.price }} <span class="text-[9px] font-normal text-slate-400">/night</span></span>
                  </div>
                </div>
              </div>
            </div>

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

    <!-- INFINITE MARQUEE BANNER: PAYMENT & VERIFICATION PARTNERS -->
    <div class="bg-slate-950 text-white py-5 overflow-hidden border-y border-slate-800 relative z-20">
      <div class="max-w-content mx-auto px-4 mb-2.5 text-center">
        <span class="text-[10px] font-black uppercase tracking-widest text-slate-400">Integrated Payment & Verification Ecosystem</span>
      </div>
      
      <!-- Gradient Fades on Edges -->
      <div class="relative w-full overflow-hidden">
        <div class="absolute top-0 bottom-0 left-0 w-24 bg-gradient-to-r from-slate-950 to-transparent z-10 pointer-events-none"></div>
        <div class="absolute top-0 bottom-0 right-0 w-24 bg-gradient-to-l from-slate-950 to-transparent z-10 pointer-events-none"></div>

        <!-- Marquee Track -->
        <div class="animate-marquee-track flex items-center gap-6">
          <div 
            v-for="(item, idx) in marqueePartners" 
            :key="idx"
            class="flex items-center gap-3 bg-slate-900/90 border border-slate-800 px-5 py-2.5 rounded-full whitespace-nowrap hover:border-accent/60 transition-colors shadow-sm cursor-pointer group"
          >
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-black shrink-0" :class="item.bg">
              <i :class="[item.icon, item.color]"></i>
            </div>
            <div>
              <span class="text-xs font-black text-white group-hover:text-accent transition-colors block">{{ item.title }}</span>
              <span class="text-[10px] font-bold text-slate-400 block">{{ item.subtitle }}</span>
            </div>
            <span class="text-[9px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full ml-1" :class="item.badgeBg">
              {{ item.badge }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- PLATFORM PILLARS & FEATURES ("WHY APARTEX") -->

    <section id="why-apartex" class="max-w-content mx-auto px-4 sm:px-6 py-24">

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

    <!-- PROPERTY OWNER PRICING SECTION -->
    <section id="owner-pricing" class="bg-slate-900 text-white py-24 relative overflow-hidden border-y border-slate-800">
      <!-- Ambient Lighting Orbs -->
      <div class="absolute top-0 right-0 w-96 h-96 bg-accent/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute bottom-0 left-0 w-96 h-96 bg-navy/40 rounded-full blur-3xl pointer-events-none"></div>

      <div class="max-w-content mx-auto px-4 sm:px-6 relative z-10">
        
        <!-- Header -->
        <div class="text-center max-w-3xl mx-auto mb-12">
          <span class="text-xs font-black uppercase tracking-widest text-accent mb-3 block">Property Owner Pricing (2026)</span>
          <h2 class="text-3xl sm:text-5xl font-black tracking-tight text-white mb-4">
            Zero Commission. Keep 100% of What Guests Pay.
          </h2>
          <p class="text-slate-300 text-base sm:text-lg font-medium leading-relaxed">
            Simple fixed monthly subscriptions with a one-time setup fee. No booking commissions, no guest service markups.
          </p>
        </div>

        <!-- Special Banner Promos -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto mb-14">
          <!-- Early Adopter Promo -->
          <div class="bg-gradient-to-r from-amber-500/20 to-accent/20 border border-amber-500/30 rounded-2xl p-5 flex items-start gap-4 backdrop-blur-md">
            <div class="w-12 h-12 rounded-xl bg-amber-500 text-slate-950 flex items-center justify-center shrink-0 text-xl font-black">
              <i class="pi pi-bolt"></i>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs font-black text-amber-400 uppercase tracking-wider">Early Adopter Offer</span>
                <span class="bg-amber-400/20 text-amber-300 text-[10px] font-bold px-2 py-0.5 rounded-full">Save 50%</span>
              </div>
              <p class="text-sm font-bold text-white mt-1">Properties onboarded before 1 October 2026 receive 50% OFF setup fees & locked monthly rates for 12 months.</p>
            </div>
          </div>

          <!-- Referral Program Promo -->
          <div class="bg-gradient-to-r from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-2xl p-5 flex items-start gap-4 backdrop-blur-md">
            <div class="w-12 h-12 rounded-xl bg-emerald-500 text-slate-950 flex items-center justify-center shrink-0 text-xl font-black">
              <i class="pi pi-gift"></i>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs font-black text-emerald-400 uppercase tracking-wider">Owner Referral Reward</span>
                <span class="bg-emerald-400/20 text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full">Unlimited</span>
              </div>
              <p class="text-sm font-bold text-white mt-1">Refer another property owner and receive 1 month FREE on your subscription for every successful referral.</p>
            </div>
          </div>
        </div>


        <!-- INTERACTIVE HOST SAVINGS & PROFIT CALCULATOR -->
        <div id="host-calculator" class="max-w-5xl mx-auto mb-20 bg-gradient-to-b from-slate-900/90 to-navy-950/90 border border-amber-500/30 rounded-3xl p-6 sm:p-10 shadow-2xl backdrop-blur-xl relative overflow-hidden">
          <!-- Subtle Glow Accent -->
          <div class="absolute -right-20 -bottom-20 w-80 h-80 bg-accent/15 rounded-full blur-3xl pointer-events-none"></div>

          <div class="flex items-center gap-3 mb-6">
            <div class="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-400 font-black flex items-center justify-center text-xl">
              <i class="pi pi-calculator"></i>
            </div>
            <div>
              <h3 class="text-xl sm:text-2xl font-black text-white">Interactive Host Profit & Savings Calculator</h3>
              <p class="text-xs sm:text-sm text-slate-400 font-medium">See how much 0% commission saves you compared to traditional 18% OTA booking fees.</p>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            
            <!-- Left Controls Column (Sliders) -->
            <div class="lg:col-span-7 space-y-6 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
              
              <!-- Slider 1: Number of Properties -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <label class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                    <i class="pi pi-building text-accent"></i> Number of Properties
                  </label>
                  <span class="text-sm font-black text-amber-400 bg-amber-400/10 px-3 py-1 rounded-full border border-amber-400/20">
                    {{ calcPropertiesCount }} {{ calcPropertiesCount === 1 ? 'Property' : 'Properties' }}
                  </span>
                </div>
                <input 
                  type="range" 
                  min="1" 
                  max="20" 
                  v-model.number="calcPropertiesCount"
                  class="w-full accent-accent cursor-pointer h-2 bg-slate-700 rounded-lg"
                />
                <div class="flex justify-between text-[11px] text-slate-500 font-bold mt-1">
                  <span>1 Property</span>
                  <span>10 Properties</span>
                  <span>20 Properties</span>
                </div>
              </div>

              <!-- Slider 2: Average Nightly Rate ($) -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <label class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                    <i class="pi pi-dollar text-emerald-400"></i> Average Nightly Rate
                  </label>
                  <span class="text-sm font-black text-emerald-400 bg-emerald-400/10 px-3 py-1 rounded-full border border-emerald-400/20">
                    ${{ calcNightlyRate }} / night
                  </span>
                </div>
                <input 
                  type="range" 
                  min="30" 
                  max="500" 
                  step="10" 
                  v-model.number="calcNightlyRate"
                  class="w-full accent-accent cursor-pointer h-2 bg-slate-700 rounded-lg"
                />
                <div class="flex justify-between text-[11px] text-slate-500 font-bold mt-1">
                  <span>$30</span>
                  <span>$250</span>
                  <span>$500</span>
                </div>
              </div>

              <!-- Slider 3: Occupancy Rate (%) -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <label class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                    <i class="pi pi-chart-line text-blue-400"></i> Estimated Monthly Occupancy
                  </label>
                  <span class="text-sm font-black text-blue-400 bg-blue-400/10 px-3 py-1 rounded-full border border-blue-400/20">
                    {{ calcOccupancyRate }}% Occupancy (~{{ Math.round(30 * (calcOccupancyRate / 100)) }} nights/mo)
                  </span>
                </div>
                <input 
                  type="range" 
                  min="30" 
                  max="90" 
                  step="5" 
                  v-model.number="calcOccupancyRate"
                  class="w-full accent-accent cursor-pointer h-2 bg-slate-700 rounded-lg"
                />
                <div class="flex justify-between text-[11px] text-slate-500 font-bold mt-1">
                  <span>30% Low</span>
                  <span>65% Average</span>
                  <span>90% High</span>
                </div>
              </div>

            </div>

            <!-- Right Results Display Column -->
            <div class="lg:col-span-5 flex flex-col gap-4">
              
              <!-- Gross Revenue Preview -->
              <div class="bg-slate-900/80 p-4 rounded-2xl border border-slate-800 flex justify-between items-center">
                <div>
                  <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 block">Est. Gross Monthly Revenue</span>
                  <span class="text-xl font-black text-white">${{ calcGrossMonthlyRevenue.toLocaleString() }} <span class="text-xs font-normal text-slate-400">/ mo</span></span>
                </div>
                <div class="text-right">
                  <span class="text-[10px] font-bold text-slate-400 block">Annual Revenue</span>
                  <span class="text-sm font-extrabold text-slate-300">${{ calcGrossAnnualRevenue.toLocaleString() }}</span>
                </div>
              </div>

              <!-- Breakdown Comparison -->
              <div class="bg-slate-950/80 p-4 rounded-2xl border border-slate-800 space-y-2 text-xs">
                <div class="flex justify-between items-center text-red-400">
                  <span class="flex items-center gap-1.5 font-bold">
                    <i class="pi pi-times-circle"></i> 18% Traditional OTA Fees:
                  </span>
                  <span class="font-black text-sm">-${{ calcAnnualOtaCommissionLost.toLocaleString() }} / yr</span>
                </div>

                <div class="flex justify-between items-center text-slate-300 pt-2 border-t border-slate-800">
                  <span class="flex items-center gap-1.5 font-bold">
                    <i class="pi pi-check-circle text-accent"></i> Apartex {{ calcRecommendedPlan.name }}:
                  </span>
                  <span class="font-black text-white">${{ calcRecommendedPlan.annual }} / yr (${{ calcRecommendedPlan.monthly }}/mo)</span>
                </div>
              </div>

              <!-- Highlighted Net Annual Money Saved -->
              <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-emerald-950/80 p-5 rounded-2xl border border-emerald-500/40 shadow-lg text-center relative overflow-hidden group">
                <span class="text-xs font-black uppercase tracking-widest text-emerald-400 block mb-1">Your Net Annual Money Saved</span>
                <p class="text-3xl sm:text-4xl font-black text-emerald-400 tracking-tight group-hover:scale-105 transition-transform duration-300">
                  +${{ calcNetAnnualSavings.toLocaleString() }} <span class="text-sm font-bold text-emerald-300">/ year</span>
                </p>
                <p class="text-[11px] text-slate-300 font-medium mt-1">100% extra profit straight into your bank account!</p>
              </div>

              <router-link 
                to="/register?role=owner" 
                class="btn-accent text-center font-black py-3.5 px-6 rounded-xl shadow-accent hover:scale-[1.02] transition-transform no-underline flex items-center justify-center gap-2 text-sm"
              >
                <span>Claim Your Savings — List Property</span>
                <i class="pi pi-arrow-right text-xs"></i>
              </router-link>

            </div>

          </div>
        </div>


        <!-- Toggle Switch: Early Adopter 50% Off vs Standard -->
        <div class="flex justify-center items-center gap-4 mb-14">
          <span :class="!isEarlyAdopterOffer ? 'text-white font-bold' : 'text-slate-400 font-medium'" class="text-sm cursor-pointer" @click="isEarlyAdopterOffer = false">
            Standard Rates
          </span>
          <button 
            @click="isEarlyAdopterOffer = !isEarlyAdopterOffer" 
            class="w-14 h-8 bg-accent rounded-full p-1 transition-colors relative flex items-center shadow-inner"
            aria-label="Toggle Early Adopter Rates"
          >
            <div 
              class="w-6 h-6 bg-white rounded-full transition-transform duration-300 shadow-md"
              :class="isEarlyAdopterOffer ? 'translate-x-6' : 'translate-x-0'"
            ></div>
          </button>
          <span :class="isEarlyAdopterOffer ? 'text-amber-400 font-bold' : 'text-slate-400 font-medium'" class="text-sm flex items-center gap-2 cursor-pointer" @click="isEarlyAdopterOffer = true">
            <span>Early Adopter (50% Off Setup)</span>
            <span class="bg-amber-400 text-slate-950 text-[10px] font-black px-2 py-0.5 rounded-full">PROMO</span>
          </span>
        </div>

        <!-- 3 Pricing Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto items-stretch">
          
          <div 
            v-for="plan in ownerPricingPlans" 
            :key="plan.name"
            class="rounded-3xl p-8 flex flex-col justify-between transition-all duration-300 relative border"
            :class="plan.popular 
              ? 'bg-gradient-to-b from-slate-900 via-navy-900 to-slate-900 border-accent shadow-2xl scale-105 z-20 glow-accent' 
              : 'bg-slate-800/60 border-slate-700/80 hover:border-slate-500 z-10'"
          >
            <!-- Popular Badge -->
            <div v-if="plan.popular" class="absolute -top-4 left-1/2 -translate-x-1/2 bg-accent text-white text-xs font-black uppercase tracking-widest px-4 py-1.5 rounded-full shadow-lg flex items-center gap-1.5">
              <i class="pi pi-star-fill text-amber-300 text-xs"></i> Most Popular for Hosts
            </div>

            <div>
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-black uppercase tracking-widest text-accent">{{ plan.bestFor }}</span>
              </div>
              
              <h3 class="text-2xl font-black text-white mb-2">{{ plan.name }}</h3>
              <p class="text-xs text-slate-400 font-medium mb-6 min-h-[36px]">{{ plan.description }}</p>

              <!-- Monthly Price -->
              <div class="mb-6 pb-6 border-b border-slate-700/80">
                <div class="flex items-baseline gap-1">
                  <span class="text-4xl font-black text-white">${{ plan.monthlyFee }}</span>
                  <span class="text-sm font-bold text-slate-400">/ month</span>
                </div>
                
                <!-- Setup Fee Breakdown -->
                <div class="mt-3 inline-flex items-center gap-2 bg-slate-950/60 px-3 py-1.5 rounded-xl border border-slate-700 text-xs">
                  <span class="text-slate-400 font-medium">One-time setup:</span>
                  <span v-if="isEarlyAdopterOffer" class="text-amber-400 font-black flex items-center gap-1">
                    <span class="line-through text-slate-500">${{ plan.setupFee }}</span>
                    <span>${{ plan.setupFee / 2 }}</span>
                  </span>
                  <span v-else class="text-white font-bold">${{ plan.setupFee }}</span>
                </div>
              </div>

              <!-- Scope Highlights -->
              <div class="mb-6 space-y-2 text-xs font-bold text-slate-300">
                <div class="flex items-center justify-between bg-slate-900/80 px-3 py-2 rounded-lg border border-slate-700/50">
                  <span>Properties Supported:</span>
                  <span class="text-accent font-black">{{ plan.propertiesCount }}</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900/80 px-3 py-2 rounded-lg border border-slate-700/50">
                  <span>Listings / Room Types:</span>
                  <span class="text-accent font-black">{{ plan.listingsCount }}</span>
                </div>
              </div>

              <!-- Feature Checklist -->
              <div class="space-y-3 mb-8">
                <p class="text-xs font-black uppercase tracking-wider text-slate-400">Included Features:</p>
                <div 
                  v-for="feature in plan.features" 
                  :key="feature.name"
                  class="flex items-center gap-3 text-xs font-medium"
                  :class="feature.included ? 'text-slate-200' : 'text-slate-500 line-through'"
                >
                  <i :class="feature.included ? 'pi pi-check-circle text-emerald-400' : 'pi pi-minus-circle text-slate-600'" class="text-sm shrink-0"></i>
                  <span>{{ feature.name }}</span>
                </div>
              </div>
            </div>

            <!-- CTA button -->
            <router-link 
              to="/register?role=owner" 
              class="w-full text-center font-black py-4 px-6 rounded-2xl no-underline transition-all duration-200 block"
              :class="plan.popular 
                ? 'btn-accent shadow-accent hover:scale-[1.02]' 
                : 'bg-slate-700 hover:bg-slate-600 text-white hover:scale-[1.02]'"
            >
              Get Started with {{ plan.name }}
            </router-link>
          </div>

        </div>

        <!-- Setup Fee Guarantee Breakdown Section -->
        <div class="mt-16 bg-slate-800/40 border border-slate-700/60 rounded-3xl p-8 max-w-5xl mx-auto">
          <div class="flex flex-col lg:flex-row items-center gap-8 justify-between">
            <div class="lg:w-1/3 text-center lg:text-left">
              <span class="text-xs font-black uppercase tracking-widest text-accent mb-2 block">Full Service Onboarding</span>
              <h4 class="text-2xl font-black text-white">What Your Setup Fee Covers</h4>
              <p class="text-xs text-slate-400 mt-2 font-medium">We handle 100% of the technical setup so you can start receiving bookings immediately.</p>
            </div>

            <div class="lg:w-2/3 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-300 font-medium">
              <div v-for="item in setupFeeItems" :key="item" class="flex items-center gap-3 bg-slate-900/60 p-3 rounded-xl border border-slate-700/40">
                <i class="pi pi-check text-emerald-400 text-sm font-bold shrink-0"></i>
                <span>{{ item }}</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- INTERACTIVE DESTINATION HIGHLIGHTS -->
    <section id="destinations" class="bg-slate-950 text-white py-24 relative overflow-hidden">

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

    <!-- INTERACTIVE FAQ SECTION -->
    <section id="faq" class="max-w-content mx-auto px-4 sm:px-6 py-24 border-t border-surface-border">
      <div class="text-center max-w-3xl mx-auto mb-12">
        <span class="section-tag">Got Questions?</span>
        <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-slate-900">
          Frequently Asked Questions
        </h2>
        <p class="text-slate-600 text-base sm:text-lg mt-3 font-medium">
          Everything you need to know about listing your property, syncing reservations, or booking extraordinary stays on Apartex.
        </p>
      </div>

      <!-- FAQ Category Filter Tabs & Real-Time Search Bar -->
      <div class="max-w-4xl mx-auto mb-10 flex flex-col md:flex-row items-center justify-between gap-4">
        <!-- Category Filter Tabs -->
        <div class="flex items-center gap-1.5 bg-slate-200/60 p-1.5 rounded-full border border-slate-300/60 overflow-x-auto max-w-full">
          <button 
            v-for="cat in faqCategories" 
            :key="cat.id"
            @click="activeFaqCategory = cat.id"
            class="px-4 py-2 rounded-full text-xs font-black transition-all duration-200 cursor-pointer whitespace-nowrap border-0"
            :class="activeFaqCategory === cat.id ? 'bg-white text-slate-900 shadow-md scale-[1.02]' : 'text-slate-600 hover:text-slate-900 bg-transparent'"
          >
            <i :class="[cat.icon, 'mr-1.5 text-xs']" :style="{ color: activeFaqCategory === cat.id ? '#E8621A' : '' }"></i>
            {{ cat.label }}
          </button>
        </div>

        <!-- Real-time Search Input -->
        <div class="relative w-full md:w-72">
          <i class="pi pi-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
          <input 
            v-model="faqSearchQuery"
            type="text" 
            placeholder="Search questions (e.g. MoMo, POS, fee)..." 
            class="w-full pl-10 pr-9 py-2.5 rounded-full bg-white border border-surface-border text-xs font-bold text-slate-800 focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/15 transition-all"
          />
          <button 
            v-if="faqSearchQuery" 
            @click="faqSearchQuery = ''"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 text-xs bg-transparent border-0 cursor-pointer"
          >
            <i class="pi pi-times-circle"></i>
          </button>
        </div>
      </div>

      <!-- FAQ Accordion List -->
      <div class="max-w-4xl mx-auto space-y-4">
        <div 
          v-for="(item, idx) in filteredFaqs" 
          :key="item.question"
          class="bg-white rounded-3xl border transition-all duration-300 overflow-hidden"
          :class="activeFaq === idx 
            ? 'border-accent/40 shadow-xl ring-2 ring-accent/10' 
            : 'border-surface-border shadow-sm hover:shadow-md hover:border-slate-300'"
        >
          <!-- Accordion Question Header Button -->
          <button 
            @click="toggleFaq(idx)"
            class="w-full p-6 text-left flex items-start justify-between gap-4 font-black text-base sm:text-lg text-slate-900 hover:text-accent transition-colors bg-white cursor-pointer"
          >
            <div class="flex items-start gap-3.5 pr-2">
              <div 
                class="w-10 h-10 rounded-2xl flex items-center justify-center shrink-0 text-base shadow-sm mt-0.5"
                :class="item.bgClass"
              >
                <i :class="[item.icon, item.iconColor]"></i>
              </div>
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-[10px] font-black uppercase tracking-wider px-2.5 py-0.5 rounded-full" :class="item.badgeClass">
                    {{ item.badge }}
                  </span>
                </div>
                <h3 class="text-base sm:text-lg font-black text-slate-900 leading-snug">{{ item.question }}</h3>
              </div>
            </div>

            <!-- Expand Chevron Icon -->
            <div 
              class="w-9 h-9 rounded-full bg-slate-100 flex items-center justify-center shrink-0 transition-transform duration-300 mt-1" 
              :class="activeFaq === idx ? 'rotate-180 bg-accent text-white shadow-md' : 'text-slate-500'"
            >
              <i class="pi pi-chevron-down text-xs font-extrabold"></i>
            </div>
          </button>
          
          <!-- Expandable Answer Body -->
          <div 
            v-show="activeFaq === idx"
            class="px-6 pb-6 pt-2 text-sm text-slate-600 font-medium leading-relaxed border-t border-slate-100 bg-slate-50/60"
          >
            <p class="mb-4 text-slate-700 font-semibold">{{ item.answer }}</p>

            <!-- Key Highlight Bullet Points -->
            <div v-if="item.bullets && item.bullets.length" class="space-y-2 bg-white p-4 rounded-2xl border border-slate-200/80 shadow-inner">
              <div v-for="(bullet, bIdx) in item.bullets" :key="bIdx" class="flex items-start gap-2 text-xs font-bold text-slate-800">
                <i class="pi pi-check-circle text-emerald-500 text-sm shrink-0 mt-0.5"></i>
                <span>{{ bullet }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty Search State -->
        <div v-if="filteredFaqs.length === 0" class="text-center py-12 bg-white rounded-3xl border border-surface-border p-8">
          <div class="w-14 h-14 rounded-2xl bg-amber-100 text-amber-600 flex items-center justify-center text-2xl mx-auto mb-4">
            <i class="pi pi-question-circle"></i>
          </div>
          <h3 class="text-lg font-black text-slate-900 mb-1">No matching questions found</h3>
          <p class="text-xs text-slate-500 mb-4">Try searching with different keywords like "MoMo", "POS", or "pricing".</p>
          <button 
            @click="faqSearchQuery = ''; activeFaqCategory = 'all'" 
            class="btn-accent text-xs font-bold px-5 py-2.5 rounded-full cursor-pointer border-0"
          >
            Reset Search Filters
          </button>
        </div>
      </div>

      <!-- Support CTA Banner -->
      <div class="max-w-4xl mx-auto mt-12 bg-gradient-to-r from-navy-900 via-slate-900 to-navy-950 p-6 sm:p-8 rounded-3xl border border-white/10 text-white flex flex-col sm:flex-row items-center justify-between gap-6 shadow-xl">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-2xl bg-accent text-white font-black flex items-center justify-center text-xl shrink-0 shadow-lg">
            <i class="pi pi-comments"></i>
          </div>
          <div>
            <h4 class="text-lg font-black text-white">Have a custom requirement or question?</h4>
            <p class="text-xs text-slate-300 font-medium mt-0.5">Our Lusaka hospitality support team is available 24/7 to assist property owners & guests.</p>
          </div>
        </div>
        <div class="flex items-center gap-3 shrink-0">
          <a href="https://wa.me/260970000000" target="_blank" rel="noopener" class="btn-accent text-xs font-black px-5 py-3 rounded-full no-underline flex items-center gap-2 shadow-accent">
            <i class="pi pi-whatsapp text-sm"></i>
            <span>WhatsApp Support</span>
          </a>
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Interactive Live Hero Search Bar State
const heroSearchCity = ref('Lusaka');
const heroSearchGuests = ref(2);
const isPreviewOpen = ref(false);

const heroCities = [
  { name: 'All Cities', value: 'All', icon: 'pi pi-globe', label: 'Nationwide' },
  { name: 'Lusaka', value: 'Lusaka', icon: 'pi pi-building', label: 'Capital District' },
  { name: 'Livingstone', value: 'Livingstone', icon: 'pi pi-compass', label: 'Victoria Falls' },
  { name: 'Ndola', value: 'Ndola', icon: 'pi pi-briefcase', label: 'Commercial Hub' },
  { name: 'Kitwe', value: 'Kitwe', icon: 'pi pi-sun', label: 'Copperbelt Core' }
];

const sampleProperties = [
  {
    id: 1,
    title: 'The Rhodes Park Executive Penthouse',
    city: 'Lusaka',
    price: 125,
    rating: 4.96,
    maxGuests: 4,
    bedrooms: 3,
    image: 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80',
    amenities: ['Solar Backup', 'Private Pool', 'High-Speed Wi-Fi']
  },
  {
    id: 2,
    title: 'Zambezi Riverfront Eco Safari Lodge',
    city: 'Livingstone',
    price: 185,
    rating: 4.98,
    maxGuests: 6,
    bedrooms: 4,
    image: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80',
    amenities: ['River View', 'Solar Power', 'Airport Shuttle']
  },
  {
    id: 3,
    title: 'Kansenshi Luxury Garden Suite',
    city: 'Ndola',
    price: 95,
    rating: 4.90,
    maxGuests: 2,
    bedrooms: 1,
    image: 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80',
    amenities: ['Generator Backup', 'Secured Parking', 'Workspace']
  },
  {
    id: 4,
    title: 'Nkana Executive Villa & Gardens',
    city: 'Kitwe',
    price: 110,
    rating: 4.92,
    maxGuests: 5,
    bedrooms: 3,
    image: 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?auto=format&fit=crop&w=800&q=80',
    amenities: ['Solar Inverter', 'Gym Access', 'Smart TV']
  },
  {
    id: 5,
    title: 'Mass Media Executive Heights',
    city: 'Lusaka',
    price: 140,
    rating: 4.94,
    maxGuests: 4,
    bedrooms: 2,
    image: 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80',
    amenities: ['Rooftop Pool', 'Solar Backup', 'Concierge']
  }
];

const filteredHeroProperties = computed(() => {
  return sampleProperties.filter(p => {
    const matchesCity = heroSearchCity.value === 'All' || p.city === heroSearchCity.value;
    const matchesGuests = p.maxGuests >= heroSearchGuests.value;
    return matchesCity && matchesGuests;
  });
});

const executeHeroSearch = () => {
  router.push({
    path: '/apartments',
    query: {
      city: heroSearchCity.value !== 'All' ? heroSearchCity.value : undefined,
      guests: heroSearchGuests.value
    }
  });
};

const activeFaq = ref(0);
const activeFaqCategory = ref('all');
const faqSearchQuery = ref('');

const toggleFaq = (idx) => {
  activeFaq.value = activeFaq.value === idx ? null : idx;
};

const faqCategories = [
  { id: 'all', label: 'All Questions', icon: 'pi pi-list' },
  { id: 'hosts', label: 'For Property Hosts', icon: 'pi pi-building' },
  { id: 'guests', label: 'For Guests & Travelers', icon: 'pi pi-user' },
  { id: 'payments', label: 'Payments & MoMo', icon: 'pi pi-wallet' },
];

const faqItems = [
  {
    category: 'hosts',
    badge: 'Host Profit & Pricing',
    badgeClass: 'bg-emerald-500/10 text-emerald-700 border border-emerald-500/20',
    icon: 'pi pi-percentage',
    iconColor: 'text-emerald-600',
    bgClass: 'bg-emerald-50',
    question: 'How does 0% commission work?',
    answer: 'Unlike traditional online travel agencies (OTAs) that charge property owners 15% to 25% commission on every single guest reservation, Apartex operates on a simple flat monthly subscription ($20, $40, or $70/mo). You keep 100% of guest payments directly into your account with zero booking service markups.',
    bullets: [
      'Zero booking commissions or hidden guest service surcharges.',
      'Hosts keep 100% of nightly rates paid directly into bank or Mobile Money.',
      'Fixed monthly subscription starting at only $20/month.'
    ]
  },
  {
    category: 'hosts',
    badge: 'Real-Time Sync Tech',
    badgeClass: 'bg-blue-500/10 text-blue-700 border border-blue-500/20',
    icon: 'pi pi-sync',
    iconColor: 'text-blue-600',
    bgClass: 'bg-blue-50',
    question: 'How do walk-in POS bookings sync with online availability?',
    answer: 'Our built-in Walk-in POS terminal allows receptionists and property owners to log cash, swipe card, or direct mobile money walk-in guests instantly. The system instantly locks out those dates across the online booking calendar in real-time, preventing double-bookings completely.',
    bullets: [
      'Instant calendar block across online Apartex listing when walk-in is logged.',
      'Supports cash, Mobile Money, and card POS terminal receipts.',
      'Automated check-in/check-out status tracking on Host Dashboard.'
    ]
  },
  {
    category: 'hosts',
    badge: 'Onboarding & Service',
    badgeClass: 'bg-amber-500/10 text-amber-700 border border-amber-500/20',
    icon: 'pi pi-cog',
    iconColor: 'text-amber-600',
    bgClass: 'bg-amber-50',
    question: 'What does the one-time setup fee include?',
    answer: 'The one-time onboarding setup fee ($100 for Basic, $250 for Pro, $500 for Portfolio) includes complete full-service setup by our local Zambian team so your properties start earning immediately with zero technical effort.',
    bullets: [
      'High-resolution property photo editing and wizard upload.',
      'Custom interactive Google Map pin & neighborhood highlight positioning.',
      'Pricing calendar setup, seasonal rate rules & room type configuration.',
      'On-site or remote staff training for front-desk Walk-in POS usage.',
      'First 1 MONTH of platform subscription completely FREE!'
    ]
  },
  {
    category: 'payments',
    badge: 'Mobile Money & Checkout',
    badgeClass: 'bg-rose-500/10 text-rose-700 border border-rose-500/20',
    icon: 'pi pi-mobile',
    iconColor: 'text-rose-600',
    bgClass: 'bg-rose-50',
    question: 'How do guests pay with MTN or Airtel Mobile Money?',
    answer: 'During checkout, guests select MTN Mobile Money, Airtel Money, or Zamtel. A secure USSD payment prompt is pushed directly to their phone screen. Once the guest inputs their PIN, funds are instantly verified and transferred directly to the host.',
    bullets: [
      'Seamless USSD push notification right to the guest’s phone.',
      'Instant reservation confirmation with real-time SMS & Email voucher.',
      'Host receives direct Mobile Money or Bank deposit settlement.'
    ]
  },
  {
    category: 'guests',
    badge: 'Loyalty Rewards',
    badgeClass: 'bg-purple-500/10 text-purple-700 border border-purple-500/20',
    icon: 'pi pi-star-fill',
    iconColor: 'text-purple-600',
    bgClass: 'bg-purple-50',
    question: 'How do loyalty rewards (Apartex Club) work for guests?',
    answer: 'Every verified booking earns loyalty points based on your stay amount (5 points per $1 spent). Points automatically accumulate in your Apartex Club wallet and can be redeemed for free night vouchers, room upgrades, and local airport shuttle transfers.',
    bullets: [
      '5 Loyalty Points earned for every $1 spent on stays.',
      'Tiered VIP status (Silver, Gold, Platinum) with exclusive host discounts.',
      'Instant points redemption during checkout on future bookings.'
    ]
  },
  {
    category: 'hosts',
    badge: 'Early Adopter Promo',
    badgeClass: 'bg-orange-500/10 text-orange-700 border border-orange-500/20',
    icon: 'pi pi-bolt',
    iconColor: 'text-orange-600',
    bgClass: 'bg-orange-50',
    question: 'What is the 50% OFF Early Adopter promotion?',
    answer: 'Properties onboarded before 1 October 2026 receive 50% OFF their initial setup fee and are locked into their flat monthly subscription rate for 12 months with a price-freeze guarantee.',
    bullets: [
      '50% discount applied automatically on setup fees.',
      '12-Month subscription rate freeze guarantee.',
      'Priority placement on Apartex homepage featured suites.'
    ]
  }
];

const filteredFaqs = computed(() => {
  return faqItems.filter(item => {
    const matchesCategory = activeFaqCategory.value === 'all' || item.category === activeFaqCategory.value;
    const q = faqSearchQuery.value.toLowerCase().trim();
    const matchesSearch = !q || 
      item.question.toLowerCase().includes(q) || 
      item.answer.toLowerCase().includes(q) || 
      item.badge.toLowerCase().includes(q) ||
      (item.bullets && item.bullets.some(b => b.toLowerCase().includes(q)));
    return matchesCategory && matchesSearch;
  });
});


const partnerList = [

  {
    title: 'MTN Mobile Money',
    subtitle: 'Instant Host Payout Settlement',
    badge: 'Zambia Direct',
    icon: 'pi pi-mobile',
    color: 'text-amber-400',
    bg: 'bg-amber-500/10',
    badgeBg: 'bg-amber-400/20 text-amber-300'
  },
  {
    title: 'Airtel Money',
    subtitle: 'Direct Pay & Instant Confirmation',
    badge: 'Escrow Protected',
    icon: 'pi pi-send',
    color: 'text-rose-400',
    bg: 'bg-rose-500/10',
    badgeBg: 'bg-rose-400/20 text-rose-300'
  },
  {
    title: 'Visa & Mastercard Security',
    subtitle: '256-bit SSL Encrypted Payments',
    badge: 'PCI-DSS Level 1',
    icon: 'pi pi-shield',
    color: 'text-blue-400',
    bg: 'bg-blue-500/10',
    badgeBg: 'bg-blue-400/20 text-blue-300'
  },
  {
    title: 'Zambian Hospitality Standards',
    subtitle: 'Full Tourism & Safety Compliance',
    badge: 'ZTA Verified',
    icon: 'pi pi-check-square',
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10',
    badgeBg: 'bg-emerald-400/20 text-emerald-300'
  },
  {
    title: 'Solar & Generator Guarantee',
    subtitle: '24/7 Uninterrupted Power Supply',
    badge: 'Power Verified',
    icon: 'pi pi-bolt',
    color: 'text-yellow-400',
    bg: 'bg-yellow-500/10',
    badgeBg: 'bg-yellow-400/20 text-yellow-300'
  },
  {
    title: 'Zanaco & Stanbic Settlement',
    subtitle: 'Direct Commercial Bank Deposits',
    badge: 'Local Payouts',
    icon: 'pi pi-building',
    color: 'text-indigo-400',
    bg: 'bg-indigo-500/10',
    badgeBg: 'bg-indigo-400/20 text-indigo-300'
  }
];

const marqueePartners = [...partnerList, ...partnerList];

const isEarlyAdopterOffer = ref(true);


// Host Profit Calculator State
const calcPropertiesCount = ref(2);
const calcNightlyRate = ref(100);
const calcOccupancyRate = ref(65);

const calcMonthlyNights = computed(() => {
  return Math.round(30 * (calcOccupancyRate.value / 100)) * calcPropertiesCount.value;
});

const calcGrossMonthlyRevenue = computed(() => {
  return calcMonthlyNights.value * calcNightlyRate.value;
});

const calcGrossAnnualRevenue = computed(() => {
  return calcGrossMonthlyRevenue.value * 12;
});

const calcAnnualOtaCommissionLost = computed(() => {
  return Math.round(calcGrossAnnualRevenue.value * 0.18);
});

const calcRecommendedPlan = computed(() => {
  if (calcPropertiesCount.value === 1) {
    return { name: 'Starter Plan', monthly: 20, annual: 240 };
  } else if (calcPropertiesCount.value <= 5) {
    return { name: 'Growth Plan', monthly: 40, annual: 480 };
  } else {
    return { name: 'Professional Plan', monthly: 70, annual: 840 };
  }
});

const calcNetAnnualSavings = computed(() => {
  return Math.max(0, calcAnnualOtaCommissionLost.value - calcRecommendedPlan.value.annual);
});


const ownerPricingPlans = [
  {
    name: 'Starter',
    bestFor: 'Single Property Owners',
    description: 'Ideal for independent hosts managing a single house or apartment unit',
    monthlyFee: 20,
    setupFee: 150,
    propertiesCount: '1 Property',
    listingsCount: '1 Listing',
    popular: false,
    features: [
      { name: '0% Commission on Bookings', included: true },
      { name: 'Online Booking Engine', included: true },
      { name: 'Walk-in Booking POS', included: true },
      { name: 'Real-time Availability Calendar', included: true },
      { name: 'Basic Owner Dashboard', included: true },
      { name: 'Verified Guest Reviews', included: true },
      { name: 'Map Pin Listing', included: true },
      { name: 'Apartex Loyalty Rewards Program', included: false },
      { name: 'Priority 24/7 VIP Support', included: false }
    ]
  },
  {
    name: 'Growth',
    bestFor: '2–5 Property Owners',
    description: 'Perfect for growing property hosts expanding across Zambia',
    monthlyFee: 40,
    setupFee: 300,
    propertiesCount: 'Up to 5 Properties',
    listingsCount: 'Up to 10 Listings',
    popular: true,
    features: [
      { name: '0% Commission on Bookings', included: true },
      { name: 'Online Booking Engine', included: true },
      { name: 'Walk-in Booking POS', included: true },
      { name: 'Real-time Availability Calendar', included: true },
      { name: 'Full Analytics Dashboard', included: true },
      { name: 'Verified Guest Reviews', included: true },
      { name: 'Map Pin Listing', included: true },
      { name: 'Apartex Loyalty Rewards Program', included: true },
      { name: 'Priority 24/7 VIP Support', included: false }
    ]
  },
  {
    name: 'Professional',
    bestFor: 'Hotels, Lodges & Guest Houses',
    description: 'Designed for commercial hospitality with multi-room inventory',
    monthlyFee: 70,
    setupFee: 500,
    propertiesCount: 'Unlimited Properties',
    listingsCount: 'Unlimited Room Types',
    popular: false,
    features: [
      { name: '0% Commission on Bookings', included: true },
      { name: 'Online Booking Engine', included: true },
      { name: 'Walk-in Booking POS', included: true },
      { name: 'Real-time Availability Calendar', included: true },
      { name: 'Full Analytics + Walk-in Revenue', included: true },
      { name: 'Verified Guest Reviews', included: true },
      { name: 'Map Pin Listing', included: true },
      { name: 'Apartex Loyalty Rewards Program', included: true },
      { name: 'Priority 24/7 VIP Support', included: true }
    ]
  }
];

const setupFeeItems = [
  'On-site visit or remote listing setup session',
  'Professional property description & amenities setup',
  'Photo upload & map pin placement',
  'Room types & rate configuration (hotels/lodges)',
  'Owner account setup & dashboard walkthrough',
  'Training session for owner & receptionists',
  'First month of hosting included free'
];

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
  { feature: 'Booking Commissions Charged', apartex: '0% Commission (Keep 100%)', others: '15% - 25% Host Commission' },
  { feature: 'Service Markups & Fees', apartex: '0% Guest Markups', others: '12% - 20% Hidden Fees' },
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

