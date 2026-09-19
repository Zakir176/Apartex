<template>
  <Teleport to="body">
    <Transition name="modal-fade">
      <div
        v-if="show"
        class="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-6 overflow-y-auto"
        @click.self="handleClose"
      >
        <!-- Backdrop with glass blur -->
        <div class="fixed inset-0 bg-slate-955/70 backdrop-blur-md transition-opacity"></div>

        <!-- Main Modal Container -->
        <div class="relative w-full max-w-2xl bg-white rounded-t-3xl sm:rounded-3xl shadow-2xl border border-slate-100 flex flex-col max-h-[92vh] overflow-hidden animate-scale-up z-10">

          <!-- ──────────────── Header ──────────────── -->
          <div class="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 px-6 py-5 border-b border-slate-700/50 flex items-center justify-between shrink-0 text-white relative">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-2xl bg-accent/20 border border-accent/40 flex items-center justify-center text-accent shadow-inner">
                <i class="pi pi-desktop text-lg"></i>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h2 class="text-lg font-black text-white tracking-tight">Front Office POS Desk</h2>
                  <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 text-[10px] font-black uppercase tracking-wider border border-emerald-500/30 flex items-center gap-1">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
                    Live Terminal
                  </span>
                </div>
                <p class="text-xs text-slate-400 font-medium mt-0.5">Record instant walk-in guest arrivals & issue digital receipt</p>
              </div>
            </div>

            <button
              @click="handleClose"
              class="w-9 h-9 rounded-full bg-slate-800/80 border border-slate-700 text-slate-400 hover:text-white hover:bg-slate-700 flex items-center justify-center transition-all cursor-pointer"
            >
              <i class="pi pi-times text-sm"></i>
            </button>
          </div>

          <!-- ──────────────── SUCCESS STATE / RECEIPT CARD ──────────────── -->
          <div v-if="successBooking" class="flex-1 overflow-y-auto p-6 flex flex-col items-center justify-center text-center animate-fade-in">
            <div class="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-3xl mb-4 border border-emerald-200 shadow-md animate-bounce-short">
              <i class="pi pi-check-circle"></i>
            </div>
            
            <span class="text-xs font-black text-emerald-600 uppercase tracking-widest bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 mb-2">
              Walk-in Registered
            </span>
            <h3 class="text-2xl font-black text-slate-900 tracking-tight">Reservation Confirmed</h3>
            <p class="text-xs text-slate-500 font-medium max-w-sm mt-1 mb-6">
              Guest record has been added to your host ledger and room inventory updated.
            </p>

            <!-- Digital Receipt Card -->
            <div class="w-full max-w-md bg-gradient-to-b from-slate-50 to-white rounded-2xl p-5 border border-surface-border shadow-sm text-left relative overflow-hidden mb-6">
              <div class="absolute top-0 right-0 w-24 h-24 bg-accent/5 rounded-full blur-2xl pointer-events-none"></div>
              
              <div class="flex items-center justify-between border-b border-slate-200 pb-3 mb-3">
                <div>
                  <span class="text-[10px] font-black uppercase text-slate-400 tracking-wider">Booking Ref</span>
                  <p class="text-sm font-black text-slate-800">#WALK-{{ successBooking.id || Math.floor(1000 + Math.random() * 9000) }}</p>
                </div>
                <div class="text-right">
                  <span class="text-[10px] font-black uppercase text-slate-400 tracking-wider">Payment Status</span>
                  <span class="block px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold capitalize">
                    Paid via {{ (successBooking.payment_method || 'Cash').replace('_', ' ') }}
                  </span>
                </div>
              </div>

              <div class="space-y-2 text-xs">
                <div class="flex justify-between">
                  <span class="text-slate-500 font-semibold">Guest Name:</span>
                  <span class="font-bold text-slate-900">{{ successBooking.walk_in_guest_name || form.walk_in_guest_name }}</span>
                </div>
                <div v-if="successBooking.walk_in_guest_phone || form.walk_in_guest_phone" class="flex justify-between">
                  <span class="text-slate-500 font-semibold">Contact:</span>
                  <span class="font-bold text-slate-800">{{ successBooking.walk_in_guest_phone || form.walk_in_guest_phone }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-500 font-semibold">Property:</span>
                  <span class="font-bold text-slate-800">{{ selectedPropertyName }}</span>
                </div>
                <div v-if="selectedRoomName" class="flex justify-between">
                  <span class="text-slate-500 font-semibold">Room Type:</span>
                  <span class="font-bold text-accent">{{ selectedRoomName }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-500 font-semibold">Dates:</span>
                  <span class="font-bold text-slate-800">{{ form.check_in }} → {{ form.check_out }} ({{ nightsCount }} nights)</span>
                </div>
                <div class="border-t border-slate-200 pt-2.5 mt-2 flex justify-between items-center text-sm font-black">
                  <span class="text-slate-800">Total Collected:</span>
                  <span class="text-accent text-base">${{ (successBooking.total_price || estimatedPrice).toFixed(2) }}</span>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-3 w-full max-w-md">
              <button
                @click="downloadReceiptPDF"
                class="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-accent text-white text-xs font-semibold hover:bg-accent-hover transition-colors duration-150 cursor-pointer border-0"
              >
                <i class="pi pi-download text-sm"></i>
                <span>Download Receipt (PDF)</span>
              </button>
              <button
                @click="resetFormState"
                class="px-4 py-3 rounded-xl border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-bold transition-colors cursor-pointer"
              >
                New Booking
              </button>
              <button
                @click="handleClose"
                class="px-4 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors cursor-pointer"
              >
                Done
              </button>
            </div>
          </div>

          <!-- ──────────────── FORM BODY ──────────────── -->
          <div v-else class="flex-1 overflow-y-auto px-6 py-6 space-y-6">

            <!-- Section 1: Guest Information -->
            <div class="bg-slate-50/80 rounded-2xl p-4 border border-slate-200/80 space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center gap-2">
                  <div class="w-6 h-6 rounded-lg bg-accent/10 text-accent flex items-center justify-center text-xs">1</div>
                  Guest Information
                </span>
                <span class="text-[10px] font-bold text-slate-400">Step 1 of 4</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-extrabold text-slate-700 mb-1">
                    Guest Full Name <span class="text-red-500">*</span>
                  </label>
                  <div class="relative">
                    <i class="pi pi-user absolute left-3.5 top-3 text-slate-400 text-xs"></i>
                    <input
                      v-model="form.walk_in_guest_name"
                      type="text"
                      placeholder="e.g. Mwansa Zulu"
                      class="w-full pl-9 pr-3 py-2.5 rounded-xl border bg-white text-xs font-bold text-slate-800 placeholder:slate-400 focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all"
                      :class="errors.walk_in_guest_name ? 'border-red-400 bg-red-50/30' : 'border-slate-200'"
                    />
                  </div>
                  <p v-if="errors.walk_in_guest_name" class="text-red-500 text-[11px] mt-1 font-medium">{{ errors.walk_in_guest_name }}</p>
                </div>

                <div>
                  <label class="block text-xs font-extrabold text-slate-700 mb-1">
                    Guest Phone Number <span class="text-gray-400 font-normal">(optional)</span>
                  </label>
                  <div class="relative">
                    <i class="pi pi-phone absolute left-3.5 top-3 text-slate-400 text-xs"></i>
                    <input
                      v-model="form.walk_in_guest_phone"
                      type="tel"
                      placeholder="+260 97 000 0000"
                      class="w-full pl-9 pr-3 py-2.5 rounded-xl border border-slate-200 bg-white text-xs font-bold text-slate-800 placeholder:slate-400 focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Section 2: Property & Room Selection -->
            <div class="bg-slate-50/80 rounded-2xl p-4 border border-slate-200/80 space-y-4">
              <div class="flex items-center justify-between">
                <span class="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center gap-2">
                  <div class="w-6 h-6 rounded-lg bg-accent/10 text-accent flex items-center justify-center text-xs">2</div>
                  Property & Room Selection
                </span>
                <span class="text-[10px] font-bold text-slate-400">Step 2 of 4</span>
              </div>

              <!-- Property Selector -->
              <div>
                <label class="block text-xs font-extrabold text-slate-700 mb-1.5">
                  Select Property <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="form.property_id"
                  @change="onPropertyChange"
                  class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-white text-xs font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-all cursor-pointer"
                  :class="errors.property_id ? 'border-red-400 bg-red-50/30' : ''"
                >
                  <option value="">-- Choose a property --</option>
                  <option v-for="p in ownerProperties" :key="p.id" :value="p.id">
                    {{ p.title }} ({{ formatPropertyType(p.property_type) }}) — ${{ p.price_per_night }}/night
                  </option>
                </select>
                <p v-if="errors.property_id" class="text-red-500 text-[11px] mt-1 font-medium">{{ errors.property_id }}</p>
              </div>

              <!-- Room Selection Cards (if property has room types) -->
              <div v-if="loadingRooms" class="flex items-center justify-center py-4 text-xs font-bold text-slate-400 gap-2">
                <i class="pi pi-spin pi-spinner text-accent"></i> Loading room types...
              </div>
              
              <div v-else-if="propertyRooms.length > 0" class="space-y-2">
                <label class="block text-xs font-extrabold text-slate-700">
                  Select Room Type <span class="text-red-500">*</span>
                </label>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  <div
                    v-for="room in propertyRooms"
                    :key="room.id"
                    @click="form.room_id = room.id"
                    class="p-3.5 rounded-xl border-2 transition-all cursor-pointer flex flex-col justify-between group relative overflow-hidden"
                    :class="form.room_id === room.id
                      ? 'border-accent bg-accent/5 shadow-sm'
                      : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/50'"
                  >
                    <div class="flex items-start justify-between">
                      <div>
                        <h4 class="text-xs font-black text-slate-800 group-hover:text-accent transition-colors">{{ room.room_type }}</h4>
                        <p class="text-[11px] font-bold text-slate-500 mt-0.5">${{ room.price_per_night }} <span class="font-normal opacity-70">/ night</span></p>
                      </div>
                      <div class="w-5 h-5 rounded-full border flex items-center justify-center shrink-0 transition-colors"
                        :class="form.room_id === room.id ? 'border-accent bg-accent text-white' : 'border-slate-300 bg-white'">
                        <i v-if="form.room_id === room.id" class="pi pi-check text-[10px] font-bold"></i>
                      </div>
                    </div>

                    <div class="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] font-bold text-slate-500">
                      <span><i class="pi pi-users text-[9px] mr-1 text-slate-400"></i>Up to {{ room.capacity }} guests</span>
                      <span class="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 font-extrabold">{{ room.total_units }} units</span>
                    </div>
                  </div>
                </div>
                <p v-if="errors.room_id" class="text-red-500 text-[11px] mt-1 font-medium">{{ errors.room_id }}</p>
              </div>
            </div>

            <!-- Section 3: Stay Dates & Capacity -->
            <div class="bg-slate-50/80 rounded-2xl p-4 border border-slate-200/80 space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center gap-2">
                  <div class="w-6 h-6 rounded-lg bg-accent/10 text-accent flex items-center justify-center text-xs">3</div>
                  Stay Dates & Guests
                </span>
                <span class="text-[10px] font-bold text-slate-400">Step 3 of 4</span>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-extrabold text-slate-700 mb-1">
                    Check-in Date <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.check_in"
                    type="date"
                    :min="today"
                    class="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-xs font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent"
                    :class="errors.dates ? 'border-red-400 bg-red-50/30' : ''"
                  />
                </div>

                <div>
                  <label class="block text-xs font-extrabold text-slate-700 mb-1">
                    Check-out Date <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="form.check_out"
                    type="date"
                    :min="form.check_in || today"
                    class="w-full px-3 py-2 rounded-xl border border-slate-200 bg-white text-xs font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent"
                    :class="errors.dates ? 'border-red-400 bg-red-50/30' : ''"
                  />
                </div>
              </div>
              <!-- Availability panel -->
              <div v-if="form.property_id" class="mt-2">
                <div v-if="availabilityLoading" class="flex items-center gap-2 text-xs text-gray-400 py-2">
                  <i class="pi pi-spin pi-spinner text-xs"></i> Checking availability...
                </div>
                <div v-else-if="bookedRanges.length === 0" class="flex items-center gap-2 text-xs font-medium text-accent bg-accent-light border border-accent/20 px-3 py-2 rounded-lg">
                  <i class="pi pi-check-circle"></i> All dates available
                </div>
                <div v-else class="flex flex-col gap-1.5">
                  <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Booked Periods</p>
                  <div class="flex flex-col gap-1 max-h-28 overflow-y-auto">
                    <div
                      v-for="(range, i) in bookedRanges"
                      :key="i"
                      class="flex items-center gap-2 text-xs px-3 py-2 rounded-lg border transition-colors duration-150"
                      :class="form.check_in && form.check_out && new Date(form.check_in) < new Date(range.check_out) && new Date(form.check_out) > new Date(range.check_in)
                        ? 'bg-red-50 border-red-200 text-red-600'
                        : 'bg-gray-50 border-surface-border text-gray-500'"
                    >
                      <i class="pi pi-calendar text-xs shrink-0"
                        :class="form.check_in && form.check_out && new Date(form.check_in) < new Date(range.check_out) && new Date(form.check_out) > new Date(range.check_in) ? 'text-red-400' : 'text-gray-300'">
                      </i>
                      <span class="font-medium">
                        {{ new Date(range.check_in).toLocaleDateString('en-US', { day: 'numeric', month: 'short' }) }}
                        →
                        {{ new Date(range.check_out).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' }) }}
                      </span>
                      <span v-if="form.check_in && form.check_out && new Date(form.check_in) < new Date(range.check_out) && new Date(form.check_out) > new Date(range.check_in)" class="ml-auto font-semibold text-red-500 text-[10px] uppercase">Conflict</span>
                    </div>
                  </div>
                  <div v-if="selectedDatesConflict" class="flex items-center gap-2 text-xs font-semibold text-red-600 bg-red-50 border border-red-200 px-3 py-2.5 rounded-lg">
                    <i class="pi pi-exclamation-triangle"></i>
                    Selected dates overlap with an existing booking. Please choose different dates.
                  </div>
                </div>
              </div>

              <!-- Guest Count Stepper -->
              <div class="flex items-center justify-between pt-1">
                <div>
                  <span class="text-xs font-extrabold text-slate-700">Number of Occupants</span>
                  <p class="text-[11px] text-slate-400 font-medium">Guest count for this stay</p>
                </div>
                <div class="flex items-center border border-slate-200 bg-white rounded-xl overflow-hidden shadow-xs">
                  <button
                    type="button"
                    @click="form.guests = Math.max(1, form.guests - 1)"
                    class="w-8 h-8 flex items-center justify-center text-slate-600 hover:bg-slate-100 font-bold transition-colors cursor-pointer"
                  >
                    -
                  </button>
                  <span class="px-3 text-xs font-black text-slate-800">{{ form.guests }}</span>
                  <button
                    type="button"
                    @click="form.guests = Math.min(10, form.guests + 1)"
                    class="w-8 h-8 flex items-center justify-center text-slate-600 hover:bg-slate-100 font-bold transition-colors cursor-pointer"
                  >
                    +
                  </button>
                </div>
              </div>
            </div>

            <!-- Section 4: POS Payment Method -->
            <div class="bg-slate-50/80 rounded-2xl p-4 border border-slate-200/80 space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-xs font-black uppercase tracking-wider text-slate-700 flex items-center gap-2">
                  <div class="w-6 h-6 rounded-lg bg-accent/10 text-accent flex items-center justify-center text-xs">4</div>
                  Payment Channel
                </span>
                <span class="text-[10px] font-bold text-slate-400">Step 4 of 4</span>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button
                  v-for="method in paymentMethods"
                  :key="method.value"
                  type="button"
                  @click="form.payment_method = method.value"
                  class="p-3 rounded-xl border-2 flex flex-col items-center justify-center text-center gap-1.5 transition-all cursor-pointer"
                  :class="form.payment_method === method.value
                    ? 'border-accent bg-accent/10 text-accent font-black shadow-xs scale-[1.02]'
                    : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300 font-bold'"
                >
                  <i :class="method.icon" class="text-lg"></i>
                  <span class="text-[11px] leading-tight">{{ method.label }}</span>
                </button>
              </div>
              <p v-if="errors.payment_method" class="text-red-500 text-[11px] font-medium">{{ errors.payment_method }}</p>
            </div>

            <!-- Live Ledger Calculation Bar -->
            <div v-if="nightsCount > 0 && estimatedPrice > 0" class="bg-gradient-to-r from-slate-900 to-slate-800 text-white rounded-2xl p-4 shadow-lg border border-slate-700/60 flex items-center justify-between">
              <div>
                <span class="text-[10px] font-black uppercase tracking-widest text-accent">Real-Time Ledger</span>
                <div class="flex items-center gap-2 text-xs font-bold text-slate-300 mt-0.5">
                  <span>{{ nightsCount }} Night{{ nightsCount > 1 ? 's' : '' }}</span>
                  <span>•</span>
                  <span>${{ currentNightlyRate }}/night</span>
                </div>
              </div>
              <div class="text-right">
                <span class="text-[10px] font-black uppercase tracking-wider text-slate-400">Total Due</span>
                <p class="text-xl font-black text-accent tracking-tight">${{ estimatedPrice.toFixed(2) }}</p>
              </div>
            </div>

            <!-- Error Banner -->
            <div v-if="submitError" class="bg-red-50 border border-red-200 text-red-700 rounded-xl p-3.5 text-xs font-bold flex items-center gap-2">
              <i class="pi pi-exclamation-circle text-base text-red-500 shrink-0"></i>
              <span>{{ submitError }}</span>
            </div>

          </div>

          <!-- ──────────────── FOOTER ──────────────── -->
          <div v-if="!successBooking" class="bg-slate-50 px-6 py-4 border-t border-slate-200 flex items-center justify-between shrink-0">
            <button
              @click="handleClose"
              type="button"
              class="px-5 py-2.5 rounded-xl border border-slate-300 text-slate-600 font-bold text-xs hover:bg-slate-100 transition-colors cursor-pointer"
              :disabled="submitting"
            >
              Cancel
            </button>

            <button
              @click="handleSubmit"
              type="button"
              class="btn-accent shadow-accent px-6 py-2.5 rounded-xl font-black text-xs flex items-center gap-2 cursor-pointer transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="submitting || selectedDatesConflict"
            >
              <i v-if="submitting" class="pi pi-spin pi-spinner text-xs"></i>
              <i v-else class="pi pi-check text-xs"></i>
              <span>{{ submitting ? 'Processing Entry...' : 'Confirm Walk-In Booking' }}</span>
            </button>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useBookingsStore } from '@/stores/bookings';
import apiClient from '@/api/index';

const props = defineProps({
  show: { type: Boolean, default: false },
  ownerProperties: { type: Array, default: () => [] },
});

const emit = defineEmits(['close', 'booked']);

const bookingsStore = useBookingsStore();
const today = new Date().toISOString().split('T')[0];

const form = ref({
  walk_in_guest_name: '',
  walk_in_guest_phone: '',
  property_id: '',
  room_id: '',
  check_in: today,
  check_out: '',
  guests: 2,
  payment_method: 'cash',
});

const propertyRooms = ref([]);
const loadingRooms = ref(false);
const bookedRanges = ref([]);
const availabilityLoading = ref(false);

async function fetchBookedDates(propertyId) {
  if (!propertyId) {
    bookedRanges.value = [];
    return;
  }
  availabilityLoading.value = true;
  try {
    const res = await apiClient.get(`/bookings/property/${propertyId}/booked-dates`);
    bookedRanges.value = res.data;
  } catch {
    bookedRanges.value = [];
  } finally {
    availabilityLoading.value = false;
  }
}

const errors = ref({});
const submitError = ref('');
const submitting = ref(false);
const successBooking = ref(null);
const lastBooking = successBooking;

const paymentMethods = [
  { value: 'cash', label: 'Cash (Physical)', icon: 'pi pi-money-bill' },
  { value: 'mobile_money', label: 'Mobile Money', icon: 'pi pi-mobile' },
  { value: 'card', label: 'POS Terminal', icon: 'pi pi-credit-card' },
  { value: 'bank_transfer', label: 'Bank Transfer', icon: 'pi pi-building-columns' },
];

const selectedProperty = computed(() => {
  return props.ownerProperties.find(p => p.id === form.value.property_id);
});

const selectedPropertyName = computed(() => selectedProperty.value?.title || 'Selected Property');

const selectedRoom = computed(() => {
  return propertyRooms.value.find(r => r.id === form.value.room_id);
});

const selectedRoomName = computed(() => selectedRoom.value?.room_type || '');

const currentNightlyRate = computed(() => {
  if (selectedRoom.value) return parseFloat(selectedRoom.value.price_per_night);
  if (selectedProperty.value) return parseFloat(selectedProperty.value.price_per_night);
  return 0;
});

const nightsCount = computed(() => {
  if (!form.value.check_in || !form.value.check_out) return 0;
  const diff = new Date(form.value.check_out) - new Date(form.value.check_in);
  return Math.max(0, Math.floor(diff / (1000 * 60 * 60 * 24)));
});

const estimatedPrice = computed(() => {
  return nightsCount.value * currentNightlyRate.value;
});

const selectedDatesConflict = computed(() => {
  if (!form.value.check_in || !form.value.check_out) return false;
  const checkIn = new Date(form.value.check_in);
  const checkOut = new Date(form.value.check_out);
  return bookedRanges.value.some(range => {
    const bookedIn = new Date(range.check_in);
    const bookedOut = new Date(range.check_out);
    return checkIn < bookedOut && checkOut > bookedIn;
  });
});

async function downloadReceiptPDF() {
  if (!lastBooking.value) return;

  const booking = lastBooking.value;
  const guestName = booking.walk_in_guest_name || 'Walk-in Guest';
  const property = props.ownerProperties?.find?.(p => p.id === booking.property_id);
  const propertyName = property?.title || `Property #${booking.property_id}`;
  const propertyCity = property?.city || 'Zambia';
  const checkIn = new Date(booking.check_in);
  const checkOut = new Date(booking.check_out);
  const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
  const checkInStr = checkIn.toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'long', year: 'numeric' });
  const checkOutStr = checkOut.toLocaleDateString('en-US', { weekday: 'short', day: 'numeric', month: 'long', year: 'numeric' });
  const paymentLabel = { cash: 'Cash', mobile_money: 'Mobile Money', card: 'Card', bank_transfer: 'Bank Transfer' }[booking.payment_method] || booking.payment_method;
  const ref = `APX-${booking.id?.toString().padStart(6, '0') || '000001'}`;
  const verifyUrl = `https://apartex.vercel.app/bookings/verify/${booking.id || '1'}`;
  const issueDate = new Date().toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' });

  let qrDataUrl = '';
  try {
    const QRCode = (await import('qrcode')).default;
    qrDataUrl = await QRCode.toDataURL(verifyUrl, {
      width: 120, margin: 1,
      color: { dark: '#0A6640', light: '#FFFFFF' }
    });
  } catch {}

  const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Receipt ${ref}</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;background:#f9fafb}
  .page{max-width:580px;margin:32px auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08)}
  .hdr{background:#0A6640;padding:32px 36px;position:relative;overflow:hidden}
  .hdr::before{content:'';position:absolute;top:-40px;right:-40px;width:180px;height:180px;background:rgba(255,255,255,0.06);border-radius:50%}
  .brand{color:rgba(255,255,255,0.65);font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px}
  .hdr-title{color:#fff;font-size:26px;font-weight:700;margin-bottom:4px}
  .hdr-sub{color:rgba(255,255,255,0.6);font-size:13px}
  .pill{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.15);border:1px solid rgba(255,255,255,0.25);color:#fff;font-size:11px;font-weight:600;padding:4px 12px;border-radius:20px;margin-top:16px}
  .dot{width:6px;height:6px;background:#86efac;border-radius:50%}
  .body{padding:32px 36px}
  .ref-banner{display:flex;align-items:center;justify-content:space-between;background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:14px 18px;margin-bottom:28px}
  .ref-lbl{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#6b7280;margin-bottom:2px}
  .ref-num{font-size:18px;font-weight:700;color:#0A6640;letter-spacing:.05em}
  .ref-dt{font-size:11px;color:#9ca3af;text-align:right}
  .sec-lbl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#9ca3af;padding-bottom:8px;border-bottom:1px solid #f3f4f6;margin-bottom:12px;margin-top:20px}
  .row{display:flex;justify-content:space-between;align-items:baseline;padding:5px 0}
  .rk{font-size:13px;color:#6b7280}
  .rv{font-size:13px;font-weight:500;color:#111827;text-align:right}
  .stay-card{background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:18px;margin:16px 0;display:flex;gap:16px;align-items:center}
  .sd{flex:1}
  .sdl{font-size:10px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#9ca3af;margin-bottom:4px}
  .sdv{font-size:14px;font-weight:600;color:#111827}
  .sdiv{width:1px;background:#e5e7eb;align-self:stretch}
  .nbadge{background:#0A6640;color:#fff;font-size:12px;font-weight:700;padding:6px 14px;border-radius:20px;white-space:nowrap}
  .total{background:#111827;border-radius:12px;padding:20px 24px;display:flex;align-items:center;justify-content:space-between;margin:24px 0}
  .tl{color:rgba(255,255,255,0.6);font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.08em}
  .ts{color:rgba(255,255,255,0.5);font-size:11px;margin-top:3px}
  .ta{color:#fff;font-size:28px;font-weight:700}
  .qr-sec{display:flex;align-items:center;gap:20px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:18px;margin-bottom:28px}
  .qr-img{width:90px;height:90px;border-radius:8px;flex-shrink:0}
  .qr-h{font-size:13px;font-weight:600;color:#111827;margin-bottom:4px}
  .qr-p{font-size:11px;color:#6b7280;line-height:1.5}
  .qr-url{font-size:10px;color:#0A6640;margin-top:6px;word-break:break-all}
  .footer{text-align:center;padding-top:20px;border-top:1px solid #f3f4f6}
  .footer p{font-size:11px;color:#9ca3af;line-height:1.8}
  .footer strong{color:#0A6640}
  .badge{display:inline-block;background:#ecfdf5;color:#0A6640;font-size:10px;font-weight:600;padding:2px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.04em}
  @media print{body{background:#fff}.page{box-shadow:none;border-radius:0;margin:0;max-width:100%}@page{margin:.5in}}
</style>
</head>
<body>
<div class="page">
  <div class="hdr">
    <div class="brand">Apartex · Official Receipt</div>
    <div class="hdr-title">Booking Confirmed</div>
    <div class="hdr-sub">${propertyName} · ${propertyCity}</div>
    <div class="pill"><span class="dot"></span>Walk-in · ${paymentLabel}</div>
  </div>
  <div class="body">
    <div class="ref-banner">
      <div>
        <div class="ref-lbl">Booking Reference</div>
        <div class="ref-num">${ref}</div>
      </div>
      <div class="ref-dt">Issued<br>${issueDate}</div>
    </div>

    <div class="sec-lbl">Guest</div>
    <div class="row"><span class="rk">Name</span><span class="rv">${guestName}</span></div>
    ${booking.walk_in_guest_phone ? `<div class="row"><span class="rk">Phone</span><span class="rv">${booking.walk_in_guest_phone}</span></div>` : ''}
    <div class="row"><span class="rk">Guests</span><span class="rv">${booking.guests} person${booking.guests !== 1 ? 's' : ''}</span></div>

    <div class="sec-lbl">Stay</div>
    <div class="stay-card">
      <div class="sd"><div class="sdl">Check-in</div><div class="sdv">${checkInStr}</div></div>
      <div class="sdiv"></div>
      <div class="sd"><div class="sdl">Check-out</div><div class="sdv">${checkOutStr}</div></div>
      <div class="nbadge">${nights}N</div>
    </div>

    <div class="sec-lbl">Payment</div>
    <div class="row"><span class="rk">Method</span><span class="rv">${paymentLabel}</span></div>
    <div class="row"><span class="rk">Status</span><span class="rv"><span class="badge">Paid</span></span></div>

    <div class="total">
      <div>
        <div class="tl">Total Amount</div>
        <div class="ts">${nights} nights · ${paymentLabel}</div>
      </div>
      <div class="ta">$${parseFloat(booking.total_price || 0).toFixed(2)}</div>
    </div>

    ${qrDataUrl ? `
    <div class="qr-sec">
      <img src="${qrDataUrl}" class="qr-img" alt="QR" />
      <div>
        <div class="qr-h">Scan to Verify Booking</div>
        <div class="qr-p">Show at check-in or scan to view booking details instantly. No app required.</div>
        <div class="qr-url">${verifyUrl}</div>
      </div>
    </div>` : ''}

    <div class="footer">
      <p><strong>apartex.vercel.app</strong><br>
      Official Apartex booking receipt. Retain for your records.<br>
      Reference: ${ref}</p>
    </div>
  </div>
</div>
</body>
</html>`;

  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const win = window.open(url, '_blank');
  if (win) {
    win.onload = () => { setTimeout(() => { win.print(); URL.revokeObjectURL(url); }, 500); };
  }
}

function formatPropertyType(type) {
  if (!type) return 'Apartment';
  return type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
}

async function onPropertyChange() {
  form.value.room_id = '';
  propertyRooms.value = [];
  if (!form.value.property_id) {
    bookedRanges.value = [];
    return;
  }

  loadingRooms.value = true;
  try {
    const res = await apiClient.get(`/rooms/my/property/${form.value.property_id}`);
    propertyRooms.value = res.data;
  } catch {
    propertyRooms.value = [];
  } finally {
    loadingRooms.value = false;
  }

  await fetchBookedDates(form.value.property_id);
}

function validate() {
  errors.value = {};
  if (!form.value.walk_in_guest_name.trim()) {
    errors.value.walk_in_guest_name = 'Guest name is required';
  }
  if (!form.value.property_id) {
    errors.value.property_id = 'Please select a property';
  }
  if (propertyRooms.value.length > 0 && !form.value.room_id) {
    errors.value.room_id = 'Please select a room type for this property';
  }
  if (!form.value.check_in || !form.value.check_out) {
    errors.value.dates = 'Check-in and Check-out dates are required';
  } else if (form.value.check_in >= form.value.check_out) {
    errors.value.dates = 'Check-out date must be after Check-in';
  }
  if (!form.value.payment_method) {
    errors.value.payment_method = 'Select a payment method';
  }
  return Object.keys(errors.value).length === 0;
}

async function handleSubmit() {
  submitError.value = '';
  if (!validate()) return;

  if (selectedDatesConflict.value) {
    submitError.value = 'These dates are already booked. Please select different dates.';
    return;
  }

  submitting.value = true;
  try {
    const payload = {
      property_id: form.value.property_id,
      room_id: form.value.room_id || null,
      check_in: form.value.check_in,
      check_out: form.value.check_out,
      guests: form.value.guests,
      walk_in_guest_name: form.value.walk_in_guest_name.trim(),
      walk_in_guest_phone: form.value.walk_in_guest_phone || null,
      payment_method: form.value.payment_method,
      is_walk_in: true,
      created_by_owner: true,
    };
    const result = await bookingsStore.createWalkInBooking(payload);
    successBooking.value = result || payload;
    emit('booked', result);
  } catch (err) {
    submitError.value = err.response?.data?.detail || bookingsStore.error || 'Failed to record booking. Please verify input.';
  } finally {
    submitting.value = false;
  }
}

function handleClose() {
  resetFormState();
  emit('close');
}

function resetFormState() {
  bookedRanges.value = [];
  form.value = {
    walk_in_guest_name: '',
    walk_in_guest_phone: '',
    property_id: '',
    room_id: '',
    check_in: today,
    check_out: '',
    guests: 2,
    payment_method: 'cash',
  };
  propertyRooms.value = [];
  errors.value = {};
  submitError.value = '';
  successBooking.value = null;
}

watch(() => props.show, (val) => {
  if (!val) resetFormState();
});
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

@keyframes scaleUp {
  from {
    opacity: 0;
    transform: scale(0.96) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.animate-scale-up {
  animation: scaleUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes bounceShort {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.animate-bounce-short {
  animation: bounceShort 0.6s ease-in-out 2;
}
</style>
