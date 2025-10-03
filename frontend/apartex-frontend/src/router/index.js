// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
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
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue')
  },
  {
    path: '/bookings',
    name: 'Bookings',
    component: () => import('@/views/BookingsView.vue')
  },
  {
    path: '/loyalty',
    name: 'Loyalty',
    component: () => import('@/views/LoyaltyView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router