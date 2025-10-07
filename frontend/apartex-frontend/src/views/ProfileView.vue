<template>
  <div class="page-container">
    <h2>My Profile</h2>

    <form class="form" @submit.prevent="save">
      <label>
        Full name
        <input v-model="fullName" placeholder="Your full name" />
      </label>
      <div class="row">
        <div><strong>Email:</strong> {{ auth.user?.email }}</div>
        <div><strong>Role:</strong> {{ auth.user?.role }}</div>
      </div>
      <button class="btn" type="submit" :disabled="saving">{{ saving ? 'Saving...' : 'Save' }}</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api/index';
import { useAuthStore } from '@/stores/auth';

const auth = useAuthStore();
const fullName = ref('');
const saving = ref(false);

onMounted(async () => {
  if (!auth.user) {
    try { await auth.fetchCurrentUser(); } catch {}
  }
  fullName.value = auth.user?.full_name || '';
});

async function save() {
  saving.value = true;
  try {
    const resp = await api.put('/auth-enhanced/me', { full_name: fullName.value });
    await auth.fetchCurrentUser();
    return resp;
  } finally {
    saving.value = false;
  }
}
</script>

<style scoped>
.page-container { padding: 24px; max-width: 640px; margin: 0 auto; }
.h2 { margin-bottom: 12px; }
.form { display: grid; gap: 12px; background: var(--bg); border: 1px solid var(--border); border-radius: 12px; padding: 16px; }
input { width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: 8px; font-size: 1rem; background: var(--bg); color: var(--text); }
input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(37,99,235,0.15); }
.row { display: flex; gap: 24px; align-items: center; color: var(--muted); }
.btn { padding: 0.75rem 1rem; background: var(--primary); color: var(--primary-contrast); border: none; border-radius: 8px; cursor: pointer; width: fit-content; }
</style>

