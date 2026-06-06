<template>
  <div 
    class="ax-apartment-card" 
    :class="{'is-selected': isSelected}"
    @click="viewApartment"
    @mouseover="$emit('card-hover', apartment.id)"
    @mouseleave="$emit('card-leave', apartment.id)"
  >
    <div class="card-image-wrapper">
      <img :src="apartment.image_url || '/placeholder-apartment.png'" :alt="apartment.title" class="card-image">
      
      <!-- Premium Overlay Gradients -->
      <div class="image-overlay-top"></div>
      <div class="image-overlay-bottom"></div>
      
      <!-- Top Actions -->
      <div class="card-actions-top">
        <div class="price-pill">
          <span class="currency">$</span>
          <span class="amount">{{ apartment.price_per_night }}</span>
          <span class="period">/night</span>
        </div>
        
        <button class="wishlist-btn" :class="{ 'is-active': isWishlisted }" @click.stop="toggleWishlist">
          <i :class="isWishlisted ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
        </button>
      </div>

      <!-- Badge for New/Featured if applicable -->
      <div v-if="apartment.id % 5 === 0" class="featured-badge">
        <i class="pi pi-sparkles"></i>
        <span>Premier Selection</span>
      </div>
    </div>

    <div class="card-content">
      <div class="card-header">
        <div class="location-group">
          <i class="pi pi-map-marker"></i>
          <span>{{ apartment.city }}</span>
        </div>
        <h3 class="card-title">{{ apartment.title }}</h3>
      </div>

      <p class="card-description">{{ apartment.description }}</p>

      <div class="card-stats">
        <div class="stat-item">
          <i class="pi pi-users"></i>
          <span>{{ apartment.capacity }} guests</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <i class="pi pi-home"></i>
          <span>{{ apartment.bedrooms }} beds</span>
        </div>
      </div>

      <div class="card-footer">
        <div class="amenity-preview">
          <i v-for="icon in amenityIcons" :key="icon" :class="['pi', icon]"></i>
        </div>
        <button class="explore-btn">
          <span>Explore</span>
          <i class="pi pi-arrow-right"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useWishlistStore } from '@/stores/wishlist';
import { useAuthStore } from '@/stores/auth';
import { computed } from 'vue';

const props = defineProps({
  apartment: {
    type: Object,
    required: true
  },
  isWishlisted: {
    type: Boolean,
    default: false
  },
  isSelected: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['toggle-wishlist', 'card-hover', 'card-leave']);

const router = useRouter();
const wishlistStore = useWishlistStore();
const authStore = useAuthStore();

const amenityIcons = computed(() => {
  // Simple mapping for visual variety in the preview
  const icons = ['pi-wifi', 'pi-car'];
  if (props.apartment.bedrooms > 2) icons.push('pi-video');
  return icons;
});

const viewApartment = () => {
  router.push(`/apartments/${props.apartment.id}`);
};

const toggleWishlist = async () => {
  if (!authStore.user) {
    router.push('/login');
    return;
  }

  if (props.isWishlisted) {
    await wishlistStore.removeFromWishlist(props.apartment.id);
  } else {
    await wishlistStore.addToWishlist(props.apartment.id);
  }
  emit('toggle-wishlist', props.apartment.id, !props.isWishlisted);
};
</script>

<style scoped>
.ax-apartment-card {
  background: var(--surface-0);
  border-radius: calc(var(--border-radius) * 1.5);
  overflow: hidden;
  cursor: pointer;
  transition: var(--transition);
  height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--surface-100);
  box-shadow: var(--shadow-sm);
}

.ax-apartment-card:hover, .ax-apartment-card.is-selected {
  transform: translateY(-8px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary-color);
}

.ax-apartment-card.is-selected {
  border-width: 2px;
}

/* Image Section */
.card-image-wrapper {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.ax-apartment-card:hover .card-image {
  transform: scale(1.08);
}

.image-overlay-top {
  position: absolute;
  top: 0; left: 0; right: 0; height: 40%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, transparent 100%);
  z-index: 1;
}

.image-overlay-bottom {
  position: absolute;
  bottom: 0; left: 0; right: 0; height: 30%;
  background: linear-gradient(to top, rgba(0,0,0,0.2) 0%, transparent 100%);
  z-index: 1;
}

/* Actions Overlay */
.card-actions-top {
  position: absolute;
  top: 1rem;
  left: 1rem;
  right: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  z-index: 2;
}

.price-pill {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(8px);
  color: #fff;
  padding: 0.5rem 0.875rem;
  border-radius: 999px;
  display: flex;
  align-items: baseline;
  gap: 0.125rem;
  box-shadow: var(--shadow-md);
  border: 1px solid rgba(255,255,255,0.1);
}

.price-pill .amount { font-weight: 800; font-size: 1.125rem; }
.price-pill .currency { font-size: 0.75rem; font-weight: 600; opacity: 0.8; }
.price-pill .period { font-size: 0.75rem; font-weight: 500; opacity: 0.7; }

.wishlist-btn {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
  color: var(--surface-600);
  box-shadow: var(--shadow-sm);
}

.wishlist-btn:hover {
  transform: scale(1.1);
  background: #fff;
  color: #ef4444;
}

.wishlist-btn.is-active {
  color: #ef4444;
  background: #fff;
}

.featured-badge {
  position: absolute;
  bottom: 1rem;
  left: 1rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 0.375rem 0.75rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 2;
  box-shadow: var(--shadow-sm);
}

.featured-badge i { color: #f59e0b; font-size: 0.875rem; }
.featured-badge span { font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; color: var(--surface-900); }

/* Content Section */
.card-content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-header { margin-bottom: 0.75rem; }

.location-group {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  color: var(--surface-500);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.location-group i { color: var(--primary-color); }

.card-title {
  font-size: 1.125rem;
  font-weight: 800;
  color: var(--surface-900);
  line-height: 1.4;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-description {
  font-size: 0.875rem;
  color: var(--surface-500);
  line-height: 1.6;
  margin: 0 0 1.25rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
  padding: 0.75rem 1rem;
  background: var(--surface-50);
  border-radius: 0.75rem;
  border: 1px solid var(--surface-100);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--surface-700);
  font-size: 0.8125rem;
  font-weight: 600;
}

.stat-item i { color: var(--surface-400); font-size: 0.875rem; }
.stat-divider { width: 1px; height: 1rem; background: var(--surface-200); }

.card-footer {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid var(--surface-100);
}

.amenity-preview { display: flex; gap: 0.75rem; }
.amenity-preview i { color: var(--surface-300); font-size: 0.875rem; }

.explore-btn {
  background: transparent;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--primary-600);
  font-weight: 700;
  font-size: 0.875rem;
  padding: 0;
  cursor: pointer;
  transition: var(--transition);
}

.explore-btn:hover {
  color: var(--primary-700);
  transform: translateX(4px);
}
</style>
