<template>
  <div class="home">
    <section class="hero">
      <h1>Find Your Perfect Stay</h1>
      <p>Discover amazing apartments for your next trip</p>
    </section>

    <section class="featured-apartments">
      <h2>Featured Apartments</h2>
      <div v-if="apartmentsStore.loading" class="loading">Loading...</div>
      <div v-else class="apartments-grid">
        <ApartmentCard 
          v-for="apartment in apartmentsStore.featuredApartments" 
          :key="apartment.id" 
          :apartment="apartment" 
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useApartmentsStore } from '@/stores/apartments';
import ApartmentCard from '@/components/ApartmentCard.vue';

const apartmentsStore = useApartmentsStore();

onMounted(async () => {
  if (apartmentsStore.apartments.length === 0) {
    await apartmentsStore.fetchApartments();
  }
});
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.featured-apartments {
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.featured-apartments h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.apartments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
}
</style>