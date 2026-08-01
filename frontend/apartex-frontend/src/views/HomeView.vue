<template>
  <div class="min-h-screen bg-[#F8F7F4] text-slate-800 selection:bg-accent selection:text-white">

    <!-- HERO SECTION -->
    <header class="bg-animated-mesh border-b border-surface-border relative pt-6 pb-24 lg:py-24">
      <div class="max-w-content mx-auto px-4 sm:px-6 relative z-10">
        
        <!-- Live Trust Badge -->
        <div class="flex justify-center mb-6">
          <div class="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-white/80 backdrop-blur-md border border-surface-border shadow-sm text-xs font-bold text-slate-700">
            <span class="flex h-2.5 w-2.5 relative">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span>Zambia's #1 Luxury Accommodation & Booking Platform</span>
            <span class="text-slate-300">|</span>
            <span class="text-accent font-extrabold flex items-center gap-1">
              <i class="pi pi-star-fill text-[10px]"></i> 4.9 Rating
            </span>
          </div>
        </div>

        <!-- Main Title & Tagline -->
        <div class="text-center max-w-4xl mx-auto mb-10">
          <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black text-slate-900 tracking-tight leading-[1.08] mb-6 animate-fade-up">
            Escape to Handpicked Luxury<br class="hidden sm:block" />
            <span class="text-gradient">Across Beautiful Zambia</span>
          </h1>
          <p class="text-base sm:text-lg md:text-xl text-slate-600 font-medium max-w-2xl mx-auto leading-relaxed animate-fade-up-delay-1">
            Hand-inspected executive penthouses, safari lodges & urban retreats. Direct bookings with guaranteed zero service markups.
          </p>
        </div>

        <!-- Multi-Tab Hero Search Container -->
        <div class="max-w-5xl mx-auto bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-surface-border p-3 sm:p-5 relative z-20 animate-fade-up-delay-2">
          <!-- Search Type Tabs -->
          <div class="flex items-center gap-2 mb-4 border-b border-surface-border pb-3 overflow-x-auto no-scrollbar">
            <button
              v-for="tab in searchTabs"
              :key="tab.id"
              @click="activeSearchTab = tab.id"
              class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all flex items-center gap-2 whitespace-nowrap cursor-pointer"
              :class="activeSearchTab === tab.id ? 'bg-navy text-white shadow-sm' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'"
            >
              <i :class="tab.icon"></i>
              <span>{{ tab.label }}</span>
            </button>
          </div>

          <!-- Search Form Inputs Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 items-center">
            <!-- Location -->
            <div class="flex flex-col px-4 py-2.5 bg-slate-50 hover:bg-white rounded-xl border border-slate-200 transition-all focus-within:ring-2 focus-within:ring-accent focus-within:border-accent">
              <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1">
                <i class="pi pi-map-marker text-accent"></i> Location
              </label>
              <select v-model="selectedCity" class="bg-transparent text-sm font-bold text-slate-800 outline-none cursor-pointer border-none p-0 focus:ring-0">
                <option value="">All Cities in Zambia</option>
                <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
              </select>
            </div>

            <!-- Check-In -->
            <div class="flex flex-col px-4 py-2.5 bg-slate-50 hover:bg-white rounded-xl border border-slate-200 transition-all focus-within:ring-2 focus-within:ring-accent focus-within:border-accent">
              <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1">
                <i class="pi pi-calendar text-accent"></i> Check-in
              </label>
              <input 
                type="date" 
                v-model="checkInDate" 
                :min="todayDate" 
                class="bg-transparent text-sm font-bold text-slate-800 outline-none cursor-pointer border-none p-0 focus:ring-0" 
              />
            </div>

            <!-- Check-Out -->
            <div class="flex flex-col px-4 py-2.5 bg-slate-50 hover:bg-white rounded-xl border border-slate-200 transition-all focus-within:ring-2 focus-within:ring-accent focus-within:border-accent">
              <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1">
                <i class="pi pi-calendar-plus text-accent"></i> Check-out
              </label>
              <input 
                type="date" 
                v-model="checkOutDate" 
                :min="checkInDate || todayDate" 
                class="bg-transparent text-sm font-bold text-slate-800 outline-none cursor-pointer border-none p-0 focus:ring-0" 
              />
            </div>

            <!-- Guests & Budget -->
            <div class="flex flex-col px-4 py-2.5 bg-slate-50 hover:bg-white rounded-xl border border-slate-200 transition-all focus-within:ring-2 focus-within:ring-accent focus-within:border-accent">
              <label class="text-[10px] font-black text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1">
                <i class="pi pi-users text-accent"></i> Guests & Suite
              </label>
              <select v-model="guestCount" class="bg-transparent text-sm font-bold text-slate-800 outline-none cursor-pointer border-none p-0 focus:ring-0">
                <option v-for="n in 8" :key="n" :value="n">{{ n }} Guest{{ n > 1 ? 's' : '' }}</option>
              </select>
            </div>

            <!-- Search Action Button -->
            <button 
              @click="triggerSearch" 
              class="w-full h-full min-h-[52px] bg-gradient-to-r from-accent to-orange-500 hover:from-accent-hover hover:to-orange-600 text-white font-extrabold text-sm rounded-xl px-6 py-3.5 flex items-center justify-center gap-2 shadow-accent transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
            >
              <i class="pi pi-search"></i>
              <span>Find Stays</span>
            </button>
          </div>

          <!-- Quick Filters Tags -->
          <div class="flex items-center gap-2 mt-4 pt-3 border-t border-slate-100 flex-wrap text-xs text-slate-500">
            <span class="font-bold text-slate-400">Popular Searches:</span>
            <button @click="quickFilter('Lusaka')" class="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-accent-light hover:text-accent font-semibold transition-colors cursor-pointer">Lusaka Penthouses</button>
            <button @click="quickFilter('Livingstone')" class="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-accent-light hover:text-accent font-semibold transition-colors cursor-pointer">Victoria Falls Lodges</button>
            <button @click="quickFilter('Ndola')" class="px-2.5 py-1 rounded-md bg-slate-100 hover:bg-accent-light hover:text-accent font-semibold transition-colors cursor-pointer">Ndola Executive Suites</button>
          </div>
        </div>

        <!-- Trust Stats Strip -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto mt-12 text-center animate-fade-up-delay-3">
          <div class="bg-white/60 backdrop-blur-md p-4 rounded-xl border border-surface-border">
            <p class="text-2xl sm:text-3xl font-black text-navy">1,200+</p>
            <p class="text-xs text-slate-500 font-semibold mt-1">Verified Stays</p>
          </div>
          <div class="bg-white/60 backdrop-blur-md p-4 rounded-xl border border-surface-border">
            <p class="text-2xl sm:text-3xl font-black text-accent">4.9 ★</p>
            <p class="text-xs text-slate-500 font-semibold mt-1">Average Guest Rating</p>
          </div>
          <div class="bg-white/60 backdrop-blur-md p-4 rounded-xl border border-surface-border">
            <p class="text-2xl sm:text-3xl font-black text-navy">$0</p>
            <p class="text-xs text-slate-500 font-semibold mt-1">Hidden Booking Fees</p>
          </div>
          <div class="bg-white/60 backdrop-blur-md p-4 rounded-xl border border-surface-border">
            <p class="text-2xl sm:text-3xl font-black text-emerald-600">24/7</p>
            <p class="text-xs text-slate-500 font-semibold mt-1">VIP Concierge Support</p>
          </div>
        </div>

      </div>
    </header>

    <!-- DESTINATION DISCOVERY GALLERY -->
    <section class="max-w-content mx-auto px-4 sm:px-6 py-20">
      <div class="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4 reveal-up">
        <div>
          <span class="section-tag">Prime Locations</span>
          <h2 class="section-title">Explore Zambia's Top Destinations</h2>
          <p class="text-slate-500 text-sm mt-1">Handpicked properties in Zambia's most desirable cities and tourism hubs.</p>
        </div>

        <!-- Destination Filter Buttons -->
        <div class="flex items-center gap-1.5 overflow-x-auto pb-2 no-scrollbar">
          <button
            v-for="cityFilter in cityFilters"
            :key="cityFilter"
            @click="activeCityFilter = cityFilter"
            class="px-4 py-2 rounded-full text-xs font-bold transition-all whitespace-nowrap cursor-pointer"
            :class="activeCityFilter === cityFilter ? 'bg-accent text-white shadow-sm' : 'bg-white border border-surface-border text-slate-600 hover:bg-slate-100'"
          >
            {{ cityFilter }}
          </button>
        </div>
      </div>

      <!-- Destination Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 reveal-up delay-100">
        <div
          v-for="destination in filteredDestinations"
          :key="destination.name"
          class="group relative rounded-2xl overflow-hidden cursor-pointer shadow-md hover:shadow-2xl transition-all duration-500 aspect-[4/5] flex flex-col justify-end"
          @click="selectTrendingCity(destination.name)"
        >
          <!-- Background Image -->
          <img 
            :src="destination.image" 
            :alt="destination.name" 
            class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" 
          />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/30 to-transparent"></div>
          
          <!-- Top Badges -->
          <div class="absolute top-4 left-4 right-4 flex justify-between items-center z-10">
            <span class="bg-white/90 backdrop-blur-md text-slate-800 text-xs font-bold px-3 py-1 rounded-full shadow-sm">
              {{ destination.count }} Properties
            </span>
            <span class="bg-navy/80 backdrop-blur-md text-white text-[11px] font-bold px-2.5 py-1 rounded-full flex items-center gap-1">
              <i class="pi pi-sun text-yellow-400"></i> {{ destination.temp }}
            </span>
          </div>

          <!-- Bottom Content -->
          <div class="relative z-10 p-6">
            <span class="text-xs font-bold text-accent uppercase tracking-widest block mb-1">{{ destination.tagline }}</span>
            <h3 class="text-2xl font-black text-white leading-tight mb-2 group-hover:text-amber-300 transition-colors">
              {{ destination.name }}
            </h3>
            <p class="text-white/70 text-xs line-clamp-2 leading-relaxed mb-4">
              {{ destination.description }}
            </p>
            <div class="flex items-center text-white font-bold text-xs group-hover:translate-x-2 transition-transform duration-300">
              <span>Explore {{ destination.name }}</span>
              <i class="pi pi-arrow-right ml-2 text-[10px]"></i>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURED STAYS SHOWCASE -->
    <section class="bg-white border-y border-surface-border py-20">
      <div class="max-w-content mx-auto px-4 sm:px-6">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-10 gap-4 reveal-up">
          <div>
            <span class="section-tag">Handpicked Selection</span>
            <h2 class="section-title">Featured Stays & Luxury Suites</h2>
            <p class="text-slate-500 text-sm mt-1">Inspected for comfort, high-speed Wi-Fi, air conditioning, and top security.</p>
          </div>

          <!-- Property Filter Tabs -->
          <div class="flex items-center gap-2 overflow-x-auto pb-2 no-scrollbar">
            <button
              v-for="category in propertyCategories"
              :key="category"
              @click="activeCategory = category"
              class="px-4 py-2 rounded-full text-xs font-bold transition-all cursor-pointer whitespace-nowrap"
              :class="activeCategory === category ? 'bg-navy text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
            >
              {{ category }}
            </button>
            <router-link to="/apartments" class="text-xs font-bold text-accent hover:text-accent-hover ml-2 whitespace-nowrap no-underline">
              View All ({{ apartmentsStore.apartments.length }}) →
            </router-link>
          </div>
        </div>

        <!-- Skeleton Loader -->
        <div v-if="apartmentsStore.loading" class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div v-for="i in 3" :key="i" class="bg-slate-50 rounded-2xl border border-surface-border overflow-hidden">
            <div class="aspect-[4/3] bg-slate-200 animate-pulse"></div>
            <div class="p-5 flex flex-col gap-3">
              <div class="h-4 bg-slate-200 rounded animate-pulse w-1/3"></div>
              <div class="h-6 bg-slate-200 rounded animate-pulse w-3/4"></div>
              <div class="h-4 bg-slate-200 rounded animate-pulse w-full"></div>
            </div>
          </div>
        </div>

        <!-- Apartments Grid -->
        <div v-else-if="displayApartments.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 reveal-up delay-200">
          <div 
            v-for="apartment in displayApartments" 
            :key="apartment.id"
            class="bg-white rounded-2xl border border-surface-border shadow-card hover:shadow-card-hover transition-all duration-300 hover:-translate-y-1.5 flex flex-col overflow-hidden group cursor-pointer"
            @click="viewApartmentDetail(apartment.id)"
          >
            <!-- Image & Badges -->
            <div class="relative aspect-[4/3] overflow-hidden bg-slate-100">
              <img 
                :src="apartment.image_url || getFallbackImage(apartment.id)" 
                :alt="apartment.title"
                class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              />
              
              <!-- Price Pill -->
              <div class="absolute top-4 left-4 bg-slate-950/85 backdrop-blur-md text-white text-xs font-extrabold px-3.5 py-1.5 rounded-full flex items-center gap-1 shadow-md">
                <span class="text-amber-400 font-semibold">$</span>
                <span class="text-sm">{{ apartment.price_per_night }}</span>
                <span class="text-[10px] font-normal text-slate-300">/ night</span>
              </div>

              <!-- Wishlist Button -->
              <button 
                @click.stop="toggleWishlist(apartment)"
                class="absolute top-4 right-4 w-9 h-9 rounded-full bg-white/90 backdrop-blur-md flex items-center justify-center text-slate-500 hover:text-red-500 hover:scale-110 transition-all duration-200 shadow-sm"
              >
                <i class="pi pi-heart text-sm"></i>
              </button>

              <!-- Verified Pill -->
              <div class="absolute bottom-4 left-4 bg-emerald-500/90 backdrop-blur-md text-white text-[10px] font-bold px-2.5 py-1 rounded-md flex items-center gap-1">
                <i class="pi pi-shield"></i> Apartex Verified
              </div>
            </div>

            <!-- Card Content -->
            <div class="p-6 flex flex-col flex-1 gap-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-accent uppercase tracking-wider flex items-center gap-1">
                  <i class="pi pi-map-marker"></i> {{ apartment.city }}
                </span>
                <span class="text-xs font-bold text-slate-700 flex items-center gap-1 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                  <i class="pi pi-star-fill text-amber-500 text-[10px]"></i> 4.92
                </span>
              </div>

              <h3 class="text-lg font-black text-slate-900 group-hover:text-accent transition-colors line-clamp-1">
                {{ apartment.title }}
              </h3>

              <p class="text-xs text-slate-500 leading-relaxed line-clamp-2">
                {{ apartment.description }}
              </p>

              <!-- Amenities Bar -->
              <div class="flex items-center gap-4 py-2.5 px-3 bg-slate-50 rounded-xl text-xs font-semibold text-slate-600 mt-auto">
                <div class="flex items-center gap-1.5">
                  <i class="pi pi-users text-accent text-xs"></i>
                  <span>{{ apartment.capacity }} Guests</span>
                </div>
                <div class="w-px h-3 bg-slate-300"></div>
                <div class="flex items-center gap-1.5">
                  <i class="pi pi-home text-accent text-xs"></i>
                  <span>{{ apartment.bedrooms }} Beds</span>
                </div>
                <div class="w-px h-3 bg-slate-300"></div>
                <div class="flex items-center gap-1.5">
                  <i class="pi pi-wifi text-accent text-xs"></i>
                  <span>High-speed</span>
                </div>
              </div>

              <!-- Action Bar -->
              <div class="pt-3 border-t border-surface-border flex items-center justify-between">
                <span class="text-xs font-bold text-slate-400">Instant Book</span>
                <span class="text-xs font-extrabold text-accent group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  View Details <i class="pi pi-arrow-right text-[10px]"></i>
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-16 bg-slate-50 rounded-2xl border border-surface-border">
          <i class="pi pi-building text-4xl text-slate-300 mb-3 block"></i>
          <p class="font-bold text-slate-700">No properties available in this category currently.</p>
          <button @click="activeCategory = 'All Stays'" class="btn-accent text-xs mt-4">Reset Filters</button>
        </div>
      </div>
    </section>

    <!-- INTERACTIVE STAY & REWARDS CALCULATOR -->
    <section class="max-w-content mx-auto px-4 sm:px-6 py-12 sm:py-20">
      <div class="bg-gradient-to-br from-slate-900 via-navy-700 to-slate-900 rounded-3xl p-5 sm:p-12 lg:p-16 text-white relative overflow-hidden shadow-2xl">
        <!-- Ambient Glow -->
        <div class="absolute -top-24 -right-24 w-96 h-96 bg-accent/20 rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center relative z-10">
          
          <!-- Left Specs -->
          <div class="lg:col-span-6 flex flex-col gap-6">
            <div>
              <span class="text-xs font-black uppercase tracking-widest text-accent mb-2 block">Interactive Vacation Planner</span>
              <h2 class="text-2xl sm:text-4xl font-black text-white tracking-tight leading-tight">
                Calculate Your Stay & Loyalty Rewards
              </h2>
              <p class="text-slate-300 text-sm sm:text-base leading-relaxed mt-3">
                See how much you save and how many Apartex Club reward points you accumulate on your upcoming trip.
              </p>
            </div>

            <!-- Night Slider -->
            <div class="bg-white/10 backdrop-blur-md rounded-2xl p-5 sm:p-6 border border-white/10">
              <div class="flex justify-between items-center mb-3">
                <label class="text-xs font-bold text-slate-300 uppercase tracking-wider">Number of Nights</label>
                <span class="text-xl font-black text-amber-400">{{ calcNights }} {{ calcNights === 1 ? 'Night' : 'Nights' }}</span>
              </div>
              <input 
                type="range" 
                min="1" 
                max="30" 
                v-model.number="calcNights" 
                class="w-full accent-accent cursor-pointer" 
              />
              <div class="flex justify-between text-[10px] text-slate-400 font-semibold mt-1">
                <span>1 Night</span>
                <span>15 Nights</span>
                <span>30 Nights</span>
              </div>
            </div>

            <!-- Stay Type Selector -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-3">
              <button
                v-for="grade in stayGrades"
                :key="grade.id"
                @click="calcGrade = grade.id"
                class="p-3.5 rounded-xl text-left border transition-all cursor-pointer"
                :class="calcGrade === grade.id ? 'bg-accent border-accent text-white shadow-lg' : 'bg-white/5 border-white/10 text-slate-300 hover:bg-white/10'"
              >
                <p class="text-xs font-bold">{{ grade.label }}</p>
                <p class="text-[11px] opacity-80 mt-1">${{ grade.rate }}/night</p>
              </button>
            </div>
          </div>

          <!-- Right Interactive Reward Card -->
          <div class="lg:col-span-6">
            <div class="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-5 sm:p-8 relative shadow-2xl">
              <div class="flex items-center justify-between border-b border-white/10 pb-6 mb-6">
                <div>
                  <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Estimated Total</p>
                  <p class="text-4xl font-black text-white mt-1">${{ calculatedTotal }} <span class="text-xs font-medium text-slate-400">USD</span></p>
                </div>
                <div class="text-right">
                  <p class="text-xs font-bold text-accent uppercase tracking-wider">Apartex Loyalty Points</p>
                  <p class="text-3xl font-black text-amber-400 mt-1">+{{ calculatedPoints }} <span class="text-xs font-medium text-slate-400">PTS</span></p>
                </div>
              </div>

              <!-- Unlocked Perks -->
              <h4 class="text-xs font-bold text-slate-300 uppercase tracking-widest mb-3">Unlocked Benefits For This Stay:</h4>
              <ul class="flex flex-col gap-3 mb-8">
                <li class="flex items-center gap-3 text-sm text-slate-200">
                  <i class="pi pi-check-circle text-emerald-400"></i>
                  <span>Zero Booking & Service Fees (Save ${{ (calculatedTotal * 0.12).toFixed(0) }})</span>
                </li>
                <li class="flex items-center gap-3 text-sm text-slate-200">
                  <i class="pi pi-check-circle text-emerald-400"></i>
                  <span>Instant Confirmation & Free Cancellation options</span>
                </li>
                <li class="flex items-center gap-3 text-sm text-slate-200" v-if="calcNights >= 5">
                  <i class="pi pi-star-fill text-amber-400"></i>
                  <span class="text-amber-300 font-bold">Bonus: Free VIP Airport Shuttle Included</span>
                </li>
              </ul>

              <router-link 
                to="/apartments" 
                class="w-full btn-accent text-center font-extrabold py-3.5 rounded-xl block no-underline shadow-accent hover:scale-[1.02] transition-transform"
              >
                Book Stay & Earn {{ calculatedPoints }} Points Now
              </router-link>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- VIP LOYALTY CLUB TIER SWITCHER -->
    <section class="max-w-content mx-auto px-4 sm:px-6 py-16">
      <div class="text-center max-w-2xl mx-auto mb-12 reveal-up delay-100">
        <span class="section-tag">Apartex Club</span>
        <h2 class="section-title">Elevate Your Travel Status</h2>
        <p class="text-slate-500 text-sm mt-2">Every night you stay brings higher reward multipliers and exclusive VIP privileges.</p>
      </div>

      <!-- Tier Selection Pills -->
      <div class="flex justify-center items-center gap-2 mb-10 overflow-x-auto pb-2 no-scrollbar">
        <button
          v-for="tier in loyaltyTiers"
          :key="tier.name"
          @click="selectedTier = tier.name"
          class="px-6 py-2.5 rounded-full text-xs font-black transition-all cursor-pointer border"
          :class="selectedTier === tier.name ? 'bg-navy border-navy text-white shadow-md scale-105' : 'bg-white border-surface-border text-slate-600 hover:bg-slate-100'"
        >
          {{ tier.name }} Tier
        </button>
      </div>

      <!-- Active Tier Display Card -->
      <div class="max-w-4xl mx-auto bg-white rounded-3xl border border-surface-border shadow-xl p-8 sm:p-12 grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
        <!-- Digital Card Mockup -->
        <div 
          class="rounded-2xl p-8 text-white relative overflow-hidden shadow-2xl aspect-[1.6/1] flex flex-col justify-between transition-all duration-500"
          :class="activeTierData.cardBg"
        >
          <div class="flex justify-between items-start">
            <div>
              <p class="text-[10px] font-black uppercase tracking-widest opacity-75">Apartex Club VIP</p>
              <p class="text-2xl font-black tracking-wider mt-1">{{ activeTierData.name }} MEMBER</p>
            </div>
            <i class="pi pi-star-fill text-xl text-amber-300"></i>
          </div>

          <div>
            <p class="text-[10px] uppercase tracking-widest opacity-60">Reward Multiplier</p>
            <p class="text-3xl font-black text-amber-300">{{ activeTierData.multiplier }}</p>
          </div>

          <div class="flex justify-between items-end border-t border-white/20 pt-3">
            <div>
              <p class="text-[9px] uppercase tracking-widest opacity-60">Min Nights</p>
              <p class="text-sm font-bold">{{ activeTierData.minNights }} Nights / Year</p>
            </div>
            <span class="text-xs font-black px-3 py-1 bg-white/20 rounded-md backdrop-blur-md">APARTEX VIP</span>
          </div>
        </div>

        <!-- Tier Privileges -->
        <div class="flex flex-col gap-4">
          <span class="text-xs font-bold text-accent uppercase tracking-widest">{{ activeTierData.name }} Privileges</span>
          <h3 class="text-2xl font-black text-slate-900">Why Join {{ activeTierData.name }} Tier?</h3>
          <ul class="flex flex-col gap-3">
            <li v-for="perk in activeTierData.perks" :key="perk" class="flex items-center gap-3 text-sm font-semibold text-slate-700">
              <div class="w-6 h-6 rounded-full bg-accent-light text-accent flex items-center justify-center shrink-0">
                <i class="pi pi-check text-xs"></i>
              </div>
              <span>{{ perk }}</span>
            </li>
          </ul>
          <router-link to="/loyalty" class="inline-flex items-center gap-2 text-sm font-bold text-accent hover:text-accent-hover mt-2 no-underline">
            Explore All Tier Benefits <i class="pi pi-arrow-right text-xs"></i>
          </router-link>
        </div>
      </div>
    </section>

    <!-- HOST & PROPERTY OWNER ROI CALCULATOR -->
    <section class="bg-surface-alt border-y border-surface-border py-20">
      <div class="max-w-content mx-auto px-4 sm:px-6">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          <div class="lg:col-span-6 flex flex-col gap-4">
            <span class="section-tag">For Property Owners</span>
            <h2 class="section-title">Turn Your Luxury Property into Passive Revenue</h2>
            <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
              List your apartment, lodge, or villa on Apartex. Gain access to verified business travelers, tourists, and digital nomads across Zambia.
            </p>

            <ul class="flex flex-col gap-3 my-2">
              <li class="flex items-center gap-3 text-sm font-semibold text-slate-700">
                <i class="pi pi-shield-check text-accent text-base"></i>
                Guest Identity Verification & Property Protection
              </li>
              <li class="flex items-center gap-3 text-sm font-semibold text-slate-700">
                <i class="pi pi-wallet text-accent text-base"></i>
                Direct Payouts via Bank or Mobile Money (MTN / Airtel)
              </li>
              <li class="flex items-center gap-3 text-sm font-semibold text-slate-700">
                <i class="pi pi-chart-line text-accent text-base"></i>
                Real-time Owner Dashboard with Analytics & Booking Control
              </li>
            </ul>

            <router-link to="/register?role=owner" class="btn-accent text-center sm:w-fit px-8 py-3.5 text-sm font-bold no-underline shadow-md">
              Become a Host Today
            </router-link>
          </div>

          <!-- Host Revenue Estimator Widget -->
          <div class="lg:col-span-6">
            <div class="bg-white rounded-3xl border border-surface-border p-5 sm:p-8 shadow-xl">
              <h3 class="text-lg font-black text-slate-900 mb-6 flex items-center gap-2">
                <i class="pi pi-calculator text-accent"></i> Host Monthly Revenue Estimator
              </h3>

              <!-- City Selection -->
              <div class="mb-5">
                <label class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2 block">Property City</label>
                <select v-model="hostCity" class="w-full input-base !py-2.5 text-sm font-semibold">
                  <option value="Lusaka">Lusaka (High Demand)</option>
                  <option value="Livingstone">Livingstone (Tourism Hub)</option>
                  <option value="Ndola">Ndola (Business Hub)</option>
                  <option value="Kitwe">Kitwe (Commercial Hub)</option>
                </select>
              </div>

              <!-- Bedrooms Slider -->
              <div class="mb-6">
                <div class="flex justify-between items-center mb-2">
                  <label class="text-xs font-bold text-slate-500 uppercase tracking-wider">Number of Bedrooms</label>
                  <span class="text-sm font-extrabold text-navy">{{ hostBedrooms }} Bedrooms</span>
                </div>
                <input type="range" min="1" max="5" v-model.number="hostBedrooms" class="w-full accent-accent" />
              </div>

              <!-- Monthly Result Box -->
              <div class="bg-accent-light rounded-2xl p-6 border border-orange-200 text-center">
                <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Estimated Monthly Earnings</p>
                <p class="text-4xl font-black text-accent my-2">${{ estimatedHostIncome }} <span class="text-xs text-slate-500 font-normal">/ month</span></p>
                <p class="text-xs text-slate-500">Based on an average 72% monthly occupancy rate in {{ hostCity }}.</p>
              </div>

              <router-link to="/register?role=owner" class="w-full mt-6 bg-navy text-white text-center font-bold text-sm py-3.5 rounded-xl block no-underline hover:bg-slate-800 transition-colors">
                List Property in {{ hostCity }}
              </router-link>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- VERIFIED TRAVELER REVIEWS & SOCIAL PROOF -->
    <section class="max-w-content mx-auto px-4 sm:px-6 py-20">
      <div class="text-center max-w-2xl mx-auto mb-14 reveal-up">
        <span class="section-tag">Traveler Experiences</span>
        <h2 class="section-title">Loved by Guests Across Zambia</h2>
        <div class="flex items-center justify-center gap-2 mt-3">
          <div class="flex gap-1 text-amber-400 text-sm">
            <i v-for="s in 5" :key="s" class="pi pi-star-fill"></i>
          </div>
          <span class="text-sm font-bold text-slate-800">4.9 / 5.0 Rating</span>
          <span class="text-slate-400 text-xs">(3,400+ Verified Reviews)</span>
        </div>
      </div>

      <!-- Reviews Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 reveal-up delay-100">
        <div 
          v-for="review in reviews" 
          :key="review.author" 
          class="bg-white rounded-2xl border border-surface-border p-7 shadow-sm hover:shadow-md transition-all flex flex-col justify-between"
        >
          <div class="flex flex-col gap-3">
            <div class="flex justify-between items-center">
              <div class="flex gap-0.5 text-amber-400 text-xs">
                <i v-for="s in 5" :key="s" class="pi pi-star-fill"></i>
              </div>
              <span class="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                <i class="pi pi-check-circle text-[9px]"></i> Verified Booking
              </span>
            </div>

            <p class="text-slate-600 text-sm leading-relaxed italic">
              "{{ review.text }}"
            </p>
          </div>

          <div class="flex items-center gap-3 pt-4 border-t border-slate-100 mt-6">
            <div class="w-10 h-10 rounded-full bg-navy text-white font-black text-sm flex items-center justify-center shrink-0 shadow-sm">
              {{ review.initials }}
            </div>
            <div>
              <p class="font-bold text-sm text-slate-900">{{ review.author }}</p>
              <p class="text-xs text-slate-400 flex items-center gap-1">
                <i class="pi pi-map-marker text-[10px]"></i> Stayed in {{ review.city }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- INTERACTIVE FAQ ACCORDION -->
    <section class="bg-white border-t border-surface-border py-20">
      <div class="max-w-3xl mx-auto px-4 sm:px-6">
        <div class="text-center mb-12">
          <span class="section-tag">Clear Answers</span>
          <h2 class="section-title">Frequently Asked Questions</h2>
          <p class="text-slate-500 text-sm mt-1">Everything you need to know about booking, payments, and hosting.</p>
        </div>

        <div class="flex flex-col gap-4">
          <div
            v-for="(faq, index) in faqs"
            :key="index"
            class="border border-surface-border rounded-2xl overflow-hidden transition-all"
            :class="openFaqIndex === index ? 'bg-slate-50 border-slate-300 shadow-sm' : 'bg-white'"
          >
            <button
              @click="openFaqIndex = openFaqIndex === index ? -1 : index"
              class="w-full text-left p-6 font-bold text-slate-900 text-base flex justify-between items-center gap-4 cursor-pointer"
            >
              <span>{{ faq.question }}</span>
              <i :class="openFaqIndex === index ? 'pi pi-chevron-up text-accent' : 'pi pi-chevron-down text-slate-400'"></i>
            </button>

            <div v-show="openFaqIndex === index" class="px-6 pb-6 text-sm text-slate-600 leading-relaxed border-t border-slate-200/60 pt-4">
              {{ faq.answer }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- NEWSLETTER & FOOTER BANNER -->
    <footer class="bg-slate-950 text-white border-t border-slate-800">
      <!-- Newsletter Row -->
      <div class="border-b border-slate-800 py-12">
        <div class="max-w-content mx-auto px-4 sm:px-6 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div class="lg:col-span-7">
            <h3 class="text-2xl font-black text-white">Join the Apartex VIP Travelers Club</h3>
            <p class="text-slate-400 text-sm mt-1">Get exclusive access to unlisted luxury villas, early-bird discounts, and travel perks.</p>
          </div>
          <div class="lg:col-span-5 flex gap-2">
            <input 
              type="email" 
              v-model="newsletterEmail" 
              placeholder="Enter your email address" 
              class="input-base !bg-slate-900 !border-slate-800 !text-white placeholder-slate-500 text-sm"
            />
            <button @click="subscribeNewsletter" class="btn-accent shrink-0 font-bold px-6">
              Subscribe
            </button>
          </div>
        </div>
      </div>

      <!-- Links Grid -->
      <div class="max-w-content mx-auto px-4 sm:px-6 py-16 grid grid-cols-1 md:grid-cols-4 gap-10">
        <div class="col-span-1">
          <div class="flex items-center gap-2 text-xl font-black tracking-tight text-white mb-4">
            <div class="w-8 h-8 rounded-lg bg-accent text-white flex items-center justify-center text-sm">
              <i class="pi pi-building"></i>
            </div>
            APARTEX
          </div>
          <p class="text-sm text-slate-400 leading-relaxed mb-6">
            Zambia's premier luxury apartment and vacation lodge ecosystem. Redefining accommodation discovery with zero hidden fees.
          </p>
          <div class="flex gap-3">
            <a href="#" class="w-9 h-9 rounded-full border border-slate-800 flex items-center justify-center text-slate-400 hover:border-accent hover:text-accent transition-colors"><i class="pi pi-facebook text-sm"></i></a>
            <a href="#" class="w-9 h-9 rounded-full border border-slate-800 flex items-center justify-center text-slate-400 hover:border-accent hover:text-accent transition-colors"><i class="pi pi-twitter text-sm"></i></a>
            <a href="#" class="w-9 h-9 rounded-full border border-slate-800 flex items-center justify-center text-slate-400 hover:border-accent hover:text-accent transition-colors"><i class="pi pi-instagram text-sm"></i></a>
          </div>
        </div>

        <div>
          <h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">Quick Links</h4>
          <ul class="flex flex-col gap-2.5 text-sm text-slate-400">
            <li><router-link to="/" class="hover:text-white no-underline transition-colors">Home</router-link></li>
            <li><router-link to="/apartments" class="hover:text-white no-underline transition-colors">Explore All Stays</router-link></li>
            <li><router-link to="/loyalty" class="hover:text-white no-underline transition-colors">Apartex Club Rewards</router-link></li>
            <li><router-link to="/register?role=owner" class="hover:text-white no-underline transition-colors">List Your Property</router-link></li>
          </ul>
        </div>

        <div>
          <h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">Top Destinations</h4>
          <ul class="flex flex-col gap-2.5 text-sm text-slate-400">
            <li><button @click="selectTrendingCity('Lusaka')" class="hover:text-white transition-colors cursor-pointer bg-transparent border-none p-0 text-left">Lusaka Luxury Apartments</button></li>
            <li><button @click="selectTrendingCity('Livingstone')" class="hover:text-white transition-colors cursor-pointer bg-transparent border-none p-0 text-left">Livingstone Victoria Falls</button></li>
            <li><button @click="selectTrendingCity('Ndola')" class="hover:text-white transition-colors cursor-pointer bg-transparent border-none p-0 text-left">Ndola Executive Suites</button></li>
            <li><button @click="selectTrendingCity('Kitwe')" class="hover:text-white transition-colors cursor-pointer bg-transparent border-none p-0 text-left">Kitwe Lodges</button></li>
          </ul>
        </div>

        <div>
          <h4 class="text-xs font-bold uppercase tracking-widest text-slate-400 mb-4">Accepted Payments</h4>
          <p class="text-xs text-slate-400 mb-4">Secure instant payment via Airtel Money, MTN Mobile Money, or Credit Card.</p>
          <div class="flex flex-wrap gap-2 text-xs font-bold text-slate-300">
            <span class="px-2.5 py-1 rounded bg-slate-900 border border-slate-800">MTN Mobile Money</span>
            <span class="px-2.5 py-1 rounded bg-slate-900 border border-slate-800">Airtel Money</span>
            <span class="px-2.5 py-1 rounded bg-slate-900 border border-slate-800">Visa / Mastercard</span>
          </div>
        </div>
      </div>

      <div class="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        <div class="max-w-content mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>&copy; 2026 Apartex Ecosystem. All rights reserved. Created by Zakir Motala.</p>
          <div class="flex gap-4">
            <a href="#" class="hover:text-slate-300 no-underline">Privacy Policy</a>
            <a href="#" class="hover:text-slate-300 no-underline">Terms of Service</a>
            <a href="#" class="hover:text-slate-300 no-underline">Security</a>
          </div>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import { useWishlistStore } from '@/stores/wishlist';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'primevue/usetoast';

const router = useRouter();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();
const authStore = useAuthStore();
const toast = useToast();

// ── Scroll Reveal ────────────────────────────────────────────
function useScrollReveal() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
        }
      });
    },
    { threshold: 0.1 }
  );

  onMounted(() => {
    document.querySelectorAll('.reveal-up').forEach((el) => observer.observe(el));
  });

  onUnmounted(() => observer.disconnect());
}

