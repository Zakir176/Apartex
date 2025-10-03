import sqlite3
from datetime import date

def debug_apartment():
    conn = sqlite3.connect('apartex.db')
    cursor = conn.cursor()
    
    print("=== Debugging Apartment 1 ===\n")
    
    # Check apartment details
    cursor.execute("SELECT * FROM apartments WHERE id = 1")
    apartment = cursor.fetchone()
    if apartment:
        print(f"Apartment 1: {apartment}")
        print(f"ID: {apartment[0]}")
        print(f"Title: {apartment[1]}")
        print(f"is_available: {apartment[10]}")  # Adjust index based on your table structure
    else:
        print("Apartment 1 not found!")
    
    # Check bookings for apartment 1
    cursor.execute("SELECT * FROM bookings WHERE apartment_id = 1")
    bookings = cursor.fetchall()
    print(f"\nBookings for apartment 1: {len(bookings)}")
    for booking in bookings:
        print(f"  Booking: {booking}")
    
    # Check if there are any bookings at all
    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]
    print(f"\nTotal bookings in database: {total_bookings}")
    
    conn.close()

if __name__ == "__main__":
    debug_apartment()