<template>
  <div 
    class="apartment-card" 
    :class="{'is-selected': isSelected}"
    @click="viewApartment"
    @mouseover="$emit('card-hover', apartment.id)"
    @mouseleave="$emit('card-leave', apartment.id)"
  >
    <div class="card-image-section">
      <img :src="apartment.image_url || '/placeholder-apartment.png'" :alt="apartment.title" class="card-image">
      
      <div class="price-pill">
        <span class="currency">$</span>
        <span class="amount">{{ apartment.price_per_night }}</span>
      </div>
      
      <button class="wishlist-btn" :class="{ 'active': isWishlisted }" @click.stop="toggleWishlist">
        <i :class="isWishlisted ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
      </button>
    </div>

    <div class="card-body">
      <div class="location">
        <i class="pi pi-map-marker"></i>
        <span>{{ apartment.city }}</span>
      </div>
      
      <h3 class="title">{{ apartment.title }}</h3>
      <p class="description">{{ apartment.description }}</p>

      <div class="stats-strip">
        <div class="stat">
          <i class="pi pi-users"></i>
          <span>{{ apartment.capacity }} guests</span>
        </div>
        <div class="stat">
          <i class="pi pi-home"></i>
          <span>{{ apartment.bedrooms }} beds</span>
        </div>
      </div>

      <div class="card-footer">
        <span class="explore-link">Explore &rarr;</span>
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
.apartment-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  transition: transform var(--transition-base), box-shadow var(--transition-base), border-color var(--transition-base);
}

.apartment-card:hover, .apartment-card.is-selected {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
  border-color: var(--color-border-strong);
}

.card-image-section {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.price-pill {
  position: absolute;
  top: var(--space-3);
  left: var(--space-3);
  background: rgba(0, 0, 0, 0.75);
  color: white;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.price-pill .amount {
  font-weight: 700;
  font-size: var(--font-size-base);
}

.price-pill .currency {
  font-size: var(--font-size-xs);
}

.wishlist-btn {
  position: absolute;
  top: var(--space-3);
  right: var(--space-3);
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-muted);
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-fast);
}

.wishlist-btn:hover {
  transform: scale(1.1);
}

.wishlist-btn.active {
  color: var(--color-error);
}

.card-body {
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  flex: 1;
}

.location {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  color: var(--color-accent);
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: var(--space-2);
}

.title {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 var(--space-2) 0;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.description {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin: 0 0 var(--space-4) 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.stats-strip {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  background: var(--color-surface-alt);
  border-radius: var(--radius-sm);
  padding: var(--space-2) var(--space-3);
  margin-bottom: var(--space-4);
}

.stat {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  color: var(--color-text-secondary);
  font-size: var(--font-size-xs);
  font-weight: 600;
}

.stat i {
  color: var(--color-text-muted);
}

.card-footer {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
}

.explore-link {
  color: var(--color-accent);
  font-weight: 600;
  font-size: var(--font-size-sm);
}
</style>
