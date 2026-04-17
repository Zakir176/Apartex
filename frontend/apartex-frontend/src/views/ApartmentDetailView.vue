<template>
  <div class="apartment-detail-container">
    <div v-if="apartmentsStore.loading" class="flex justify-content-center align-items-center min-h-screen">
      <ProgressSpinner />
    </div>
    
    <div v-else-if="apartmentsStore.error" class="error-wrapper p-6">
      <Message severity="error" :closable="false">{{ apartmentsStore.error }}</Message>
      <Button label="Back to Search" icon="pi pi-arrow-left" @click="router.push('/apartments')" class="p-button-text mt-3" />
    </div>

    <div v-else-if="apartment" class="detail-content fadein animation-duration-500">
      <!-- Breadcrumbs / Top Actions -->
      <nav class="breadcrumb-nav mb-4">
        <Button icon="pi pi-arrow-left" label="Back to listings" @click="router.back()" class="p-button-text p-button-sm mr-auto" />
        <div class="flex gap-2">
          <Button icon="pi pi-share-alt" class="p-button-rounded p-button-outlined p-button-secondary" />
          <Button 
            :icon="isApartmentWishlisted ? 'pi pi-heart-fill' : 'pi pi-heart'" 
            class="p-button-rounded p-button-outlined" 
            :class="{'p-button-danger': isApartmentWishlisted}" 
            @click="toggleWishlist" 
          />
        </div>
      </nav>

      <!-- Main Header -->
      <header class="header-section mb-5">
        <h1 class="text-4xl font-bold mb-2">{{ apartment.title }}</h1>
        <div class="flex align-items-center gap-3 text-gray-600">
          <div class="location">
            <i class="pi pi-map-marker mr-1"></i>
            {{ apartment.city }}, Zambia
          </div>
          <span>•</span>
          <div class="rating flex align-items-center">
            <i class="pi pi-star-fill text-yellow-500 mr-1"></i>
            <span class="font-bold">4.95</span>
            <span class="ml-1 opacity-70">(128 reviews)</span>
          </div>
        </div>
      </header>

      <!-- Image Gallery -->
      <section class="gallery-section mb-6">
        <Galleria 
          :value="galleryImages" 
          :responsiveOptions="responsiveOptions" 
          :numVisible="5" 
          containerStyle="max-width: 100%"
          :showThumbnails="true"
          :showItemNavigators="true"
          class="custom-galleria"
        >
          <template #item="slotProps">
            <img :src="slotProps.item.itemImageSrc" :alt="slotProps.item.alt" style="width: 100%; display: block; border-radius: 16px; height: 500px; object-fit: cover;" />
          </template>
          <template #thumbnail="slotProps">
            <img :src="slotProps.item.thumbnailImageSrc" :alt="slotProps.item.alt" style="display: block; border-radius: 8px; width: 100px; height: 75px; object-fit: cover;" />
          </template>
        </Galleria>
      </section>

      <!-- Main Grid (Description & Booking) -->
      <div class="main-grid">
        <div class="info-column">
          <section class="host-intro flex align-items-center justify-content-between mb-5 p-4 border-1 border-round-xl border-gray-200">
            <div>
              <h2 class="text-xl font-bold mb-1">Entire stay hosted by Sarah</h2>
              <p class="text-gray-600">{{ apartment.bedrooms }} bedrooms • {{ apartment.bathrooms }} bathrooms</p>
            </div>
            <Avatar icon="pi pi-user" size="xlarge" shape="circle" class="bg-primary text-white" />
          </section>

          <Divider />

          <section class="description-section py-4">
            <h3 class="text-2xl font-bold mb-3">About this place</h3>
            <p class="line-height-3 text-gray-700">{{ apartment.description }}</p>
            <Button label="Read more" class="p-button-link p-0 mt-2 font-bold" />
          </section>

          <Divider />

          <section class="amenities-section py-4">
            <h3 class="text-2xl font-bold mb-4">What this place offers</h3>
            <div class="amenities-chips">
              <Tag v-if="apartment.wifi" value="Fast WiFi" icon="pi pi-wifi" class="p-tag-secondary p-tag-rounded px-4 py-2 text-base font-semibold mr-3 mb-3" />
              <Tag value="Free Parking" icon="pi pi-car" class="p-tag-secondary p-tag-rounded px-4 py-2 text-base font-semibold mr-3 mb-3" />
              <Tag value="Air Conditioning" icon="pi pi-sun" class="p-tag-secondary p-tag-rounded px-4 py-2 text-base font-semibold mr-3 mb-3" />
              <Tag value="Kitchen" icon="pi pi-briefcase" class="p-tag-secondary p-tag-rounded px-4 py-2 text-base font-semibold mr-3 mb-3" />
              <Tag value="Pool Access" icon="pi pi-check" class="p-tag-secondary p-tag-rounded px-4 py-2 text-base font-semibold mr-3 mb-3" />
            </div>
            <Button label="Show all 24 amenities" class="p-button-outlined p-button-secondary mt-3 px-4 font-bold" />
          </section>
        </div>

        <div class="booking-column">
          <div class="sticky-sidebar">
            <BookingForm :apartment="apartment" />
          </div>
        </div>
      </div>

      <Divider class="my-6" />

      <!-- Reviews Section (Mocked) -->
      <section class="reviews-section pb-6">
        <header class="flex align-items-center gap-2 mb-5">
           <i class="pi pi-star-fill text-2xl text-yellow-500"></i>
           <h3 class="text-2xl font-bold m-0">4.95 • 128 reviews</h3>
        </header>

        <div class="reviews-grid">
          <div v-for="i in 4" :key="i" class="review-card mb-5">
            <div class="flex align-items-center mb-3">
              <Avatar icon="pi pi-user" shape="circle" class="mr-3" />
              <div>
                <div class="font-bold">Guest User {{ i }}</div>
                <div class="text-xs text-gray-500">October 2025</div>
              </div>
            </div>
            <p class="text-gray-700 line-height-3">
              This was an amazing stay! The apartment is exactly like the photos, and Sarah was a fantastic host. Very clean and great location!
            </p>
          </div>
        </div>
        <Button label="Show all reviews" class="p-button-outlined p-button-secondary px-5 font-bold" />
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useApartmentsStore } from '@/stores/apartments';
import { useWishlistStore } from '@/stores/wishlist';
import { useAuthStore } from '@/stores/auth';
import BookingForm from '@/components/BookingForm.vue';

