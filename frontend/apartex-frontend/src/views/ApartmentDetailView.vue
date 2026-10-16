<template>
  <div class="bg-white min-h-screen pb-20">
    <!-- LOADING SKELETON -->
    <div v-if="apartmentsStore.loading" class="max-w-[1250px] mx-auto px-6 pt-8 flex flex-col gap-6">
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
    
    <!-- ERROR STATE -->
    <div v-else-if="apartmentsStore.error" class="max-w-2xl mx-auto p-12 text-center mt-20 card-base border-red-100 bg-red-50">
      <i class="pi pi-exclamation-triangle text-5xl text-red-500 mb-6"></i>
      <h2 class="text-3xl font-extrabold text-slate-800 mb-3">Unable to Load Stay</h2>
      <p class="text-slate-600 font-medium mb-8 text-lg">{{ apartmentsStore.error }}</p>
      <button @click="router.push('/apartments')" class="px-6 py-3 rounded-full bg-white border border-surface-border font-bold text-slate-700 hover:bg-slate-50 transition-colors inline-flex items-center gap-2 shadow-sm cursor-pointer">
        <i class="pi pi-arrow-left"></i>
        <span>Return to Stay Directory</span>
      </button>
    </div>

    <!-- MAIN APARTMENT CONTENT -->
    <div v-else-if="apartment" class="animate-fade-in">
      
      <!-- STICKY TOP NAVIGATION BAR -->
      <nav class="sticky top-16 z-40 bg-white/90 backdrop-blur-md border-b border-surface-border">
        <div class="max-w-[1250px] mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <button @click="router.push('/apartments')" class="flex items-center gap-2 text-xs font-bold text-slate-600 hover:text-slate-900 transition-colors group cursor-pointer border-0 bg-transparent">
              <div class="w-8 h-8 rounded-full border border-surface-border bg-white flex items-center justify-center group-hover:bg-slate-100 transition-colors">
                <i class="pi pi-chevron-left text-xs"></i>
              </div>
              <span class="hidden sm:inline">Explore Stays</span>
            </button>
            <span class="text-slate-300 hidden sm:inline">/</span>
            <span class="text-xs font-bold text-slate-500 truncate max-w-[200px] sm:max-w-[300px]">{{ apartment.city }}</span>
          </div>
          
          <div class="flex items-center gap-2">
            <button 
              @click="shareApartment" 
              class="px-3 py-1.5 rounded-full border border-surface-border bg-white text-slate-700 text-xs font-bold flex items-center gap-1.5 hover:bg-slate-50 transition-colors cursor-pointer"
              title="Share Listing"
            >
              <i class="pi pi-share-alt text-xs"></i>
              <span class="hidden sm:inline">{{ copied ? 'Link Copied!' : 'Share' }}</span>
            </button>
            <button 
              class="px-3.5 py-1.5 rounded-full border text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer"
              :class="isApartmentWishlisted ? 'border-red-200 text-red-500 bg-red-50' : 'border-surface-border text-slate-700 bg-white hover:bg-slate-50'"
              @click="toggleWishlist"
            >
              <i :class="isApartmentWishlisted ? 'pi pi-heart-fill' : 'pi pi-heart'" class="text-xs"></i>
              <span class="hidden sm:inline">{{ isApartmentWishlisted ? 'Saved' : 'Save' }}</span>
            </button>
          </div>
        </div>
      </nav>

      <div class="max-w-[1250px] mx-auto px-4 sm:px-6 pt-6 sm:pt-8">
        
        <!-- HEADER TITLE & HIGHLIGHT BADGES -->
        <header class="mb-6 sm:mb-8">
          <div class="flex items-center gap-2 mb-3">
            <span class="px-3 py-1 rounded-full bg-slate-900 text-white text-[10px] font-black uppercase tracking-widest shadow-xs">
              {{ apartment.property_type ? apartment.property_type.replace('_', ' ') : 'Luxury Suite' }}
            </span>
            <span class="px-3 py-1 rounded-full bg-orange-50 text-accent text-[10px] font-black uppercase tracking-widest border border-orange-100">
              <i class="pi pi-verified text-[10px] mr-1"></i> Apartex Verified
            </span>
          </div>

          <h1 class="text-2xl sm:text-4xl lg:text-5xl font-black text-slate-900 mb-3 tracking-tight leading-tight">
            {{ apartment.title }}
          </h1>
          
          <div class="flex flex-wrap items-center gap-3 text-xs sm:text-sm font-bold text-slate-600">
            <div class="flex items-center gap-1 text-slate-800">
              <i class="pi pi-map-marker text-accent"></i>
              <span>{{ apartment.address ? `${apartment.address}, ` : '' }}{{ apartment.city }}, Zambia</span>
            </div>
            <div class="w-1 h-1 rounded-full bg-slate-300"></div>
            <div class="flex items-center gap-1">
              <i class="pi pi-star-fill text-amber-400 text-xs"></i>
              <span class="text-slate-900 font-extrabold">{{ avgRating.toFixed(2) }}</span>
              <span class="font-medium text-slate-500">({{ reviews.length }} verified review{{ reviews.length !== 1 ? 's' : '' }})</span>
            </div>
          </div>
        </header>

        <!-- LUXURY PHOTO GALLERY MASONRY GRID -->
        <section class="mb-8 sm:mb-12 h-[260px] sm:h-[420px] lg:h-[480px] grid grid-cols-1 md:grid-cols-4 grid-rows-2 gap-3 rounded-3xl overflow-hidden relative shadow-sm group/gallery">
          <!-- Main Cover Photo -->
          <div class="md:col-span-2 row-span-2 relative overflow-hidden cursor-pointer group/img h-full" @click="showGalleryModal = true">
            <img :src="resolvePhotoUrl(apartment.image_url)" :alt="apartment.title" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-700">
            <div class="absolute inset-0 bg-black/10 group-hover/img:bg-transparent transition-colors"></div>
          </div>
          
          <!-- Secondary Side Photos -->
          <div v-for="(photoUrl, i) in secondaryPhotos" :key="i" class="hidden md:block relative overflow-hidden cursor-pointer group/img" @click="showGalleryModal = true">
            <img :src="photoUrl" :alt="`${apartment.title} photo ${i+2}`" class="w-full h-full object-cover group-hover/img:scale-105 transition-transform duration-700">
            <div class="absolute inset-0 bg-black/10 group-hover/img:bg-transparent transition-colors"></div>
            
            <!-- View All Overlay on Last Card -->
            <div v-if="i === 2" class="absolute inset-0 bg-slate-900/60 backdrop-blur-[2px] flex flex-col items-center justify-center text-white transition-opacity group-hover/img:bg-slate-900/70">
              <i class="pi pi-images text-2xl mb-1"></i>
              <span class="font-black text-xs tracking-widest uppercase">View All Photos</span>
            </div>
          </div>

          <!-- Mobile View Photos Pill Button -->
          <button @click="showGalleryModal = true" class="md:hidden absolute bottom-4 right-4 px-4 py-2 rounded-full bg-slate-900/90 text-white backdrop-blur-md shadow-md text-xs font-black flex items-center gap-2 border-0 cursor-pointer">
            <i class="pi pi-images text-xs"></i> Show Photos
          </button>
        </section>

        <!-- MAIN TWO-COLUMN LAYOUT -->
        <div class="grid grid-cols-1 lg:grid-cols-[1.8fr_1fr] gap-10 lg:gap-14 relative">
          
          <!-- LEFT COLUMN: PROPERTY DETAILS -->
          <div class="flex flex-col gap-10">
            
            <!-- HOST & QUICK SPECIFICATIONS CARD -->
            <section class="bg-white rounded-3xl p-6 border border-surface-border shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-6">
              <div>
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-xs font-black uppercase tracking-wider text-accent">Managed by Apartex Premier Host</span>
                  <i class="pi pi-shield-check text-emerald-500 text-sm"></i>
                </div>
                <h2 class="text-xl sm:text-2xl font-black text-slate-900 mb-3">Residence Specs & Capacity</h2>
                <div class="flex flex-wrap gap-2 text-xs font-bold text-slate-600">
                  <span class="px-3 py-1 bg-slate-100 rounded-lg text-slate-700">
                    <i class="pi pi-home text-slate-400 mr-1"></i> {{ apartment.bedrooms || 1 }} Bedrooms
                  </span>
                  <span class="px-3 py-1 bg-slate-100 rounded-lg text-slate-700">
                    <i class="pi pi-bath text-slate-400 mr-1"></i> {{ apartment.bathrooms || 1 }} Bathrooms
                  </span>
                  <span class="px-3 py-1 bg-slate-100 rounded-lg text-slate-700">
                    <i class="pi pi-users text-slate-400 mr-1"></i> Up to {{ apartment.capacity || 2 }} Guests
                  </span>
                  <span class="px-3 py-1 bg-emerald-50 text-emerald-700 border border-emerald-100 rounded-lg">
                    <i class="pi pi-sun text-emerald-500 mr-1"></i> 24/7 Solar Backup
                  </span>
                </div>
              </div>

              <div class="flex items-center gap-3 shrink-0 sm:border-l sm:border-slate-100 sm:pl-6">
                <div class="w-14 h-14 rounded-full bg-accent text-white font-black text-lg flex items-center justify-center shadow-md">
                  AP
                </div>
                <div>
                  <p class="text-xs font-extrabold text-slate-900 mb-0.5">Apartex Concierge</p>
                  <p class="text-[11px] text-emerald-600 font-bold mb-0">100% Response Rate</p>
                </div>
              </div>
            </section>

            <!-- DESCRIPTION NARRATIVE -->
            <section>
              <h3 class="text-xs font-black uppercase tracking-widest text-slate-400 mb-4">The Stay Narrative</h3>
              <p class="text-base text-slate-700 leading-relaxed font-medium whitespace-pre-line">
                {{ apartment.description || 'Experience ultimate luxury and serenity. This property comes fully furnished with high-speed fiber internet, continuous backup power, private parking, and round-the-clock security.' }}
              </p>
            </section>

            <div class="w-full h-px bg-slate-100"></div>

            <!-- REFINED AMENITIES GRID -->
            <section>
              <h3 class="text-xs font-black uppercase tracking-widest text-slate-400 mb-6">Featured Amenities</h3>
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-6">
                <div v-for="amenity in displayAmenities" :key="amenity" class="flex items-center gap-3 p-3 bg-slate-50 rounded-2xl border border-slate-100">
                  <div class="w-9 h-9 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-accent shadow-2xs">
                    <i :class="getAmenityIcon(amenity)" class="text-base"></i>
                  </div>
                  <span class="font-bold text-xs text-slate-800">{{ amenity }}</span>
                </div>
              </div>
            </section>

            <div class="w-full h-px bg-slate-100"></div>

            <!-- LOCATION MAP -->
            <section>
              <h3 class="text-xs font-black uppercase tracking-widest text-slate-400 mb-4">Location & Neighborhood</h3>
              <p class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                <i class="pi pi-map-marker text-accent"></i>
                {{ apartment.address ? `${apartment.address}, ` : '' }}{{ apartment.city }}, Zambia
              </p>
              <div class="h-[380px] rounded-3xl overflow-hidden border border-slate-200 shadow-sm">
                <MapComponent :city="apartment.city" :title="apartment.title" :lat="apartment.latitude" :lng="apartment.longitude" />
              </div>
            </section>
          </div>

          <!-- RIGHT COLUMN: STICKY RESERVATION WIDGET -->
          <div class="relative">
            <div class="sticky top-24 z-30 flex flex-col gap-5">
              
              <!-- CARD CONTAINER -->
              <div class="bg-white rounded-3xl border border-slate-200 shadow-xl overflow-hidden p-6">
                <!-- PRICE DISPLAY HEADER -->
                <div class="flex items-baseline justify-between mb-6 pb-4 border-b border-slate-100">
                  <div>
                    <span class="text-3xl font-black text-slate-900 tracking-tight">{{ formattedPrice }}</span>
                    <span class="text-xs font-bold text-slate-400 ml-1">/ night</span>
                  </div>
                  <div class="flex items-center gap-1 text-xs font-bold text-slate-700 bg-slate-100 px-2.5 py-1 rounded-full">
                    <i class="pi pi-star-fill text-amber-400 text-xs"></i>
                    <span>{{ avgRating.toFixed(2) }}</span>
                  </div>
                </div>

                <!-- DIRECT BOOKING FORM OR MULTI-ROOM TYPE -->
                <BookingForm v-if="!isMultiRoomProperty" :apartment="apartment" />

                <div v-else class="flex flex-col gap-4">
                  <!-- Date selector -->
                  <div class="bg-slate-50 border border-slate-200 rounded-2xl p-4">
                    <p class="text-[10px] font-black uppercase tracking-widest text-accent mb-3">Select Reservation Dates</p>
                    <div class="grid grid-cols-2 gap-3">
                      <div>
                        <label class="text-[10px] font-black text-slate-400 uppercase block mb-1">Check-in</label>
                        <input
                          v-model="selectedCheckIn"
                          type="date"
                          :min="todayDate"
                          class="input-base !py-2 !text-xs"
                        />
                      </div>
                      <div>
                        <label class="text-[10px] font-black text-slate-400 uppercase block mb-1">Check-out</label>
                        <input
                          v-model="selectedCheckOut"
                          type="date"
                          :min="selectedCheckIn || todayDate"
                          class="input-base !py-2 !text-xs"
                        />
                      </div>
                    </div>
                    <p v-if="nightsCount > 0" class="text-xs font-bold text-accent mt-3 flex items-center gap-1">
                      <i class="pi pi-moon text-xs"></i>
                      {{ nightsCount }} night{{ nightsCount !== 1 ? 's' : '' }} stay
                    </p>
                  </div>

                  <!-- Available Room Cards -->
                  <div v-if="roomsLoading" class="flex flex-col gap-3">
                    <div v-for="i in 2" :key="i" class="h-36 bg-slate-100 rounded-2xl animate-pulse"></div>
                  </div>
                  <div v-else-if="propertyRooms.length > 0" class="flex flex-col gap-3">
                    <p class="text-xs font-black uppercase tracking-wider text-slate-700">Available Room Types</p>
                    <RoomCard
                      v-for="room in propertyRooms"
                      :key="room.id"
                      :room="room"
                      :nightsCount="nightsCount"
                      @book="handleRoomBook"
                    />
                  </div>
                </div>

                <!-- TRUST PROTECTION STRIP -->
                <div class="mt-6 pt-4 border-t border-slate-100 flex flex-col gap-3 text-xs text-slate-500 font-medium">
                  <div class="flex items-center gap-2 text-slate-700 font-bold">
                    <i class="pi pi-shield-check text-emerald-500 text-sm"></i>
                    <span>Apartex Guarantee Included</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <i class="pi pi-calendar text-slate-400 text-xs"></i>
                    <span>Free cancellation up to 48h before check-in</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>

        <div class="w-full h-px bg-slate-100 my-12"></div>

        <!-- REVIEWS & EXPERIENCE RATING SECTION -->
        <section class="pb-10">
          <header class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
            <div class="flex items-center gap-4">
              <div class="px-4 py-2.5 rounded-2xl bg-slate-900 text-white flex items-center gap-2 font-black text-xl shadow-md">
                <i class="pi pi-star-fill text-amber-400"></i>
                {{ avgRating.toFixed(2) }}
              </div>
              <div>
                <h3 class="text-2xl sm:text-3xl font-black text-slate-900 m-0">Guest Reviews</h3>
                <p class="text-xs text-slate-500 font-bold m-0 mt-0.5">Based on {{ reviews.length }} verified stay reviews</p>
              </div>
            </div>
            
            <button v-if="authStore.user" @click="showReviewDialog = true" class="btn-accent px-6 py-3 rounded-full text-xs font-black inline-flex items-center gap-2 shadow-accent">
              <i class="pi pi-pencil"></i>
              Write Review
            </button>
          </header>

          <!-- CATEGORY SCORE BREAKDOWN -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10 p-6 bg-slate-50 rounded-3xl border border-slate-100">
            <div>
              <span class="block text-[10px] font-black text-slate-400 uppercase tracking-wider mb-1">Cleanliness</span>
              <div class="flex items-center gap-2">
                <div class="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                  <div class="h-full bg-accent rounded-full" style="width: 98%"></div>
                </div>
                <span class="text-xs font-black text-slate-800">4.9</span>
              </div>
            </div>
            <div>
              <span class="block text-[10px] font-black text-slate-400 uppercase tracking-wider mb-1">Accuracy</span>
              <div class="flex items-center gap-2">
                <div class="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                  <div class="h-full bg-accent rounded-full" style="width: 100%"></div>
                </div>
                <span class="text-xs font-black text-slate-800">5.0</span>
              </div>
            </div>
            <div>
              <span class="block text-[10px] font-black text-slate-400 uppercase tracking-wider mb-1">Communication</span>
              <div class="flex items-center gap-2">
                <div class="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                  <div class="h-full bg-accent rounded-full" style="width: 96%"></div>
                </div>
                <span class="text-xs font-black text-slate-800">4.8</span>
              </div>
            </div>
            <div>
              <span class="block text-[10px] font-black text-slate-400 uppercase tracking-wider mb-1">Value</span>
              <div class="flex items-center gap-2">
                <div class="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                  <div class="h-full bg-accent rounded-full" style="width: 98%"></div>
                </div>
                <span class="text-xs font-black text-slate-800">4.9</span>
              </div>
            </div>
          </div>

          <!-- REVIEWS LIST -->
          <div v-if="reviews.length === 0" class="bg-white rounded-3xl p-12 text-center border border-slate-200 flex flex-col items-center">
            <div class="w-14 h-14 rounded-full bg-orange-50 text-accent flex items-center justify-center mb-4">
              <i class="pi pi-comments text-2xl"></i>
            </div>
            <p class="text-slate-800 font-black text-base mb-1">No Reviews Yet</p>
            <p class="text-slate-500 font-medium text-xs max-w-sm">Be the first guest to share your review after your stay at this residence.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="review in reviews" :key="review.id" class="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-xs flex flex-col">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-3">
                  <Avatar icon="pi pi-user" shape="circle" class="bg-slate-900 text-white font-bold" />
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="font-black text-slate-900 text-xs">Verified Guest</span>
                      <Tag v-if="review.is_verified" value="Verified Stay" severity="success" class="text-[9px] uppercase tracking-wider font-bold" rounded />
                    </div>
                    <span class="text-[11px] text-slate-400 font-medium">{{ formatDate(review.created_at) }}</span>
                  </div>
                </div>
                <div class="flex gap-0.5 text-xs">
                  <i v-for="s in 5" :key="s" :class="['pi pi-star-fill', s <= review.rating ? 'text-amber-400' : 'text-slate-200']"></i>
                </div>
              </div>
              
              <p class="text-slate-700 font-medium leading-relaxed text-xs flex-grow">
                {{ review.comment || 'Exceptional stay. The accommodation exceeded expectations in cleanliness, comfort, and prime location.' }}
              </p>
            </div>
          </div>
        </section>

      </div>

      <!-- FULLSCREEN GALLERY LIGHTBOX DIALOG -->
      <Dialog 
        v-model:visible="showGalleryModal" 
        header="Photo Gallery" 
        :modal="true" 
        :style="{ width: '800px', maxWidth: '95vw' }"
      >
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 py-3">
          <div v-for="(img, idx) in allGalleryPhotos" :key="idx" class="rounded-2xl overflow-hidden aspect-[4/3] bg-slate-100">
            <img :src="img" :alt="`${apartment.title} gallery photo ${idx+1}`" class="w-full h-full object-cover" />
          </div>
        </div>
      </Dialog>

      <!-- WRITE REVIEW DIALOG -->
      <Dialog v-model:visible="showReviewDialog" modal header="Share Your Experience" :style="{ width: '480px', maxWidth: '95vw' }">
        <div class="flex flex-col gap-5 py-3">
          <div>
            <label class="label-base">Overall Rating</label>
            <Rating v-model="newReview.rating" :stars="5" :cancel="false" />
          </div>
          <div>
            <label class="label-base">Your Experience</label>
            <Textarea v-model="newReview.comment" rows="4" placeholder="Describe the highlights, cleanliness, and ambiance..." class="input-base w-full resize-none !text-xs" />
          </div>
        </div>
        <template #footer>
          <div class="flex gap-3 justify-end pt-3 border-t border-slate-100 w-full">
            <button @click="showReviewDialog = false" class="px-5 py-2 rounded-full text-xs font-bold text-slate-500 hover:bg-slate-100">Cancel</button>
            <button @click="submitReview" :disabled="submittingReview || !newReview.rating" class="btn-accent text-xs font-black px-6 py-2.5 rounded-full inline-flex items-center gap-2">
              <i class="pi pi-check" v-if="!submittingReview"></i>
              <i class="pi pi-spinner pi-spin" v-else></i>
              <span>{{ submittingReview ? 'Submitting...' : 'Submit Review' }}</span>
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
import { useCurrencyStore } from '@/stores/currency';
import BookingForm from '@/components/BookingForm.vue';
import RoomCard from '@/components/RoomCard.vue';
import MapComponent from '@/components/MapComponent.vue';
import { reviewsApi } from '@/api/reviews.js';
import { apartmentsApi } from '@/api/apartments.js';

