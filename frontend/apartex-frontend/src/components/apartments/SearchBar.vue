<!-- src/components/apartments/SearchBar.vue -->
<template>
  <div class="search-bar">
    <div class="search-inputs">
      <div class="search-field">
        <label>📍 Location</label>
        <InputText 
          v-model="search.location" 
          placeholder="Where are you going?"
          class="search-input"
        />
      </div>
      
      <div class="search-field">
        <label>📅 Check-in</label>
        <Calendar 
          v-model="search.checkIn" 
          placeholder="Check-in date"
          class="search-input"
          :minDate="minDate"
        />
      </div>
      
      <div class="search-field">
        <label>📅 Check-out</label>
        <Calendar 
          v-model="search.checkOut" 
          placeholder="Check-out date"
          class="search-input"
          :minDate="search.checkIn || minDate"
        />
      </div>
      
      <div class="search-field">
        <label>👥 Guests</label>
        <div class="guests-selector">
          <Button 
            icon="pi pi-minus" 
            @click="decrementGuests"
            :disabled="search.guests <= 1"
            class="guest-btn"
          />
          <span class="guest-count">{{ search.guests }}</span>
          <Button 
            icon="pi pi-plus" 
            @click="incrementGuests"
            :disabled="search.guests >= 10"
            class="guest-btn"
          />
        </div>
      </div>
    </div>
    
    <Button 
      label="Search" 
      icon="pi pi-search" 
      @click="handleSearch"
      class="search-button"
      :disabled="!search.location"
    />
  </div>
</template>

<script>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import InputText from 'primevue/inputtext'
import Calendar from 'primevue/calendar'
import Button from 'primevue/button'

export default {
  name: 'SearchBar',
  components: {
    InputText,
    Calendar,
    Button
  },
  setup() {
    const router = useRouter()
    const minDate = new Date()
    
    const search = reactive({
      location: '',
      checkIn: null,
      checkOut: null,
      guests: 2
    })
    
    const incrementGuests = () => {
      if (search.guests < 10) {
        search.guests++
      }
    }
    
    const decrementGuests = () => {
      if (search.guests > 1) {
        search.guests--
      }
    }
    
    const handleSearch = () => {
      if (!search.location) return
      
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
      minDate,
      incrementGuests,
      decrementGuests,
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
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 1.5rem;
  align-items: end;
  max-width: 1000px;
  margin: 0 auto;
}

.search-inputs {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.5rem;
  flex: 1;
}

.search-field label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2d3748;
  font-size: 0.875rem;
}

.search-input {
  width: 100%;
}

.guests-selector {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
}

.guest-count {
  font-weight: 600;
  color: #2d3748;
  min-width: 2rem;
  text-align: center;
}

.guest-btn {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  min-width: 140px;
  height: fit-content;
}

.search-button:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .search-bar {
    flex-direction: column;
    align-items: stretch;
    gap: 1.5rem;
  }
  
  .search-inputs {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .search-bar {
    padding: 1.5rem;
  }
  
  .search-inputs {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .search-button {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .search-bar {
    padding: 1rem;
    margin: 0 1rem;
  }
}
</style>