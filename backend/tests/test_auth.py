import requests

def test_enhanced_auth():
    BASE_URL = "http://localhost:8000"
    
    print("=== Testing Enhanced Authentication ===\n")
    
    # 1. Register a test user
    register_data = {
        "email": "authtest@example.com",
        "password": "test123",
        "full_name": "Auth Test User",
        "role": "owner"
    }
    
    print("1. Registering user...")
    register_response = requests.post(f"{BASE_URL}/auth-enhanced/register", json=register_data)
    if register_response.status_code == 200:
        print("✅ Registration successful")
        user_id = register_response.json()["id"]
    else:
        print(f"❌ Registration failed: {register_response.json()}")
        return
    
    # 2. Login (using simple login for easier testing)
    print("\n2. Logging in...")
    login_data = {
        "email": "authtest@example.com",
        "password": "test123"
    }
    
    login_response = requests.post(
        f"{BASE_URL}/auth-enhanced/simple-login",
        json=login_data
    )
    
    if login_response.status_code == 200:
        tokens = login_response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        print("✅ Login successful")
        print(f"   Access token: {access_token[:20]}...")
        print(f"   User ID: {tokens['user']['id']}")
        print(f"   User role: {tokens['user']['role']}")
    else:
        print(f"❌ Login failed: {login_response.status_code} - {login_response.text}")
        return
    
    # 3. Test protected endpoint
    print("\n3. Testing protected endpoint...")
    headers = {"Authorization": f"Bearer {access_token}"}
    dashboard_response = requests.get(
        f"{BASE_URL}/dashboard/owners/{user_id}/overview",
        headers=headers
    )
    
    if dashboard_response.status_code == 200:
        print("✅ Protected endpoint access successful")
        dashboard_data = dashboard_response.json()
        print(f"   Revenue summary: ${dashboard_data['revenue_summary']['total_revenue']}")
    else:
        print(f"❌ Protected endpoint failed: {dashboard_response.status_code} - {dashboard_response.text}")
    
    # 4. Test token refresh (FIXED - using JSON body)
    print("\n4. Testing token refresh...")
    refresh_response = requests.post(
        f"{BASE_URL}/auth-enhanced/refresh",
        json={"refresh_token": refresh_token}  # Fixed - using JSON body
    )
    
    if refresh_response.status_code == 200:
        new_tokens = refresh_response.json()
        print("✅ Token refresh successful")
        print(f"   New access token: {new_tokens['access_token'][:20]}...")
    else:
        print(f"❌ Token refresh failed: {refresh_response.status_code} - {refresh_response.text}")

if __name__ == "__main__":
    test_enhanced_auth()