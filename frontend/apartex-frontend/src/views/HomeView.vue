<template>
  <div class="home-container">
    
    <!-- HERO SECTION -->
    <header class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Find Your Perfect Stay in Zambia</h1>
        <p class="hero-subtitle">Handpicked apartments, lodges and guest houses — no hidden fees.</p>
        
        <div class="search-bar">
          <div class="search-input-group">
            <label>Location</label>
            <select v-model="selectedCity" class="search-select">
              <option value="">Where are you going?</option>
              <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
            </select>
          </div>
          <div class="search-divider"></div>
          
          <div class="search-input-group">
            <label>Check-in</label>
            <input type="date" v-model="checkInDate" class="search-input" :min="todayDate" />
          </div>
          <div class="search-divider"></div>
          
          <div class="search-input-group">
            <label>Check-out</label>
            <input type="date" v-model="checkOutDate" class="search-input" :min="checkInDate || todayDate" />
          </div>
          <div class="search-divider"></div>
          
          <div class="search-input-group">
            <label>Guests</label>
            <select v-model="guestCount" class="search-select">
              <option v-for="n in 6" :key="n" :value="n">{{ n }} Guest{{ n > 1 ? 's' : '' }}</option>
            </select>
          </div>
          
          <button @click="triggerSearch" class="btn-search">Search</button>
        </div>
        
        <div class="trust-row">
          <span><i class="pi pi-check"></i> No booking fees</span>
          <span class="dot">·</span>
          <span><i class="pi pi-check"></i> Verified properties</span>
          <span class="dot">·</span>
          <span><i class="pi pi-check"></i> Instant confirmation</span>
        </div>
      </div>
    </header>

    <!-- DESTINATIONS SECTION -->
    <section class="home-section">
      <div class="section-header">
        <h2 class="section-title">Explore by City</h2>
      </div>
      
      <div class="destinations-grid">
        <div 
          v-for="destination in destinationList" 
          :key="destination.name" 
          class="city-card"
          @click="selectTrendingCity(destination.name)"
        >
          <img :src="destination.image" :alt="destination.name" class="city-image" />
          <div class="city-overlay">
            <h3 class="city-name">{{ destination.name }}</h3>
            <p class="city-count">{{ destination.count }} Properties</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURED STAYS SECTION -->
    <section class="home-section">
      <div class="section-header-flex">
        <h2 class="section-title">Featured Stays</h2>
        <router-link to="/apartments" class="btn-view-all">View All &rarr;</router-link>
      </div>

      <div v-if="apartmentsStore.loading" class="featured-grid">
        <div v-for="i in 3" :key="i" class="skeleton-card">
          <div class="skeleton-image pulse"></div>
          <div class="skeleton-text pulse title"></div>
          <div class="skeleton-text pulse desc"></div>
        </div>
      </div>

      <div v-else class="featured-grid">
        <ApartmentCard 
          v-for="apartment in apartmentsStore.featuredApartments" 
          :key="apartment.id"
          :apartment="apartment"
          @click="viewApartmentDetail(apartment.id)"
        />
      </div>
    </section>

    <!-- WHY APARTEX SECTION -->
    <section class="home-section bg-alt">
      <div class="why-grid">
        <div v-for="perk in perks" :key="perk.title" class="feature-card">
          <div class="feature-icon">
            <i :class="perk.icon"></i>
          </div>
          <h3 class="feature-title">{{ perk.title }}</h3>
          <p class="feature-desc">{{ perk.description }}</p>
        </div>
      </div>
    </section>

    <!-- LOYALTY TEASER SECTION -->
    <section class="home-section loyalty-section">
      <div class="loyalty-grid">
        <div class="loyalty-content">
          <h2 class="section-title">Apartex Loyalty Club</h2>
          <p class="loyalty-desc">Unlock premium rewards with every booking. Travel more, earn more.</p>
          <ul class="loyalty-list">
            <li><i class="pi pi-check-circle"></i> Earn points on every night spent</li>
            <li><i class="pi pi-check-circle"></i> Redeem rewards for discount bookings</li>
            <li><i class="pi pi-check-circle"></i> Enjoy lifetime tier benefits</li>
          </ul>
          <router-link to="/loyalty" class="btn-loyalty">Join the Club</router-link>
        </div>
        
        <div class="loyalty-card-wrapper">
          <div class="membership-card">
            <div class="card-top">
              <span class="brand">APARTEX</span>
              <span class="tier">GOLD MEMBER</span>
            </div>
            <div class="card-chip"></div>
            <div class="card-bottom">
              <div class="member-info">
                <span class="label">MEMBER</span>
                <span class="name">Demo Traveler</span>
              </div>
              <div class="points-info">
                <span class="label">POINTS</span>
                <span class="value">4,250</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TESTIMONIALS SECTION -->
    <section class="home-section">
      <div class="section-header">
        <h2 class="section-title">Traveler Stories</h2>
      </div>
      <div class="testimonials-grid">
        <div v-for="review in reviews" :key="review.author" class="testimonial-card">
          <div class="stars">
            <i v-for="s in 5" :key="s" class="pi pi-star-fill"></i>
          </div>
          <p class="quote">"{{ review.text }}"</p>
          <div class="reviewer">
            <div class="avatar">{{ review.initials }}</div>
            <div class="info">
              <h4>{{ review.author }}</h4>
              <span>Verified Guest</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="footer-grid">
        <div class="footer-col brand-col">
          <h3>Apartex</h3>
          <p>Redefining temporary stays with handpicked collections across Zambia.</p>
          <div class="socials">
            <a href="#"><i class="pi pi-facebook"></i></a>
            <a href="#"><i class="pi pi-twitter"></i></a>
            <a href="#"><i class="pi pi-instagram"></i></a>
          </div>
        </div>
        
        <div class="footer-col">
          <h4>Quick Links</h4>
          <ul>
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/apartments">Explore Stays</router-link></li>
            <li><router-link to="/bookings">Reservations</router-link></li>
            <li><router-link to="/loyalty">Loyalty Club</router-link></li>
          </ul>
        </div>
        
        <div class="footer-col">
          <h4>Destinations</h4>
          <ul>
            <li><a href="#" @click.prevent="selectTrendingCity('Lusaka')">Lusaka</a></li>
            <li><a href="#" @click.prevent="selectTrendingCity('Livingstone')">Livingstone</a></li>
            <li><a href="#" @click.prevent="selectTrendingCity('Ndola')">Ndola</a></li>
          </ul>
        </div>
        
        <div class="footer-col">
          <h4>Newsletter</h4>
          <p>Stay updated on premium properties and exclusive offers.</p>
          <div class="newsletter">
            <input type="email" placeholder="Your email address" />
            <button>Subscribe</button>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p>&copy; 2026 Apartex Inc. All rights reserved.</p>
        <div class="legal-links">
          <a href="#">Privacy Policy</a>
          <a href="#">Terms of Service</a>
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

