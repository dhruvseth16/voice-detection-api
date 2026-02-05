"""
API Test Script for Voice Detection API
========================================
This script tests your API to make sure everything works correctly.

Run this AFTER starting your server with: python main.py

Usage: python test_api.py
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "123456"

def print_header(text):
    """Print a nice header for each test"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_response(response):
    """Print the response in a nice format"""
    print(f"Status Code: {response.status_code}")
    print(f"Response Body:")
    print(json.dumps(response.json(), indent=2))

def test_root():
    """Test 1: Check if API is running"""
    print_header("TEST 1: Check if API is Running")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response)
        
        if response.status_code == 200:
            print("✅ PASS: API is running!")
        else:
            print("❌ FAIL: API returned unexpected status code")
    except Exception as e:
        print(f"❌ FAIL: Could not connect to API. Error: {e}")
        print("Make sure the server is running with: python main.py")

def test_no_api_key():
    """Test 2: Request without API key (should fail)"""
    print_header("TEST 2: Request WITHOUT API Key (Should Fail)")
    
    payload = {
        "language": "Tamil",
        "audioFormat": "mp3",
        "audioBase64": "SUQzBAAAAAAAI1RTU0U="
    }
    
    headers = {
        "Content-Type": "application/json"
        # Intentionally NOT including x-api-key header
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/voice-detection",
            headers=headers,
            json=payload
        )
        print_response(response)
        
        if response.status_code == 401:
            print("✅ PASS: API correctly rejected request without API key")
        else:
            print("❌ FAIL: API should return 401 for missing API key")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_wrong_api_key():
    """Test 3: Request with wrong API key (should fail)"""
    print_header("TEST 3: Request with WRONG API Key (Should Fail)")
    
    payload = {
        "language": "Tamil",
        "audioFormat": "mp3",
        "audioBase64": "SUQzBAAAAAAAI1RTU0U="
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "wrong_key_123"  # Wrong API key
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/voice-detection",
            headers=headers,
            json=payload
        )
        print_response(response)
        
        if response.status_code == 401:
            print("✅ PASS: API correctly rejected request with wrong API key")
        else:
            print("❌ FAIL: API should return 401 for wrong API key")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_missing_fields():
    """Test 4: Request with missing required fields (should fail)"""
    print_header("TEST 4: Request with Missing Fields (Should Fail)")
    
    payload = {
        "language": "Tamil"
        # Missing audioFormat and audioBase64
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/voice-detection",
            headers=headers,
            json=payload
        )
        print_response(response)
        
        if response.status_code == 422:
            print("✅ PASS: API correctly rejected request with missing fields")
        else:
            print("❌ FAIL: API should return 422 for missing fields")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_valid_request():
    """Test 5: Valid request with correct API key (should succeed)"""
    print_header("TEST 5: Valid Request with Correct API Key (Should Succeed)")
    
    payload = {
        "language": "Tamil",
        "audioFormat": "mp3",
        "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAAAAAA"
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/voice-detection",
            headers=headers,
            json=payload
        )
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify response structure
            required_fields = ["status", "language", "classification", 
                             "confidenceScore", "explanation"]
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                print(f"❌ FAIL: Response missing fields: {missing_fields}")
            elif data["status"] == "success":
                print("✅ PASS: Valid request succeeded with correct response structure")
            else:
                print("❌ FAIL: Status should be 'success'")
        else:
            print(f"❌ FAIL: Expected status 200, got {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_all_languages():
    """Test 6: Test all supported languages"""
    print_header("TEST 6: Test All Supported Languages")
    
    languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    print("Testing with different languages:")
    for lang in languages:
        payload = {
            "language": lang,
            "audioFormat": "mp3",
            "audioBase64": "SUQzBAAAAAAAI1RTU0U="
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/voice-detection",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                print(f"  ✅ {lang}: Success")
            else:
                print(f"  ❌ {lang}: Failed (status {response.status_code})")
        except Exception as e:
            print(f"  ❌ {lang}: Error - {e}")

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  🧪 VOICE DETECTION API TEST SUITE")
    print("=" * 70)
    print(f"\nTesting API at: {BASE_URL}")
    print(f"Using API Key: {API_KEY}")
    
    # Run all tests
    test_root()
    test_no_api_key()
    test_wrong_api_key()
    test_missing_fields()
    test_valid_request()
    test_all_languages()
    
    # Summary
    print("\n" + "=" * 70)
    print("  ✅ TEST SUITE COMPLETED")
    print("=" * 70)
    print("\nIf all tests passed, your Phase 1 API is working correctly!")
    print("You can now proceed to Phase 2 to add actual voice detection logic.")
    print("\n")

if __name__ == "__main__":
    # Check if requests library is installed
    try:
        import requests
    except ImportError:
        print("❌ ERROR: 'requests' library not installed")
        print("Install it with: pip install requests")
        exit(1)
    
    main()