useScrollReveal();

// Search State
const selectedCity = ref('');
const checkInDate = ref('');
const checkOutDate = ref('');
const guestCount = ref(1);
const todayDate = new Date().toISOString().split('T')[0];

const activeSearchTab = ref('stays');
const searchTabs = [
  { id: 'stays', label: 'All Stays', icon: 'pi pi-home' },
  { id: 'penthouses', label: 'Luxury Penthouses', icon: 'pi pi-star' },
  { id: 'monthly', label: 'Long-Term Stays', icon: 'pi pi-calendar' }
];

const cities = ['Lusaka', 'Livingstone', 'Ndola', 'Kitwe'];

// Destination Filter
const activeCityFilter = ref('All Cities');
const cityFilters = ['All Cities', 'Lusaka', 'Livingstone', 'Ndola', 'Kitwe'];

const destinationList = [
  { 
    name: 'Lusaka', 
    count: '14', 
    temp: '26°C', 
    tagline: 'Capital Luxury', 
    description: 'Modern high-rise penthouses, corporate suites, and private villas in Kabulonga & Rhodes Park.', 
    image: 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80' 
  },
  { 
    name: 'Livingstone', 
    count: '9', 
    temp: '29°C', 
    tagline: 'Victoria Falls', 
    description: 'Riverside cottages, luxury safari lodges, and eco-retreats along the Zambezi River.', 
    image: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80' 
  },
  { 
    name: 'Ndola', 
    count: '7', 
    temp: '25°C', 
    tagline: 'Copperbelt Central', 
    description: 'Quiet executive apartments and private guesthouses tailored for business travelers.', 
    image: 'https://images.unsplash.com/photo-1449034446853-66c86144b0ad?auto=format&fit=crop&w=800&q=80' 
  },
  { 
    name: 'Kitwe', 
    count: '5', 
    temp: '27°C', 
    tagline: 'Commercial Hub', 
    description: 'Modern serviced suites near Nkana Golf Club and Riverside commercial district.', 
    image: 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80' 
  }
];

