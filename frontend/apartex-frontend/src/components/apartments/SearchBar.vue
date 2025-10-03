<!-- src/components/apartments/SearchBar.vue -->
<template>
  <div class="search-bar">
    <div class="search-inputs">
      <div class="search-field">
        <label>Location</label>
        <InputText v-model="search.location" placeholder="Where are you going?" />
      </div>
      <div class="search-field">
        <label>Check-in</label>
        <Calendar v-model="search.checkIn" placeholder="Check-in date" />
      </div>
      <div class="search-field">
        <label>Check-out</label>
        <Calendar v-model="search.checkOut" placeholder="Check-out date" />
      </div>
      <div class="search-field">
        <label>Guests</label>
        <InputNumber v-model="search.guests" :min="1" :max="10" />
      </div>
    </div>
    <Button label="Search" icon="pi pi-search" @click="handleSearch" />
  </div>
</template>

<script>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import InputText from 'primevue/inputtext'
import Calendar from 'primevue/calendar'
import InputNumber from 'primevue/inputnumber'
import Button from 'primevue/button'

export default {
  name: 'SearchBar',
  components: {
    InputText,
    Calendar,
    InputNumber,
    Button
  },
  setup() {
    const router = useRouter()
    
    const search = reactive({
      location: '',
      checkIn: null,
      checkOut: null,
      guests: 1
    })
    
    const handleSearch = () => {
      router.push({
        path: '/apartments',
        query: {
          location: search.location,
          checkIn: search.checkIn?.toISOString(),
          checkOut: search.checkOut?.toISOString(),
          guests: search.guests
        }
      })
    }
    
    return {
      search,
      handleSearch
    }
  }
}
</script>

<style scoped>
.search-bar {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 1rem;
  align-items: end;
  max-width: 800px;
  margin: 0 auto;
}

.search-inputs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  flex: 1;
}

.search-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #4a5568;
}
</style>