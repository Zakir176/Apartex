<template>
  <div class="home-container">
    <!-- Ambient glowing backgrounds -->
    <div class="ambient-glow bg-glow-1"></div>
    <div class="ambient-glow bg-glow-2"></div>
    
    <!-- 🌌 HERO SECTION -->
    <header class="hero-section">
      <div class="hero-header-content">
        <span class="hero-badge">✨ Discover Zambia's Premium Stays</span>
        <h1 class="hero-title">
          Where Comfort Meets <span class="text-gradient">Luxury</span>
        </h1>
        <p class="hero-subtitle">
          Book handpicked premium apartments, boutique suites, and scenic cottages for your next getaway.
        </p>
      </div>

      <!-- Glassmorphic Search Dashboard -->
      <div class="search-dashboard-wrapper">
        <div class="search-tabs">
          <button 
            v-for="tab in tabs" 
            :key="tab.id" 
            class="tab-btn" 
            :class="{ active: activeTab === tab.id }"
            @click="activeTab = tab.id"
          >
            <i :class="tab.icon"></i>
            <span>{{ tab.label }}</span>
          </button>
        </div>
        
        <div class="search-inputs-grid">
          <!-- Destination Field -->
          <div class="input-block">
            <label class="input-label"><i class="pi pi-map-marker"></i> Where to?</label>
            <div class="dropdown-wrapper">
              <select v-model="selectedCity" class="custom-select">
                <option value="">Select a city...</option>
                <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
              </select>
            </div>
          </div>

          <!-- Check-in Date -->
          <div class="input-block">
            <label class="input-label"><i class="pi pi-calendar"></i> Check-in</label>
            <input type="date" v-model="checkInDate" class="custom-date-input" :min="todayDate" />
          </div>

          <!-- Check-out Date -->
          <div class="input-block">
            <label class="input-label"><i class="pi pi-calendar"></i> Check-out</label>
            <input type="date" v-model="checkOutDate" class="custom-date-input" :min="checkInDate || todayDate" />
          </div>

          <!-- Guests Selector -->
          <div class="input-block">
            <label class="input-label"><i class="pi pi-users"></i> Guests</label>
            <div class="dropdown-wrapper">
              <select v-model="guestCount" class="custom-select">
                <option v-for="n in 6" :key="n" :value="n">{{ n }} Guest{{ n > 1 ? 's' : '' }}</option>
              </select>
            </div>
          </div>

          <!-- Action Button -->
          <div class="search-action-block">
            <button @click="triggerSearch" class="btn-search-trigger">
              <i class="pi pi-search"></i>
              <span>Find Stay</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 🗺️ TRENDING DESTINATIONS SECTION -->
    <section class="home-section text-center">
      <div class="section-header">
        <span class="section-tag">Explore Zambia</span>
        <h2 class="section-title">Trending Destinations</h2>
        <p class="section-subtitle">Browse properties in our most sought-after cities</p>
      </div>

      <div class="destinations-grid">
        <div 
          v-for="destination in destinationList" 
          :key="destination.name" 
          class="destination-card"
          @click="selectTrendingCity(destination.name)"
        >
          <div class="dest-image-wrapper">
            <img :src="destination.image" :alt="destination.name" class="dest-image" />
            <div class="dest-overlay">
              <div class="dest-info">
                <h3 class="dest-name">{{ destination.name }}</h3>
                <span class="dest-badge">{{ destination.count }} Properties</span>
              </div>
              <div class="dest-arrow">
                <i class="pi pi-arrow-up-right"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 🏢 FEATURED APARTMENTS -->
    <section class="home-section bg-gradient-alt">
      <div class="section-header flex flex-column md:flex-row align-items-center justify-content-between mb-6 gap-3">
        <div>
          <span class="section-tag">Curated Collection</span>
          <h2 class="section-title m-0">Featured Premium Stays</h2>
          <p class="section-subtitle">Exquisite design and high-end comfort matched together</p>
        </div>
        <router-link to="/apartments" class="btn-secondary-custom">
          <span>View All Apartments</span>
          <i class="pi pi-arrow-right"></i>
        </router-link>
      </div>

      <div v-if="apartmentsStore.loading" class="loading-grid">
        <div v-for="i in 3" :key="i" class="loading-skeleton-card">
          <div class="skeleton-img"></div>
          <div class="skeleton-body">
            <div class="skeleton-line w-8"></div>
            <div class="skeleton-line w-6"></div>
          </div>
        </div>
      </div>

      <div v-else class="apartments-grid">
        <div 
          v-for="apartment in apartmentsStore.featuredApartments" 
          :key="apartment.id"
          class="premium-apartment-card"
          @click="viewApartmentDetail(apartment.id)"
        >
          <div class="card-image-section">
            <img 
              :src="apartment.image_url || 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80'" 
              :alt="apartment.title" 
              class="card-img" 
            />
            <div class="card-price-pill">
              <span class="price-val">${{ apartment.price_per_night }}</span>
              <span class="price-unit">/ night</span>
            </div>
            <div class="card-badges">
              <span class="badge-pill rating-badge">
                <i class="pi pi-star-fill"></i>
                <span>4.9</span>
              </span>
              <span class="badge-pill tag-badge">Premium</span>
            </div>
          </div>
          
          <div class="card-details-section">
            <span class="card-location"><i class="pi pi-map-marker"></i> {{ apartment.city }}, Zambia</span>
            <h3 class="card-title">{{ apartment.title }}</h3>
            
            <div class="card-amenities-strip">
              <span><i class="pi pi-users"></i> Up to {{ apartment.capacity }} Guests</span>
              <span class="dot-separator">•</span>
              <span><i class="pi pi-home"></i> {{ apartment.bedrooms }} Bed{{ apartment.bedrooms > 1 ? 's' : '' }}</span>
            </div>

            <div class="card-footer-trigger">
              <span class="btn-details">Explore Details</span>
              <i class="pi pi-arrow-right"></i>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="!apartmentsStore.loading && apartmentsStore.featuredApartments.length === 0"
        class="empty-fallback-card text-center py-8"
      >
        <div class="empty-icon-circle mb-4">🏠</div>
        <h3 class="text-xl font-bold text-900 mb-2">No Featured Collections</h3>
        <p class="text-500 max-w-sm mx-auto mb-4">We are currently curating premium properties. Check back shortly!</p>
      </div>
    </section>

    <!-- 🔑 VALUE PROPOSITIONS -->
    <section class="home-section text-center">
      <div class="section-header">
        <span class="section-tag">Apartex Standard</span>
        <h2 class="section-title">Designed for Discerning Travelers</h2>
        <p class="section-subtitle">Experience hospitality defined by excellence and security</p>
      </div>

      <div class="perks-grid">
        <div v-for="perk in perks" :key="perk.title" class="perk-card">
          <div class="perk-icon-circle" :style="{ background: perk.bg }">
            <i :class="[perk.icon, perk.color]"></i>
          </div>
          <h3 class="perk-title">{{ perk.title }}</h3>
          <p class="perk-desc">{{ perk.description }}</p>
        </div>
      </div>
    </section>

    <!-- 💎 LOYALTY CLUB PREVIEW -->
    <section class="home-section bg-gradient-alt relative overflow-hidden">
      <div class="loyalty-teaser-wrapper">
        <div class="grid align-items-center gap-6">
          <div class="col-12 lg:col-6 text-left">
            <span class="section-tag">Apartex Club</span>
            <h2 class="section-title text-left m-0 mb-4">Unlock Premium Rewards</h2>
            <p class="text-600 text-lg line-height-3 mb-5">
              Every booking unlocks points that elevate your travel tier. Progress from Bronze to Gold status and enjoy free room upgrades, late check-outs, and exclusive VIP cashbacks.
            </p>
            
            <div class="loyalty-perks-list flex flex-column gap-3 mb-6">
              <div class="loyalty-perk-item flex align-items-center gap-3">
                <i class="pi pi-check-circle text-primary-500 text-xl"></i>
                <span class="font-semibold text-800">Earn points on every night spent</span>
              </div>
              <div class="loyalty-perk-item flex align-items-center gap-3">
                <i class="pi pi-check-circle text-primary-500 text-xl"></i>
                <span class="font-semibold text-800">Redeem rewards for discount bookings</span>
              </div>
              <div class="loyalty-perk-item flex align-items-center gap-3">
                <i class="pi pi-check-circle text-primary-500 text-xl"></i>
                <span class="font-semibold text-800">Enjoy lifetime tier benefits</span>
              </div>
            </div>

            <router-link to="/loyalty" class="btn-primary-custom">
              <span>View Loyalty Perks</span>
              <i class="pi pi-star-fill ml-2"></i>
            </router-link>
          </div>
          
          <div class="col-12 lg:col-6 flex justify-content-center">
            <!-- Simulated Loyalty Card UI -->
            <div class="loyalty-preview-card">
              <div class="card-inner-glow"></div>
              <div class="flex justify-content-between align-items-start mb-6">
                <div>
                  <span class="card-brand">APARTEX CLUB</span>
                  <div class="card-tier-title">GOLD TIER</div>
                </div>
                <div class="card-vip-badge">VIP VIP</div>
              </div>
              <div class="mb-5">
                <span class="card-holder-label">CARD HOLDER</span>
                <div class="card-holder-name">Demo Traveler</div>
              </div>
              <div class="flex justify-content-between align-items-end">
                <div>
                  <span class="card-points-label">MEMBERSHIP POINTS</span>
                  <div class="card-points-val">4,250 PTS</div>
                </div>
                <div class="card-chip-icon">
                  <i class="pi pi-id-card text-4xl text-yellow-500"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 👤 TESTIMONIALS -->
    <section class="home-section text-center">
      <div class="section-header">
        <span class="section-tag">Traveler Stories</span>
        <h2 class="section-title">Loved by Travelers Worldwide</h2>
        <p class="section-subtitle">Read what our guests say about their premium stays</p>
      </div>

      <div class="testimonials-grid">
        <div v-for="review in reviews" :key="review.author" class="testimonial-card">
          <div class="flex align-items-center gap-1 text-yellow-500 mb-4 justify-content-center">
            <i v-for="star in 5" :key="star" class="pi pi-star-fill"></i>
          </div>
          <p class="testimonial-text">"{{ review.text }}"</p>
          <div class="flex align-items-center gap-3 justify-content-center mt-5">
            <div class="review-avatar bg-primary-100 text-primary-700 font-bold">
              {{ review.initials }}
            </div>
            <div class="text-left">
              <h4 class="review-author m-0">{{ review.author }}</h4>
              <span class="review-status text-500"><i class="pi pi-shield-check text-green-500"></i> Verified Guest</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 📩 PREMIUM BRAND FOOTER -->
    <footer class="app-footer">
      <div class="footer-grid">
        <div class="footer-col brand-col">
          <h2 class="footer-brand">Apartex</h2>
          <p class="footer-about">
            Redefining contemporary urban living and temporary stays with handpicked luxury collections across Zambia.
          </p>
          <div class="footer-socials flex gap-3 mt-4">
            <a href="#" class="social-icon"><i class="pi pi-facebook"></i></a>
            <a href="#" class="social-icon"><i class="pi pi-twitter"></i></a>
            <a href="#" class="social-icon"><i class="pi pi-instagram"></i></a>
            <a href="#" class="social-icon"><i class="pi pi-linkedin"></i></a>
          </div>
        </div>
        
        <div class="footer-col">
          <h3 class="footer-header">Quick Links</h3>
          <ul class="footer-links">
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/apartments">Explore Stays</router-link></li>
            <li><router-link to="/bookings">Reservations</router-link></li>
            <li><router-link to="/loyalty">Loyalty Club</router-link></li>
          </ul>
        </div>
        
        <div class="footer-col">
          <h3 class="footer-header">Destinations</h3>
          <ul class="footer-links">
            <li><a href="#" @click.prevent="selectTrendingCity('Lusaka')">Lusaka Apartments</a></li>
            <li><a href="#" @click.prevent="selectTrendingCity('Livingstone')">Livingstone Cottages</a></li>
            <li><a href="#" @click.prevent="selectTrendingCity('Ndola')">Ndola Business Suites</a></li>
          </ul>
        </div>

        <div class="footer-col newsletter-col">
          <h3 class="footer-header">Subscribe Newsletter</h3>
          <p class="footer-desc">Stay updated on premium properties and exclusive member offers.</p>
          <div class="newsletter-form mt-4">
            <input type="email" placeholder="Your email address" class="newsletter-input" />
            <button class="btn-newsletter-subscribe"><i class="pi pi-send"></i></button>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom flex flex-column md:flex-row align-items-center justify-content-between">
        <p class="m-0 text-500 text-sm">&copy; 2026 Apartex Inc. All rights reserved.</p>
        <div class="flex gap-4 mt-3 md:mt-0">
          <a href="#" class="text-500 text-sm">Privacy Policy</a>
          <a href="#" class="text-500 text-sm">Terms of Service</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';

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
    icon: 'pi pi-shield',
    color: 'text-indigo-500',
    bg: 'rgba(99, 102, 241, 0.1)'
  },
  {
    title: 'Zero Booking Fees',
    description: 'Direct bookings with no hidden service charges. Best price guaranteed.',
    icon: 'pi pi-wallet',
    color: 'text-emerald-500',
    bg: 'rgba(16, 185, 129, 0.1)'
  },
  {
    title: 'VIP Loyalty Program',
    description: 'Accumulate reward points with every night stay and redeem free stays/payout benefits.',
    icon: 'pi pi-star',
    color: 'text-amber-500',
    bg: 'rgba(245, 158, 11, 0.1)'
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

<style scoped>
/* Core Container with Dark elegant theme baseline */
.home-container {
  width: 100%;
  position: relative;
  background-color: #0b0914; /* Deep dark purple-toned midnight */
  color: #f4f4f5;
  overflow: hidden;
  font-family: 'Outfit', 'Inter', sans-serif;
  min-height: 100%;
  padding-bottom: 0;
}

/* Background glowing blur elements */
.ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(140px);
  z-index: 0;
  pointer-events: none;
  opacity: 0.15;
}
.bg-glow-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #6366f1, #3b82f6);
  top: -100px;
  right: -50px;
}
.bg-glow-2 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, #a855f7, #6366f1);
  top: 40%;
  left: -150px;
}

