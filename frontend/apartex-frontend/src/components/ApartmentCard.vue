<template>
  <div class="apartment-card" @click="viewApartment">
    <div class="apartment-image">
      <img :src="apartment.image_url || '/placeholder-apartment.jpg'" :alt="apartment.title">
      <div class="image-overlay"></div>
      <div class="price-tag">${{ apartment.price_per_night }}<span class="price-period">/night</span></div>
      <div class="favorite-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
        </svg>
      </div>
    </div>
    <div class="apartment-info">
      <h3 class="apartment-title">{{ apartment.title }}</h3>
      <p class="location">
        <svg class="location-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
          <circle cx="12" cy="10" r="3"></circle>
        </svg>
        {{ apartment.location }}
      </p>
      <p class="description">{{ apartment.description }}</p>
      <div class="amenities">
        <span v-if="apartment.bedrooms" class="amenity-badge">
          <svg class="amenity-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M2 4v16"></path>
            <path d="M2 8h18a2 2 0 0 1 2 2v10"></path>
            <path d="M2 17h20"></path>
            <path d="M6 8V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v4"></path>
          </svg>
          {{ apartment.bedrooms }} beds
        </span>
        <span v-if="apartment.bathrooms" class="amenity-badge">
          <svg class="amenity-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1-.5C4.683 3 4 3.683 4 4.5V17a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"></path>
            <line x1="10" x2="8" y1="5" y2="7"></line>
            <line x1="2" x2="22" y1="12" y2="12"></line>
            <line x1="7" x2="7" y1="19" y2="21"></line>
            <line x1="17" x2="17" y1="19" y2="21"></line>
          </svg>
          {{ apartment.bathrooms }} baths
        </span>
      </div>
      <div class="card-footer">
        <span class="view-details">View Details →</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  apartment: {
    type: Object,
    required: true
  }
});

const router = useRouter();

const viewApartment = () => {
  router.push(`/apartments/${props.apartment.id}`);
};
</script>

<style scoped>
.apartment-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.apartment-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
  z-index: 1;
}

.apartment-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 40px rgba(102, 126, 234, 0.25);
}

.apartment-card:hover::before {
  opacity: 1;
}

.apartment-image {
  position: relative;
  height: 240px;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.apartment-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.apartment-card:hover .apartment-image img {
  transform: scale(1.15);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.4) 100%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.apartment-card:hover .image-overlay {
  opacity: 1;
}

.price-tag {
  position: absolute;
  top: 16px;
  right: 16px;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.95));
  backdrop-filter: blur(10px);
  color: white;
  padding: 0.65rem 1.2rem;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  z-index: 2;
}

.apartment-card:hover .price-tag {
  transform: scale(1.1);
  background: linear-gradient(135deg, #667eea, #764ba2);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.price-period {
  font-size: 0.75rem;
  font-weight: 500;
  opacity: 0.9;
  margin-left: 2px;
}

.favorite-btn {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2;
  color: #667eea;
}

.favorite-btn:hover {
  background: white;
  transform: scale(1.15);
  color: #e91e63;
}

.apartment-info {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.apartment-title {
  margin: 0 0 0.75rem 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: #1a202c;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 0.3s ease;
}

.apartment-card:hover .apartment-title {
  color: #667eea;
}

.location {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #718096;
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
  font-weight: 500;
}

.location-icon {
  flex-shrink: 0;
  color: #667eea;
}

.description {
  color: #4a5568;
  margin: 0 0 1.25rem 0;
  font-size: 0.9rem;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.amenities {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.amenity-badge {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #f7fafc, #edf2f7);
  color: #4a5568;
  padding: 0.5rem 0.85rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
}

.apartment-card:hover .amenity-badge {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: transparent;
  transform: translateY(-2px);
}

.amenity-icon {
  flex-shrink: 0;
}

.card-footer {
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
  margin-top: auto;
}

.view-details {
  color: #667eea;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  display: inline-block;
}

.apartment-card:hover .view-details {
  transform: translateX(5px);
  color: #764ba2;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .apartment-image {
    height: 200px;
  }

  .apartment-title {
    font-size: 1.1rem;
  }

  .price-tag {
    font-size: 1rem;
    padding: 0.5rem 1rem;
  }
}
</style>