<style scoped>
.home-container {
  width: 100%;
}

/* HERO SECTION */
.hero-section {
  width: 100%;
  padding: var(--space-16) var(--space-6);
  background: var(--color-bg);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.hero-content {
  max-width: 1000px;
  width: 100%;
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 900;
  color: var(--color-text-primary);
  letter-spacing: -0.04em;
  margin-bottom: var(--space-4);
  line-height: 1.1;
}

.hero-subtitle {
  font-size: var(--font-size-xl);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-10);
  font-weight: 500;
}

.search-bar {
  display: flex;
  background: var(--color-surface);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  padding: var(--space-4) var(--space-6);
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
}

.search-input-group {
  display: flex;
  flex-direction: column;
  text-align: left;
  flex: 1;
  padding: 0 var(--space-4);
}

.search-input-group label {
  font-size: var(--font-size-xs);
  font-weight: 700;
  color: var(--color-text-primary);
  text-transform: uppercase;
  margin-bottom: var(--space-1);
}

.search-select, .search-input {
  border: none;
  outline: none;
  background: transparent;
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  font-family: var(--font-family);
  cursor: pointer;
  padding: var(--space-2) 0;
}

.search-select:focus, .search-input:focus {
  color: var(--color-text-primary);
}

.search-divider {
  width: 1px;
  height: 40px;
  background: var(--color-border);
}

