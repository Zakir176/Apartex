// src/utils/errorHandler.js
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    const message = error.response.data?.detail || error.response.data?.message || 'An error occurred'
    return message
  } else if (error.request) {
    // Request made but no response received
    return 'Network error. Please check your connection.'
  } else {
    // Something else happened
    return error.message || 'An unexpected error occurred'
  }
}

export const showErrorToast = (message) => {
  // You can integrate with a toast library here
  alert(message) // Temporary - replace with proper toast
}