/* 🌌 HERO SECTION */
.hero-section {
  position: relative;
  width: 100%;
  padding: 8rem 2rem 6rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  z-index: 2;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  padding: 0.5rem 1.25rem;
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #c084fc;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.hero-title {
  font-size: 4.25rem;
  font-weight: 800;
  line-height: 1.15;
  margin: 0 0 1.5rem 0;
  letter-spacing: -0.03em;
  color: #ffffff;
  max-width: 900px;
}

.text-gradient {
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 1.35rem;
  color: #a1a1aa;
  max-width: 680px;
  margin: 0 auto 4rem auto;
  line-height: 1.6;
}

/* Glassmorphic Search Dashboard widget */
.search-dashboard-wrapper {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 24px;
  padding: 1.75rem;
  width: 100%;
  max-width: 1100px;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.8);
  animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

.search-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding-bottom: 1rem;
}

.tab-btn {
  background: transparent;
  border: none;
  color: #71717a;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.tab-btn i {
  font-size: 1rem;
}

.tab-btn:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.02);
}

.tab-btn.active {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.search-inputs-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr 1fr 1fr 0.8fr;
  gap: 1.25rem;
  align-items: end;
  text-align: left;
}

.input-block {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #a1a1aa;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.dropdown-wrapper {
  position: relative;
  width: 100%;
}

