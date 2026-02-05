"""
Test Script: List Available Gemini Models
==========================================
Run this locally to see which models you can use.
"""

import google.generativeai as genai
import os

# Configure with your API key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyDSNGj11QC6FMYpWEiIqxF1mKcN8yG_Sew")
genai.configure(api_key=GOOGLE_API_KEY)

print("=" * 70)
print("Available Gemini Models:")
print("=" * 70)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"\n✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:100]}...")
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("\nTrying common model names manually:")
    
    # Test common model names
    test_models = [
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-1.5-flash-latest",
        "models/gemini-1.5-flash",
        "models/gemini-pro",
    ]
    
    for model_name in test_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'test'")
            print(f"✅ {model_name} - WORKS")
        except Exception as e:
            print(f"❌ {model_name} - {str(e)[:80]}")

print("\n" + "=" * 70)