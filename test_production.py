"""
Production API Test Script
===========================
Test your deployed Render API with real audio files.

Usage:
1. Update PRODUCTION_URL with your Render URL
2. Run: python test_production.py test_voice.mp3
"""

import sys
import base64
import requests
import json

# ============================================================================
# CONFIGURATION - UPDATE THESE!
# ============================================================================

# Your Render URL (update this after deployment)
PRODUCTION_URL = "https://voice-detection-api-992e.onrender.com/api/voice-detection"

# API Key
API_KEY = "123456"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def test_health_check():
    """Test if the API is running"""
    print("\n" + "="*70)
    print("🏥 HEALTH CHECK TEST")
    print("="*70)
    
    base_url = PRODUCTION_URL.replace("/api/voice-detection", "")
    
    try:
        response = requests.get(base_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API is running")
            print(f"   Version: {data.get('version', 'unknown')}")
            print(f"   Status: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to API: {e}")
        return False


def test_voice_detection(audio_file, language="English"):
    """Test voice detection with an audio file"""
    print("\n" + "="*70)
    print(f"🔍 VOICE DETECTION TEST")
    print("="*70)
    print(f"📁 File: {audio_file}")
    print(f"🌐 Language: {language}")
    print(f"📡 URL: {PRODUCTION_URL}")
    
    # Step 1: Read and encode audio
    print(f"\n📝 Step 1: Reading audio file...")
    try:
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        print(f"✅ Audio encoded ({len(audio_base64)} characters, {len(audio_bytes)} bytes)")
    except FileNotFoundError:
        print(f"❌ Error: File not found: {audio_file}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Step 2: Prepare request
    print(f"\n📦 Step 2: Preparing API request...")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    payload = {
        "language": language,
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
    
    # Step 3: Send request
    print(f"\n🚀 Step 3: Sending request to production API...")
    print(f"⏱️  This may take 5-15 seconds...")
    
    try:
        response = requests.post(
            PRODUCTION_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Step 4: Handle response
        print(f"\n📨 Step 4: Response received")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n" + "="*70)
            print("✅ SUCCESS - ANALYSIS RESULTS")
            print("="*70)
            print(f"\n🔍 Classification: {result['classification']}")
            print(f"📊 Confidence: {result['confidenceScore']:.2f}")
            print(f"🌐 Language: {result['language']}")
            print(f"\n💬 Explanation:")
            print(f"   {result['explanation']}")
            print("\n" + "="*70)
            
            return True
            
        elif response.status_code == 401:
            print(f"\n❌ AUTHENTICATION ERROR")
            print(f"Your API key is invalid or missing.")
            print(f"Current key: {API_KEY}")
            
        elif response.status_code == 422:
            print(f"\n❌ VALIDATION ERROR")
            try:
                error = response.json()
                print(f"Message: {error.get('message', 'Unknown error')}")
            except:
                print(f"Response: {response.text}")
                
        else:
            print(f"\n❌ ERROR")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        
        return False
        
    except requests.exceptions.Timeout:
        print(f"\n❌ REQUEST TIMEOUT")
        print(f"The request took too long. Possible causes:")
        print(f"  - Service is sleeping (free tier - try again)")
        print(f"  - Audio file is too large")
        print(f"  - Network issues")
        return False
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ CONNECTION ERROR")
        print(f"Could not connect to: {PRODUCTION_URL}")
        print(f"Possible causes:")
        print(f"  - URL is incorrect")
        print(f"  - Service is not deployed")
        print(f"  - Network issues")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False


def test_all_languages(audio_file):
    """Test API with all supported languages"""
    print("\n" + "="*70)
    print("🌍 MULTI-LANGUAGE TEST")
    print("="*70)
    
    languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    results = []
    
    for lang in languages:
        print(f"\n🧪 Testing: {lang}")
        
        try:
            with open(audio_file, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode("utf-8")
            
            response = requests.post(
                PRODUCTION_URL,
                headers={"Content-Type": "application/json", "x-api-key": API_KEY},
                json={
                    "language": lang,
                    "audioFormat": "mp3",
                    "audioBase64": audio_base64
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "language": lang,
                    "classification": result["classification"],
                    "confidence": result["confidenceScore"]
                })
                print(f"   ✅ {result['classification']} ({result['confidenceScore']:.2%})")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                results.append({"language": lang, "status": "failed"})
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}")
            results.append({"language": lang, "status": "error"})
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    for r in results:
        if "classification" in r:
            print(f"{r['language']:12} - {r['classification']:15} ({r['confidence']:.2%})")
        else:
            print(f"{r['language']:12} - {r['status']}")
    print("="*70)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function"""
    
    print("\n" + "="*70)
    print("🧪 PRODUCTION API TEST SUITE")
    print("="*70)
    print(f"📡 Target: {PRODUCTION_URL}")
    print(f"🔑 API Key: {API_KEY}")
    
    # Check URL is updated
    if "your-app-name" in PRODUCTION_URL:
        print("\n⚠️  WARNING: Please update PRODUCTION_URL in this script!")
        print("Replace 'your-app-name' with your actual Render app name.")
        return
    
    # Check arguments
    if len(sys.argv) < 2:
        print("\n📖 Usage:")
        print("  python test_production.py <audio_file.mp3> [language]")
        print("\nExamples:")
        print("  python test_production.py test_voice.mp3")
        print("  python test_production.py my_audio.mp3 Tamil")
        print("  python test_production.py test.mp3 --all-languages")
        print("\nSupported languages: Tamil, English, Hindi, Malayalam, Telugu")
        return
    
    audio_file = sys.argv[1]
    
    # Run tests
    health_ok = test_health_check()
    
    if not health_ok:
        print("\n⚠️  Health check failed. API may not be running.")
        print("Continue anyway? (y/n): ", end="")
        if input().lower() != 'y':
            return
    
    if len(sys.argv) > 2 and sys.argv[2] == "--all-languages":
        test_all_languages(audio_file)
    else:
        language = sys.argv[2] if len(sys.argv) > 2 else "English"
        test_voice_detection(audio_file, language)
    
    print("\n✅ Testing complete!")


if __name__ == "__main__":
    main()