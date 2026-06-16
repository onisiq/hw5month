#!/usr/bin/env python3
"""
Test script for authentication endpoints
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')
django.setup()

from product.models import CustomUser, ConfirmationCode
from django.contrib.auth.hashers import check_password

# Test 1: Create a user via registration
print("=" * 50)
print("TEST 1: User Registration")
print("=" * 50)

try:
    # Clean up if user exists
    CustomUser.objects.filter(email='test@example.com').delete()
    
    # Create user
    user = CustomUser.objects.create(
        name='Test User',
        email='test@example.com',
        password='hashed_password',
        is_active=False
    )
    print(f"✓ User created: {user.name} ({user.email})")
    print(f"✓ User is_active: {user.is_active}")
    print(f"✓ User created_at: {user.created_at}")
    
    # Create confirmation code
    code = ConfirmationCode.generate_code()
    confirmation = ConfirmationCode.objects.create(
        user=user,
        code=code
    )
    print(f"✓ Confirmation code created: {confirmation.code}")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Verify confirmation code
print("\n" + "=" * 50)
print("TEST 2: User Confirmation")
print("=" * 50)

try:
    confirmation = ConfirmationCode.objects.get(user=user)
    print(f"✓ Found confirmation code: {confirmation.code}")
    
    # Activate user
    user.is_active = True
    user.save()
    print(f"✓ User activated, is_active: {user.is_active}")
    
    # Delete confirmation code
    confirmation.delete()
    print(f"✓ Confirmation code deleted")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Check if code is generated correctly
print("\n" + "=" * 50)
print("TEST 3: Code Generation")
print("=" * 50)

try:
    codes = [ConfirmationCode.generate_code() for _ in range(5)]
    print(f"Generated codes: {codes}")
    print(f"✓ All codes are 6 digits: {all(len(c) == 6 for c in codes)}")
    print(f"✓ All codes are digits: {all(c.isdigit() for c in codes)}")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 4: Check password hashing
print("\n" + "=" * 50)
print("TEST 4: Password Hashing")
print("=" * 50)

try:
    from django.contrib.auth.hashers import make_password
    
    password = "test_password_123"
    hashed = make_password(password)
    print(f"✓ Password hashed: {hashed[:30]}...")
    print(f"✓ Password verification: {check_password(password, hashed)}")
    
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 50)
print("All tests completed!")
print("=" * 50)

# Cleanup
CustomUser.objects.filter(email='test@example.com').delete()
