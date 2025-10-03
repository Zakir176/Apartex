// src/services/apartments.js
import api from './api'

export default {
  getFeatured() {
    // Mock data for now - replace with actual API call
    return Promise.resolve({
      data: [
        {
          id: 1,
          title: "Luxury Downtown Apartment",
          location: "New York, NY",
          price_per_night: 150,
          max_guests: 4,
          bedrooms: 2,
          rating: 4.8,
          review_count: 124,
          image_url: "/placeholder-apartment.jpg"
        },
        {
          id: 2,
          title: "Beachfront Condo",
          location: "Miami, FL",
          price_per_night: 200,
          max_guests: 6,
          bedrooms: 3,
          rating: 4.9,
          review_count: 89,
          image_url: "/placeholder-apartment.jpg"
        },
        {
          id: 3,
          title: "Mountain View Cabin",
          location: "Denver, CO",
          price_per_night: 120,
          max_guests: 4,
          bedrooms: 2,
          rating: 4.7,
          review_count: 67,
          image_url: "/placeholder-apartment.jpg"
        }
      ]
    })
  }
}