const filteredDestinations = computed(() => {
  if (activeCityFilter.value === 'All Cities') return destinationList;
  return destinationList.filter(d => d.name === activeCityFilter.value);
});

// Property Categories & Filtering
const activeCategory = ref('All Stays');
const propertyCategories = ['All Stays', 'Top Rated', 'Executive Suites', 'Safari Lodges'];

const displayApartments = computed(() => {
  let list = apartmentsStore.apartments;
  if (!list || list.length === 0) return [];
  if (activeCategory.value === 'Top Rated') return list.slice().sort((a, b) => b.price_per_night - a.price_per_night);
  if (activeCategory.value === 'Executive Suites') return list.filter(a => a.bedrooms >= 2);
  if (activeCategory.value === 'Safari Lodges') return list.filter(a => a.city === 'Livingstone');
  return list.slice(0, 6);
});

// Stay & Rewards Calculator
const calcNights = ref(5);
const calcGrade = ref('executive');
const stayGrades = [
  { id: 'standard', label: 'Standard Suite', rate: 65 },
  { id: 'executive', label: 'Executive Suite', rate: 120 },
  { id: 'penthouse', label: 'Luxury Penthouse', rate: 240 }
];

const calculatedTotal = computed(() => {
  const gradeObj = stayGrades.find(g => g.id === calcGrade.value);
  const rate = gradeObj ? gradeObj.rate : 120;
  return calcNights.value * rate;
});