.btn-search {
  background: var(--color-accent);
  color: white;
  border: none;
  border-radius: var(--radius-full);
  padding: var(--space-3) var(--space-6);
  font-weight: 600;
  font-size: var(--font-size-base);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.btn-search:hover {
  background: var(--color-accent-hover);
}

.trust-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-4);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

.trust-row i {
  color: var(--color-success);
  margin-right: var(--space-1);
}

.dot {
  color: var(--color-border-strong);
}

@media (max-width: 768px) {
  .search-bar {
    flex-direction: column;
    padding: var(--space-4);
    gap: var(--space-4);
    border-radius: var(--radius-lg);
  }
  .search-input-group {
    width: 100%;
    padding: var(--space-2);
  }
  .search-divider {
    display: none;
  }
  .btn-search {
    width: 100%;
  }
  .trust-row {
    flex-direction: column;
    gap: var(--space-2);
  }
}

/* SECTION STANDARDS */
.home-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: var(--space-12) var(--space-6);
}

.bg-alt {
  background: var(--color-surface-alt);
  max-width: 100%;
}

.section-header {
  margin-bottom: var(--space-8);
}

.section-header-flex {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: var(--space-8);
}

.section-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0;
  text-align: left;
}

.btn-view-all {
  color: var(--color-accent);
  text-decoration: none;
  font-weight: 600;
  font-size: var(--font-size-base);
}

.btn-view-all:hover {
  text-decoration: underline;
}

/* DESTINATIONS */
.destinations-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-6);
}

.city-card {
  position: relative;
  height: 280px;
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: transform var(--transition-base), box-shadow var(--transition-base);
}

.city-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.city-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition-slow);
}

.city-card:hover .city-image {
  transform: scale(1.05);
}

.city-overlay {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: var(--space-6);
  background: linear-gradient(transparent, rgba(0,0,0,0.8));
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.city-name {
  font-size: var(--font-size-xl);
  font-weight: 700;
  margin: 0 0 var(--space-1) 0;
}

.city-count {
  font-size: var(--font-size-sm);
  margin: 0;
  opacity: 0.9;
}

@media (max-width: 1024px) {
  .destinations-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .destinations-grid { grid-template-columns: 1fr; }
}

/* FEATURED STAYS */
.featured-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);
}

@media (max-width: 1024px) {
  .featured-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .featured-grid { grid-template-columns: 1fr; }
}

.skeleton-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}
.skeleton-image { height: 200px; border-radius: var(--radius-md); background: #e2e8f0; }
.skeleton-text { height: 20px; border-radius: var(--radius-sm); background: #e2e8f0; }
.skeleton-text.title { width: 60%; }
.skeleton-text.desc { width: 100%; height: 40px; }
.pulse { animation: pulse 2s infinite ease-in-out; }

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 0.2; }
  100% { opacity: 0.6; }
}

/* WHY APARTEX */
.why-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-8);
  max-width: 1400px;
  margin: 0 auto;
}

.feature-card {
  background: transparent;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}

.feature-icon {
  width: 3.5rem;
  height: 3.5rem;
  background: var(--color-accent-light);
  color: var(--color-accent);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: var(--space-4);
}

.feature-title {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-2) 0;
}

.feature-desc {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}

@media (max-width: 768px) {
  .why-grid { grid-template-columns: 1fr; }
}

/* LOYALTY TEASER */
.loyalty-section {
  padding: var(--space-16) var(--space-6);
}

.loyalty-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-12);
  align-items: center;
}

.loyalty-desc {
  font-size: var(--font-size-xl);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-6);
}

.loyalty-list {
  list-style: none;
  padding: 0;
  margin: 0 0 var(--space-8) 0;
}

.loyalty-list li {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  font-weight: 500;
  margin-bottom: var(--space-3);
}

.loyalty-list i {
  color: var(--color-accent);
  font-size: 1.25rem;
}

