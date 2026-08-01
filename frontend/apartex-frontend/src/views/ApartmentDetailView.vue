<template>
  <div class="bg-white min-h-screen pb-20">
    <div v-if="apartmentsStore.loading" class="max-w-[1200px] mx-auto px-6 pt-8 flex flex-col gap-6">
      <Skeleton width="15rem" height="2rem" />
      <Skeleton width="60%" height="3rem" />
      <Skeleton width="40%" height="2rem" />
      <Skeleton width="100%" height="500px" class="rounded-3xl" />
      <div class="grid grid-cols-1 lg:grid-cols-[1.8fr_1fr] gap-12 mt-6">
         <div class="flex flex-col gap-6">
           <Skeleton width="100%" height="100px" class="rounded-2xl" />
           <Skeleton width="100%" height="250px" class="rounded-2xl" />
         </div>
         <Skeleton width="100%" height="400px" class="rounded-2xl" />
      </div>
    </div>
    
    <div v-else-if="apartmentsStore.error" class="max-w-2xl mx-auto p-12 text-center mt-20 card-base border-red-100 bg-red-50">
      <i class="pi pi-exclamation-triangle text-5xl text-red-500 mb-6"></i>
      <h2 class="text-3xl font-extrabold text-slate-800 mb-3">Something went wrong</h2>
      <p class="text-slate-600 font-medium mb-8 text-lg">{{ apartmentsStore.error }}</p>
      <button @click="router.push('/apartments')" class="px-6 py-3 rounded-full bg-white border border-surface-border font-bold text-slate-700 hover:bg-slate-50 transition-colors inline-flex items-center gap-2 shadow-sm">
        <i class="pi pi-arrow-left"></i>
        Return to Listings
      </button>
    </div>

    <div v-else-if="apartment" class="animate-fade-in">
      <!-- Top Contextual Navigation -->
      <nav class="sticky top-16 z-40 bg-white/80 backdrop-blur-md border-b border-surface-border">
        <div class="max-w-[1200px] mx-auto px-6 py-3 flex items-center justify-between">
          <button @click="router.back()" class="flex items-center gap-2 text-sm font-bold text-slate-600 hover:text-slate-900 transition-colors group">
            <div class="w-8 h-8 rounded-full border border-surface-border bg-white flex items-center justify-center group-hover:bg-slate-50">
              <i class="pi pi-chevron-left"></i>
            </div>
            <span>Back to Listings</span>
          </button>
          
          <div class="flex gap-2">
            <button class="w-10 h-10 rounded-full border border-surface-border bg-white text-slate-600 flex items-center justify-center hover:bg-slate-50 transition-colors">
              <i class="pi pi-share-alt"></i>
            </button>
            <button 
              class="w-10 h-10 rounded-full border bg-white flex items-center justify-center transition-all duration-300 transform active:scale-95"
              :class="isApartmentWishlisted ? 'border-red-200 text-red-500 bg-red-50' : 'border-surface-border text-slate-600 hover:bg-slate-50'"
              @click="toggleWishlist"
            >
              <i :class="isApartmentWishlisted ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
            </button>
          </div>
        </div>
      </nav>

      <div class="max-w-[1200px] mx-auto px-4 sm:px-6 pt-4 sm:pt-8">
        <!-- Main Header -->
        <header
          class="mb-6 sm:mb-8"
          v-motion
          :initial="{ opacity: 0, y: 24 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 100, duration: 400 } }"
        >
          <h1 class="text-2xl xs:text-3xl sm:text-4xl md:text-5xl font-black text-slate-800 mb-3 sm:mb-4 tracking-tight leading-tight">{{ apartment.title }}</h1>
          
          <div class="flex flex-wrap items-center gap-2 sm:gap-3 text-xs sm:text-sm font-bold text-slate-600">
            <div class="flex items-center gap-1.5 hover:underline cursor-pointer">
              <i class="pi pi-map-marker text-accent"></i>
              <span>{{ apartment.city }}, Zambia</span>
            </div>
            <div class="w-1 h-1 rounded-full bg-slate-300"></div>
            <div class="flex items-center gap-1.5 cursor-pointer hover:underline">
              <i class="pi pi-star-fill text-yellow-500"></i>
              <span class="text-slate-900">4.95</span>
              <span class="font-medium text-slate-500">({{ reviews.length }} reviews)</span>
            </div>
            <div class="w-1 h-1 rounded-full bg-slate-300"></div>
            <div class="px-3 py-1 rounded-full bg-gradient-to-r from-slate-900 to-slate-700 text-white text-[10px] font-black uppercase tracking-widest shadow-sm">
              Premier Selection
            </div>
          </div>
        </header>

        <!-- Premium Image Gallery (Pure Tailwind Grid) -->
        <section
          class="mb-8 sm:mb-12 h-[240px] xs:h-[300px] sm:h-[400px] lg:h-[500px] grid grid-cols-1 md:grid-cols-4 grid-rows-2 gap-3 rounded-2xl sm:rounded-3xl overflow-hidden group/gallery relative"
          v-motion
          :initial="{ opacity: 0 }"
          :enter="{ opacity: 1, transition: { duration: 600 } }"
        >
          <!-- Main Large Image -->
          <div class="md:col-span-2 row-span-2 relative overflow-hidden cursor-pointer group/img h-full" @click="showGallery = true">
            <img :src="galleryImages[0].itemImageSrc" :alt="apartment.title" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-700">
            <div class="absolute inset-0 bg-black/10 group-hover/img:bg-transparent transition-colors duration-300"></div>
          </div>
          
          <!-- Smaller Side Images -->
          <div class="hidden md:block relative overflow-hidden cursor-pointer group/img" @click="showGallery = true">
            <img :src="galleryImages[1].itemImageSrc" :alt="apartment.title" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-700">
            <div class="absolute inset-0 bg-black/10 group-hover/img:bg-transparent transition-colors duration-300"></div>
          </div>
          <div class="hidden md:block relative overflow-hidden cursor-pointer group/img" @click="showGallery = true">
            <img :src="galleryImages[2].itemImageSrc" :alt="apartment.title" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-700">
            <div class="absolute inset-0 bg-black/10 group-hover/img:bg-transparent transition-colors duration-300"></div>
          </div>
          <div class="hidden md:block relative overflow-hidden cursor-pointer group/img" @click="showGallery = true">
            <img :src="galleryImages[3].itemImageSrc" :alt="apartment.title" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-700">
            <div class="absolute inset-0 bg-black/10 group-hover/img:bg-transparent transition-colors duration-300"></div>
          </div>
          <div class="hidden md:block relative overflow-hidden cursor-pointer group/img" @click="showGallery = true">
            <img :src="galleryImages[4].itemImageSrc" :alt="apartment.title" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-700">
            <div class="absolute inset-0 bg-black/40 group-hover/img:bg-black/50 transition-colors duration-300"></div>
            <div class="absolute inset-0 flex flex-col items-center justify-center text-white backdrop-blur-[2px]">
              <i class="pi pi-images text-2xl mb-1"></i>
              <span class="font-bold text-sm tracking-widest uppercase">View All</span>
            </div>
          </div>

          <!-- Floating View All Button for Mobile -->
          <button @click="showGallery = true" class="md:hidden absolute bottom-4 right-4 px-4 py-2 rounded-lg bg-white/90 backdrop-blur-md shadow-md text-sm font-bold text-slate-800 flex items-center gap-2">
            <i class="pi pi-images"></i> 5+ Photos
          </button>
        </section>

        <!-- Main Layout Split -->
        <div class="grid grid-cols-1 lg:grid-cols-[1.8fr_1fr] gap-12 lg:gap-16 relative">
          
          <!-- Left Column: Details -->
          <div class="flex flex-col gap-10">
            
            <!-- Host Card -->
            <section class="card-base p-6 border-l-4 border-l-accent flex items-center justify-between">
              <div>
                <h2 class="text-2xl font-extrabold text-slate-800 mb-2">Hosted by Apartex Premier</h2>
                <div class="flex flex-wrap gap-x-4 gap-y-2 text-slate-500 font-bold text-sm">
                  <span>{{ apartment.bedrooms }} Bedrooms</span>
                  <span class="hidden sm:block">•</span>
                  <span>{{ apartment.bathrooms }} Bathrooms</span>
                  <span class="hidden sm:block">•</span>
                  <span>Up to {{ apartment.capacity }} Guests</span>
                </div>
              </div>
              <div class="relative w-14 h-14 flex-shrink-0 ml-4">
                <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150" alt="Host" class="w-full h-full rounded-full object-cover shadow-sm">
                <div class="absolute bottom-0 right-0 w-5 h-5 bg-accent text-white rounded-full flex items-center justify-center border-2 border-white">
                  <i class="pi pi-check text-[10px] font-bold"></i>
                </div>
              </div>
            </section>

            <div class="w-full h-px bg-surface-border"></div>

            <!-- Description -->
            <section>
              <h3 class="text-sm font-black uppercase tracking-widest text-slate-400 mb-5">The Residence</h3>
              <p class="text-lg text-slate-700 leading-relaxed font-medium mb-4 whitespace-pre-line">{{ apartment.description }}</p>
              <button class="text-slate-900 font-extrabold border-b-2 border-slate-900 pb-0.5 hover:text-accent hover:border-accent transition-colors">
                Read the full narrative <i class="pi pi-angle-right ml-1 text-sm"></i>
              </button>
            </section>

            <div class="w-full h-px bg-surface-border"></div>

            <!-- Amenities -->
            <section>
              <h3 class="text-sm font-black uppercase tracking-widest text-slate-400 mb-6">Refined Amenities</h3>
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-6 mb-6">
                <div v-for="amenity in (apartment.amenities || commonAmenities.slice(0, 6))" :key="amenity" class="flex items-center gap-3 group">
                  <div class="w-10 h-10 rounded-xl bg-slate-50 border border-surface-border flex items-center justify-center text-slate-500 group-hover:bg-white group-hover:shadow-sm group-hover:border-slate-200 group-hover:text-accent transition-all">
                    <i :class="getAmenityIcon(amenity)" class="text-lg"></i>
                  </div>
                  <span class="font-bold text-slate-700 group-hover:text-slate-900 transition-colors">{{ amenity }}</span>
                </div>
              </div>
              <button class="px-6 py-3 rounded-full border border-surface-border text-sm font-bold text-slate-700 hover:bg-slate-50 transition-colors inline-flex items-center gap-2">
                Show all {{ apartment.amenities?.length || 12 }} amenities
              </button>
            </section>

            <div class="w-full h-px bg-surface-border"></div>

            <!-- Location Map -->
            <section>
              <h3 class="text-sm font-black uppercase tracking-widest text-slate-400 mb-5">Location</h3>
              <p class="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
                <i class="pi pi-map-marker text-accent"></i>
                {{ apartment.address }}, {{ apartment.city }}
              </p>
              <div class="h-[400px] rounded-3xl overflow-hidden border border-surface-border shadow-sm">
                <MapComponent :city="apartment.city" :title="apartment.title" :lat="apartment.latitude" :lng="apartment.longitude" />
              </div>
            </section>
          </div>

          <!-- Right Column: Sticky Booking Widget -->
          <div
            class="relative"
            v-motion
            :initial="{ opacity: 0, x: 40 }"
            :enter="{ opacity: 1, x: 0, transition: { delay: 200, duration: 400 } }"
          >
            <div class="sticky top-32 z-30 flex flex-col gap-5">
              <!-- Wrapping the original BookingForm in a card-base container was already done inside the component usually, but let's ensure it has our shadow -->
              <div class="shadow-xl rounded-3xl overflow-hidden border border-surface-border bg-white">
                <!-- Apartment: direct booking form -->
                <BookingForm v-if="!isMultiRoomProperty" :apartment="apartment" />

                <!-- Hotel / Lodge / Guest House: date picker + room type cards -->
                <div v-else class="flex flex-col gap-4">
                  <!-- Date pickers -->
                  <div class="bg-white border border-surface-border rounded-xl p-4 shadow-sm">
                    <p class="text-xs font-black uppercase tracking-widest text-accent mb-3">Select Dates</p>
                    <div class="flex flex-col gap-3">
                      <div>
                        <label class="label-base">Check-in</label>
                        <input
                          v-model="selectedCheckIn"
                          type="date"
                          :min="new Date().toISOString().split('T')[0]"
                          class="input-base"
                        />
                      </div>
                      <div>
                        <label class="label-base">Check-out</label>
                        <input
                          v-model="selectedCheckOut"
                          type="date"
                          :min="selectedCheckIn || new Date().toISOString().split('T')[0]"
                          class="input-base"
                        />
                      </div>
                    </div>
                    <p v-if="nightsCount > 0" class="text-xs font-bold text-accent mt-3 flex items-center gap-1">
                      <i class="pi pi-moon text-xs"></i>
                      {{ nightsCount }} night{{ nightsCount !== 1 ? 's' : '' }} selected
                    </p>
                  </div>

                  <!-- Room type cards -->
                  <div v-if="roomsLoading" class="flex flex-col gap-3">
                    <div v-for="i in 3" :key="i" class="h-48 bg-slate-100 rounded-xl animate-pulse"></div>
                  </div>
                  <div v-else-if="propertyRooms.length > 0" class="flex flex-col gap-4">
                    <p class="text-sm font-black text-slate-700">Available Room Types</p>
                    <RoomCard
                      v-for="room in propertyRooms"
                      :key="room.id"
                      :room="room"
                      :nightsCount="nightsCount"
                      @book="handleRoomBook"
                    />
                  </div>
                  <div v-else class="bg-slate-50 border border-surface-border rounded-xl p-6 text-center">
                    <i class="pi pi-home text-2xl text-slate-300 mb-2"></i>
                    <p class="text-sm font-semibold text-slate-500">No room types configured yet.</p>
                  </div>
                </div>
              </div>
              
              <!-- Trust Indicators -->
              <div class="card-base p-5 flex flex-col gap-4 bg-slate-50/50">
                <div class="flex items-start gap-3">
                  <i class="pi pi-shield text-accent mt-0.5 text-lg"></i>
                  <div>
                    <h4 class="text-sm font-bold text-slate-800 mb-0.5">Apartex Protection Included</h4>
                    <p class="text-xs font-medium text-slate-500 m-0 leading-relaxed">Every booking includes free protection from Host cancellations and listing inaccuracies.</p>
                  </div>
                </div>
                <div class="h-px w-full bg-surface-border"></div>
                <div class="flex items-start gap-3">
                  <i class="pi pi-calendar-times text-accent mt-0.5 text-lg"></i>
                  <div>
                    <h4 class="text-sm font-bold text-slate-800 mb-0.5">Flexible Cancellation</h4>
                    <p class="text-xs font-medium text-slate-500 m-0 leading-relaxed">Cancel for free up to 48 hours before check-in for a full refund.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="w-full h-px bg-surface-border my-12"></div>

        <!-- Reviews Section -->
        <section class="pb-10">
          <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-10">
            <div class="flex items-center gap-4">
              <div class="px-4 py-2 rounded-xl bg-slate-900 text-white flex items-center gap-2 font-black text-xl shadow-md">
                <i class="pi pi-star-fill text-yellow-500"></i>
                {{ avgRating.toFixed(2) }}
              </div>
              <h3 class="text-3xl font-extrabold text-slate-800 m-0">{{ reviews.length }} Guest Reviews</h3>
            </div>
            <button v-if="authStore.user" @click="showReviewDialog = true" class="btn-accent shadow-accent inline-flex items-center gap-2">
              <i class="pi pi-pencil"></i>
              Share Experience
            </button>
          </header>

          <div v-if="reviews.length === 0" class="card-base p-12 text-center flex flex-col items-center bg-slate-50">
            <div class="w-16 h-16 rounded-full bg-white flex items-center justify-center mb-4 border border-surface-border text-slate-300">
              <i class="pi pi-comments text-2xl"></i>
            </div>
            <p class="text-slate-500 font-bold uppercase tracking-widest text-sm">No reviews yet for this sanctuary</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-12">
            <div v-for="review in reviews" :key="review.id" class="flex flex-col">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-3">
                  <Avatar icon="pi pi-user" shape="circle" class="bg-blue-100 text-blue-600 font-bold" />
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="font-extrabold text-slate-800 text-sm">Verified Guest</span>
                      <Tag v-if="review.is_verified" value="Verified Stay" severity="success" class="text-[9px] uppercase tracking-wider font-bold" rounded />
                    </div>
                    <span class="text-xs text-slate-500 font-medium">{{ formatDate(review.created_at) }}</span>
                  </div>
                </div>
                <div class="flex gap-0.5 text-xs">
                  <i v-for="s in 5" :key="s" :class="['pi pi-star-fill', s <= review.rating ? 'text-yellow-500' : 'text-slate-200']"></i>
                </div>
              </div>
              
              <p class="text-slate-700 font-medium leading-relaxed mb-4 flex-grow text-sm">
                {{ review.comment || 'An exceptional stay at this beautiful residence. Every detail was curated for comfort.' }}
              </p>
              
              <div v-if="review.images && review.images.length > 0" class="flex gap-2 flex-wrap">
                <div v-for="img in review.images" :key="img.id" class="w-20 h-20 rounded-lg overflow-hidden border border-surface-border">
                  <Image :src="img.image_url" alt="Review Image" class="w-full h-full object-cover" preview />
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Review Dialog -->
      <Dialog v-model:visible="showReviewDialog" modal header="Experience Feedback" :style="{ width: '500px', maxWidth: '95vw' }" contentClass="pt-2">
        <div class="flex flex-col gap-6 py-4">
          <div>
            <label class="label-base">Overall Rating</label>
            <Rating v-model="newReview.rating" :stars="5" :cancel="false" />
          </div>
          <div>
            <label class="label-base">Narrative</label>
            <Textarea v-model="newReview.comment" rows="4" placeholder="Share the highlights of your stay..." class="input-base w-full resize-none" />
          </div>
          <div>
            <label class="label-base">Photos of your stay (Optional)</label>
            <div class="flex flex-wrap gap-3 mb-3">
               <div v-for="(url, index) in newReview.image_urls" :key="index" class="relative w-16 h-16 rounded-lg overflow-hidden border border-surface-border">
                 <img :src="url" class="w-full h-full object-cover" />
                 <button @click="removeReviewImage(index)" class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center hover:bg-red-600 shadow-sm">
                   <i class="pi pi-times text-[10px]"></i>
                 </button>
               </div>
            </div>
            
            <input type="file" multiple accept="image/*" @change="handleReviewImageUpload" class="hidden" ref="fileInput" />
            <button @click="$refs.fileInput.click()" :disabled="uploadingImages" class="w-full px-4 py-3 rounded-xl border-2 border-dashed border-surface-border text-sm font-bold text-slate-500 hover:bg-slate-50 hover:text-slate-800 transition-colors flex items-center justify-center gap-2">
              <i :class="uploadingImages ? 'pi pi-spin pi-spinner' : 'pi pi-camera'"></i>
              <span>{{ uploadingImages ? 'Uploading photos...' : 'Upload Photos' }}</span>
            </button>
          </div>
        </div>
        <template #footer>
          <div class="flex gap-3 justify-end pt-4 border-t border-surface-border w-full">
            <button @click="showReviewDialog = false" class="px-5 py-2.5 rounded-full text-sm font-bold text-slate-500 hover:bg-slate-100 transition-colors">Cancel</button>
            <button @click="submitReview" :disabled="submittingReview || !newReview.rating" class="btn-accent inline-flex items-center gap-2">
              <i class="pi pi-check" v-if="!submittingReview"></i>
              <i class="pi pi-spinner pi-spin" v-else></i>
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
import RoomCard from '@/components/RoomCard.vue';
import MapComponent from '@/components/MapComponent.vue';
import { reviewsApi } from '@/api/reviews.js';
import { apartmentsApi } from '@/api/apartments.js';
import { uploadImage } from '@/api/uploads.js';