// PrimeVue components
import Avatar from 'primevue/avatar';
import Skeleton from 'primevue/skeleton';
import Dialog from 'primevue/dialog';
import Rating from 'primevue/rating';
import Textarea from 'primevue/textarea';
import Tag from 'primevue/tag';

const route = useRoute();
const router = useRouter();
const apartmentsStore = useApartmentsStore();
const wishlistStore = useWishlistStore();
const authStore = useAuthStore();
const currencyStore = useCurrencyStore();

const apartment = computed(() => apartmentsStore.currentApartment);

const isApartmentWishlisted = computed(() => {
  return wishlistStore.wishlistItems.some(item => item.apartment_id === apartment.value?.id);
});

const copied = ref(false);
const showGalleryModal = ref(false);

const presetPhotos = [
  'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80',
  'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80',
  'https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=800&q=80'
];

const resolvePhotoUrl = (url) => {
  if (!url || url.includes('placeholder')) return presetPhotos[0];
  return url;
};

const secondaryPhotos = computed(() => {
  const main = resolvePhotoUrl(apartment.value?.image_url);
  return presetPhotos.slice(1, 4);
});

const allGalleryPhotos = computed(() => {
  return [resolvePhotoUrl(apartment.value?.image_url), ...presetPhotos.slice(1)];
});

