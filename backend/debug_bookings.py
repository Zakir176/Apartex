import requests
import json

BASE_URL = "http://localhost:8000"

def debug_apartment_status():
    print("=== Debugging Apartment Status ===\n")
    
    # Check apartment details
    print("1. Checking apartment details...")
    apt_response = requests.get(f"{BASE_URL}/apartments/1")
    if apt_response.status_code == 200:
        apartment = apt_response.json()
        print(f"   Apartment: {apartment['title']}")
        print(f"   Available: {apartment.get('is_available', 'N/A')}")
    else:
        print(f"   Error: {apt_response.status_code}")
    
    # Check existing bookings
    print("\n2. Checking existing bookings...")
    bookings_response = requests.get(f"{BASE_URL}/bookings/")
    if bookings_response.status_code == 200:
        bookings = bookings_response.json()
        print(f"   Total bookings: {len(bookings)}")
        for booking in bookings:
            print(f"   - Booking {booking['id']}: Apt {booking['apartment_id']}, {booking['check_in']} to {booking['check_out']}")
    else:
        print(f"   Error: {bookings_response.status_code}")
    
    # Test availability for different dates
    print("\n3. Testing availability for different date ranges...")
    test_ranges = [
        ("2024-06-01", "2024-06-03"),
        ("2024-07-01", "2024-07-03"),
        ("2024-08-01", "2024-08-03")
    ]
    
    for check_in, check_out in test_ranges:
        availability_response = requests.get(
            f"{BASE_URL}/bookings/apartment/1/availability",
            params={"check_in": check_in, "check_out": check_out}
        )
        if availability_response.status_code == 200:
            availability = availability_response.json()
            print(f"   {check_in} to {check_out}: {availability['is_available']}")
        else:
            print(f"   {check_in} to {check_out}: Error {availability_response.status_code}")

if __name__ == "__main__":
    debug_apartment_status()