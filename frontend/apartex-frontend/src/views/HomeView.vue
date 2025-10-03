<template>
  <div class="home">
    <header class="hero">
      <h1>Find Your Perfect Stay</h1>
      <p>Book apartments with ease and earn loyalty rewards</p>
    </header>

    <main class="main-content">
      <h2>Featured Apartments</h2>
      
      <div class="apartments-grid">
        <div class="apartment-card" v-for="apartment in apartments" :key="apartment.id">
          <img :src="apartment.image" :alt="apartment.title" class="apartment-image">
          <div class="apartment-info">
            <h3>{{ apartment.title }}</h3>
            <p class="location">{{ apartment.location }}</p>
            <p class="price">${{ apartment.price }}/night</p>
            <div class="details">
              <span class="detail-item">
                <span class="icon">👥</span>
                {{ apartment.guests }} guests
              </span>
              <span class="detail-item">
                <span class="icon">🛏️</span>
                {{ apartment.bedrooms }} bedroom{{ apartment.bedrooms !== 1 ? 's' : '' }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      apartments: [
        {
          id: 1,
          title: "Luxury Downtown Apartment",
          location: "New York, NY",
          price: 150,
          guests: 4,
          bedrooms: 2,
          image: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400"
        },
        {
          id: 2,
          title: "Beachfront Condo",
          location: "Miami, FL",
          price: 200,
          guests: 6,
          bedrooms: 3,
          image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400"
        },
        {
          id: 3,
          title: "Mountain View Cabin",
          location: "Denver, CO",
          price: 120,
          guests: 4,
          bedrooms: 2,
          image: "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400"
        }
      ]
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 4rem 2rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.hero p {
  font-size: 1.2rem;
  opacity: 0.9;
  font-weight: 300;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 1rem;
}

.main-content h2 {
  text-align: center;
  margin-bottom: 3rem;
  font-size: 2.2rem;
  color: #2d3748;
  font-weight: 600;
}

.apartments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
}

.apartment-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
}

.apartment-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.apartment-image {
  width: 100%;
  height: 220px;
  object-fit: cover;
  display: block;
}

.apartment-info {
  padding: 1.5rem;
}

.apartment-info h3 {
  margin-bottom: 0.5rem;
  color: #2d3748;
  font-size: 1.25rem;
  font-weight: 600;
}

.location {
  color: #718096;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 1rem;
}

.details {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #4a5568;
  font-size: 0.9rem;
}

.icon {
  font-size: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero {
    padding: 3rem 1rem;
  }
  
  .hero h1 {
    font-size: 2rem;
  }
  
  .apartments-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .main-content {
    padding: 2rem 1rem;
  }
  
  .details {
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 2rem 1rem;
  }
  
  .hero h1 {
    font-size: 1.75rem;
  }
  
  .apartment-info {
    padding: 1.25rem;
  }
}
</style>