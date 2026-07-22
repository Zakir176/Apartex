<template>
  <div
    class="card-base cursor-pointer flex flex-col overflow-hidden rounded-lg group"
    :class="isSelected ? 'ring-2 ring-accent' : ''"
    @click="viewApartment"
    @mouseover="$emit('card-hover', apartment.id)"
    @mouseleave="$emit('card-leave', apartment.id)"
  >
    <!-- Image -->
    <div class="relative aspect-[4/3] overflow-hidden">
      <img
        :src="imageUrl"
        :alt="apartment.title"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
      />

      <!-- Price pill -->
      <div class="absolute top-3 left-3 bg-slate-900/80 backdrop-blur-sm text-white text-sm font-bold px-3 py-1.5 rounded-full flex items-baseline gap-0.5">
        <span class="text-xs font-medium opacity-75">$</span>
        <span>{{ apartment.price_per_night }}</span>
        <span class="text-xs font-normal opacity-60">/night</span>
      </div>

      <!-- Wishlist -->
      <button
        class="absolute top-3 right-3 w-9 h-9 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center shadow-sm hover:scale-110 transition-transform duration-150"
        :class="isWishlisted ? 'text-red-500' : 'text-slate-400 hover:text-red-400'"
        @click.stop="toggleWishlist"
      >
        <i :class="isWishlisted ? 'pi pi-heart-fill' : 'pi pi-heart'" class="text-sm"></i>
      </button>
    </div>

    <!-- Body -->
    <div class="flex flex-col flex-1 p-4 gap-2">
      <!-- Location -->
      <div class="flex items-center gap-1 text-accent text-xs font-bold uppercase tracking-wide">
        <i class="pi pi-map-marker text-xs"></i>
        <span>{{ apartment.city }}</span>
      </div>

      <!-- Title -->
      <h3 class="text-base font-bold text-slate-800 leading-snug line-clamp-1">{{ apartment.title }}</h3>

      <!-- Description -->
      <p class="text-sm text-slate-500 line-clamp-2 leading-relaxed">{{ apartment.description }}</p>

      <!-- Stats strip -->
      <div class="flex items-center gap-3 mt-1 px-3 py-2 bg-[#F8F7F4] rounded-md text-sm text-slate-600">
        <div class="flex items-center gap-1.5">
          <i class="pi pi-users text-slate-400 text-xs"></i>
          <span class="font-medium">{{ apartment.capacity }} guests</span>
        </div>
        <div class="w-px h-3 bg-slate-200"></div>
        <div class="flex items-center gap-1.5">
          <i class="pi pi-home text-slate-400 text-xs"></i>
          <span class="font-medium">{{ apartment.bedrooms }} beds</span>
        </div>
      </div>

      <!-- Footer -->
      <div class="mt-auto pt-3 border-t border-surface-border flex justify-end">
        <span class="text-sm font-semibold text-accent group-hover:translate-x-1 transition-transform duration-150 inline-flex items-center gap-1">
          Explore <i class="pi pi-arrow-right text-xs"></i>
        </span>
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
