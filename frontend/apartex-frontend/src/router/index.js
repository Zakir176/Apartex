// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // Public Landing Page for all visitors
  {
    path: '/',
    name: 'Landing',
    component: () => import('@/views/LandingView.vue'),
    meta: { allowGuest: true }
  },
  {
    path: '/landing',
    name: 'LandingDirect',
    component: () => import('@/views/LandingView.vue'),
    meta: { allowGuest: true }
  },

  // Dedicated Host Hub & Calculator (Public)
  {
    path: '/host',
    name: 'HostLanding',
    component: () => import('@/views/HostLandingView.vue'),
    meta: { allowGuest: true }
  },

  // Help & Support Center (Public)
  {
    path: '/help',
    name: 'Help',
    component: () => import('@/views/HelpView.vue'),
    meta: { allowGuest: true }
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
    meta: { allowGuest: true }
  },
  {
    path: '/apartments/:id',
    name: 'ApartmentDetail',
    component: () => import('@/views/ApartmentDetailView.vue'),
    meta: { allowGuest: true }
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: () => import('@/views/CheckoutView.vue'),
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
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/wishlist',
    name: 'Wishlist',
    component: () => import('@/views/WishlistView.vue'),
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
    component: () => import('@/views/LoginView.vue'),
    meta: { requiresGuest: true, targetRole: 'owner' }
  },
  {
    path: '/owner/register',
    name: 'OwnerRegister',
    component: () => import('@/views/RegisterView.vue'),
    meta: { requiresGuest: true, targetRole: 'owner' }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true, role: 'owner' }
  },
  {
    path: '/owner/apartments',
    name: 'OwnerApartments',
    component: () => import('@/views/OwnerApartmentsView.vue'),
    meta: { requiresAuth: true, role: 'owner' }
  },
  {
    path: '/owner/bookings',
    name: 'OwnerBookings',
    component: () => import('@/views/OwnerBookingsView.vue'),
    meta: { requiresAuth: true, role: 'owner' }
  },
  {
    path: '/owner/payouts',
    name: 'OwnerPayouts',
    component: () => import('@/views/OwnerPayoutsView.vue'),
    meta: { requiresAuth: true, role: 'owner' }
  },
  // Catch-all 404 route
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue')
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

  // Require authentication for action routes
  if (to.meta.requiresAuth && !isAuth) {
    if (to.meta.role === 'owner') return next('/owner/login')
    return next('/login')
  }

  // Prevent authenticated users from accessing guest auth routes (like /login or /register)
  if (to.meta.requiresGuest && isAuth) {
    if (role === 'owner') return next('/owner')
    return next('/home')
  }

  // Enforce role restrictions for authenticated users on role-gated routes
  if (to.meta.role && isAuth && role !== to.meta.role) {
    if (role === 'owner') return next('/owner')
    return next('/home')
  }

  next()
})

export default router