// PrimeVue components
import Galleria from 'primevue/galleria';
import ProgressSpinner from 'primevue/progressspinner';
import Message from 'primevue/message';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import Divider from 'primevue/divider';
import Avatar from 'primevue/avatar';

const route = useRoute();
const router = useRouter();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();
const authStore = useAuthStore();

const apartment = computed(() => apartmentsStore.currentApartment);

const isApartmentWishlisted = computed(() => {
  return wishlistStore.wishlistItems.some(item => item.apartment_id === apartment.value?.id);
});

// Mocked gallery images using our placeholder
const galleryImages = computed(() => {
  const mainImg = apartment.value?.image_url || '/placeholder-apartment.png';
  return [
    { itemImageSrc: mainImg, thumbnailImageSrc: mainImg, alt: 'Main view' },
    { itemImageSrc: mainImg, thumbnailImageSrc: mainImg, alt: 'Living area' },
    { itemImageSrc: mainImg, thumbnailImageSrc: mainImg, alt: 'Bedroom' },
    { itemImageSrc: mainImg, thumbnailImageSrc: mainImg, alt: 'Kitchen' }
  ];
});

const responsiveOptions = [
  { breakpoint: '1024px', numVisible: 5 },
  { breakpoint: '768px', numVisible: 3 },
  { breakpoint: '560px', numVisible: 1 }
];

onMounted(async () => {
  await apartmentsStore.fetchApartmentById(route.params.id);
  await wishlistStore.fetchWishlist();
});

const toggleWishlist = async () => {
  if (!authStore.user) {
    router.push('/login');
    return;
  }

  if (isApartmentWishlisted.value) {
    await wishlistStore.removeFromWishlist(apartment.value.id);
  } else {
    await wishlistStore.addToWishlist(apartment.value.id);
  }
};
</script>

<style scoped>
.apartment-detail-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem;
}

.breadcrumb-nav {
  display: flex;
  align-items: center;
}

.main-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 4rem;
}

.sticky-sidebar {
  position: sticky;
  top: 100px;
}

.custom-galleria :deep(.p-galleria-item-wrapper) {
  border-radius: 16px;
}

.reviews-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 960px) {
  .main-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .reviews-grid {
    grid-template-columns: 1fr;
  }
  
  .apartment-detail-container {
    padding: 1rem;
  }
}
</style>