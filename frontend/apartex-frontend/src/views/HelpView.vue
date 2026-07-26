<template>
  <div class="min-h-screen bg-[#F8F7F4] text-slate-900 overflow-x-hidden selection:bg-accent selection:text-white">
    <!-- HERO HEADER -->
    <header class="bg-navy text-white relative pt-16 pb-20 overflow-hidden border-b border-surface-border">
      <div class="max-w-[1280px] mx-auto px-4 sm:px-6 relative z-10 text-center">
        <span class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 text-amber-300 text-xs font-black uppercase tracking-widest mb-4">
          <i class="pi pi-question-circle"></i> Apartex Help & Support Center
        </span>
        <h1 class="text-4xl sm:text-6xl font-black tracking-tight text-white mb-4">
          How Can We Help You Today?
        </h1>
        <p class="text-slate-300 text-base sm:text-lg font-medium max-w-2xl mx-auto mb-8">
          Find instant answers regarding bookings, Mobile Money payments, 0% host commissions, and trust standards.
        </p>

        <!-- Search Bar -->
        <div class="max-w-2xl mx-auto relative">
          <i class="pi pi-search absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 text-base"></i>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search questions (e.g., Mobile Money, Host Payouts, Cancellation)..."
            class="w-full pl-12 pr-12 py-4 rounded-full bg-white text-slate-900 placeholder:text-slate-400 text-sm font-bold shadow-2xl focus:outline-none focus:ring-4 focus:ring-accent/20 border-0"
          />
          <button v-if="searchQuery" @click="searchQuery = ''" class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 text-sm bg-transparent border-0 cursor-pointer">
            <i class="pi pi-times"></i>
          </button>
        </div>
      </div>
    </header>

    <!-- MAIN HELP CONTENT -->
    <main class="max-w-[1280px] mx-auto px-4 sm:px-6 py-16">
      <!-- Category Tabs -->
      <div class="flex items-center justify-center gap-2 mb-12 flex-wrap">
        <button 
          v-for="cat in categories" 
          :key="cat.id"
          @click="activeCategory = cat.id"
          class="px-5 py-2.5 rounded-full text-xs font-black transition-all cursor-pointer border-0"
          :class="activeCategory === cat.id ? 'bg-slate-900 text-white shadow-md' : 'bg-white text-slate-600 hover:text-slate-900 border border-slate-200'"
        >
          <i :class="cat.icon" class="mr-1.5 text-xs text-accent"></i>
          {{ cat.label }}
        </button>
      </div>

      <!-- FAQ List -->
      <div class="max-w-3xl mx-auto space-y-4 mb-20">
        <div 
          v-for="(item, idx) in filteredFaqs" 
          :key="item.question"
          class="bg-white rounded-2xl border transition-all duration-300 overflow-hidden"
          :class="activeFaq === idx ? 'border-accent shadow-lg' : 'border-surface-border hover:border-slate-300 shadow-sm'"
        >
          <button 
            @click="activeFaq = activeFaq === idx ? null : idx"
            class="w-full p-6 text-left flex items-center justify-between gap-4 font-black text-base sm:text-lg text-slate-900 bg-white cursor-pointer"
          >
            <span class="flex items-center gap-3">
              <span class="w-8 h-8 rounded-full bg-orange-50 text-accent font-black text-xs flex items-center justify-center shrink-0">
                <i class="pi pi-question text-xs"></i>
              </span>
              <span>{{ item.question }}</span>
            </span>
            <i :class="activeFaq === idx ? 'rotate-180' : ''" class="pi pi-chevron-down text-xs text-slate-400 transition-transform shrink-0"></i>
          </button>

          <div v-show="activeFaq === idx" class="px-6 pb-6 pt-2 text-sm text-slate-600 font-medium border-t border-slate-100 bg-slate-50/50 leading-relaxed">
            <p>{{ item.answer }}</p>
          </div>
        </div>

        <div v-if="filteredFaqs.length === 0" class="text-center py-12 bg-white rounded-2xl border border-surface-border p-8">
          <i class="pi pi-info-circle text-3xl text-slate-400 mb-3"></i>
          <h3 class="text-base font-black text-slate-800">No matching questions found</h3>
          <p class="text-xs text-slate-500 mt-1">Try clearing your search query or switching categories.</p>
        </div>
      </div>

      <!-- TRUST & SAFETY & CONCIERGE CARDS -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <div class="bg-white p-6 rounded-2xl border border-surface-border shadow-sm text-center flex flex-col items-center">
          <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 font-black flex items-center justify-center text-xl mb-4">
            <i class="pi pi-shield"></i>
          </div>
          <h3 class="text-base font-black text-slate-900 mb-2">Apartex Protection</h3>
          <p class="text-xs text-slate-500 font-medium leading-relaxed">Every booking includes 100% verified inspection & host cancellation protection.</p>
        </div>

        <div class="bg-white p-6 rounded-2xl border border-surface-border shadow-sm text-center flex flex-col items-center">
          <div class="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 font-black flex items-center justify-center text-xl mb-4">
            <i class="pi pi-phone"></i>
          </div>
          <h3 class="text-base font-black text-slate-900 mb-2">24/7 Local Support</h3>
          <p class="text-xs text-slate-500 font-medium leading-relaxed">Our Lusaka hospitality team is on standby 24 hours a day to assist guests and hosts.</p>
        </div>

        <div class="bg-white p-6 rounded-2xl border border-surface-border shadow-sm text-center flex flex-col items-center">
          <div class="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 font-black flex items-center justify-center text-xl mb-4">
            <i class="pi pi-whatsapp"></i>
          </div>
          <h3 class="text-base font-black text-slate-900 mb-2">WhatsApp Concierge</h3>
          <p class="text-xs text-slate-500 font-medium leading-relaxed mb-4">Need instant assistance? Message our direct team on WhatsApp.</p>
          <a href="https://wa.me/260970000000" target="_blank" rel="noopener" class="btn-accent text-xs font-black px-4 py-2 rounded-full no-underline inline-flex items-center gap-1.5 shadow-accent">
            <i class="pi pi-whatsapp"></i> Chat Now
          </a>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const searchQuery = ref('');
