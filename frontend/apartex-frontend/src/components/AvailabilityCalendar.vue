<template>
  <div class="availability-calendar">
    <div class="cal-header flex items-center justify-between mb-4">
      <div>
        <h3 class="text-xl font-bold text-slate-800 m-0">Manage Availability</h3>
        <p class="text-slate-400 text-sm mt-1">Click dates to toggle blocking. Drag across multiple dates to block a range.</p>
      </div>
      <div class="flex gap-2 items-center">
        <span class="legend-dot" style="background:#3b82f6"></span><span class="text-xs text-slate-400 mr-3">Guest Booking</span>
        <span class="legend-dot" style="background:#f97316"></span><span class="text-xs text-slate-400 mr-3">Maintenance</span>
        <span class="legend-dot" style="background:#64748b"></span><span class="text-xs text-slate-400">Off-market</span>
      </div>
    </div>

    <!-- Reason Picker -->
    <div class="reason-bar flex gap-2 mb-4 p-3 rounded-xl bg-slate-50 border border-slate-100">
      <span class="text-sm font-bold text-slate-400 mr-2 align-self-center">Block as:</span>
      <div
        v-for="r in reasons"
        :key="r.value"
        class="reason-chip px-3 py-2 rounded-2xl cursor-pointer text-sm font-bold transition-all transition-duration-200 border-1"
        :class="selectedReason === r.value ? r.activeClass : 'border-gray-200 text-gray-500 bg-white'"
        @click="selectedReason = r.value"
      >
        <i :class="r.icon" class="mr-1"></i> {{ r.label }}
      </div>
    </div>

    <!-- Calendar Grid -->
    <div v-if="loading" class="flex justify-center py-6">
      <ProgressSpinner style="width:40px; height:40px" strokeWidth="4" />
    </div>

    <div v-else class="month-grid">
      <!-- Month Navigator -->
      <div class="flex items-center justify-between mb-4">
        <Button icon="pi pi-chevron-left" class="p-button-rounded p-button-text p-button-secondary" @click="prevMonth" />
        <span class="text-lg font-bold text-slate-800">{{ currentMonthLabel }}</span>
        <Button icon="pi pi-chevron-right" class="p-button-rounded p-button-text p-button-secondary" @click="nextMonth" />
      </div>

      <!-- Day-of-week headers -->
      <div class="day-header-row">
        <div v-for="d in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']" :key="d" class="day-header">{{ d }}</div>
      </div>

      <!-- Day cells -->
      <div class="days-grid">
        <div
          v-for="(cell, idx) in calendarCells"
          :key="idx"
          class="day-cell"
          :class="getDayClass(cell)"
          @click="cell.date && toggleDay(cell.date)"
          @mousedown="cell.date && startDrag(cell.date)"
          @mouseenter="cell.date && continueDrag(cell.date)"
          @mouseup="endDrag"
        >
          <span v-if="cell.date" class="day-number">{{ cell.date.getDate() }}</span>
          <span v-if="getDayReason(cell.date)" class="day-label">{{ getDayReason(cell.date) }}</span>
        </div>
      </div>
    </div>

    <!-- Action Bar -->
    <div v-if="pendingDates.length > 0" class="action-bar mt-4 p-4 rounded-xl border border-accent bg-accent-subtle flex items-center justify-between">
      <span class="text-sm font-bold text-accent">
        <i class="pi pi-calendar mr-2"></i>
        {{ pendingDates.length }} date{{ pendingDates.length > 1 ? 's' : '' }} selected
      </span>
      <div class="flex gap-2">
        <Button label="Cancel" class="p-button-text p-button-sm font-bold" @click="pendingDates = []" />
        <Button
          :label="`Block as ${selectedReasonLabel}`"
          icon="pi pi-lock"
          class="p-button-sm font-bold"
          :class="selectedReason === 'maintenance' ? 'p-button-warning' : 'p-button-secondary'"
          :loading="saving"
          @click="savePendingDates"
        />
      </div>
    </div>

    <!-- Blocked Dates List -->
    <div v-if="blockedDates.length > 0" class="blocked-list mt-5">
      <h4 class="font-bold text-slate-800 mb-3 flex items-center gap-2">
        <i class="pi pi-list text-accent"></i> All Blocked Dates ({{ blockedDates.length }})
      </h4>
      <DataTable
        :value="groupedBlocked"
        :rows="5"
        paginator
        class="p-datatable-sm"
        responsiveLayout="scroll"
      >
        <Column field="date_str" header="Date" sortable />
        <Column field="reason" header="Reason">
          <template #body="{ data }">
            <Tag
              :value="data.reason"
              :severity="data.reason === 'maintenance' ? 'warning' : 'secondary'"
              class="capitalize"
            />
          </template>
        </Column>
        <Column header="Remove" style="width: 80px">
          <template #body="{ data }">
            <Button
              icon="pi pi-times"
              class="p-button-rounded p-button-text p-button-danger p-button-sm"
              @click="removeBlock(data.id)"
            />
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { availabilityApi } from '@/api/availability.js';

