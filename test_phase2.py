import base64
import requests
import sys

API_URL = "http://localhost:8000/api/voice-detection"
API_KEY = "123456"
AUDIO_FILE = "test_voice.mp3"
LANGUAGE = "English"

# -------------------------------
# Encode MP3 to Base64
# -------------------------------
try:
    with open(AUDIO_FILE, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")
except FileNotFoundError:
    print(f"❌ Audio file not found: {AUDIO_FILE}")
    sys.exit(1)

# -------------------------------
# Send API Request
# -------------------------------
response = requests.post(
    API_URL,
    headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    },
    json={
        "language": LANGUAGE,
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    },
    timeout=30
)

# -------------------------------
# Handle Response Safely
# -------------------------------
try:
    result = response.json()
except Exception:
    print("❌ Invalid JSON response from API")
    print(response.text)
    sys.exit(1)

if response.status_code != 200:
    print("❌ API Error")
    print(f"Status Code: {response.status_code}")
    print(f"Message: {result.get('message')}")
    sys.exit(1)

# -------------------------------
# Success Output
# -------------------------------
print("\n✅ Voice Detection Result")
print("-" * 40)
print(f"Language        : {result['language']}")
print(f"Classification  : {result['classification']}")
print(f"Confidence      : {result['confidenceScore']:.2%}")
print(f"Explanation     : {result['explanation']}")
print("-" * 40)
