# debug_reward.py
import requests

BASE_URL = "http://localhost:8000"

def debug_reward():
    print("=== Debugging Reward Data ===\n")
    
    # Check available rewards
    rewards_response = requests.get(f"{BASE_URL}/loyalty/users/1/rewards")
    if rewards_response.status_code == 200:
        rewards = rewards_response.json()
        print(f"Available rewards: {len(rewards)}")
        for reward in rewards:
            print(f"  - Reward ID: {reward['id']}")
            print(f"    Type: {reward['reward_type']}")
            print(f"    Value: {reward.get('reward_value', 'N/A')}")
            print(f"    Status: {reward['status']}")
    
    # Check booking 4
    booking_response = requests.get(f"{BASE_URL}/bookings/5")
    if booking_response.status_code == 200:
        booking = booking_response.json()
        print(f"\nBooking 5 details:")
        print(f"  - Total Price: {booking['total_price']} (type: {type(booking['total_price'])})")
        print(f"  - Status: {booking['status']}")

if __name__ == "__main__":
    debug_reward()