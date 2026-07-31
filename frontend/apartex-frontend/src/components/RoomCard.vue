<template>
  <div class="bg-white border border-surface-border rounded-xl overflow-hidden shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200">
    <!-- Image -->
    <div class="relative aspect-[16/9] overflow-hidden bg-slate-100">
      <img
        :src="room.image_url || '/placeholder-room.png'"
        :alt="room.room_type"
        class="w-full h-full object-cover"
        @error="$event.target.src = 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=600'"
      />
      <div class="absolute top-3 left-3 bg-slate-900/80 text-white text-xs font-black px-3 py-1.5 rounded-full">
        ${{ room.price_per_night }}<span class="font-normal opacity-70">/night</span>
      </div>
      <div class="absolute top-3 right-3 bg-white/90 text-slate-700 text-xs font-bold px-2.5 py-1 rounded-full border border-white/60">
        {{ room.total_units }} unit{{ room.total_units !== 1 ? 's' : '' }}
      </div>
    </div>

    <!-- Body -->
    <div class="p-4 flex flex-col gap-3">
      <div>
        <h3 class="font-extrabold text-slate-800 text-base leading-tight">{{ room.room_type }}</h3>
        <p v-if="room.description" class="text-slate-500 text-xs mt-1 line-clamp-2 leading-relaxed">{{ room.description }}</p>
      </div>

      <!-- Stats -->
      <div class="flex items-center gap-3 px-3 py-2 bg-slate-50 rounded-lg text-xs text-slate-600 font-semibold">
        <span class="flex items-center gap-1.5">
          <i class="pi pi-users text-slate-400 text-xs"></i>
          Up to {{ room.capacity }} guests
        </span>
        <span class="w-px h-3 bg-slate-200"></span>
        <span class="flex items-center gap-1.5">
          <i class="pi pi-check-circle text-emerald-500 text-xs"></i>
          Available
        </span>
      </div>

      <!-- Price breakdown if dates selected -->
      <div v-if="nightsCount > 0" class="text-xs text-slate-500 font-medium">
        ${{ room.price_per_night }} × {{ nightsCount }} night{{ nightsCount > 1 ? 's' : '' }} =
        <span class="font-black text-slate-800">${{ (parseFloat(room.price_per_night) * nightsCount).toFixed(2) }}</span>
      </div>

      <!-- Book button -->
      <button
        @click="$emit('book', room)"
        class="w-full bg-accent hover:bg-accent-hover text-white font-bold py-2.5 rounded-lg text-sm transition-colors duration-150 flex items-center justify-center gap-2"
      >
        <i class="pi pi-bolt text-sm"></i>
        Reserve Room
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  room: { type: Object, required: true },
  nightsCount: { type: Number, default: 0 },
});
defineEmits(['book']);
</script>
