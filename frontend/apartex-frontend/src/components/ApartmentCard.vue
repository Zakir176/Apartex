<template>
  <div class="apartment-card" @click="viewApartment">
    <div class="apartment-image">
      <img :src="apartment.image_url || '/placeholder-apartment.jpg'" :alt="apartment.title">
      <div class="price">${{ apartment.price_per_night }}/night</div>
    </div>
    <div class="apartment-info">
      <h3>{{ apartment.title }}</h3>
      <p class="location">{{ apartment.location }}</p>
      <p class="description">{{ apartment.description }}</p>
      <div class="amenities">
        <span v-if="apartment.bedrooms">🛏️ {{ apartment.bedrooms }} beds</span>
        <span v-if="apartment.bathrooms">🚿 {{ apartment.bathrooms }} baths</span>
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
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.apartment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.apartment-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.apartment-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.price {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: bold;
}

.apartment-info {
  padding: 1.5rem;
}

.apartment-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
}

.location {
  color: #666;
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
}

.description {
  color: #555;
  margin: 0 0 1rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.amenities {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #666;
}
</style>