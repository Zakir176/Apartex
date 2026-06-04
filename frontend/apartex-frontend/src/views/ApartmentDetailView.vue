<template>
  <div class="ax-detail-page">
    <div v-if="apartmentsStore.loading" class="flex flex-column gap-5 min-h-screen pt-4 ax-container">
      <Skeleton width="15rem" height="2rem" class="mb-4" />
      <Skeleton width="60%" height="3rem" class="mb-2" />
      <Skeleton width="40%" height="2rem" class="mb-5" />
      <Skeleton width="100%" height="500px" class="border-round-2xl mb-6" />
      
      <div class="main-layout-grid">
        <div class="info-column">
           <Skeleton width="100%" height="100px" class="border-round-xl mb-4" />
           <Skeleton width="100%" height="250px" class="border-round-xl mb-4" />
        </div>
        <div class="booking-column">
           <Skeleton width="100%" height="400px" class="border-round-xl" />
        </div>
      </div>
    </div>
    
    <div v-else-if="apartmentsStore.error" class="error-wrapper p-6 text-center">
      <i class="pi pi-exclamation-triangle text-4xl text-red-500 mb-4"></i>
      <h2 class="text-2xl font-bold mb-2">Something went wrong</h2>
      <p class="text-600 mb-6">{{ apartmentsStore.error }}</p>
      <button @click="router.push('/apartments')" class="ax-button">
        <i class="pi pi-arrow-left mr-2"></i>
        <span>Return to Listings</span>
      </button>
    </div>

    <div v-else-if="apartment" class="detail-wrapper fadein animation-duration-500">
      <!-- Top Contextual Navigation -->
      <nav class="top-context-nav px-4 py-3 flex align-items-center justify-content-between">
        <button @click="router.back()" class="back-btn">
          <i class="pi pi-chevron-left"></i>
          <span>Listings</span>
        </button>
        <div class="flex gap-2">
          <button class="circle-action-btn"><i class="pi pi-share-alt"></i></button>
          <button 
            class="circle-action-btn" 
            :class="{'is-active': isApartmentWishlisted}" 
            @click="toggleWishlist"
          >
            <i :class="isApartmentWishlisted ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
          </button>
        </div>
      </nav>

      <div class="ax-container">
        <!-- Main Header -->
        <header class="header-section mt-4 mb-6 text-left">
          <h1 class="text-5xl font-extrabold tracking-tight mb-3">{{ apartment.title }}</h1>
          <div class="header-meta flex flex-wrap align-items-center gap-4">
            <div class="meta-item">
              <i class="pi pi-map-marker"></i>
              <span>{{ apartment.city }}, Zambia</span>
            </div>
            <div class="meta-divider"></div>
            <div class="meta-item highlight">
              <i class="pi pi-star-fill"></i>
              <span class="font-bold">4.95</span>
              <span class="count opacity-60">({{ reviews.length }} reviews)</span>
            </div>
            <div class="meta-divider"></div>
            <div class="meta-item">
              <span class="badge-elite">Premier Selection</span>
            </div>
          </div>
        </header>

        <!-- Premium Image Gallery -->
        <section class="gallery-section mb-8">
          <div class="gallery-grid">
            <div class="main-image">
              <img :src="galleryImages[0].itemImageSrc" :alt="apartment.title">
            </div>
            <div class="side-images">
              <div v-for="i in 2" :key="i" class="side-img-wrapper">
                <img :src="galleryImages[i].itemImageSrc" :alt="apartment.title">
              </div>
              <div class="side-img-wrapper more-images">
                <img :src="galleryImages[3].itemImageSrc" :alt="apartment.title">
                <div class="overlay-count">
                  <span class="text-2xl font-bold">+12</span>
                  <span class="text-xs font-bold uppercase tracking-widest">Photos</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Main Layout Split -->
        <div class="main-layout-grid">
          <div class="info-column">
            <!-- Host Card -->
            <section class="host-premium-card mb-6">
              <div class="flex align-items-center justify-content-between">
                <div class="host-info">
                  <h2 class="text-2xl font-extrabold text-900 mb-1">Managed by Sarah</h2>
                  <div class="flex gap-3 text-500 font-semibold text-sm">
                    <span>{{ apartment.bedrooms }} Bedrooms</span>
                    <span>•</span>
                    <span>{{ apartment.bathrooms }} Bathrooms</span>
                    <span>•</span>
                    <span>Up to {{ apartment.capacity }} Guests</span>
                  </div>
                </div>
                <div class="host-avatar">
                  <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150" alt="Host">
                  <div class="verified-badge"><i class="pi pi-check"></i></div>
                </div>
              </div>
            </section>

            <Divider class="my-6 opacity-40" />

            <!-- Description -->
            <section class="description-premium mb-8 text-left">
              <h3 class="text-xl font-extrabold uppercase tracking-widest text-400 mb-4">The Residence</h3>
              <p class="text-xl text-700 line-height-4 font-medium">{{ apartment.description }}</p>
              <button class="text-900 font-extrabold border-bottom-2 border-900 bg-transparent border-none p-0 pb-1 mt-4 cursor-pointer">Read the full narrative</button>
            </section>

            <Divider class="my-6 opacity-40" />

            <!-- Amenities -->
            <section class="amenities-premium mb-8 text-left">
              <h3 class="text-xl font-extrabold uppercase tracking-widest text-400 mb-6">Refined Amenities</h3>
              <div class="amenity-luxury-grid">
                <div v-for="amenity in (apartment.amenities || commonAmenities.slice(0, 6))" :key="amenity" class="amenity-item">
                  <div class="amenity-icon-box">
                    <i :class="getAmenityIcon(amenity)"></i>
                  </div>
                  <span class="font-bold text-700">{{ amenity }}</span>
                </div>
              </div>
              <button class="ax-button p-button-outlined mt-6">
                <span>All {{ apartment.amenities?.length || 12 }} Amenities</span>
              </button>
            </section>

            <Divider class="my-6 opacity-40" />

            <!-- Location Map -->
            <section class="location-premium mb-8 text-left">
              <h3 class="text-xl font-extrabold uppercase tracking-widest text-400 mb-6">Location</h3>
              <p class="text-lg font-bold text-900 mb-6">{{ apartment.address }}, {{ apartment.city }}</p>
              <div class="map-premium-wrapper">
                   <MapComponent 
                     :city="apartment.city" 
                     :title="apartment.title" 
                     :lat="apartment.latitude" 
                     :lng="apartment.longitude" 
                   />
              </div>
            </section>
          </div>

          <!-- Sticky Booking Sidebar -->
          <div class="booking-column">
            <div class="sticky-booking-card">
              <BookingForm :apartment="apartment" />
              
              <div class="trust-indicators mt-4 p-3 border-round-xl bg-slate-50 flex flex-column gap-3">
                <div class="flex align-items-center gap-3">
                  <i class="pi pi-shield text-primary-600 font-bold"></i>
                  <span class="text-xs font-bold text-700 uppercase tracking-wider">Apartex Protection Included</span>
                </div>
                <div class="flex align-items-center gap-3">
                  <i class="pi pi-calendar-times text-primary-600 font-bold"></i>
                  <span class="text-xs font-bold text-700 uppercase tracking-wider">Free cancellation for 48h</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <Divider class="my-8 opacity-40" />

        <!-- Reviews: Enhanced Premium Layout -->
        <section class="reviews-luxury pb-8 text-left">
          <header class="flex align-items-center justify-content-between mb-8">
            <div class="flex align-items-center gap-3">
              <div class="rating-hero">
                <i class="pi pi-star-fill"></i>
                <span>{{ avgRating.toFixed(2) }}</span>
              </div>
              <h3 class="text-3xl font-extrabold m-0">{{ reviews.length }} Guest Reviews</h3>
            </div>
            <button
              v-if="authStore.user"
              @click="showReviewDialog = true"
              class="ax-button"
            >
              <i class="pi pi-pencil mr-2"></i>
              <span>Share Experience</span>
            </button>
          </header>

          <!-- Review Grid -->
          <div v-if="reviews.length === 0" class="empty-reviews text-center py-6 bg-slate-50 border-round-2xl border-1 border-100">
            <i class="pi pi-comments text-4xl text-300 mb-3"></i>
            <p class="text-500 font-bold uppercase tracking-widest">No reviews yet for this sanctuary</p>
          </div>

          <div v-else class="reviews-luxury-grid">
            <div v-for="review in reviews" :key="review.id" class="luxury-review-card">
              <div class="review-header mb-4">
                <div class="reviewer-meta">
                  <Avatar icon="pi pi-user" shape="circle" class="bg-primary text-white" />
                  <div>
                    <div class="flex align-items-center gap-2">
                      <span class="block font-extrabold text-900">Verified Member</span>
                      <Tag v-if="review.is_verified" value="Verified Stay" severity="success" class="text-xs" rounded />
                    </div>
                    <span class="block text-xs text-500 font-bold uppercase tracking-wider">{{ formatDate(review.created_at) }}</span>
                  </div>
                </div>
                <div class="review-rating">
                  <i v-for="s in 5" :key="s" :class="['pi pi-star-fill', s <= review.rating ? 'text-primary-500' : 'text-100']"></i>
                </div>
              </div>
              <p class="review-text line-height-4 text-700 font-medium mb-4">{{ review.comment || 'An exceptional stay at this beautiful residence. Every detail was curated for comfort.' }}</p>
              
              <!-- Review Images -->
              <div v-if="review.images && review.images.length > 0" class="review-images-grid flex gap-2 flex-wrap">
                <div v-for="img in review.images" :key="img.id" class="review-img-thumb">
                  <Image :src="img.image_url" alt="Review Image" width="80" height="80" preview class="border-round-lg overflow-hidden" />
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Review Dialog (Kept simple but styled) -->
      <Dialog v-model:visible="showReviewDialog" modal header="Experience Feedback" :style="{ width: '480px' }" class="ax-sidebar-premium">
        <div class="p-fluid pt-2">
          <div class="mb-4">
            <label class="ax-label mb-3">Overall Rating</label>
            <Rating v-model="newReview.rating" :stars="5" :cancel="false" />
          </div>
          <div class="mb-4">
            <label class="ax-label mb-3">Narrative</label>
            <Textarea v-model="newReview.comment" rows="5" placeholder="Share the highlights of your stay..." class="ax-input" />
          </div>
          <div class="mb-4">
            <label class="ax-label mb-3">Photos of your stay</label>
            <div class="flex flex-wrap gap-2 mb-2">
               <div v-for="(url, index) in newReview.image_urls" :key="index" class="relative">
                 <img :src="url" class="w-4rem h-4rem border-round-lg object-cover" />
                 <button @click="removeReviewImage(index)" class="absolute top-0 right-0 bg-red-500 text-white border-none border-circle w-1rem h-1rem flex align-items-center justify-content-center cursor-pointer -mt-1 -mr-1">
                   <i class="pi pi-times text-xs"></i>
                 </button>
               </div>
            </div>
            <div class="upload-trigger-box">
              <input type="file" multiple accept="image/*" @change="handleReviewImageUpload" class="hidden" ref="fileInput" />
              <button @click="$refs.fileInput.click()" class="ax-button p-button-outlined w-full" :disabled="uploadingImages">
                <i :class="uploadingImages ? 'pi pi-spin pi-spinner' : 'pi pi-camera'" class="mr-2"></i>
                <span>{{ uploadingImages ? 'Uploading...' : 'Add Photos' }}</span>
              </button>
            </div>
          </div>
        </div>
        <template #footer>
          <div class="flex gap-2 w-full">
            <button @click="showReviewDialog = false" class="p-button p-button-text flex-1 font-bold">Cancel</button>
            <button @click="submitReview" :disabled="submittingReview || !newReview.rating" class="ax-button flex-1">
              <span>{{ submittingReview ? 'Publishing...' : 'Publish Review' }}</span>
            </button>
          </div>
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
import { uploadImage } from '@/api/uploads.js';