import Button from 'primevue/button';
import ProgressSpinner from 'primevue/progressspinner';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tag from 'primevue/tag';

const props = defineProps({
  apartmentId: { type: Number, required: true },
  // Optional: existing guest bookings to show as blue (passed from parent)
  guestBookings: { type: Array, default: () => [] }
});

const emit = defineEmits(['updated']);

const loading = ref(false);
const saving = ref(false);
const blockedDates = ref([]);  // Raw list from API
const pendingDates = ref([]);  // Dates user has selected but not yet saved
const selectedReason = ref('maintenance');
const isDragging = ref(false);
const dragStart = ref(null);

// Month navigation
const today = new Date();
const viewYear = ref(today.getFullYear());
const viewMonth = ref(today.getMonth());

const reasons = [
  { value: 'maintenance', label: 'Maintenance', icon: 'pi pi-wrench', activeClass: 'border-orange-400 bg-orange-50 text-orange-600' },
  { value: 'off-market', label: 'Off-market', icon: 'pi pi-eye-slash', activeClass: 'border-gray-500 bg-gray-100 text-gray-700' },
  { value: 'personal', label: 'Personal', icon: 'pi pi-user', activeClass: 'border-purple-400 bg-purple-50 text-purple-600' },
];

const selectedReasonLabel = computed(() => reasons.find(r => r.value === selectedReason.value)?.label || '');

const currentMonthLabel = computed(() => {
  return new Date(viewYear.value, viewMonth.value, 1).toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
});

const prevMonth = () => {
  if (viewMonth.value === 0) { viewMonth.value = 11; viewYear.value--; }
  else viewMonth.value--;
};

const nextMonth = () => {
  if (viewMonth.value === 11) { viewMonth.value = 0; viewYear.value++; }
  else viewMonth.value++;
};

// Build calendar grid with leading/trailing empty cells
const calendarCells = computed(() => {
  const firstDay = new Date(viewYear.value, viewMonth.value, 1).getDay();
  const daysInMonth = new Date(viewYear.value, viewMonth.value + 1, 0).getDate();
  const cells = [];
  for (let i = 0; i < firstDay; i++) cells.push({ date: null });
  for (let d = 1; d <= daysInMonth; d++) cells.push({ date: new Date(viewYear.value, viewMonth.value, d) });
  return cells;
});

const toKey = (d) => d ? d.toISOString().split('T')[0] : null;

// Build a set of blocked date keys for O(1) lookup
const blockedKeys = computed(() => new Set(blockedDates.value.map(b => b.blocked_date)));
const guestBookingKeys = computed(() => {
  const keys = new Set();
  for (const booking of props.guestBookings) {
    if (!booking.check_in || !booking.check_out) continue;
    let cur = new Date(booking.check_in);
    const end = new Date(booking.check_out);
    while (cur < end) { keys.add(toKey(cur)); cur.setDate(cur.getDate() + 1); }
  }
  return keys;
});

const getDayReason = (date) => {
  if (!date) return null;
  const key = toKey(date);
  const entry = blockedDates.value.find(b => b.blocked_date === key);
  return entry ? entry.reason : null;
};

const getDayClass = (cell) => {
  if (!cell.date) return 'day-empty';
  const key = toKey(cell.date);
  const isPast = cell.date < new Date(new Date().setHours(0,0,0,0));
  const reason = getDayReason(cell.date);
  const isPending = pendingDates.value.includes(key);
  const isGuestBooked = guestBookingKeys.value.has(key);

  return {
    'day-past': isPast,
    'day-maintenance': reason === 'maintenance',
    'day-offmarket': reason === 'off-market' || reason === 'personal',
    'day-guest': isGuestBooked,
    'day-pending': isPending,
    'day-today': key === toKey(today),
    'cursor-pointer': !isPast,
    'cursor-not-allowed': isPast
  };
};

