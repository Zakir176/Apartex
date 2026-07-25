import sys
import os
from datetime import datetime
from fastapi.testclient import TestClient

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base

client = TestClient(app)

def test_enhanced_auth():
    print("=== Testing Enhanced Authentication ===")
    
    # Ensure database schema is initialized
    Base.metadata.create_all(bind=engine)
    
    unique_email = f"authtest_{int(datetime.now().timestamp())}@example.com"
    
    # 1. Register a test user
    register_data = {
        "email": unique_email,
        "password": "testpassword123",
        "full_name": "Auth Test User",
        "role": "owner"
    }
    
    print("1. Registering user...")
    register_response = client.post("/api/auth-enhanced/register", json=register_data)
    assert register_response.status_code == 200, f"Registration failed: {register_response.text}"
    
    user_data = register_response.json()
    user_id = user_data["id"]
    print("✅ Registration successful")
    
    # 2. Login
    print("\n2. Logging in...")
    login_data = {
        "email": unique_email,
        "password": "testpassword123"
    }
    
    login_response = client.post("/api/auth-enhanced/simple-login", json=login_data)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    
    tokens = login_response.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    print("✅ Login successful")
    print(f"   Access token: {access_token[:20]}...")
    print(f"   User ID: {tokens['user']['id']}")
    
    # 3. Test protected endpoint
    print("\n3. Testing protected endpoint...")
    headers = {"Authorization": f"Bearer {access_token}"}
    dashboard_response = client.get(
        f"/api/dashboard/owners/{user_id}/overview",
        headers=headers
    )
    assert dashboard_response.status_code == 200, f"Protected endpoint access failed: {dashboard_response.text}"
    dashboard_data = dashboard_response.json()
    print("✅ Protected endpoint access successful")
    print(f"   Total revenue: ${dashboard_data['revenue_summary']['total_revenue']}")
    
    # 4. Test token refresh
    print("\n4. Testing token refresh...")
    refresh_response = client.post(
        "/api/auth-enhanced/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200, f"Token refresh failed: {refresh_response.text}"
    new_tokens = refresh_response.json()
    print("✅ Token refresh successful")
    print(f"   New access token: {new_tokens['access_token'][:20]}...")

if __name__ == "__main__":
    test_enhanced_auth()