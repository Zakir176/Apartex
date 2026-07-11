<template>
  <div class="max-w-[1200px] mx-auto px-6 py-8">
    <div class="mb-10">
      <h1 class="text-4xl font-extrabold text-slate-800 mb-3">Welcome back, {{ authStore.user?.full_name }}!</h1>
      <p class="text-lg text-slate-500 font-medium max-w-2xl leading-relaxed">Efficiently manage your properties and maximize your earnings from one central hub.</p>
    </div>

    <!-- Quick Action Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
      <div class="card-base p-6 cursor-pointer group" @click="router.push('/owner/apartments')">
        <div class="w-14 h-14 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-blue-600 group-hover:text-white transition-all duration-300">
          <i class="pi pi-plus-circle text-2xl"></i>
        </div>
        <h3 class="text-xl font-bold text-slate-800 mb-3">List New Apartment</h3>
        <p class="text-slate-500 text-sm font-medium leading-relaxed mb-6">Create a beautiful listing and start reaching guests instantly.</p>
        <span class="inline-flex items-center gap-2 text-sm font-bold text-blue-600 group-hover:text-blue-700 transition-colors">
          <i class="pi pi-plus"></i> Add Listing
        </span>
      </div>

      <div class="card-base p-6 cursor-pointer group" @click="router.push('/dashboard')">
        <div class="w-14 h-14 rounded-2xl bg-orange-50 text-accent flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-accent group-hover:text-white transition-all duration-300">
          <i class="pi pi-chart-line text-2xl"></i>
        </div>
        <h3 class="text-xl font-bold text-slate-800 mb-3">View Performance</h3>
        <p class="text-slate-500 text-sm font-medium leading-relaxed mb-6">Analyze revenue, occupancy rates, and optimization tips.</p>
        <span class="inline-flex items-center gap-2 text-sm font-bold text-accent group-hover:text-accent-hover transition-colors">
          <i class="pi pi-external-link"></i> Open Analytics
        </span>
      </div>

      <div class="card-base p-6 cursor-pointer group" @click="router.push('/owner/bookings')">
        <div class="w-14 h-14 rounded-2xl bg-green-50 text-green-600 flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-green-600 group-hover:text-white transition-all duration-300">
          <i class="pi pi-calendar-check text-2xl"></i>
        </div>
        <h3 class="text-xl font-bold text-slate-800 mb-3">Manage Bookings</h3>
        <p class="text-slate-500 text-sm font-medium leading-relaxed mb-6">Review incoming requests and coordinate check-ins.</p>
        <span class="inline-flex items-center gap-2 text-sm font-bold text-green-600 group-hover:text-green-700 transition-colors">
          <i class="pi pi-arrow-right"></i> View Bookings
        </span>
      </div>
    </div>

    <!-- Getting Started / News Section -->
    <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
      <!-- Getting Started Guide -->
      <div class="lg:col-span-3 card-base">
        <div class="p-6 border-b border-surface-border">
          <h3 class="text-lg font-bold text-slate-800">Getting Started Guide</h3>
        </div>
        <div class="p-6">
          <ul class="flex flex-col gap-4">
            <li class="flex items-start gap-4 pb-4 border-b border-surface-border last:border-0 last:pb-0">
              <i class="pi pi-check-circle text-green-500 text-xl mt-0.5"></i>
              <div>
                <h4 class="font-bold text-slate-800 mb-1">Complete your profile and payout details</h4>
                <p class="text-sm font-medium text-slate-500 m-0">Ensure you can receive payments seamlessly.</p>
              </div>
            </li>
            <li class="flex items-start gap-4 pb-4 border-b border-surface-border last:border-0 last:pb-0">
              <i class="pi pi-check-circle text-green-500 text-xl mt-0.5"></i>
              <div>
                <h4 class="font-bold text-slate-800 mb-1">Add high-quality photos</h4>
                <p class="text-sm font-medium text-slate-500 m-0">Listings with 5+ professional photos get 40% more bookings.</p>
              </div>
            </li>
            <li class="flex items-start gap-4 pb-4 border-b border-surface-border last:border-0 last:pb-0">
              <i class="pi pi-circle text-slate-300 text-xl mt-0.5"></i>
              <div>
                <h4 class="font-bold text-slate-800 mb-1">Verify your identity</h4>
                <p class="text-sm font-medium text-slate-500 m-0">Verified hosts increase guest trust and booking conversions.</p>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <!-- What's New -->
      <div class="lg:col-span-2 card-base">
        <div class="p-6 border-b border-surface-border">
          <h3 class="text-lg font-bold text-slate-800">What's New</h3>
        </div>
        <div class="p-6 flex flex-col gap-6">
          <div class="flex flex-col items-start">
            <span class="inline-block px-2.5 py-1 bg-blue-50 text-blue-600 rounded-md text-[10px] font-bold uppercase tracking-wider mb-2">Platform Update</span>
            <p class="text-sm font-medium text-slate-700 m-0 leading-relaxed">The new "Instant Book" feature is now available for premium members. Turn it on in your listing settings to boost visibility.</p>
          </div>
          <div class="flex flex-col items-start">
            <span class="inline-block px-2.5 py-1 bg-pink-50 text-pink-600 rounded-md text-[10px] font-bold uppercase tracking-wider mb-2">Host Tips</span>
            <p class="text-sm font-medium text-slate-700 m-0 leading-relaxed">Seasonal pricing trends: Learn how to optimize your nightly rates during the upcoming summer peak season.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
</script>
