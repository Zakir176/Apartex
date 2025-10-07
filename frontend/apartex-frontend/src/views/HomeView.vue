<template>
  <div class="home flex flex-col items-center w-full">
    <!-- 🌆 HERO SECTION -->
    <section
      class="relative w-full h-[70vh] flex flex-col justify-center items-center text-center bg-gradient-to-br from-indigo-500 via-purple-500 to-fuchsia-500 text-white overflow-hidden"
    >
      <!-- Optional background pattern -->
      <div class="absolute inset-0 opacity-20 bg-[url('/grid-pattern.svg')] bg-cover bg-center"></div>

      <div class="relative z-10 max-w-3xl px-6">
        <h1 class="text-5xl md:text-6xl font-bold mb-4 leading-tight drop-shadow-lg">
          Find Your Perfect Stay
        </h1>
        <p class="text-lg md:text-xl opacity-90 mb-8">
          Discover amazing apartments for your next trip
        </p>

        <!-- Optional search bar (visual only) -->
        <div
          class="flex bg-white/10 backdrop-blur-md rounded-2xl overflow-hidden shadow-md max-w-xl mx-auto border border-white/20"
        >
          <input
            type="text"
            placeholder="Search destination..."
            class="flex-1 px-4 py-3 bg-transparent text-white placeholder-white/60 focus:outline-none"
          />
          <button
            class="px-6 py-3 bg-white text-indigo-600 font-semibold hover:bg-gray-100 transition"
          >
            Search
          </button>
        </div>
      </div>
    </section>

    <!-- 🏢 FEATURED APARTMENTS -->
    <section class="w-full max-w-7xl px-6 py-16">
      <h2 class="text-3xl font-semibold text-center mb-12 text-gray-800">
        Featured Apartments
      </h2>

      <div v-if="apartmentsStore.loading" class="flex justify-center py-16">
        <div
          class="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-indigo-500"
        ></div>
      </div>

      <div
        v-else
        class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
      >
        <ApartmentCard
          v-for="apartment in apartmentsStore.featuredApartments"
          :key="apartment.id"
          :apartment="apartment"
          class="hover:scale-[1.02] transition-transform duration-300"
        />
      </div>

      <div
        v-if="!apartmentsStore.loading && apartmentsStore.featuredApartments.length === 0"
        class="text-center text-gray-500 mt-10"
      >
        <p>No featured apartments available right now.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useApartmentsStore } from '@/stores/apartments'
import ApartmentCard from '@/components/ApartmentCard.vue'

const apartmentsStore = useApartmentsStore()

onMounted(async () => {
  if (apartmentsStore.apartments.length === 0) {
    await apartmentsStore.fetchApartments()
  }
})
</script>

<style scoped>
/* Optional smooth fade for hero text */
.hero-enter-active,
.hero-leave-active {
  transition: opacity 0.8s ease;
}
.hero-enter-from,
.hero-leave-to {
  opacity: 0;
}
</style>
