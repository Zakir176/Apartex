<!-- src/views/TestView.vue -->
<template>
  <div style="padding: 2rem;">
    <h1>Simple Test</h1>
    
    <!-- Test 1: Direct data in template -->
    <div style="background: #4caf50; color: white; padding: 1rem; margin: 1rem 0;">
      <h3>Test 1: Hardcoded Data</h3>
      <div v-for="apt in hardcodedApartments" :key="apt.id" style="background: white; color: black; padding: 0.5rem; margin: 0.5rem 0;">
        {{ apt.title }} - {{ apt.location }}
      </div>
    </div>

    <!-- Test 2: Data from ref -->
    <div style="background: #2196f3; color: white; padding: 1rem; margin: 1rem 0;">
      <h3>Test 2: Ref Data</h3>
      <div v-if="refApartments.length > 0">
        <div v-for="apt in refApartments" :key="apt.id" style="background: white; color: black; padding: 0.5rem; margin: 0.5rem 0;">
          {{ apt.title }} - {{ apt.location }}
        </div>
      </div>
      <div v-else style="background: red; color: white; padding: 1rem;">
        NO DATA IN refApartments!
      </div>
    </div>

    <!-- Test 3: ApartmentList component -->
    <div style="background: #ff9800; color: white; padding: 1rem; margin: 1rem 0;">
      <h3>Test 3: ApartmentList Component</h3>
      <ApartmentList :apartments="refApartments" :loading="false" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import ApartmentList from '@/components/apartments/ApartmentList.vue'

export default {
  name: 'TestView',
  components: {
    ApartmentList
  },
  setup() {
    // Test 1: Hardcoded in template
    const hardcodedApartments = [
      { id: 1, title: "Hardcoded Apt 1", location: "Test City", price_per_night: 100 },
      { id: 2, title: "Hardcoded Apt 2", location: "Test Town", price_per_night: 150 }
    ]

    // Test 2: Data in ref
    const refApartments = ref([
      { id: 3, title: "Ref Apt 1", location: "Ref City", price_per_night: 100, max_guests: 2, bedrooms: 1, bathrooms: 1, rating: 4.5, review_count: 10 },
      { id: 4, title: "Ref Apt 2", location: "Ref Town", price_per_night: 150, max_guests: 4, bedrooms: 2, bathrooms: 1, rating: 4.8, review_count: 25 }
    ])

    onMounted(() => {
      console.log('🔍 TestView mounted')
      console.log('refApartments:', refApartments.value)
    })

    return {
      hardcodedApartments,
      refApartments
    }
  }
}
</script>