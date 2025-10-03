<!-- src/components/apartments/ApartmentList.vue -->
<template>
  <div class="apartment-list">
    <div v-if="loading" class="loading-state">
      <ProgressSpinner />
      <p>Loading apartments...</p>
    </div>
    
    <div v-else-if="apartments.length === 0" class="empty-state">
      <i class="pi pi-home" style="font-size: 3rem; color: #cbd5e0; margin-bottom: 1rem;"></i>
      <h3>No apartments found</h3>
      <p>Try adjusting your search criteria</p>
    </div>
    
    <div v-else class="apartments-grid">
      <div 
        v-for="apartment in apartments" 
        :key="apartment.id" 
        class="apartment-card"
        @click="$router.push(`/apartments/${apartment.id}`)"
      >
        <div class="apartment-image">
          <img 
            :src="apartment.image_url || '/placeholder-apartment.jpg'" 
            :alt="apartment.title"
            @error="handleImageError"
          />
          <div class="apartment-badge" v-if="apartment.is_featured">
            Featured
          </div>
          <div class="apartment-price">
            ${{ apartment.price_per_night }}<span>/night</span>
          </div>
        </div>
        
        <div class="apartment-content">
          <div class="apartment-header">
            <h3 class="apartment-title">{{ apartment.title }}</h3>
            <div class="apartment-rating">
              <i class="pi pi-star-fill" style="color: #fbbf24;"></i>
              <span>{{ apartment.rating }}</span>
              <span class="review-count">({{ apartment.review_count }})</span>
            </div>
          </div>
          
          <p class="apartment-location">
            <i class="pi pi-map-marker" style="margin-right: 0.5rem;"></i>
            {{ apartment.location }}
          </p>
          
          <div class="apartment-features">
            <div class="feature">
              <i class="pi pi-users"></i>
              <span>{{ apartment.max_guests }} guests</span>
            </div>
            <div class="feature">
              <i class="pi pi-home"></i>
              <span>{{ apartment.bedrooms }} bedroom{{ apartment.bedrooms !== 1 ? 's' : '' }}</span>
            </div>
            <div class="feature" v-if="apartment.bathrooms">
              <i class="pi pi-plus"></i>
              <span>{{ apartment.bathrooms }} bath{{ apartment.bathrooms !== 1 ? 's' : '' }}</span>
            </div>
          </div>
          
          <div class="apartment-actions">
            <Button 
              label="View Details" 
              icon="pi pi-arrow-right"
              class="view-details-btn"
              @click.stop="$router.push(`/apartments/${apartment.id}`)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProgressSpinner from 'primevue/progressspinner'
import Button from 'primevue/button'

export default {
  name: 'ApartmentList',
  components: {
    ProgressSpinner,
    Button
  },
  props: {
    apartments: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    handleImageError(event) {
      event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjdmOGZhIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0jOTlhNmIzIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+QXBhcnRtZW50IEltYWdlPC90ZXh0Pjwvc3ZnPg=='
    }
  }
}
</script>

<style scoped>
.apartment-list {
  width: 100%;
}

.apartments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

.apartment-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #f1f5f9;
}

.apartment-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.apartment-image {
  position: relative;
  height: 220px;
  overflow: hidden;
}

.apartment-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.apartment-card:hover .apartment-image img {
  transform: scale(1.05);
}

.apartment-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.apartment-price {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.95);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-weight: 700;
  color: #2d3748;
  font-size: 1.125rem;
  backdrop-filter: blur(10px);
}

.apartment-price span {
  font-size: 0.875rem;
  font-weight: 500;
  color: #718096;
}

.apartment-content {
  padding: 1.5rem;
}

.apartment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.apartment-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
  line-height: 1.4;
  flex: 1;
}

.apartment-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 600;
  color: #2d3748;
  white-space: nowrap;
  margin-left: 0.5rem;
}

.review-count {
  color: #718096;
  font-weight: 400;
}

.apartment-location {
  color: #718096;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  font-size: 0.875rem;
}

.apartment-features {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: #4a5568;
  font-size: 0.875rem;
}

.feature i {
  color: #667eea;
}

.apartment-actions {
  display: flex;
  justify-content: flex-end;
}

.view-details-btn {
  background: transparent;
  color: #667eea;
  border: 1px solid #667eea;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}

.view-details-btn:hover {
  background: #667eea;
  color: white;
}

/* Loading and Empty States */
.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-state p,
.empty-state p {
  color: #718096;
  margin-top: 1rem;
}

.empty-state h3 {
  color: #2d3748;
  margin-bottom: 0.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .apartments-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }
  
  .apartment-content {
    padding: 1.25rem;
  }
  
  .apartment-features {
    gap: 0.75rem;
  }
}

@media (max-width: 640px) {
  .apartments-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .apartment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .apartment-rating {
    margin-left: 0;
  }
}

@media (max-width: 480px) {
  .apartment-image {
    height: 200px;
  }
  
  .apartment-content {
    padding: 1rem;
  }
}
</style>