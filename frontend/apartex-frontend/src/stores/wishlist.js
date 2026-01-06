import { defineStore } from 'pinia';
import { ref } from 'vue';
import { wishlistApi } from '../api/wishlist';

export const useWishlistStore = defineStore('wishlist', () => {
  const wishlistItems = ref([]);
  const loading = ref(false);
  const error = ref(null);

  async function fetchWishlist() {
    loading.value = true;
    error.value = null;
    try {
      const response = await wishlistApi.getWishlist();
      wishlistItems.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch wishlist';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function addToWishlist(apartmentId) {
    loading.value = true;
    error.value = null;
    try {
      const response = await wishlistApi.addToWishlist(apartmentId);
      wishlistItems.value.push(response.data);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to add to wishlist';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function removeFromWishlist(apartmentId) {
    loading.value = true;
    error.value = null;
    try {
      await wishlistApi.removeFromWishlist(apartmentId);
      wishlistItems.value = wishlistItems.value.filter(item => item.apartment_id !== apartmentId);
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to remove from wishlist';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    wishlistItems,
    loading,
    error,
    fetchWishlist,
    addToWishlist,
    removeFromWishlist
  };
});