// PrimeVue components
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
const showGallery = ref(false); // Can be used to trigger a fullscreen lightbox later

const propertyRooms = ref([]);
const roomsLoading = ref(false);
const selectedCheckIn = ref('');
const selectedCheckOut = ref('');

const nightsCount = computed(() => {
  if (!selectedCheckIn.value || !selectedCheckOut.value) return 0;
  const diff = new Date(selectedCheckOut.value) - new Date(selectedCheckIn.value);
  return Math.max(0, Math.floor(diff / (1000 * 60 * 60 * 24)));
});

const isMultiRoomProperty = computed(() => {
  return apartment.value?.property_type &&
    ['hotel', 'lodge', 'guest_house'].includes(apartment.value.property_type);
});

const avgRating = computed(() => {
  if (reviews.value.length === 0) return 4.95;
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
  if (authStore.user) {
    await wishlistStore.fetchWishlist();
  }
  if (apartment.value?.id) {
    await fetchReviews(apartment.value.id);
  }

  // Load rooms for hotel/lodge/guest house properties
  if (apartment.value?.property_type && ['hotel', 'lodge', 'guest_house'].includes(apartment.value.property_type)) {
    roomsLoading.value = true;
    try {
      const res = await apartmentsApi.getRoomsForProperty(apartment.value.id);
      propertyRooms.value = res.data;
    } catch {
      propertyRooms.value = [];
    } finally {
      roomsLoading.value = false;
    }
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

function handleRoomBook(room) {
  // Navigate to checkout with room context
  router.push({
    path: '/checkout',
    query: {
      property_id: apartment.value.id,
      room_id: room.id,
      check_in: selectedCheckIn.value,
      check_out: selectedCheckOut.value,
    }
  });
}

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
.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
</style>
