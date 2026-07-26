<template>
  <!-- Backdrop -->
  <Teleport to="body">
    <div
      v-if="show"
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
      @click.self="$emit('close')"
    >
      <!-- Dark backdrop -->
      <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm"></div>

      <!-- Modal -->
      <div class="relative w-full max-w-lg bg-white rounded-2xl shadow-2xl flex flex-col max-h-[90vh] overflow-hidden">

        <!-- Header -->
        <div class="flex items-center justify-between px-6 py-5 border-b border-surface-border shrink-0">
          <div>
            <h2 class="text-lg font-black text-slate-800">Walk-in Booking</h2>
            <p class="text-xs text-slate-400 font-medium mt-0.5">Record a guest arriving in person or by phone</p>
          </div>
          <button
            @click="$emit('close')"
            class="w-9 h-9 rounded-full flex items-center justify-center text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors duration-150"
          >
            <i class="pi pi-times text-sm"></i>
          </button>
        </div>

        <!-- Form -->
        <div class="flex-1 overflow-y-auto px-6 py-5 flex flex-col gap-5">

          <!-- Guest Info -->
          <div>
            <p class="text-xs font-black uppercase tracking-widest text-accent mb-3">Guest Information</p>
            <div class="flex flex-col gap-3">
              <div>
                <label class="label-base">Guest Name <span class="text-red-500">*</span></label>
                <input
                  v-model="form.walk_in_guest_name"
                  type="text"
                  placeholder="e.g. John Banda"
                  class="input-base"
                  :class="errors.walk_in_guest_name ? 'border-red-400 focus:border-red-400 focus:ring-red-100' : ''"
                />
                <p v-if="errors.walk_in_guest_name" class="text-red-500 text-xs mt-1 font-medium">{{ errors.walk_in_guest_name }}</p>
              </div>
              <div>
                <label class="label-base">Guest Phone <span class="text-slate-400 font-normal">(optional)</span></label>
                <input
                  v-model="form.walk_in_guest_phone"
                  type="tel"
                  placeholder="+260 97 123 4567"
                  class="input-base"
                />
              </div>
            </div>
          </div>

          <!-- Property & Room -->
          <div>
            <p class="text-xs font-black uppercase tracking-widest text-accent mb-3">Property & Room</p>
            <div class="flex flex-col gap-3">
              <div>
                <label class="label-base">Property <span class="text-red-500">*</span></label>
                <select
                  v-model="form.property_id"
                  class="input-base"
                  @change="onPropertyChange"
                >
                  <option value="">Select a property</option>
                  <option v-for="p in ownerProperties" :key="p.id" :value="p.id">
                    {{ p.title }}
                  </option>
                </select>
              </div>

              <!-- Room type — only shown if property has rooms -->
              <div v-if="propertyRooms.length > 0">
                <label class="label-base">Room Type <span class="text-red-500">*</span></label>
                <select v-model="form.room_id" class="input-base">
                  <option value="">Select a room type</option>
                  <option v-for="room in propertyRooms" :key="room.id" :value="room.id">
                    {{ room.room_type }} — ${{ room.price_per_night }}/night ({{ room.total_units }} units)
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Dates & Guests -->
          <div>
            <p class="text-xs font-black uppercase tracking-widest text-accent mb-3">Stay Details</p>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="label-base">Check-in <span class="text-red-500">*</span></label>
                <input
                  v-model="form.check_in"
                  type="date"
                  :min="today"
                  class="input-base"
                  :class="errors.dates ? 'border-red-400' : ''"
                />
              </div>
              <div>
                <label class="label-base">Check-out <span class="text-red-500">*</span></label>
                <input
                  v-model="form.check_out"
                  type="date"
                  :min="form.check_in || today"
                  class="input-base"
                  :class="errors.dates ? 'border-red-400' : ''"
                />
              </div>
            </div>
            <p v-if="errors.dates" class="text-red-500 text-xs mt-1 font-medium">{{ errors.dates }}</p>

            <div class="mt-3">
              <label class="label-base">Number of Guests <span class="text-red-500">*</span></label>
              <select v-model="form.guests" class="input-base">
                <option v-for="n in 10" :key="n" :value="n">{{ n }} Guest{{ n > 1 ? 's' : '' }}</option>
              </select>
            </div>
          </div>

          <!-- Payment -->
          <div>
            <p class="text-xs font-black uppercase tracking-widest text-accent mb-3">Payment</p>
            <div class="grid grid-cols-2 gap-2">
              <button
                v-for="method in paymentMethods"
                :key="method.value"
                type="button"
                class="flex items-center gap-2.5 px-4 py-3 rounded-xl border-2 text-sm font-semibold transition-all duration-150"
                :class="form.payment_method === method.value
                  ? 'border-accent bg-accent-subtle text-accent'
                  : 'border-surface-border text-slate-600 hover:border-slate-300'"
                @click="form.payment_method = method.value"
              >
                <i :class="method.icon" class="text-base shrink-0"></i>
                {{ method.label }}
              </button>
            </div>
            <p v-if="errors.payment_method" class="text-red-500 text-xs mt-1.5 font-medium">{{ errors.payment_method }}</p>
          </div>

          <!-- Price preview -->
          <div v-if="nightsCount > 0 && estimatedPrice > 0" class="bg-[#F8F7F4] rounded-xl p-4 border border-surface-border">
            <div class="flex justify-between text-sm mb-2">
              <span class="text-slate-500">{{ nightsCount }} night{{ nightsCount > 1 ? 's' : '' }}</span>
              <span class="font-bold text-slate-800">${{ estimatedPrice.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-sm font-black border-t border-surface-border pt-2 mt-2">
              <span class="text-slate-800">Total</span>
              <span class="text-accent">${{ estimatedPrice.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Error banner -->
          <div v-if="submitError" class="bg-red-50 border border-red-200 text-red-600 rounded-xl px-4 py-3 text-sm font-medium flex items-center gap-2">
            <i class="pi pi-exclamation-circle shrink-0"></i>
            {{ submitError }}
          </div>

        </div>

        <!-- Footer -->
        <div class="px-6 py-4 border-t border-surface-border shrink-0 flex gap-3 justify-end">
          <button
            @click="$emit('close')"
            class="btn-outline text-sm"
            :disabled="submitting"
          >
            Cancel
          </button>
          <button
            @click="handleSubmit"
            class="btn-accent text-sm flex items-center gap-2"
            :disabled="submitting"
          >
            <i v-if="submitting" class="pi pi-spin pi-spinner text-sm"></i>
            <i v-else class="pi pi-check text-sm"></i>
            {{ submitting ? 'Recording...' : 'Record Booking' }}
          </button>
        </div>

      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useBookingsStore } from '@/stores/bookings';
import { useApartmentsStore } from '@/stores/apartments';
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
  check_in: '',
  check_out: '',
  guests: 2,
  payment_method: '',
});

const propertyRooms = ref([]);
const errors = ref({});
const submitError = ref('');
const submitting = ref(false);

const paymentMethods = [
  { value: 'cash', label: 'Cash', icon: 'pi pi-money-bill' },
  { value: 'mobile_money', label: 'Mobile Money', icon: 'pi pi-mobile' },
  { value: 'card', label: 'Card', icon: 'pi pi-credit-card' },
  { value: 'bank_transfer', label: 'Bank Transfer', icon: 'pi pi-building-columns' },
];

const nightsCount = computed(() => {
  if (!form.value.check_in || !form.value.check_out) return 0;
  const diff = new Date(form.value.check_out) - new Date(form.value.check_in);
  return Math.max(0, Math.floor(diff / (1000 * 60 * 60 * 24)));
});

const estimatedPrice = computed(() => {
  if (nightsCount.value <= 0) return 0;
  if (form.value.room_id) {
    const room = propertyRooms.value.find(r => r.id === form.value.room_id);
    return room ? nightsCount.value * parseFloat(room.price_per_night) : 0;
  }
  const prop = props.ownerProperties.find(p => p.id === form.value.property_id);
  return prop ? nightsCount.value * parseFloat(prop.price_per_night) : 0;
});

async function onPropertyChange() {
  form.value.room_id = '';
  propertyRooms.value = [];
  if (!form.value.property_id) return;
  try {
    const res = await apiClient.get(`/rooms/my/property/${form.value.property_id}`);
    propertyRooms.value = res.data;
  } catch {
    propertyRooms.value = [];
  }
}

function validate() {
  errors.value = {};
  if (!form.value.walk_in_guest_name.trim()) {
    errors.value.walk_in_guest_name = 'Guest name is required';
  }
  if (!form.value.check_in || !form.value.check_out) {
    errors.value.dates = 'Both check-in and check-out dates are required';
  } else if (form.value.check_in >= form.value.check_out) {
    errors.value.dates = 'Check-out must be after check-in';
  }
  if (!form.value.payment_method) {
    errors.value.payment_method = 'Please select a payment method';
  }
  return Object.keys(errors.value).length === 0;
}

async function handleSubmit() {
  submitError.value = '';
  if (!validate()) return;

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
    const booking = await bookingsStore.createWalkInBooking(payload);
    emit('booked', booking);
    resetForm();
    emit('close');
  } catch (err) {
    submitError.value = err.response?.data?.detail || bookingsStore.error || 'Failed to record booking. Please try again.';
  } finally {
    submitting.value = false;
  }
}

function resetForm() {
  form.value = {
    walk_in_guest_name: '',
    walk_in_guest_phone: '',
    property_id: '',
    room_id: '',
    check_in: '',
    check_out: '',
    guests: 2,
    payment_method: '',
  };
  propertyRooms.value = [];
  errors.value = {};
  submitError.value = '';
}

watch(() => props.show, (val) => {
  if (!val) resetForm();
});
</script>