.btn-loyalty {
  display: inline-block;
  background: var(--color-accent);
  color: white;
  text-decoration: none;
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: 600;
  transition: background var(--transition-fast);
}
.btn-loyalty:hover { background: var(--color-accent-hover); }

.loyalty-card-wrapper {
  display: flex;
  justify-content: center;
}

.membership-card {
  width: 100%;
  max-width: 400px;
  aspect-ratio: 1.58;
  background: linear-gradient(135deg, var(--color-navy) 0%, #102341 100%);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  color: white;
  box-shadow: var(--shadow-xl);
  position: relative;
  overflow: hidden;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.brand { font-weight: 800; font-size: var(--font-size-xl); letter-spacing: 0.1em; }
.tier { color: #F59E0B; font-weight: 700; font-size: var(--font-size-sm); }

.card-chip {
  width: 45px; height: 35px;
  background: #F59E0B;
  border-radius: var(--radius-sm);
  opacity: 0.8;
  margin-top: auto;
  margin-bottom: var(--space-4);
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
.label { display: block; font-size: 0.6rem; color: rgba(255,255,255,0.6); letter-spacing: 0.1em; margin-bottom: 2px; }
.name { font-size: var(--font-size-base); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }
.value { font-size: var(--font-size-xl); font-weight: 700; color: #F59E0B; }

@media (max-width: 900px) {
  .loyalty-grid { grid-template-columns: 1fr; }
  .loyalty-card-wrapper { margin-top: var(--space-8); }
}

/* TESTIMONIALS */
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);
}

.testimonial-card {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.stars { color: var(--color-accent); margin-bottom: var(--space-4); }

.quote {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  font-style: italic;
  margin-bottom: var(--space-6);
  line-height: 1.6;
}

.reviewer {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.avatar {
  width: 3rem; height: 3rem;
  background: var(--color-surface-alt);
  border-radius: var(--radius-full);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; color: var(--color-text-primary);
}

.info h4 { margin: 0; color: var(--color-text-primary); font-size: var(--font-size-sm); }
.info span { font-size: var(--font-size-xs); color: var(--color-success); font-weight: 600; }

@media (max-width: 1024px) { .testimonials-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .testimonials-grid { grid-template-columns: 1fr; } }

/* FOOTER */
.footer {
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: var(--space-12) var(--space-6) var(--space-6);
}

.footer-grid {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: var(--space-8);
  margin-bottom: var(--space-12);
}

.footer-col h3 { font-size: 1.5rem; font-weight: 800; color: var(--color-navy); margin: 0 0 var(--space-4) 0; }
.footer-col h4 { font-size: 1.125rem; font-weight: 700; color: var(--color-text-primary); margin: 0 0 var(--space-4) 0; }
.footer-col p { color: var(--color-text-secondary); line-height: 1.6; margin-bottom: var(--space-4); }

.socials { display: flex; gap: var(--space-4); }
.socials a { color: var(--color-text-secondary); font-size: 1.25rem; transition: color var(--transition-fast); }
.socials a:hover { color: var(--color-accent); }

.footer-col ul { list-style: none; padding: 0; margin: 0; }
.footer-col ul li { margin-bottom: var(--space-3); }
.footer-col ul a { color: var(--color-text-secondary); text-decoration: none; transition: color var(--transition-fast); }
.footer-col ul a:hover { color: var(--color-accent); }

.newsletter { display: flex; gap: var(--space-2); }
.newsletter input {
  flex: 1;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-family);
}
.newsletter button {
  background: var(--color-accent);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  padding: 0 var(--space-4);
  font-weight: 600;
  cursor: pointer;
}

.footer-bottom {
  max-width: 1400px;
  margin: 0 auto;
  border-top: 1px solid var(--color-border);
  padding-top: var(--space-6);
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
}

.legal-links { display: flex; gap: var(--space-4); }
.legal-links a { color: var(--color-text-muted); text-decoration: none; }
.legal-links a:hover { color: var(--color-text-secondary); }

@media (max-width: 1024px) {
  .footer-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 640px) {
  .footer-grid { grid-template-columns: 1fr; }
  .footer-bottom { flex-direction: column; gap: var(--space-4); text-align: center; }
}
</style>