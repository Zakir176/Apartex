<template>
  <div class="page-container">
    <h2>My Apartments</h2>

    <section class="create-form">
      <h3>Add New Apartment</h3>
      <form @submit.prevent="handleCreate">
        <div class="grid">
          <input v-model="form.title" placeholder="Title" required />
          <input v-model="form.address" placeholder="Address" required />
          <input v-model="form.city" placeholder="City" required />
          <input v-model.number="form.price_per_night" placeholder="Price per night" type="number" min="0" step="0.01" required />
          <input v-model.number="form.capacity" placeholder="Capacity" type="number" min="1" required />
          <input v-model.number="form.bedrooms" placeholder="Bedrooms" type="number" min="0" required />
          <input v-model.number="form.bathrooms" placeholder="Bathrooms" type="number" min="0" required />
        </div>
        <textarea v-model="form.description" placeholder="Description"></textarea>
        <input v-model="form.amenities" placeholder="Amenities (comma-separated)" />
        <button class="btn" type="submit" :disabled="loading">{{ loading ? 'Creating...' : 'Create' }}</button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </section>

    <section class="list">
      <h3>Listed Apartments</h3>
      <div v-if="loading">Loading...</div>
      <div v-else-if="apartments.length === 0">No apartments yet.</div>
      <ul v-else class="cards">
        <li v-for="apt in apartments" :key="apt.id" class="card">
          <div class="card-header">
            <strong>{{ apt.title }}</strong>
            <span>${{ Number(apt.price_per_night).toFixed(2) }}/night</span>
          </div>
          <div class="card-body">
            <div>{{ apt.address }}, {{ apt.city }}</div>
            <div>Capacity: {{ apt.capacity }} • Beds: {{ apt.bedrooms }} • Baths: {{ apt.bathrooms }}</div>
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive } from 'vue';
import { useApartmentsStore } from '@/stores/apartments';
import { useAuthStore } from '@/stores/auth';

const apartmentsStore = useApartmentsStore();
const auth = useAuthStore();

const form = reactive({
  title: '',
  description: '',
  address: '',
  city: '',
  price_per_night: 0,
  capacity: 1,
  bedrooms: 1,
  bathrooms: 1,
  amenities: ''
});

const loading = apartmentsStore.loading;
const error = apartmentsStore.error;
const apartments = apartmentsStore.apartments;

onMounted(async () => {
  // filter by current owner on the backend
  await apartmentsStore.fetchApartments({ owner_id: auth.user?.id });
});

async function handleCreate() {
  const payload = {
    ...form,
    amenities: form.amenities
  };
  await apartmentsStore.createApartment(payload);
  // refresh list filtered by owner
  await apartmentsStore.fetchApartments({ owner_id: auth.user?.id });
  // reset
  Object.assign(form, { title: '', description: '', address: '', city: '', price_per_night: 0, capacity: 1, bedrooms: 1, bathrooms: 1, amenities: '' });
}
</script>

<style scoped>
.page-container { padding: 24px; max-width: 900px; margin: 0 auto; }
.create-form, .list { margin-top: 24px; }
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
textarea { width: 100%; min-height: 80px; margin: 12px 0; }
.btn { padding: 8px 14px; background: #2563eb; color: #fff; border: none; border-radius: 6px; cursor: pointer; }
.error { color: #dc2626; margin-top: 8px; }
.cards { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.card { border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; }
.card-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
</style>

