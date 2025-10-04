import { createPinia } from 'pinia';

export const pinia = createPinia();

// Re-export all stores for easy importing
export { useAuthStore } from './auth';
export { useApartmentsStore } from './apartments';
export { useBookingsStore } from './bookings';
export { useLoyaltyStore } from './loyalty';