const calculatedPoints = computed(() => {
  return calculatedTotal.value * 5;
});

// VIP Loyalty Tier Switcher
const selectedTier = ref('Gold');
const loyaltyTiers = [
  { 
    name: 'Bronze', 
    multiplier: '1.0x', 
    minNights: 0, 
    cardBg: 'bg-gradient-to-br from-amber-700 via-amber-800 to-slate-900 border border-amber-500/30',
    perks: ['Earn 5 points per $1 spent', 'Standard cancellation windows', 'Digital member pass'] 
  },
  { 
    name: 'Silver', 
    multiplier: '1.25x', 
    minNights: 5, 
    cardBg: 'bg-gradient-to-br from-slate-400 via-slate-600 to-slate-900 border border-slate-300/30',
    perks: ['Earn 6.25 points per $1 spent', 'Late check-out upon request', '5% discount on long stays'] 
  },
  { 
    name: 'Gold', 
    multiplier: '1.5x', 
    minNights: 15, 
    cardBg: 'bg-gradient-to-br from-amber-400 via-yellow-600 to-slate-950 border border-amber-300/40',
    perks: ['Earn 7.5 points per $1 spent', 'Free room upgrade when available', 'Dedicated VIP concierge line', 'Zero cancellation penalties'] 
  },
  { 
    name: 'Platinum', 
    multiplier: '2.0x', 
    minNights: 30, 
    cardBg: 'bg-gradient-to-br from-purple-700 via-slate-900 to-black border border-purple-400/40',
    perks: ['Double points on all stays', 'Free Airport Shuttle Transfers', 'Guaranteed late check-out', 'Exclusive access to unlisted luxury villas'] 
  }
];