// PrimeVue components
import Message from 'primevue/message';
import Button from 'primevue/button';
import Divider from 'primevue/divider';
import Avatar from 'primevue/avatar';
import Skeleton from 'primevue/skeleton';
import Dialog from 'primevue/dialog';
import Rating from 'primevue/rating';
import Textarea from 'primevue/textarea';
import Tag from 'primevue/tag';
import Image from 'primevue/image';

const route = useRoute();
const router = useRouter();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();
const authStore = useAuthStore();

const apartment = computed(() => apartmentsStore.currentApartment);

const isApartmentWishlisted = computed(() => {
  return wishlistStore.wishlistItems.some(item => item.apartment_id === apartment.value?.id);
});

const commonAmenities = ['WiFi', 'Pool', 'Parking', 'Kitchen', 'TV', 'Air Con', 'Gym', 'Laundry'];

const galleryImages = computed(() => {
  const mainImg = apartment.value?.image_url || '/placeholder-apartment.png';
  return Array(5).fill({ itemImageSrc: mainImg });
});

const reviews = ref([]);
const showReviewDialog = ref(false);
const submittingReview = ref(false);
const uploadingImages = ref(false);
const newReview = ref({ rating: 0, comment: '', image_urls: [] });

const avgRating = computed(() => {
  if (reviews.value.length === 0) return 4.9;
  return reviews.value.reduce((sum, r) => sum + r.rating, 0) / reviews.value.length;
});

