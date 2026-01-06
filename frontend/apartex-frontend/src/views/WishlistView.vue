<template>
  <div class="page-container">
    <h2>My Wishlist</h2>

    <div v-if="loading" class="loading-message">
      Loading your wishlist...
    </div>
    <div v-else-if="error" class="error-message">
      Error: {{ error }}
    </div>
    <div v-else-if="wishlistItems.length === 0" class="empty-wishlist">
      <p>Your wishlist is empty. Start adding apartments you love!</p>
      <router-link to="/apartments" class="btn-browse-apartments">Browse Apartments</router-link>
    </div>
    <div v-else class="wishlist-grid">
      <div v-for="item in wishlistItems" :key="item.id" class="wishlist-item">
        <ApartmentCard :apartment="item.apartment" :is-wishlisted="true" @toggle-wishlist="handleToggleWishlist" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useWishlistStore } from '@/stores/wishlist';
import ApartmentCard from '@/components/ApartmentCard.vue';
import { useRouter } from 'vue-router';

const wishlistStore = useWishlistStore();
const router = useRouter();

const wishlistItems = computed(() => wishlistStore.wishlistItems);
const loading = computed(() => wishlistStore.loading);
const error = computed(() => wishlistStore.error);

onMounted(async () => {
  await wishlistStore.fetchWishlist();
});

const handleToggleWishlist = async (apartmentId, isWishlisted) => {
  if (!isWishlisted) {
    // If it was wishlisted and now it's not, remove it
    await wishlistStore.removeFromWishlist(apartmentId);
  } else {
    // If it was not wishlisted and now it is, add it (shouldn't happen via this button)
    // This case might be handled by an "add to wishlist" button on apartment detail page
    await wishlistStore.addToWishlist(apartmentId);
  }
};
</script>

<style scoped>
.page-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  margin-bottom: 24px;
  color: var(--text);
  text-align: center;
}

.loading-message,
.error-message,
.empty-wishlist {
  text-align: center;
  padding: 40px;
  background-color: var(--bg-light);
  border-radius: 8px;
  margin-top: 40px;
  color: var(--text-muted);
}

.error-message {
  color: var(--danger);
  background-color: var(--danger-light);
}

.empty-wishlist p {
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.btn-browse-apartments {
  display: inline-block;
  padding: 10px 20px;
  background-color: var(--primary);
  color: var(--primary-contrast);
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.2s ease;
}

.btn-browse-apartments:hover {
  background-color: var(--primary-dark);
}

.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.wishlist-item {
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease;
}

.wishlist-item:hover {
  transform: translateY(-5px);
}
</style>
