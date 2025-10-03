<!-- src/views/ApartmentDetailView.vue -->
<template>
  <div class="apartment-detail" v-if="apartment">
    <div class="container">
      <!-- Breadcrumb -->
      <nav class="breadcrumb">
        <router-link to="/apartments">Apartments</router-link>
        <span>/</span>
        <span>{{ apartment.title }}</span>
      </nav>

      <!-- Main Content -->
      <div class="detail-layout">
        <!-- Left Column - Images and Details -->
        <div class="detail-main">
          <div class="apartment-images">
            <img :src="apartment.image" :alt="apartment.title" class="main-image">
            <div class="image-thumbnails">
              <img 
                v-for="(img, index) in apartment.images" 
                :key="index" 
                :src="img" 
                :alt="`${apartment.title} ${index + 1}`"
                class="thumbnail"
              >
            </div>
          </div>

          <div class="apartment-info">
            <h1>{{ apartment.title }}</h1>
            <div class="location-rating">
              <p class="location">📍 {{ apartment.location }}</p>
              <div class="rating-badge">
                <span class="stars">⭐ {{ apartment.rating }}</span>
                <span class="reviews">({{ apartment.reviews }} reviews)</span>
              </div>
            </div>

            <div class="features-grid">
              <div class="feature">
                <span class="icon">👥</span>
                <div>
                  <strong>{{ apartment.guests }} guests</strong>
                  <p>Maximum occupancy</p>
                </div>
              </div>
              <div class="feature">
                <span class="icon">🛏️</span>
                <div>
                  <strong>{{ apartment.bedrooms }} bedrooms</strong>
                  <p>{{ apartment.beds }} beds</p>
                </div>
              </div>
              <div class="feature">
                <span class="icon">🚿</span>
                <div>
                  <strong>{{ apartment.bathrooms }} bathrooms</strong>
                  <p>Full bathrooms</p>
                </div>
              </div>
            </div>

            <div class="description">
              <h3>About this apartment</h3>
              <p>{{ apartment.description }}</p>
            </div>

            <div class="amenities">
              <h3>Amenities</h3>
              <div class="amenities-grid">
                <div 
                  v-for="amenity in apartment.amenities" 
                  :key="amenity.name"
                  class="amenity-item"
                >
                  <span class="amenity-icon">{{ amenity.icon }}</span>
                  <span>{{ amenity.name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Booking Card -->
        <div class="booking-sidebar">
          <div class="booking-card">
            <div class="price-section">
              <span class="price">${{ apartment.price }}</span>
              <span class="period">/ night</span>
            </div>
            
            <div class="booking-form">
              <div class="date-inputs">
                <div class="input-group">
                  <label>Check-in</label>
                  <input type="date" v-model="booking.checkIn" class="date-input">
                </div>
                <div class="input-group">
                  <label>Check-out</label>
                  <input type="date" v-model="booking.checkOut" class="date-input">
                </div>
              </div>
              
              <div class="guests-input">
                <label>Guests</label>
                <select v-model="booking.guests" class="guests-select">
                  <option v-for="n in apartment.guests" :key="n" :value="n">
                    {{ n }} guest{{ n !== 1 ? 's' : '' }}
                  </option>
                </select>
              </div>
              
              <div class="price-breakdown">
                <div class="price-line">
                  <span>${{ apartment.price }} x {{ nights }} nights</span>
                  <span>${{ apartment.price * nights }}</span>
                </div>
                <div class="price-line">
                  <span>Cleaning fee</span>
                  <span>$50</span>
                </div>
                <div class="price-line">
                  <span>Service fee</span>
                  <span>$30</span>
                </div>
                <div class="price-line total">
                  <span>Total</span>
                  <span>${{ totalPrice }}</span>
                </div>
              </div>
              
              <button class="book-btn" @click="handleBooking">
                Book Now
              </button>
              
              <p class="no-charge">You won't be charged yet</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <div v-else class="loading">
    <p>Loading apartment details...</p>
  </div>
</template>

<script>
export default {
  name: 'ApartmentDetailView',
  data() {
    return {
      apartment: null,
      booking: {
        checkIn: '',
        checkOut: '',
        guests: 1
      }
    }
  },
  computed: {
    nights() {
      if (!this.booking.checkIn || !this.booking.checkOut) return 1
      const checkIn = new Date(this.booking.checkIn)
      const checkOut = new Date(this.booking.checkOut)
      const diffTime = checkOut - checkIn
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      return diffDays > 0 ? diffDays : 1
    },
    totalPrice() {
      return (this.apartment.price * this.nights) + 50 + 30
    }
  },
  mounted() {
    this.loadApartment()
  },
  methods: {
    loadApartment() {
      const apartmentId = parseInt(this.$route.params.id)
      
      // Mock data - replace with API call
      const apartments = [
        {
          id: 1,
          title: "Luxury Downtown Apartment",
          location: "123 Main Street, New York, NY 10001",
          price: 150,
          guests: 4,
          bedrooms: 2,
          beds: 3,
          bathrooms: 2,
          rating: 4.8,
          reviews: 124,
          image: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800",
          images: [
            "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400",
            "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=400",
            "https://images.unsplash.com/photo-1560185127-6ed189bf02f4?w=400"
          ],
          description: "Beautiful modern apartment in the heart of downtown with stunning city views. This spacious 2-bedroom apartment features floor-to-ceiling windows, a fully equipped kitchen, and a comfortable living area. Perfect for business travelers or families looking to explore the city.",
          amenities: [
            { name: "WiFi", icon: "📶" },
            { name: "Kitchen", icon: "👨‍🍳" },
            { name: "Parking", icon: "🅿️" },
            { name: "Air Conditioning", icon: "❄️" },
            { name: "TV", icon: "📺" },
            { name: "Washer", icon: "🧺" },
            { name: "Dryer", icon: "👕" },
            { name: "Elevator", icon: "🛗" }
          ]
        }
      ]
      
      this.apartment = apartments.find(apt => apt.id === apartmentId) || apartments[0]
    },
    handleBooking() {
      if (!this.booking.checkIn || !this.booking.checkOut) {
        alert('Please select check-in and check-out dates')
        return
      }
      
      // In a real app, this would redirect to booking confirmation
      alert(`Booking request for ${this.apartment.title} from ${this.booking.checkIn} to ${this.booking.checkOut} for ${this.booking.guests} guests!`)
    }
  }
}
</script>

<style scoped>
.apartment-detail {
  min-height: 100vh;
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.breadcrumb {
  margin-bottom: 2rem;
  color: #718096;
}

.breadcrumb a {
  color: #667eea;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.breadcrumb span {
  margin: 0 0.5rem;
}

.detail-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
}

/* Main Content */
.detail-main {
  space-y: 2rem;
}

.apartment-images {
  margin-bottom: 2rem;
}

.main-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.image-thumbnails {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
}

.thumbnail {
  width: 100px;
  height: 75px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.thumbnail:hover {
  opacity: 0.8;
}

.apartment-info h1 {
  font-size: 2rem;
  color: #2d3748;
  margin-bottom: 1rem;
}

.location-rating {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.location {
  color: #718096;
  font-size: 1.1rem;
}

.rating-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stars {
  color: #fbbf24;
  font-weight: 600;
}

.reviews {
  color: #718096;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f7fafc;
  border-radius: 12px;
}

.feature {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.feature .icon {
  font-size: 1.5rem;
}

.feature strong {
  display: block;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.feature p {
  color: #718096;
  margin: 0;
  font-size: 0.9rem;
}

.description {
  margin-bottom: 2rem;
}

.description h3 {
  color: #2d3748;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.description p {
  color: #4a5568;
  line-height: 1.7;
}

.amenities h3 {
  color: #2d3748;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.amenities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.amenity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #f7fafc;
  border-radius: 8px;
}

.amenity-icon {
  font-size: 1.25rem;
}

/* Booking Sidebar */
.booking-sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.booking-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.price-section {
  text-align: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.price {
  font-size: 1.75rem;
  font-weight: bold;
  color: #2d3748;
}

.period {
  color: #718096;
}

.booking-form {
  space-y: 1.5rem;
}

.date-inputs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group label {
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.date-input, .guests-select {
  padding: 0.75rem;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 0.9rem;
  width: 100%;
}

.guests-input {
  margin-bottom: 1.5rem;
}

.guests-input label {
  display: block;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.price-breakdown {
  space-y: 0.75rem;
  margin-bottom: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.price-line {
  display: flex;
  justify-content: space-between;
  color: #4a5568;
  font-size: 0.9rem;
}

.price-line.total {
  font-weight: bold;
  color: #2d3748;
  font-size: 1.1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e2e8f0;
}

.book-btn {
  width: 100%;
  background: #667eea;
  color: white;
  border: none;
  padding: 1rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 1rem;
}

.book-btn:hover {
  background: #5a6fd8;
}

.no-charge {
  text-align: center;
  color: #718096;
  font-size: 0.9rem;
  margin: 0;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 50vh;
  font-size: 1.2rem;
  color: #718096;
}

/* Responsive Design */
@media (max-width: 968px) {
  .detail-layout {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .booking-sidebar {
    position: static;
  }
}

@media (max-width: 768px) {
  .apartment-detail {
    padding: 1rem 0;
  }
  
  .apartment-info h1 {
    font-size: 1.75rem;
  }
  
  .location-rating {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .main-image {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.5rem;
  }
  
  .date-inputs {
    grid-template-columns: 1fr;
  }
  
  .booking-card {
    padding: 1rem;
  }
}
</style>