const formatDate = (dateStr) => {
  if (!dateStr) return 'Recent Stay';
  return new Date(dateStr).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
};

const handleReviewImageUpload = async (event) => {
  const files = event.target.files;
  if (!files.length) return;
  
  uploadingImages.value = true;
  try {
    for (let file of files) {
      const result = await uploadImage(file);
      newReview.value.image_urls.push(result.url);
    }
  } catch (e) {
    console.error('Image upload failed', e);
  } finally {
    uploadingImages.value = false;
    event.target.value = ''; // Reset input
  }
};

const removeReviewImage = (index) => {
  newReview.value.image_urls.splice(index, 1);
};

const fetchReviews = async (id) => {
  try {
    const response = await reviewsApi.getApartmentReviews(id);
    reviews.value = response.data;
  } catch (e) {
    console.error('Failed to load reviews', e);
  }
};

const submitReview = async () => {
  if (!newReview.value.rating) return;
  submittingReview.value = true;
  try {
    await reviewsApi.createReview({
      apartment_id: apartment.value.id,
      rating: newReview.value.rating,
      comment: newReview.value.comment,
      image_urls: newReview.value.image_urls
    });
    showReviewDialog.value = false;
    newReview.value = { rating: 0, comment: '', image_urls: [] };
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
    'WiFi': 'pi pi-wifi', 'Parking': 'pi pi-car', 'Kitchen': 'pi pi-apple',
    'TV': 'pi pi-desktop', 'Air Con': 'pi pi-box', 'Pool': 'pi pi-water',
    'Gym': 'pi pi-user', 'Laundry': 'pi pi-refresh'
  };
  return icons[label] || 'pi pi-check';
};
</script>

