// src/services/apartments.js
import api from './api'

// Enhanced mock data with all required properties
const mockApartments = [
  {
    id: 1,
    title: "Luxury Downtown Apartment",
    location: "New York, NY",
    price_per_night: 150,
    max_guests: 4,
    bedrooms: 2,
    bathrooms: 2,
    rating: 4.8,
    review_count: 124,
    image_url: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400",
    is_featured: true,
    description: "Beautiful apartment in the heart of downtown with amazing city views."
  },
  {
    id: 2,
    title: "Beachfront Condo",
    location: "Miami, FL", 
    price_per_night: 200,
    max_guests: 6,
    bedrooms: 3,
    bathrooms: 2,
    rating: 4.9,
    review_count: 89,
    image_url: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400",
    is_featured: true,
    description: "Stunning beachfront condo with private balcony and ocean views."
  },
  {
    id: 3,
    title: "Mountain View Cabin",
    location: "Denver, CO",
    price_per_night: 120,
    max_guests: 4,
    bedrooms: 2,
    bathrooms: 1,
    rating: 4.7,
    review_count: 67,
    image_url: "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400",
    is_featured: false,
    description: "Cozy cabin nestled in the mountains with breathtaking views."
  }
]

export default {
  getFeatured() {
    console.log('getFeatured called, returning mock data')
    // Simulate API delay
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ 
          data: mockApartments.filter(apt => apt.is_featured) 
        })
      }, 500)
    })
  },
  
  getAll() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ data: mockApartments })
      }, 500)
    })
  },
  
  getById(id) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const apartment = mockApartments.find(apt => apt.id === parseInt(id))
        resolve({ data: apartment })
      }, 300)
    })
  },
  
  searchApartments(filters) {
    return new Promise((resolve) => {
      setTimeout(() => {
        let results = [...mockApartments]
        
        if (filters.location) {
          results = results.filter(apt => 
            apt.location.toLowerCase().includes(filters.location.toLowerCase())
          )
        }
        
        if (filters.guests) {
          results = results.filter(apt => apt.max_guests >= filters.guests)
        }
        
        resolve({ data: results })
      }, 500)
    })
  }
}