.custom-select, .custom-date-input {
  width: 100%;
  padding: 0.9rem 1.2rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  color: #ffffff;
  font-size: 0.95rem;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.custom-select:focus, .custom-date-input:focus {
  border-color: #a855f7;
  background: rgba(255, 255, 255, 0.06);
  box-shadow: 0 0 10px rgba(168, 85, 247, 0.2);
}

/* Custom select dropdown styling */
.custom-select option {
  background: #181524;
  color: #ffffff;
}

.btn-search-trigger {
  width: 100%;
  padding: 0.95rem 1.5rem;
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  border: none;
  border-radius: 14px;
  color: #ffffff;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  transition: all 0.3s ease;
  box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
}

.btn-search-trigger:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.6);
  filter: brightness(1.1);
}

.btn-search-trigger:active {
  transform: translateY(0);
}

/* Section styling standard */
.home-section {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 6rem 2rem;
  position: relative;
  z-index: 2;
}

.bg-gradient-alt {
  background: linear-gradient(180deg, rgba(255,255,255,0.01) 0%, rgba(255,255,255,0) 100%);
  border-top: 1px solid rgba(255,255,255,0.02);
  border-bottom: 1px solid rgba(255,255,255,0.02);
}

.section-header {
  margin-bottom: 4rem;
}

