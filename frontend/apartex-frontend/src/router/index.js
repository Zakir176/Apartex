// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // Renter-facing routes
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { requiresAuth: true, role: 'renter' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresGuest: true, targetRole: 'renter' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { requiresGuest: true, targetRole: 'renter' }
  },
  {
    path: '/apartments',
    name: 'Apartments',
    component: () => import('@/views/ApartmentsView.vue'),
    meta: { requiresAuth: true, role: 'renter' }
  },
  {
    path: '/apartments/:id',
    name: 'ApartmentDetail',
    component: () => import('@/views/ApartmentDetailView.vue'),
    meta: { requiresAuth: true, role: 'renter' }
  },
  {
    path: '/bookings',
    name: 'Bookings',
    component: () => import('@/views/BookingsView.vue'),
    meta: { requiresAuth: true, role: 'renter' }
  },
  {
    path: '/loyalty',
    name: 'Loyalty',
    component: () => import('@/views/LoyaltyView.vue'),
    meta: { requiresAuth: true, role: 'renter' }
  },

  // Owner-facing routes
  {
    path: '/owner',
    name: 'OwnerHome',
    component: () => import('@/views/OwnerHomeView.vue'),
    meta: { requiresAuth: true, role: 'owner' }
  },
  {
    path: '/owner/login',
    name: 'OwnerLogin',
    component: () => import('@/views/OwnerLoginView.vue'),
    meta: { requiresGuest: true, targetRole: 'owner' }
  },
  {
    path: '/owner/register',
    name: 'OwnerRegister',
    component: () => import('@/views/OwnerRegisterView.vue'),
    meta: { requiresGuest: true, targetRole: 'owner' }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true, role: 'owner' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards: enforce auth and role-based access
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // If we have a token but no user loaded yet, fetch current user once
  if (authStore.token && !authStore.user) {
    try { await authStore.fetchCurrentUser() } catch (e) { /* ignore */ }
  }

  const isAuth = authStore.isAuthenticated
  const role = authStore.user?.role

  // Require authentication
  if (to.meta.requiresAuth && !isAuth) {
    if (to.meta.role === 'owner') return next('/owner/login')
    return next('/login')
  }

  // Prevent authenticated users from accessing guest routes
  if (to.meta.requiresGuest && isAuth) {
    if (role === 'owner') return next('/owner')
    return next('/')
  }

  // Enforce role restrictions for authenticated users
  if (to.meta.role && isAuth && role !== to.meta.role) {
    if (role === 'owner') return next('/owner')
    return next('/')
  }

  next()
})

export default router