const toggleDay = (date) => {
  const key = toKey(date);
  if (date < new Date(new Date().setHours(0,0,0,0))) return;
  const idx = pendingDates.value.indexOf(key);
  if (idx === -1) pendingDates.value.push(key);
  else pendingDates.value.splice(idx, 1);
};

const startDrag = (date) => {
  isDragging.value = true;
  dragStart.value = date;
  const key = toKey(date);
  if (!pendingDates.value.includes(key)) pendingDates.value.push(key);
};

const continueDrag = (date) => {
  if (!isDragging.value || !dragStart.value) return;
  const start = dragStart.value < date ? dragStart.value : date;
  const end = dragStart.value < date ? date : dragStart.value;
  const keys = [];
  let cur = new Date(start);
  while (cur <= end) {
    const k = toKey(cur);
    if (!keys.includes(k)) keys.push(k);
    cur.setDate(cur.getDate() + 1);
  }
  pendingDates.value = keys;
};

const endDrag = () => { isDragging.value = false; dragStart.value = null; };

const savePendingDates = async () => {
  if (!pendingDates.value.length) return;
  saving.value = true;
  try {
    const sorted = [...pendingDates.value].sort();
    await availabilityApi.blockDateRange({
      apartment_id: props.apartmentId,
      start_date: sorted[0],
      end_date: sorted[sorted.length - 1],
      reason: selectedReason.value
    });
    pendingDates.value = [];
    await fetchBlocked();
    emit('updated');
  } catch (e) {
    console.error('Failed to save blocked dates', e);
  } finally {
    saving.value = false;
  }
};

const removeBlock = async (id) => {
  try {
    await availabilityApi.unblockDate(id);
    await fetchBlocked();
    emit('updated');
  } catch (e) {
    console.error('Failed to unblock date', e);
  }
};

const groupedBlocked = computed(() =>
  [...blockedDates.value]
    .sort((a, b) => a.blocked_date.localeCompare(b.blocked_date))
    .map(b => ({ ...b, date_str: new Date(b.blocked_date + 'T00:00:00').toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }) }))
);

const fetchBlocked = async () => {
  loading.value = true;
  try {
    const res = await availabilityApi.getBlockedDates(props.apartmentId);
    blockedDates.value = res.data;
  } catch (e) {
    console.error('Failed to load blocked dates', e);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchBlocked);
watch(() => props.apartmentId, fetchBlocked);
</script>

<style scoped>
.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 4px;
}

.reason-chip { transition: all 0.2s; }

.day-header-row {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 2px;
  margin-bottom: 4px;
}

.day-header {
  text-align: center;
  font-size: 0.7rem;
  font-weight: 700;
  color: #94a3b8;
  padding: 6px 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.days-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.day-cell {
  aspect-ratio: 1;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.15s;
  user-select: none;
  position: relative;
  background: #f8fafc;
  border: 1px solid transparent;
  min-height: 44px;
}

.day-cell:not(.day-empty):not(.day-past):hover {
  background: #e0e7ff;
  border-color: #6366f1;
  transform: scale(1.08);
  z-index: 2;
}

.day-number { line-height: 1; }
.day-label {
  font-size: 0.55rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-top: 2px;
  opacity: 0.85;
}

.day-empty { background: transparent; border: none; }
.day-past { color: #cbd5e1; background: #f8fafc; cursor: not-allowed !important; }
.day-today { border-color: #6366f1 !important; background: #eef2ff; color: #6366f1; font-weight: 800; }
.day-guest { background: #dbeafe; color: #1d4ed8; border-color: #93c5fd; }
.day-maintenance { background: #fff7ed; color: #c2410c; border-color: #fed7aa; }
.day-offmarket { background: #f1f5f9; color: #475569; border-color: #cbd5e1; }
.day-pending {
  background: #6366f1 !important;
  color: white !important;
  border-color: #4f46e5 !important;
  transform: scale(1.05);
}
</style>
