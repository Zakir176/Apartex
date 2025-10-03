<!-- src/views/ApartmentsView.vue -->
<template>
  <div class="apartments-page">
    <div class="page-header">
      <div class="container">
        <h1>Find Your Perfect Apartment</h1>
        <p>Discover amazing places to stay around the world</p>
      </div>
    </div>

    <div class="container main-layout">
      <!-- Filters Sidebar -->
      <aside class="filters-sidebar">
        <div class="filters-card">
          <h3>Filters</h3>
          
          <div class="filter-group">
            <label>Price Range</label>
            <div class="price-inputs">
              <input type="number" v-model="filters.minPrice" placeholder="Min" class="price-input">
              <span>-</span>
              <input type="number" v-model="filters.maxPrice" placeholder="Max" class="price-input">
            </div>
          </div>

          <div class="filter-group">
            <label>Guests</label>
            <select v-model="filters.guests" class="filter-select">
              <option value="">Any</option>
              <option value="1">1 guest</option>
              <option value="2">2 guests</option>
              <option value="4">4+ guests</option>
              <option value="6">6+ guests</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Bedrooms</label>
            <select v-model="filters.bedrooms" class="filter-select">
              <option value="">Any</option>
              <option value="1">1 bedroom</option>
              <option value="2">2 bedrooms</option>
              <option value="3">3+ bedrooms</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Amenities</label>
            <div class="amenities-list">
              <label class="amenity-item">
                <input type="checkbox" v-model="filters.amenities" value="wifi"> WiFi
              </label>
              <label class="amenity-item">
                <input type="checkbox" v-model="filters.amenities" value="kitchen"> Kitchen
              </label>
              <label class="amenity-item">
                <input type="checkbox" v-model="filters.amenities" value="parking"> Parking
              </label>
              <label class="amenity-item">
                <input type="checkbox" v-model="filters.amenities" value="pool"> Pool
              </label>
            </div>
          </div>

          <button @click="applyFilters" class="apply-filters-btn">Apply Filters</button>
          <button @click="clearFilters" class="clear-filters-btn">Clear All</button>
        </div>
      </aside>

      <!-- Apartments Grid -->
      <main class="apartments-main">
        <div class="results-header">
          <h2>{{ filteredApartments.length }} apartments found</h2>
          <div class="sort-options">
            <label>Sort by:</label>
            <select v-model="sortBy" class="sort-select">
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="rating">Highest Rated</option>
            </select>
          </div>
        </div>

        <div class="apartments-grid">
          <div 
            v-for="apartment in sortedApartments" 
            :key="apartment.id" 
            class="apartment-card"
            @click="$router.push(`/apartments/${apartment.id}`)"
          >
            <img :src="apartment.image" :alt="apartment.title" class="apartment-image">
            <div class="apartment-info">
              <h3>{{ apartment.title }}</h3>
              <p class="location">{{ apartment.location }}</p>
              <p class="price">${{ apartment.price }}/night</p>
              <div class="rating">
                <span class="stars">⭐ {{ apartment.rating }}</span>
                <span class="reviews">({{ apartment.reviews }} reviews)</span>
              </div>
              <div class="details">
                <span class="detail-item">
                  <span class="icon">👥</span>
                  {{ apartment.guests }} guests
                </span>
                <span class="detail-item">
                  <span class="icon">🛏️</span>
                  {{ apartment.bedrooms }} bedrooms
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredApartments.length === 0" class="no-results">
          <h3>No apartments match your filters</h3>
          <p>Try adjusting your search criteria</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApartmentsView',
  data() {
    return {
      filters: {
        minPrice: '',
        maxPrice: '',
        guests: '',
        bedrooms: '',
        amenities: []
      },
      sortBy: 'price_asc',
      apartments: [
        {
          id: 1,
          title: "Luxury Downtown Apartment",
          location: "New York, NY",
          price: 150,
          guests: 4,
          bedrooms: 2,
          rating: 4.8,
          reviews: 124,
          image: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400",
          amenities: ['wifi', 'kitchen', 'parking']
        },
        {
          id: 2,
          title: "Beachfront Condo",
          location: "Miami, FL",
          price: 200,
          guests: 6,
          bedrooms: 3,
          rating: 4.9,
          reviews: 89,
          image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
          amenities: ['wifi', 'kitchen', 'pool']
        },
        {
          id: 3,
          title: "Mountain View Cabin",
          location: "Denver, CO",
          price: 120,
          guests: 4,
          bedrooms: 2,
          rating: 4.7,
          reviews: 67,
          image: "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400",
          amenities: ['wifi', 'kitchen']
        },
        {
          id: 4,
          title: "City Center Studio",
          location: "Chicago, IL",
          price: 90,
          guests: 2,
          bedrooms: 1,
          rating: 4.5,
          reviews: 203,
          image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400",
          amenities: ['wifi', 'kitchen']
        },
        {
          id: 5,
          title: "Lakeside Retreat",
          location: "Seattle, WA",
          price: 180,
          guests: 5,
          bedrooms: 3,
          rating: 4.9,
          reviews: 56,
          image: "https://images.unsplash.com/photo-1513584684374-8bab748fbf90?w=400",
          amenities: ['wifi', 'kitchen', 'parking', 'pool']
        },
        {
          id: 6,
          title: "Historic Townhouse",
          location: "Boston, MA",
          price: 220,
          guests: 4,
          bedrooms: 2,
          rating: 4.6,
          reviews: 78,
          image: "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400",
          amenities: ['wifi', 'kitchen']
        }
      ]
    }
  },
  computed: {
    filteredApartments() {
      return this.apartments.filter(apartment => {
        // Price filter
        if (this.filters.minPrice && apartment.price < parseInt(this.filters.minPrice)) return false
        if (this.filters.maxPrice && apartment.price > parseInt(this.filters.maxPrice)) return false
        
        // Guests filter
        if (this.filters.guests && apartment.guests < parseInt(this.filters.guests)) return false
        
        // Bedrooms filter
        if (this.filters.bedrooms && apartment.bedrooms < parseInt(this.filters.bedrooms)) return false
        
        // Amenities filter
        if (this.filters.amenities.length > 0) {
          const hasAllAmenities = this.filters.amenities.every(amenity => 
            apartment.amenities.includes(amenity)
          )
          if (!hasAllAmenities) return false
        }
        
        return true
      })
    },
    sortedApartments() {
      const apartments = [...this.filteredApartments]
      
      switch (this.sortBy) {
        case 'price_asc':
          return apartments.sort((a, b) => a.price - b.price)
        case 'price_desc':
          return apartments.sort((a, b) => b.price - a.price)
        case 'rating':
          return apartments.sort((a, b) => b.rating - a.rating)
        default:
          return apartments
      }
    }
  },
  methods: {
    applyFilters() {
      // Filters are applied automatically through computed properties
    },
    clearFilters() {
      this.filters = {
        minPrice: '',
        maxPrice: '',
        guests: '',
        bedrooms: '',
        amenities: []
      }
      this.sortBy = 'price_asc'
    }
  }
}
</script>

