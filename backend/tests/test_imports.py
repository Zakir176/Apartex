import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.core.security import hash_password, verify_password
    from app.models.user import User
    from app.database import Base, engine
    
    print("✅ All imports successful!")
    
    # Test password hashing and verification properly
    test_password = "test123"
    
    # Hash a password
    hashed = hash_password(test_password)
    print("✅ Hash function works! Hash:", hashed)
    
    # Verify the correct password
    correct_verification = verify_password(test_password, hashed)
    print("✅ Correct password verification:", correct_verification)
    
    # Verify a wrong password
    wrong_verification = verify_password("wrong_password", hashed)
    print("✅ Wrong password verification:", wrong_verification)
    
    print("✅ User model:", User)
    print("✅ Database setup:", Base, engine)
    
except ImportError as e:
    print("❌ Import failed:", e)
except Exception as e:
    print("❌ Test failed:", e)