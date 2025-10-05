// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/apartments',
    name: 'Apartments',
    component: () => import('@/views/ApartmentsView.vue')
  },
  {
    path: '/apartments/:id',
    name: 'ApartmentDetail',
    component: () => import('@/views/ApartmentDetailView.vue')
  },
  {
    path: '/bookings',
    name: 'Bookings',
    component: () => import('@/views/BookingsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/loyalty',
    name: 'Loyalty',
    component: () => import('@/views/LoyaltyView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router