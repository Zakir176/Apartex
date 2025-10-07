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
        <div class="row">
          <input v-model="form.image_url" placeholder="Image URL (optional)" />
          <input type="file" accept="image/*" @change="onSelectCreateImage" />
        </div>
        <div v-if="form.image_url" class="preview">
          <img :src="form.image_url" alt="Preview" />
        </div>
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
          <div v-if="apt.image_url" class="thumb">
            <img :src="apt.image_url" alt="Apartment" />
          </div>
          <div class="card-actions">
            <button class="btn small" @click="startEdit(apt)">Edit</button>
            <button class="btn small danger" @click="removeApartment(apt.id)">Delete</button>
          </div>
        </li>
      </ul>
    </section>

    <section v-if="editing" class="edit-form">
      <h3>Edit Apartment</h3>
      <form @submit.prevent="handleUpdate">
        <div class="grid">
          <input v-model="editForm.title" placeholder="Title" required />
          <input v-model="editForm.address" placeholder="Address" required />
          <input v-model="editForm.city" placeholder="City" required />
          <input v-model.number="editForm.price_per_night" placeholder="Price per night" type="number" min="0" step="0.01" required />
          <input v-model.number="editForm.capacity" placeholder="Capacity" type="number" min="1" required />
          <input v-model.number="editForm.bedrooms" placeholder="Bedrooms" type="number" min="0" required />
          <input v-model.number="editForm.bathrooms" placeholder="Bathrooms" type="number" min="0" required />
        </div>
        <textarea v-model="editForm.description" placeholder="Description"></textarea>
        <input v-model="editForm.amenities" placeholder="Amenities (comma-separated)" />
        <div class="row">
          <input v-model="editForm.image_url" placeholder="Image URL (optional)" />
          <input type="file" accept="image/*" @change="onSelectEditImage" />
        </div>
        <div v-if="editForm.image_url" class="preview">
          <img :src="editForm.image_url" alt="Preview" />
        </div>
        <div class="row">
          <button class="btn" type="submit" :disabled="loading">Save</button>
          <button class="btn secondary" type="button" @click="cancelEdit">Cancel</button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { useApartmentsStore } from '@/stores/apartments';
import { useAuthStore } from '@/stores/auth';
import { uploadImage } from '@/api/uploads';

const apartmentsStore = useApartmentsStore();
const auth = useAuthStore();

const form = reactive({
  title: '', description: '', address: '', city: '', price_per_night: 0, capacity: 1, bedrooms: 1, bathrooms: 1, amenities: '', image_url: ''
});

const loading = apartmentsStore.loading;
const error = apartmentsStore.error;
const apartments = apartmentsStore.apartments;

onMounted(async () => {
  await apartmentsStore.fetchApartments({ owner_id: auth.user?.id });
});

async function onSelectCreateImage(e) {
  const file = e.target.files?.[0];
  if (!file) return;
  const { url } = await uploadImage(file);
  form.image_url = url;
}

async function onSelectEditImage(e) {
  const file = e.target.files?.[0];
  if (!file) return;
  const { url } = await uploadImage(file);
  editForm.image_url = url;
}

async function handleCreate() {
  const payload = { ...form, amenities: form.amenities };
  await apartmentsStore.createApartment(payload);
  await apartmentsStore.fetchApartments({ owner_id: auth.user?.id });
  Object.assign(form, { title: '', description: '', address: '', city: '', price_per_night: 0, capacity: 1, bedrooms: 1, bathrooms: 1, amenities: '', image_url: '' });
}

const editing = ref(false);
const editingId = ref(null);
const editForm = reactive({ title: '', description: '', address: '', city: '', price_per_night: 0, capacity: 1, bedrooms: 1, bathrooms: 1, amenities: '', image_url: '' });

function startEdit(apt) {
  editing.value = true;
  editingId.value = apt.id;
  Object.assign(editForm, {
    title: apt.title,
    description: apt.description || '',
    address: apt.address,
    city: apt.city,
    price_per_night: Number(apt.price_per_night),
    capacity: apt.capacity,
    bedrooms: apt.bedrooms,
    bathrooms: apt.bathrooms,
    amenities: apt.amenities || '',
    image_url: apt.image_url || ''
  });
}

function cancelEdit() { editing.value = false; editingId.value = null; }

async function handleUpdate() {
  if (!editingId.value) return;
  await apartmentsStore.updateApartment(editingId.value, { ...editForm });
  await apartmentsStore.fetchApartments({ owner_id: auth.user?.id });
  cancelEdit();
}

async function removeApartment(id) {
  await apartmentsStore.deleteApartment(id);
  await apartmentsStore.fetchApartments({ owner_id: auth.user?.id });
}
</script>

<style scoped>
.page-container { padding: 24px; max-width: 900px; margin: 0 auto; }
.create-form, .list { margin-top: 24px; }
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
textarea, input { width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: 8px; font-size: 1rem; background: var(--bg); color: var(--text); }
textarea { min-height: 80px; margin: 12px 0; }
textarea:focus, input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
.btn { padding: 8px 14px; background: var(--primary); color: var(--primary-contrast); border: none; border-radius: 8px; cursor: pointer; }
.btn.small { padding: 6px 10px; font-size: 12px; }
.btn.secondary { background: #6b7280; }
.btn.danger { background: #dc2626; }
.error { color: #dc2626; margin-top: 8px; }
.cards { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.card { border: 1px solid var(--border); border-radius: 8px; padding: 12px; background: var(--bg); }
.card-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.card-actions { display: flex; gap: 8px; margin-top: 8px; }
.edit-form { margin-top: 24px; }
.row { display: flex; gap: 12px; align-items: center; }
.thumb img, .preview img { max-width: 100%; border-radius: 8px; border: 1px solid var(--border); }
</style>