.section-tag {
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.15em;
  color: #a855f7;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
  display: inline-block;
}

.section-title {
  font-size: 2.75rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.02em;
  margin: 0 0 1rem 0;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #a1a1aa;
  margin: 0;
  font-weight: 500;
}

/* 🗺️ TRENDING DESTINATIONS SECTION */
.destinations-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
}

.destination-card {
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  aspect-ratio: 4 / 5;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.dest-image-wrapper {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.dest-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.dest-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0) 40%, rgba(0, 0, 0, 0.85) 100%);
  padding: 1.5rem;
  display: flex;
  align-items: flex-end;
  justify-content: justify;
  transition: all 0.3s ease;
}

.dest-info {
  flex-grow: 1;
  text-align: left;
}

.dest-name {
  font-size: 1.35rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 0.35rem 0;
  letter-spacing: -0.01em;
}

.dest-badge {
  font-size: 0.8rem;
  font-weight: 700;
  color: #d4d4d8;
}

.dest-arrow {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  border: 1px solid rgba(255,255,255,0.1);
  transition: all 0.3s ease;
  opacity: 0;
  transform: scale(0.8);
}

.destination-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(104, 85, 247, 0.2);
}

.destination-card:hover .dest-image {
  transform: scale(1.1);
}

.destination-card:hover .dest-overlay {
  background: linear-gradient(180deg, rgba(0,0,0,0) 20%, rgba(10, 8, 22, 0.9) 100%);
}

