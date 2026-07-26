<template>
  <div
    class="card-base cursor-pointer flex flex-col overflow-hidden rounded-2xl group border border-slate-200/80 bg-white hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
    :class="isSelected ? 'ring-2 ring-accent shadow-lg' : 'shadow-sm'"
    @click="viewApartment"
    @mouseover="$emit('card-hover', apartment.id)"
    @mouseleave="$emit('card-leave', apartment.id)"
  >
    <!-- Image Header -->
    <div class="relative aspect-[4/3] overflow-hidden bg-slate-100">
      <img
        :src="imageUrl"
        :alt="apartment.title"
        class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
      />

      <!-- Property Type Badge -->
      <div v-if="apartment.property_type" class="absolute top-3 left-3 bg-white/90 backdrop-blur-md text-slate-900 text-[11px] font-black uppercase tracking-wider px-2.5 py-1 rounded-full shadow-sm flex items-center gap-1 border border-white/60">
        <i class="pi pi-building text-accent text-[10px]"></i>
        <span>{{ formattedPropertyType }}</span>
      </div>

      <!-- Price Pill -->
      <div class="absolute bottom-3 left-3 bg-slate-900/90 backdrop-blur-md text-white text-sm font-black px-3.5 py-1.5 rounded-full flex items-baseline gap-1 shadow-md border border-white/10">
        <span>{{ formattedPrice }}</span>
        <span class="text-[11px] font-normal opacity-75">/night</span>
      </div>

      <!-- Wishlist Button -->
      <button
        class="absolute top-3 right-3 w-9 h-9 rounded-full bg-white/90 backdrop-blur-md flex items-center justify-center shadow-md hover:scale-110 transition-transform duration-200 cursor-pointer border-0"
        :class="isWishlisted ? 'text-red-500' : 'text-slate-400 hover:text-red-400'"
        @click.stop="toggleWishlist"
        title="Save to Wishlist"
      >
        <i :class="isWishlisted ? 'pi pi-heart-fill' : 'pi pi-heart'" class="text-sm"></i>
      </button>
    </div>

    <!-- Body -->
    <div class="flex flex-col flex-1 p-5 gap-2.5">
      <!-- Location & Rating -->
      <div class="flex items-center justify-between text-xs">
        <div class="flex items-center gap-1 text-accent font-black uppercase tracking-wider">
          <i class="pi pi-map-marker text-xs"></i>
          <span>{{ apartment.city }}</span>
        </div>
        <div class="flex items-center gap-1 font-bold text-slate-700 bg-slate-100/80 px-2 py-0.5 rounded-full">
          <i class="pi pi-star-fill text-amber-400 text-xs"></i>
          <span>4.9</span>
        </div>
      </div>

      <!-- Title -->
      <h3 class="text-base font-extrabold text-slate-900 leading-snug line-clamp-1 group-hover:text-accent transition-colors">
        {{ apartment.title }}
      </h3>

      <!-- Description -->
      <p class="text-xs text-slate-500 line-clamp-2 leading-relaxed font-medium">
        {{ apartment.description || 'Modern luxury stay equipped with essential amenities, prime location, and high-speed internet.' }}
      </p>

      <!-- Stats strip -->
      <div class="flex items-center gap-3 mt-1 px-3 py-2 bg-slate-50 rounded-xl text-xs text-slate-600 border border-slate-100 font-bold">
        <div class="flex items-center gap-1.5">
          <i class="pi pi-users text-slate-400 text-xs"></i>
          <span>{{ apartment.capacity }} guests</span>
        </div>
        <div class="w-px h-3 bg-slate-200"></div>
        <div class="flex items-center gap-1.5">
          <i class="pi pi-home text-slate-400 text-xs"></i>
          <span>{{ apartment.bedrooms }} beds</span>
        </div>
      </div>

      <!-- Footer CTA -->
      <div class="mt-auto pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-bold">
        <span class="text-slate-400 flex items-center gap-1">
          <i class="pi pi-check-circle text-emerald-500"></i> Instant Book
        </span>
        <span class="text-accent group-hover:translate-x-1 transition-transform duration-200 inline-flex items-center gap-1 font-black">
          View Details <i class="pi pi-arrow-right text-xs"></i>
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
