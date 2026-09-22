<template>
  <div
    class="bg-white border border-surface-border rounded-xl overflow-hidden cursor-pointer group transition-shadow duration-200 hover:shadow-card-hover flex flex-col"
    :class="isSelected ? 'ring-2 ring-accent ring-offset-1' : ''"
    @click="viewApartment"
    @mouseover="$emit('card-hover', apartment.id)"
    @mouseleave="$emit('card-leave', apartment.id)"
  >
    <!-- Image -->
    <div class="relative aspect-[16/9] overflow-hidden bg-gray-100">
      <img
        :src="apartment.image_url || 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800'"
        :alt="apartment.title"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-[1.02]"
        @error="$event.target.src = 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800'"
      />

      <!-- Property type badge -->
      <div v-if="apartment.property_type && apartment.property_type !== 'apartment'" class="absolute top-3 left-3 bg-white text-gray-700 text-[10px] font-semibold uppercase tracking-wide px-2 py-1 rounded-md shadow-xs">
        {{ apartment.property_type.replace('_', ' ') }}
      </div>

      <!-- Price -->
      <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
        <p class="text-white font-semibold text-sm">
          {{ currencyStore.formatPrice(apartment.price_per_night) }}<span class="text-white/70 font-normal text-xs"> / night</span>
        </p>
      </div>

      <!-- Wishlist -->
      <button
        class="absolute top-3 right-3 w-8 h-8 rounded-lg bg-white flex items-center justify-center shadow-sm hover:shadow-md transition-shadow duration-150 border-0 cursor-pointer"
        :class="isWishlisted ? 'text-red-500' : 'text-gray-400 hover:text-red-400'"
        @click.stop="toggleWishlist"
      >
        <i :class="isWishlisted ? 'pi pi-heart-fill' : 'pi pi-heart'" class="text-sm"></i>
      </button>
    </div>

    <!-- Body -->
    <div class="p-4 flex flex-col gap-2 flex-1">
      <!-- Location -->
      <p class="text-xs font-medium text-gray-400 uppercase tracking-wide flex items-center gap-1">
        <i class="pi pi-map-marker text-xs"></i>
        {{ apartment.city }}
      </p>

      <!-- Title -->
      <h3 class="text-sm font-semibold text-gray-900 leading-snug line-clamp-1">
        {{ apartment.title }}
      </h3>

      <!-- Description -->
      <p class="text-xs text-gray-500 line-clamp-2 leading-relaxed flex-1">
        {{ apartment.description }}
      </p>

      <!-- Stats -->
      <div class="flex items-center gap-3 text-xs text-gray-500 pt-2 border-t border-surface-border mt-1">
        <span class="flex items-center gap-1">
          <i class="pi pi-users text-gray-300"></i>
          {{ apartment.capacity }} guests
        </span>
        <span class="w-px h-3 bg-gray-200"></span>
        <span class="flex items-center gap-1">
          <i class="pi pi-home text-gray-300"></i>
          {{ apartment.bedrooms || 0 }} beds
        </span>
        <span class="ml-auto text-accent font-medium text-xs group-hover:underline">
          View →
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useWishlistStore } from '@/stores/wishlist';
import { useAuthStore } from '@/stores/auth';
import { useCurrencyStore } from '@/stores/currency';
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
const currencyStore = useCurrencyStore();

const formattedPrice = computed(() => {
  return currencyStore.formatPrice(props.apartment.price_per_night);
});

const formattedPropertyType = computed(() => {
  const type = props.apartment.property_type || 'apartment';
  if (type === 'hotel') return 'Hotel';
  if (type === 'lodge') return 'Lodge';
  if (type === 'guest_house') return 'Guest House';
  return 'Apartment';
});

const imageUrl = computed(() => {
  const url = props.apartment.image_url;
  if (!url) return '/placeholder-apartment.png';
  if (url.startsWith('http') || url.startsWith('data:')) return url;
  return `http://localhost:8000${url}`;
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
