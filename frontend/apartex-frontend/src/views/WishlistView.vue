<template>
  <div class="max-w-[1200px] mx-auto px-6 py-12 min-h-screen">
    <!-- Header -->
    <div class="mb-10 text-center md:text-left">
      <h1 class="text-4xl font-extrabold text-slate-800 mb-2">My Wishlist</h1>
      <p class="text-slate-500 font-medium text-lg">Your curated collection of premium stays</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20 text-slate-400">
      <i class="pi pi-spinner pi-spin text-4xl mb-4 text-accent"></i>
      <p class="font-bold tracking-wider uppercase text-sm">Loading wishlist...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card-base p-10 text-center bg-red-50 border-red-100 flex flex-col items-center">
      <div class="w-16 h-16 rounded-full bg-white text-red-500 flex items-center justify-center mb-4 shadow-sm">
        <i class="pi pi-exclamation-triangle text-2xl"></i>
      </div>
      <p class="text-red-600 font-bold mb-2">Failed to load wishlist</p>
      <p class="text-sm font-medium text-red-400">{{ error }}</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="wishlistItems.length === 0" class="card-base p-16 text-center flex flex-col items-center justify-center">
      <div class="w-24 h-24 rounded-full bg-slate-50 flex items-center justify-center mb-6 border border-surface-border">
        <i class="pi pi-heart text-4xl text-slate-300"></i>
      </div>
      <h2 class="text-2xl font-bold text-slate-800 mb-3">Your wishlist is empty</h2>
      <p class="text-slate-500 font-medium mb-8 max-w-md">Start exploring our premium collection and save your favorite apartments for your next getaway.</p>
      <router-link to="/apartments" class="btn-accent shadow-accent inline-flex items-center gap-2 no-underline">
        <i class="pi pi-search"></i>
        Browse Apartments
      </router-link>
    </div>

    <!-- Wishlist Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <div v-for="item in wishlistItems" :key="item.id">
        <!-- Re-use the existing ApartmentCard component. Since I can't easily rewrite it here, I'll pass props. -->
        <ApartmentCard :apartment="item.apartment" :is-wishlisted="true" @toggle-wishlist="handleToggleWishlist" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useWishlistStore } from '@/stores/wishlist';
import ApartmentCard from '@/components/ApartmentCard.vue';

const wishlistStore = useWishlistStore();

const wishlistItems = computed(() => wishlistStore.wishlistItems);
const loading = computed(() => wishlistStore.loading);
const error = computed(() => wishlistStore.error);

onMounted(async () => {
  await wishlistStore.fetchWishlist();
});

const handleToggleWishlist = async (apartmentId, isWishlisted) => {
  if (!isWishlisted) {
    await wishlistStore.removeFromWishlist(apartmentId);
  } else {
    await wishlistStore.addToWishlist(apartmentId);
  }
};
</script>