.destination-card:hover .dest-arrow {
  opacity: 1;
  transform: scale(1);
  background: #ffffff;
  color: #0b0914;
}

/* Secondary Custom Button */
.btn-secondary-custom {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.8rem 1.5rem;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  color: #ffffff;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-secondary-custom:hover {
  background: rgba(255,255,255,0.08);
  border-color: rgba(255,255,255,0.15);
  transform: translateX(3px);
}

/* 🏢 PREMIUM APARTMENTS GRID */
.apartments-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem;
}

.premium-apartment-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.card-image-section {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  overflow: hidden;
}

.card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.card-price-pill {
  position: absolute;
  bottom: 1.25rem;
  left: 1.25rem;
  background: rgba(11, 9, 20, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
  padding: 0.45rem 1rem;
  border-radius: 12px;
}

.price-val {
  font-size: 1.15rem;
  font-weight: 800;
  color: #ffffff;
}

.price-unit {
  font-size: 0.75rem;
  color: #a1a1aa;
  font-weight: 600;
}

.card-badges {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.badge-pill {
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.75rem;
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.rating-badge {
  background: #ffffff;
  color: #0b0914;
}

.rating-badge i {
  color: #eab308;
}

.tag-badge {
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  color: #ffffff;
  border: 1px solid rgba(255,255,255,0.15);
}

.card-details-section {
  padding: 1.75rem;
  text-align: left;
}

.card-location {
  font-size: 0.8rem;
  font-weight: 700;
  color: #a855f7;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.card-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0.75rem 0;
  line-height: 1.3;
}

.card-amenities-strip {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #71717a;
  font-size: 0.875rem;
  font-weight: 600;
  margin: 1.25rem 0 1.5rem 0;
}

.dot-separator {
  color: rgba(255,255,255,0.1);
}

.card-footer-trigger {
  border-top: 1px solid rgba(255,255,255,0.05);
  padding-top: 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #ffffff;
  font-weight: 700;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.card-footer-trigger i {
  transition: transform 0.3s ease;
}

.premium-apartment-card:hover {
  transform: translateY(-8px);
  border-color: rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.03);
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.premium-apartment-card:hover .card-img {
  transform: scale(1.05);
}

.premium-apartment-card:hover .card-footer-trigger {
  color: #a855f7;
}

.premium-apartment-card:hover .card-footer-trigger i {
  transform: translateX(4px);
}

/* Perks list value proposition */
.perks-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3rem;
}

.perk-card {
  background: rgba(255,255,255,0.015);
  border: 1px solid rgba(255,255,255,0.04);
  border-radius: 24px;
  padding: 3rem 2.25rem;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

.perk-icon-circle {
  width: 4.5rem;
  height: 4.5rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem auto;
  font-size: 1.85rem;
}

.perk-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 1rem 0;
}

.perk-desc {
  color: #71717a;
  line-height: 1.6;
  font-size: 0.95rem;
  font-weight: 500;
  margin: 0;
}

.perk-card:hover {
  transform: translateY(-5px);
  border-color: rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.03);
}

/* 💎 LOYALTY CLUB PREVIEW */
.loyalty-teaser-wrapper {
  background: rgba(255, 255, 255, 0.01);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 32px;
  padding: 4rem;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 50px rgba(0,0,0,0.3);
}

.btn-primary-custom {
  display: inline-flex;
  align-items: center;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
  border: none;
  border-radius: 14px;
  color: #ffffff;
  font-weight: 700;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.3);
}

.btn-primary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px -5px rgba(99, 102, 241, 0.5);
  filter: brightness(1.1);
}

