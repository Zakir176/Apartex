// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Import your components
const HomeView = () => import('@/views/HomeView.vue')
const LoginView = () => import('@/views/LoginView.vue')
const RegisterView = () => import('@/views/RegisterView.vue')
const ApartmentsView = () => import('@/views/ApartmentsView.vue')
const ApartmentDetailView = () => import('@/views/ApartmentDetailView.vue')
const DashboardView = () => import('@/views/DashboardView.vue')
const BookingsView = () => import('@/views/BookingsView.vue')
const LoyaltyView = () => import('@/views/LoyaltyView.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { guestOnly: true }
  },
  {
    path: '/apartments',
    name: 'Apartments',
    component: ApartmentsView
  },
  {
    path: '/apartments/:id',
    name: 'ApartmentDetail',
    component: ApartmentDetailView,
    props: true
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/bookings',
    name: 'Bookings',
    component: BookingsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/loyalty',
    name: 'Loyalty',
    component: LoyaltyView,
    meta: { requiresAuth: true }
  },
  // Catch all 404 - make sure this is LAST
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

// Route guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.guestOnly && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router