<style scoped>
.apartments-page {
  min-height: 100vh;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem 0;
  text-align: center;
}

.page-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.page-header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.main-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  padding: 2rem 1rem;
}

/* Filters Sidebar */
.filters-sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

.filters-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.filters-card h3 {
  margin-bottom: 1.5rem;
  color: #2d3748;
  font-size: 1.25rem;
}

.filter-group {
  margin-bottom: 1.5rem;
}

.filter-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #4a5568;
}

.price-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.price-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 0.9rem;
}

.filter-select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  background: white;
  font-size: 0.9rem;
}

.amenities-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.amenity-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
  cursor: pointer;
}

.amenity-item input {
  margin: 0;
}

.apply-filters-btn {
  width: 100%;
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 0.5rem;
  transition: background-color 0.3s;
}

.apply-filters-btn:hover {
  background: #5a6fd8;
}

.clear-filters-btn {
  width: 100%;
  background: transparent;
  color: #667eea;
  border: 1px solid #667eea;
  padding: 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.clear-filters-btn:hover {
  background: #667eea;
  color: white;
}

/* Apartments Main */
.apartments-main {
  min-height: 500px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.results-header h2 {
  color: #2d3748;
  font-size: 1.5rem;
}

.sort-options {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sort-select {
  padding: 0.5rem;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  background: white;
}

.apartments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.apartment-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #e2e8f0;
}

.apartment-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.apartment-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.apartment-info {
  padding: 1.25rem;
}

.apartment-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
  font-size: 1.1rem;
}

.location {
  color: #718096;
  margin: 0 0 0.75rem 0;
  font-size: 0.9rem;
}

.price {
  font-size: 1.25rem;
  font-weight: bold;
  color: #667eea;
  margin: 0 0 0.75rem 0;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.stars {
  color: #fbbf24;
  font-weight: 600;
}

.reviews {
  color: #718096;
}

.details {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #4a5568;
  font-size: 0.85rem;
}

.no-results {
  text-align: center;
  padding: 3rem;
  color: #718096;
}

.no-results h3 {
  margin-bottom: 0.5rem;
  color: #4a5568;
}

/* Responsive Design */
@media (max-width: 968px) {
  .main-layout {
    grid-template-columns: 1fr;
  }
  
  .filters-sidebar {
    position: static;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 2rem 0;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .results-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .apartments-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .main-layout {
    padding: 1rem 0.5rem;
  }
  
  .filters-card {
    padding: 1rem;
  }
}
</style>