/* Simulated Loyalty Card UI */
.loyalty-preview-card {
  width: 100%;
  max-width: 440px;
  aspect-ratio: 1.6 / 1;
  background: linear-gradient(135deg, #1f1936 0%, #100b21 100%);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 24px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 25px 50px -10px rgba(0, 0, 0, 0.8), 0 0 30px rgba(104, 85, 247, 0.15);
  text-align: left;
}

.card-inner-glow {
  position: absolute;
  top: -40%;
  right: -20%;
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, rgba(168, 85, 247, 0.3), transparent 70%);
  z-index: 0;
  pointer-events: none;
}

.card-brand {
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.15em;
  color: #a1a1aa;
}

.card-tier-title {
  font-size: 2rem;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -0.02em;
  margin-top: 0.25rem;
  background: linear-gradient(135deg, #fef08a 0%, #eab308 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.card-vip-badge {
  background: rgba(234, 179, 8, 0.1);
  border: 1px solid rgba(234, 179, 8, 0.2);
  color: #eab308;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 800;
}

.card-holder-label, .card-points-label {
  font-size: 0.65rem;
  font-weight: 800;
  color: #71717a;
  letter-spacing: 0.1em;
}

.card-holder-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: #ffffff;
  margin-top: 0.25rem;
}

.card-points-val {
  font-size: 1.35rem;
  font-weight: 800;
  color: #ffffff;
  margin-top: 0.25rem;
}

/* 👤 TESTIMONIALS */
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem;
}

