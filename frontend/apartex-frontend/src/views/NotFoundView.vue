<template>
  <div class="min-h-screen bg-[#F8F7F4] flex items-center justify-center px-4">
    <div class="text-center max-w-md">
      <p class="text-8xl font-black text-slate-100 leading-none select-none mb-2">404</p>
      <h1 class="text-2xl font-black text-slate-800 mb-3">Page not found</h1>
      <p class="text-slate-400 text-sm mb-8 leading-relaxed">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <router-link
        to="/"
        class="inline-flex items-center gap-2 bg-accent hover:bg-accent-hover text-white font-bold px-6 py-3 rounded-full text-sm transition-colors duration-150 no-underline"
      >
        <i class="pi pi-home"></i>
        Back to Home
      </router-link>
    </div>
  </div>
</template>

<script setup>
// No logic needed
</script>