<template>
  <div class="apartment-detail-container">
    <div v-if="apartmentsStore.loading" class="flex flex-column gap-5 min-h-screen pt-4">
      <Skeleton width="15rem" height="2rem" class="mb-4" />
      <Skeleton width="60%" height="3rem" class="mb-2" />
      <Skeleton width="40%" height="2rem" class="mb-5" />
      <Skeleton width="100%" height="500px" class="border-round-2xl mb-6" />
      
      <div class="main-grid">
        <div class="info-column">
           <Skeleton width="100%" height="100px" class="border-round-xl mb-4" />
           <Skeleton width="100%" height="250px" class="border-round-xl mb-4" />
        </div>
        <div class="booking-column">
           <Skeleton width="100%" height="400px" class="border-round-xl" />
        </div>
      </div>
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

          <section class="location-section py-4">
            <h3 class="text-2xl font-bold mb-3">Where you'll be</h3>
            <p class="text-gray-600 mb-4">{{ apartment.address }}, {{ apartment.city }}</p>
            <div style="height: 400px;" class="border-round-xl overflow-hidden relative">
                 <Skeleton v-if="!apartment" width="100%" height="100%" class="absolute top-0 left-0" />
                 <MapComponent v-else :city="apartment.city" :title="apartment.title" />
            </div>
          </section>

          <Divider />

          <section class="amenities-section py-4">
            <h3 class="text-2xl font-bold mb-4">What this place offers</h3>
            <div class="amenities-chips" v-if="apartment.amenities && apartment.amenities.length > 0">
              <Tag 
                v-for="amenity in apartment.amenities" 
                :key="amenity" 
                :value="amenity" 
                :icon="getAmenityIcon(amenity)" 
                class="p-tag-secondary p-tag-rounded px-4 py-2 text-base font-semibold mr-3 mb-3" 
              />
            </div>
            <div v-else class="text-gray-500 italic mb-3">No specific amenities listed.</div>
            <Button v-if="apartment.amenities && apartment.amenities.length > 8" label="Show all amenities" class="p-button-outlined p-button-secondary mt-3 px-4 font-bold" />
          </section>
        </div>

        <div class="booking-column">
          <div class="sticky-sidebar">
            <BookingForm :apartment="apartment" />
          </div>
        </div>
      </div>

      <Divider class="my-6" />

      <!-- Reviews Section (Live) -->
      <section class="reviews-section pb-6">
        <header class="flex align-items-center justify-content-between mb-5">
          <div class="flex align-items-center gap-2">
            <i class="pi pi-star-fill text-2xl text-yellow-500"></i>
            <h3 class="text-2xl font-bold m-0">{{ avgRating.toFixed(2) }} • {{ reviews.length }} reviews</h3>
          </div>
          <Button
            v-if="authStore.user && hasUserBooked"
            label="Write a Review"
            icon="pi pi-pencil"
            @click="showReviewDialog = true"
            class="p-button-outlined p-button-sm font-bold"
          />
        </header>

        <!-- Review Loading Skeletons -->
        <div v-if="reviewsLoading" class="reviews-grid">
          <div v-for="i in 4" :key="i" class="review-card mb-5">
            <div class="flex align-items-center mb-3 gap-3">
              <Skeleton shape="circle" size="2.5rem" />
              <div class="flex flex-column gap-1">
                <Skeleton width="8rem" height="1rem" />
                <Skeleton width="5rem" height="0.75rem" />
              </div>
            </div>
            <Skeleton width="100%" height="3.5rem" />
          </div>
        </div>

        <!-- No Reviews Empty State -->
        <div v-else-if="reviews.length === 0" class="text-center py-5 border-round-xl border-1 border-gray-100 bg-gray-50">
          <i class="pi pi-comments text-5xl text-gray-300 mb-3" style="display: block"></i>
          <h4 class="text-lg font-bold text-gray-600 mb-1">No reviews yet</h4>
          <p class="text-gray-500 text-sm">Be the first to share your experience!</p>
        </div>

        <!-- Actual Reviews Grid -->
        <div v-else class="reviews-grid">
          <div v-for="review in reviews" :key="review.id" class="review-card mb-5">
            <div class="flex align-items-center mb-3">
              <Avatar icon="pi pi-user" shape="circle" class="mr-3 bg-primary text-white" />
              <div>
                <div class="font-bold">Guest #{{ review.user_id }}</div>
                <div class="text-xs text-gray-500">{{ formatDate(review.created_at) }}</div>
              </div>
              <div class="ml-auto flex gap-1">
                <i v-for="s in 5" :key="s" :class="['pi', s <= review.rating ? 'pi-star-fill text-yellow-500' : 'pi-star text-gray-300']" style="font-size: 0.8rem;"></i>
              </div>
            </div>
            <p class="text-gray-700 line-height-3 m-0">{{ review.comment || 'No comment provided.' }}</p>
          </div>
        </div>
      </section>

      <!-- Write Review Dialog -->
      <Dialog v-model:visible="showReviewDialog" modal header="Write a Review" :style="{ width: '450px' }">
        <div class="p-fluid pt-2">
          <div class="field mb-4">
            <label class="font-bold block mb-2">Your Rating</label>
            <Rating v-model="newReview.rating" :stars="5" />
          </div>
          <div class="field mb-4">
            <label class="font-bold block mb-2">Your Review</label>
            <Textarea v-model="newReview.comment" rows="4" placeholder="Tell others about your stay..." autoResize />
          </div>
        </div>
        <template #footer>
          <Button label="Cancel" class="p-button-text" @click="showReviewDialog = false" />
          <Button label="Submit Review" icon="pi pi-check" :loading="submittingReview" @click="submitReview" class="font-bold" />
        </template>
      </Dialog>
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
import MapComponent from '@/components/MapComponent.vue';
import { reviewsApi } from '@/api/reviews.js';