const displayAmenities = computed(() => {
  if (apartment.value?.amenities) {
    let ams = apartment.value.amenities;
    if (typeof ams === 'string') {
      try {
        ams = JSON.parse(ams);
      } catch {
        ams = [ams];
      }
    }
    if (Array.isArray(ams) && ams.length > 0) return ams;
  }
  return ['High-Speed WiFi', 'Continuous Solar Power', 'Air Conditioning', 'Private Swimming Pool', 'Secure Parking', 'Fully Equipped Kitchen'];
});

const formattedPrice = computed(() => {
  if (!apartment.value?.price_per_night) return '$0';
  return currencyStore.formatPrice(apartment.value.price_per_night);
});

const reviews = ref([]);
const showReviewDialog = ref(false);
const submittingReview = ref(false);
const newReview = ref({ rating: 5, comment: '' });

const propertyRooms = ref([]);
const roomsLoading = ref(false);
const selectedCheckIn = ref('');
const selectedCheckOut = ref('');

const todayDate = new Date().toISOString().split('T')[0];

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

const shareApartment = async () => {
  try {
    await navigator.clipboard.writeText(window.location.href);
    copied.value = true;
    setTimeout(() => copied.value = false, 2500);
  } catch {
    // fallback
  }
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
      image_urls: []
    });
    showReviewDialog.value = false;
    newReview.value = { rating: 5, comment: '' };
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

