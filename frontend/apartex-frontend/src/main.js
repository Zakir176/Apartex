import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { pinia } from './stores';

// PrimeVue configuration
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/lara-light-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

import './assets/main.css';

import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import { MotionPlugin } from '@vueuse/motion';

const app = createApp(App);

app.use(pinia);
app.use(router);
app.use(PrimeVue, { ripple: true });
app.use(ConfirmationService);
app.use(ToastService);
app.use(MotionPlugin);

app.mount('#app');

// Register Service Worker for PWA support
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((reg) => console.log('⚡ Apartex Service Worker active:', reg.scope))
      .catch((err) => console.warn('⚠️ Service Worker registration failed:', err));
  });
}