<style scoped>
.ax-detail-page { background: #fff; min-height: 100vh; }

.top-context-nav {
  position: sticky;
  top: 5rem;
  z-index: 100;
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--surface-100);
}

.back-btn {
  background: transparent; border: none;
  display: flex; align-items: center; gap: 0.5rem;
  font-weight: 700; color: var(--surface-600);
  cursor: pointer; transition: var(--transition);
}
.back-btn:hover { color: var(--surface-900); transform: translateX(-4px); }

.circle-action-btn {
  width: 2.5rem; height: 2.5rem;
  border-radius: 50%; border: 1px solid var(--surface-200);
  background: #fff; display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: var(--transition);
}
.circle-action-btn:hover { background: var(--surface-50); transform: scale(1.1); }
.circle-action-btn.is-active { color: #ef4444; border-color: #fee2e2; background: #fef2f2; }

/* Header */
.meta-item { display: flex; align-items: center; gap: 0.5rem; color: var(--surface-600); font-weight: 600; font-size: 0.875rem; }
.meta-item i { color: var(--primary-600); }
.meta-divider { width: 4px; height: 4px; background: var(--surface-200); border-radius: 50%; }
.meta-item.highlight { color: var(--surface-900); }
.meta-item.highlight i { color: #f59e0b; }
.badge-elite { 
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: #fff; padding: 0.25rem 0.75rem; border-radius: 999px;
  font-size: 0.625rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;
}

/* Gallery Grid */
.gallery-section { height: 500px; }
.gallery-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
  height: 100%;
}
.main-image { border-radius: 1.5rem; overflow: hidden; position: relative; }
.main-image img { width: 100%; height: 100%; object-fit: cover; }
.side-images { display: grid; grid-template-rows: 1fr 1fr; gap: 1rem; }
.side-img-wrapper { border-radius: 1rem; overflow: hidden; position: relative; }
.side-img-wrapper img { width: 100%; height: 100%; object-fit: cover; }
.more-images { position: relative; cursor: pointer; }
.overlay-count {
  position: absolute; inset: 0; background: rgba(0,0,0,0.4);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  color: #fff; backdrop-filter: blur(4px);
}

/* Layout */
.main-layout-grid { display: grid; grid-template-columns: 1.8fr 1fr; gap: 4rem; }
.sticky-booking-card { position: sticky; top: 10rem; }

/* Host Card */
.host-premium-card {
  padding: 1.5rem; background: var(--surface-50);
  border-radius: 1.5rem; border: 1px solid var(--surface-100);
}
.host-avatar { position: relative; width: 4rem; height: 4rem; }
.host-avatar img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
.verified-badge {
  position: absolute; bottom: 0; right: 0;
  width: 1.25rem; height: 1.25rem; background: var(--primary-600);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 0.625rem; border: 2px solid #fff;
}

/* Amenities */
.amenity-luxury-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.amenity-item { display: flex; align-items: center; gap: 1rem; }
.amenity-icon-box {
  width: 2.5rem; height: 2.5rem; background: var(--surface-50);
  border-radius: 0.75rem; display: flex; align-items: center; justify-content: center;
  color: var(--surface-500); border: 1px solid var(--surface-100);
}

/* Map */
.map-premium-wrapper {
  height: 400px; border-radius: 1.5rem; overflow: hidden;
  border: 1px solid var(--surface-100); box-shadow: var(--shadow-sm);
}

/* Reviews */
.rating-hero {
  background: var(--surface-900); color: #fff;
  padding: 0.5rem 1rem; border-radius: 1rem;
  display: flex; align-items: center; gap: 0.5rem; font-weight: 800;
}
.rating-hero i { color: #f59e0b; }
.reviews-luxury-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; }
.reviewer-meta { display: flex; align-items: center; gap: 1rem; }
.review-rating i { font-size: 0.625rem; margin-right: 0.125rem; }

@media (max-width: 1024px) {
  .main-layout-grid { grid-template-columns: 1fr; gap: 3rem; }
  .gallery-section { height: 350px; }
  .gallery-grid { grid-template-columns: 1fr; }
  .side-images { display: none; }
  .reviews-luxury-grid { grid-template-columns: 1fr; gap: 2rem; }
}
</style>