function getAmenityIcon(amenity) {
  const name = (amenity || '').toLowerCase();
  if (name.includes('wifi') || name.includes('internet')) return 'pi pi-wifi';
  if (name.includes('air') || name.includes('ac') || name.includes('conditioning')) return 'pi pi-sun';
  if (name.includes('park') || name.includes('car') || name.includes('garage')) return 'pi pi-car';
  if (name.includes('pool') || name.includes('swim')) return 'pi pi-wave-pulse';
  if (name.includes('generator') || name.includes('power') || name.includes('backup') || name.includes('electric')) return 'pi pi-bolt';
  if (name.includes('security') || name.includes('cctv') || name.includes('guard') || name.includes('gated')) return 'pi pi-shield';
  if (name.includes('kitchen') || name.includes('cook')) return 'pi pi-home';
  if (name.includes('laundry') || name.includes('wash')) return 'pi pi-refresh';
  if (name.includes('restaurant') || name.includes('dining') || name.includes('food') || name.includes('bar')) return 'pi pi-star';
  if (name.includes('gym') || name.includes('fitness')) return 'pi pi-heart';
  if (name.includes('tv') || name.includes('dstv') || name.includes('television')) return 'pi pi-desktop';
  if (name.includes('hot water') || name.includes('water')) return 'pi pi-droplet';
  if (name.includes('game') || name.includes('safari') || name.includes('drive')) return 'pi pi-map';
  if (name.includes('airport') || name.includes('transfer') || name.includes('shuttle')) return 'pi pi-send';
  if (name.includes('breakfast') || name.includes('meal') || name.includes('board')) return 'pi pi-clock';
  if (name.includes('ensuite') || name.includes('bathroom') || name.includes('bath')) return 'pi pi-home';
  if (name.includes('balcony') || name.includes('veranda') || name.includes('patio') || name.includes('view')) return 'pi pi-external-link';
  if (name.includes('wheelchair') || name.includes('accessible')) return 'pi pi-user';
  if (name.includes('pet') || name.includes('dog') || name.includes('cat')) return 'pi pi-heart-fill';
  if (name.includes('conference') || name.includes('meeting') || name.includes('boardroom')) return 'pi pi-users';
  if (name.includes('spa') || name.includes('massage')) return 'pi pi-sparkles';
  return 'pi pi-check-circle';
}
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