.testimonial-card {
  background: rgba(255,255,255,0.015);
  border: 1px solid rgba(255,255,255,0.04);
  border-radius: 24px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.testimonial-text {
  font-size: 1.05rem;
  line-height: 1.6;
  color: #d4d4d8;
  font-style: italic;
  margin: 0;
}

.review-avatar {
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.review-author {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffffff;
}

.review-status {
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* Loading skeleton styles */
.loading-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem;
}

.loading-skeleton-card {
  background: rgba(255,255,255,0.015);
  border: 1px solid rgba(255,255,255,0.04);
  border-radius: 20px;
  height: 380px;
  overflow: hidden;
}

.skeleton-img {
  width: 100%;
  height: 60%;
  background: rgba(255,255,255,0.03);
  animation: pulse 1.5s infinite ease-in-out;
}

.skeleton-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.skeleton-line {
  height: 1rem;
  background: rgba(255,255,255,0.03);
  border-radius: 4px;
  animation: pulse 1.5s infinite ease-in-out;
}

.empty-fallback-card {
  background: rgba(255,255,255,0.015);
  border: 1px solid rgba(255,255,255,0.04);
  border-radius: 24px;
}

.empty-icon-circle {
  font-size: 3rem;
  opacity: 0.4;
}

/* 📩 PREMIUM BRAND FOOTER */
.app-footer {
  background: #06040a;
  border-top: 1px solid rgba(255,255,255,0.05);
  padding: 5rem 2rem 2rem 2rem;
  width: 100%;
  margin-top: 4rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr 1.5fr;
  gap: 4rem;
  max-width: 1400px;
  margin: 0 auto;
  text-align: left;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  padding-bottom: 4rem;
}

.footer-brand {
  font-size: 2rem;
  font-weight: 800;
  margin: 0 0 1.5rem 0;
  color: #ffffff;
}

.footer-about {
  color: #71717a;
  line-height: 1.6;
  font-size: 0.95rem;
  font-weight: 500;
}

.social-icon {
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.05);
  color: #a1a1aa;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  text-decoration: none;
}

.social-icon:hover {
  background: #a855f7;
  color: #ffffff;
  border-color: #a855f7;
  transform: translateY(-3px);
}

.footer-header {
  font-size: 1.05rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 1.75rem 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.footer-links a {
  color: #71717a;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 600;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #a855f7;
}

.footer-desc {
  color: #71717a;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
}

.newsletter-form {
  display: flex;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  overflow: hidden;
  padding: 0.25rem;
}

.newsletter-input {
  flex-grow: 1;
  background: transparent;
  border: none;
  padding: 0.75rem 1rem;
  color: #ffffff;
  font-size: 0.9rem;
  outline: none;
}

.newsletter-input::placeholder {
  color: #52525b;
}

.btn-newsletter-subscribe {
  padding: 0.75rem 1.25rem;
  background: #ffffff;
  color: #0b0914;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-newsletter-subscribe:hover {
  background: #a855f7;
  color: #ffffff;
}

.footer-bottom {
  max-width: 1400px;
  margin: 0 auto;
  padding-top: 2rem;
}

.footer-bottom a {
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-bottom a:hover {
  color: #a855f7;
}

/* RESPONSIVE DESIGN */
@media (max-width: 1024px) {
  .search-inputs-grid {
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }
  .search-action-block {
    grid-column: span 2;
  }
  .destinations-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .apartments-grid, .perks-grid, .testimonials-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .footer-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 3rem;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 3rem;
  }
  .hero-subtitle {
    font-size: 1.1rem;
    margin-bottom: 3rem;
  }
  .search-dashboard-wrapper {
    padding: 1.25rem;
  }
  .loyalty-teaser-wrapper {
    padding: 2rem;
  }
  .section-title {
    font-size: 2.25rem;
  }
}

@media (max-width: 580px) {
  .hero-title {
    font-size: 2.25rem;
  }
  .search-inputs-grid {
    grid-template-columns: 1fr;
  }
  .search-action-block {
    grid-column: span 1;
  }
  .destinations-grid, .apartments-grid, .perks-grid, .testimonials-grid {
    grid-template-columns: 1fr;
  }
  .footer-grid {
    grid-template-columns: 1fr;
  }
}
</style>