const activeCategory = ref('all');
const activeFaq = ref(0);

const categories = [
  { id: 'all', label: 'All Topics', icon: 'pi pi-list' },
  { id: 'guests', label: 'Guest & Booking', icon: 'pi pi-user' },
  { id: 'hosts', label: 'Host & Pricing', icon: 'pi pi-building' },
  { id: 'payments', label: 'MoMo & Payouts', icon: 'pi pi-wallet' }
];

const faqs = [
  {
    category: 'guests',
    question: 'How do I search and reserve a property?',
    answer: 'Enter your target city (Lusaka, Livingstone, Ndola, Kitwe, etc.) and guest count on the homepage. Click "Search Stays" to view listings. Choose your preferred residence and click "Reserve Property".'
  },
  {
    category: 'payments',
    question: 'What payment options are supported?',
    answer: 'Apartex supports MTN Mobile Money, Airtel Money, Zamtel, Visa, and Mastercard credit/debit cards with instant verification.'
  },
  {
    category: 'hosts',
    question: 'How do property owners get paid?',
    answer: '100% of guest payments are transferred directly to the host’s registered Mobile Money or Zambian Bank account (Zanaco, Stanbic, FNB, etc.) with 0% booking commission deducted.'
  },
  {
    category: 'hosts',
    question: 'How does walk-in POS inventory sync work?',
    answer: 'The host dashboard includes a Walk-in POS feature. When a walk-in guest arrives at reception, logging the booking instantly blocks out those calendar dates across online listings.'
  },
  {
    category: 'guests',
    question: 'What is the cancellation policy?',
    answer: 'Most executive stays on Apartex offer flexible cancellation up to 48 hours prior to check-in for a full refund.'
  }
];

const filteredFaqs = computed(() => {
  return faqs.filter(f => {
    const matchesCat = activeCategory.value === 'all' || f.category === activeCategory.value;
    const q = searchQuery.value.toLowerCase().trim();
    const matchesSearch = !q || f.question.toLowerCase().includes(q) || f.answer.toLowerCase().includes(q);
    return matchesCat && matchesSearch;
  });
});
</script>