const activeTierData = computed(() => {
  return loyaltyTiers.find(t => t.name === selectedTier.value) || loyaltyTiers[2];
});

// Host Revenue Calculator
const hostCity = ref('Lusaka');
const hostBedrooms = ref(2);

const estimatedHostIncome = computed(() => {
  const cityRates = { 'Lusaka': 95, 'Livingstone': 110, 'Ndola': 75, 'Kitwe': 70 };
  const baseRate = cityRates[hostCity.value] || 85;
  const nightsPerMonth = 22; // ~72% occupancy
  return Math.round(baseRate * hostBedrooms.value * 0.85 * nightsPerMonth);
});

// Verified Reviews
const reviews = [
  {
    text: 'Apartex made our stay in Lusaka effortless. The apartment in Rhodes Park exceeded expectations—spotless, fast Wi-Fi, and 24/7 security. The loyalty points saved us on our next trip!',
    author: 'Sharon Phiri',
    initials: 'SP',
    city: 'Lusaka'
  },
  {
    text: 'Booking our Victoria Falls retreat through Apartex was smooth. Zero hidden fees, clear pricing, and instant communication with the owner.',
    author: 'Mwansa Kabwe',
    initials: 'MK',
    city: 'Livingstone'
  },
  {
    text: 'As a frequent business traveler between Ndola and Lusaka, the VIP Gold tier benefits are unbeatable. Quick check-in and reliable solar backup power!',
    author: 'Daniel Zulu',
    initials: 'DZ',
    city: 'Ndola'
  }
];

