<template>
  <div class="auth-container">
    <!-- Left: Immersive Visual -->
    <div class="auth-visual" :style="{ backgroundImage: `url(${bgImage})` }">
      <div class="visual-overlay">
        <div class="visual-content">
          <h1 class="text-white font-bold text-5xl mb-3">Join the Elite</h1>
          <p class="text-white opacity-80 text-xl font-medium">Whether you're hosting or staycationing, we have a place for you.</p>
        </div>
      </div>
    </div>

    <!-- Right: Auth Form -->
    <div class="auth-form-wrapper flex align-items-center justify-content-center">
      <Card class="auth-card glass border-none shadow-none">
        <template #content>
          <div class="text-center mb-5">
            <h2 class="text-3xl font-bold mb-2">Create Account</h2>
            <p class="text-muted">Start your journey with Apartex today</p>
          </div>

          <!-- Role Toggle -->
          <div class="flex justify-content-center mb-5">
            <SelectButton 
              v-model="targetRole" 
              :options="roleOptions" 
              optionLabel="label" 
              optionValue="value" 
              class="premium-toggle"
            />
          </div>

          <form @submit.prevent="handleRegister" class="p-fluid">
            <div class="field mb-4">
              <label for="name" class="font-bold block mb-2 text-sm uppercase tracking-wider text-gray-500">Full Name</label>
              <InputText id="name" v-model="form.name" required placeholder="John Doe" class="p-inputtext-lg" />
            </div>

            <div class="field mb-4">
              <label for="email" class="font-bold block mb-2 text-sm uppercase tracking-wider text-gray-500">Email Address</label>
              <InputText id="email" v-model="form.email" type="email" required placeholder="name@example.com" class="p-inputtext-lg" />
            </div>
            
            <div class="field mb-5">
              <label for="password" class="font-bold block mb-2 text-sm uppercase tracking-wider text-gray-500">Create Password</label>
              <Password 
                id="password" 
                v-model="form.password" 
                toggleMask 
                required 
                minlength="6"
                placeholder="••••••••" 
                inputClass="p-inputtext-lg w-full" 
              >
                <template #footer>
                  <Divider />
                  <p class="mt-2 text-sm">Suggestions:</p>
                  <ul class="pl-2 ml-2 mt-0 text-sm line-height-3">
                    <li>At least one lowercase</li>
                    <li>At least one uppercase</li>
                    <li>At least one numeric</li>
                    <li>Minimum 8 characters</li>
                  </ul>
                </template>
              </Password>
            </div>
            
            <Button 
              type="submit" 
              :label="loading ? 'Creating Account...' : 'Register Now'" 
              :loading="loading" 
              class="p-button-lg p-button-primary font-bold py-3 text-xl border-round-xl" 
            />
            
            <Message v-if="error" severity="error" class="mt-4" :closable="false">{{ error }}</Message>
          </form>
          
          <div class="mt-5 text-center">
            <p class="text-gray-500">
              Already have an account? 
              <router-link to="/login" class="text-primary font-bold no-underline hover:underline ml-1">
                Login here
              </router-link>
            </p>
          </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

// PrimeVue components
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Message from 'primevue/message';
import SelectButton from 'primevue/selectbutton';
import Divider from 'primevue/divider';

// Assets
const bgImage = 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&q=80&w=1920';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const targetRole = ref('renter');
const roleOptions = [
  { label: 'Guest', value: 'renter' },
  { label: 'Host', value: 'owner' }
];

const form = ref({
  name: '',
  email: '',
  password: ''
});

const loading = ref(false);
const error = ref('');

onMounted(() => {
  if (route.query.role === 'owner') {
    targetRole.value = 'owner';
  }
});

const handleRegister = async () => {
  loading.value = true;
  error.value = '';
  
  try {
    await authStore.register({ ...form.value, role: targetRole.value });
    if (targetRole.value === 'owner') {
      router.push('/owner');
    } else {
      router.push('/');
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed. Please check your details.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.auth-visual {
  flex: 1.2;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: flex-end;
  padding: 4rem;
}

.auth-visual::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(to top, rgba(15, 23, 42, 0.8) 0%, rgba(15, 23, 42, 0) 100%);
}

.visual-content {
  position: relative;
  z-index: 10;
}

.auth-form-wrapper {
  flex: 1;
  background-color: var(--surface-section);
  padding: 2rem;
}

.auth-card {
  width: 100%;
  max-width: 480px;
}

.premium-toggle :deep(.p-highlight) {
  background: var(--primary-color) !important;
  color: white !important;
  border-color: var(--primary-color) !important;
}

.premium-toggle :deep(.p-button) {
  padding: 0.75rem 2rem;
  font-weight: 700;
}

.glass {
  background: transparent !important;
}

@media (max-width: 1024px) {
  .auth-visual {
    display: none;
  }
}
</style>