// PrimeVue components
import Galleria from 'primevue/galleria';
import ProgressSpinner from 'primevue/progressspinner';
import Message from 'primevue/message';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import Divider from 'primevue/divider';
import Avatar from 'primevue/avatar';
import Skeleton from 'primevue/skeleton';
import Dialog from 'primevue/dialog';
import Rating from 'primevue/rating';
import Textarea from 'primevue/textarea';

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

// Reviews state
const reviews = ref([]);
const reviewsLoading = ref(false);
const showReviewDialog = ref(false);
const submittingReview = ref(false);
const hasUserBooked = ref(false);
const newReview = ref({ rating: 0, comment: '' });

const avgRating = computed(() => {
  if (reviews.value.length === 0) return 0;
  return reviews.value.reduce((sum, r) => sum + r.rating, 0) / reviews.value.length;
});

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
};

const fetchReviews = async (id) => {
  reviewsLoading.value = true;
  try {
    const response = await reviewsApi.getApartmentReviews(id);
    reviews.value = response.data;
  } catch (e) {
    console.error('Failed to load reviews', e);
  } finally {
    reviewsLoading.value = false;
  }
};

const submitReview = async () => {
  if (!newReview.value.rating) return;
  submittingReview.value = true;
  try {
    await reviewsApi.createReview({
      apartment_id: apartment.value.id,
      rating: newReview.value.rating,
      comment: newReview.value.comment
    });
    showReviewDialog.value = false;
    newReview.value = { rating: 0, comment: '' };
    // Refresh reviews list
    await fetchReviews(apartment.value.id);
  } catch (e) {
    console.error('Failed to submit review', e);
  } finally {
    submittingReview.value = false;
  }
};

onMounted(async () => {
  await apartmentsStore.fetchApartmentById(route.params.id);
  await wishlistStore.fetchWishlist();
  if (apartment.value?.id) {
    await fetchReviews(apartment.value.id);
  }
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

const getAmenityIcon = (label) => {
  const icons = {
    'WiFi': 'pi pi-wifi',
    'Parking': 'pi pi-car',
    'Kitchen': 'pi pi-apple',
    'TV': 'pi pi-desktop',
    'Air Con': 'pi pi-box',
    'Pool': 'pi pi-water',
    'Gym': 'pi pi-user',
    'Laundry': 'pi pi-refresh',
    'Workspace': 'pi pi-briefcase',
    'Backyard': 'pi pi-sun'
  };
  return icons[label] || 'pi pi-check';
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