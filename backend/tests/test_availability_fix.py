import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

def test_fixed_availability():
    print("=== Testing Fixed Availability ===\n")
    
    # Use dates in the future
    future_date = date.today() + timedelta(days=30)
    check_in = future_date
    check_out = future_date + timedelta(days=2)
    
    print(f"Testing dates: {check_in} to {check_out}")
    
    # Test availability
    availability_response = requests.get(
        f"{BASE_URL}/bookings/apartment/1/availability",
        params={"check_in": str(check_in), "check_out": str(check_out)}
    )
    
    if availability_response.status_code == 200:
        availability = availability_response.json()
        print(f"✅ Availability check: {availability['is_available']}")
        
        if availability['is_available']:
            # Try to create booking
            booking_data = {
                "apartment_id": 1,
                "check_in": str(check_in),
                "check_out": str(check_out),
                "guests": 2
            }
            
            booking_response = requests.post(f"{BASE_URL}/bookings/", json=booking_data)
            if booking_response.status_code == 201:
                booking = booking_response.json()
                print(f"✅ Booking created! ID: {booking['id']}")
                return booking['id']
            else:
                print(f"❌ Booking failed: {booking_response.status_code} - {booking_response.json()}")
        else:
            print("❌ Apartment not available")
    else:
        print(f"❌ Availability check failed: {availability_response.status_code}")

if __name__ == "__main__":
    test_fixed_availability()