// FAQs
const openFaqIndex = ref(0);
const faqs = [
  {
    question: 'How does booking work on Apartex?',
    answer: 'Simply search your target city and dates, choose your preferred verified apartment or lodge, and complete instant reservation. You will receive an immediate confirmation code and direct host contact info.'
  },
  {
    question: 'Are there any hidden booking fees?',
    answer: 'No. Apartex guarantees zero service markups. The price per night shown is the final price you pay.'
  },
  {
    question: 'What payment methods are supported in Zambia?',
    answer: 'We support all major payment options including Airtel Money, MTN Mobile Money, Visa, Mastercard, and Bank Direct Transfers.'
  },
  {
    question: 'How do I earn and redeem Apartex VIP Loyalty points?',
    answer: 'Every completed stay automatically credits your account with loyalty points (5 to 10 points per $1 spent depending on your tier). Points can be redeemed for free extra nights, upgrades, or discount vouchers during checkout.'
  },
  {
    question: 'How can I list my property as a host?',
    answer: 'Click "List Your Property" or Register as an Owner account. Submit your property details and photo gallery. Our team verifies the listing within 24 hours to ensure high quality.'
  }
];

// Newsletter State
const newsletterEmail = ref('');

const subscribeNewsletter = () => {
  if (!newsletterEmail.value || !newsletterEmail.value.includes('@')) {
    toast?.add({ severity: 'error', summary: 'Invalid Email', detail: 'Please enter a valid email address.', life: 3000 });
    return;
  }
  toast?.add({ severity: 'success', summary: 'Subscribed!', detail: 'Thank you for joining the Apartex VIP Travelers list.', life: 4000 });
  newsletterEmail.value = '';
};

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

const quickFilter = (cityName) => {
  selectedCity.value = cityName;
  triggerSearch();
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

const toggleWishlist = async (apartment) => {
  if (!authStore.user) {
    router.push('/login');
    return;
  }
  const isWishlisted = wishlistStore.isWishlisted(apartment.id);
  if (isWishlisted) {
    await wishlistStore.removeFromWishlist(apartment.id);
    toast?.add({ severity: 'info', summary: 'Removed from Wishlist', detail: apartment.title, life: 2000 });
  } else {
    await wishlistStore.addToWishlist(apartment.id);
    toast?.add({ severity: 'success', summary: 'Saved to Wishlist', detail: apartment.title, life: 2000 });
  }
};

const getFallbackImage = (id) => {
  const photos = [
    'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80',
    'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=800&q=80'
  ];
  return photos[id % photos.length];
};
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>