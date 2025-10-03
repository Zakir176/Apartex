<!-- src/views/TestView.vue -->
<template>
  <div class="test-view">
    <div class="container">
      <h1>Debug Test Page</h1>
      
      <div class="debug-section">
        <h2>Service Test</h2>
        <Button @click="testService" label="Test Apartment Service" />
        <div v-if="serviceResult">
          <h3>Service Response:</h3>
          <pre>{{ serviceResult }}</pre>
        </div>
      </div>

      <div class="debug-section">
        <h2>Manual Data Test</h2>
        <Button @click="loadManualData" label="Load Manual Data" />
        <div v-if="manualData.length > 0">
          <h3>Manual Data Loaded ({{ manualData.length }} apartments)</h3>
          <div v-for="apt in manualData" :key="apt.id" class="manual-apartment">
            <strong>{{ apt.title }}</strong> - {{ apt.location }} - ${{ apt.price_per_night }}
          </div>
        </div>
      </div>

      <div class="debug-section">
        <h2>Component Test</h2>
        <ApartmentList :apartments="testApartments" :loading="false" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import Button from 'primevue/button'
import ApartmentList from '@/components/apartments/ApartmentList.vue'
import apartmentService from '@/services/apartments'

export default {
  name: 'TestView',
  components: {
    Button,
    ApartmentList
  },
  setup() {
    const serviceResult = ref(null)
    const manualData = ref([])
    const testApartments = ref([
      {
        id: 99,
        title: "TEST Apartment",
        location: "Test City, TS",
        price_per_night: 100,
        max_guests: 2,
        bedrooms: 1,
        bathrooms: 1,
        rating: 4.5,
        review_count: 10,
        image_url: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400",
        is_featured: true
      }
    ])

    const testService = async () => {
      try {
        console.log('Testing service...')
        const response = await apartmentService.getFeatured()
        serviceResult.value = {
          success: true,
          data: response.data,
          dataLength: response.data.length
        }
        console.log('Service test result:', serviceResult.value)
      } catch (error) {
        serviceResult.value = {
          success: false,
          error: error.message
        }
        console.error('Service test failed:', error)
      }
    }

    const loadManualData = () => {
      manualData.value = [
        {
          id: 100,
          title: "Manual Apartment 1",
          location: "Manual City, MC",
          price_per_night: 150,
          max_guests: 4,
          bedrooms: 2,
          bathrooms: 1,
          rating: 4.8,
          review_count: 25,
          image_url: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400",
          is_featured: true
        },
        {
          id: 101,
          title: "Manual Apartment 2", 
          location: "Testville, TV",
          price_per_night: 180,
          max_guests: 6,
          bedrooms: 3,
          bathrooms: 2,
          rating: 4.9,
          review_count: 42,
          image_url: "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400",
          is_featured: true
        }
      ]
    }

    return {
      serviceResult,
      manualData,
      testApartments,
      testService,
      loadManualData
    }
  }
}
</script>

<style scoped>
.test-view {
  padding: 2rem;
}

.debug-section {
  margin: 2rem 0;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
}

.manual-apartment {
  padding: 0.5rem;
  margin: 0.5rem 0;
  background: #f7fafc;
  border-radius: 0.25rem;
}

pre {
  background: #f7fafc;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
}
</style>