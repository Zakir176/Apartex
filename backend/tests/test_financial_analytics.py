import sys
import os
from datetime import datetime, date, timedelta
from fastapi.testclient import TestClient

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.database import SessionLocal, engine, Base
from app.models import User, Property, Booking
from app.core.security import create_access_token

client = TestClient(app)

def test_financial_analytics_and_csv_export():
    print("=== Testing Financial Analytics & CSV Export ===")
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        ts = int(datetime.now().timestamp())
        owner_email = f"fin_owner_{ts}@example.com"
        owner = User(
            email=owner_email,
            hashed_password="hashed_password",
            full_name="Financial Host",
            role="owner",
            is_active=True
        )
        db.add(owner)
        db.commit()
        db.refresh(owner)
        
        # Create test property
        prop = Property(
            title="Rhodes Park Financial Suite",
            description="High yield executive apartment",
            address="456 Independence Ave",
            city="Lusaka",
            price_per_night=200.00,
            capacity=4,
            bedrooms=2,
            bathrooms=2,
            owner_id=owner.id,
            property_type="apartment",
            is_available=True
        )
        db.add(prop)
        db.commit()
        db.refresh(prop)
        
        # Create completed booking for revenue calculation
        booking = Booking(
            property_id=prop.id,
            user_id=owner.id,
            check_in=date.today() - timedelta(days=10),
            check_out=date.today() - timedelta(days=8),
            guests=2,
            total_price=400.00,
            status="completed"
        )
        db.add(booking)
        db.commit()
        
        token = create_access_token({"sub": owner.email})
        headers = {"Authorization": f"Bearer {token}"}
        
        # 1. Test Overview Endpoint
        overview_res = client.get(f"/api/dashboard/owners/{owner.id}/overview", headers=headers)
        assert overview_res.status_code == 200, f"Overview failed: {overview_res.text}"
        
        data = overview_res.json()
        summary = data["revenue_summary"]
        assert "revpar" in summary, "RevPAR field must be present"
        assert summary["total_revenue"] >= 400.00
        print(f"✅ Revenue Overview successful. RevPAR: ${summary['revpar']}, Total: ${summary['total_revenue']}")
        
        # 2. Test CSV Export Endpoint
        csv_res = client.get(f"/api/dashboard/owners/{owner.id}/analytics/export-csv", headers=headers)
        assert csv_res.status_code == 200, f"CSV export failed: {csv_res.text}"
        assert csv_res.headers["content-type"].startswith("text/csv")
        assert "Booking ID" in csv_res.text
        assert "Rhodes Park Financial Suite" in csv_res.text
        print("✅ CSV Financial Report Export successful!")

    finally:
        db.close()

if __name__ == "__main__":
    test_financial_analytics_and_csv_export()
