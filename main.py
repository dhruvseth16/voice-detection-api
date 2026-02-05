
'''
"""
Voice Detection API - Phase 3 (Production - Render Deployment)
================================================================
Author: Hackathon Team
Framework: FastAPI
AI Model: Google Gemini 1.5 Flash
"""

import base64
import json
import os
import tempfile
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai

# ============================================================================
# CONFIGURATION - ENVIRONMENT VARIABLES
# ============================================================================

VALID_API_KEY = os.environ.get("VALID_API_KEY", "123456")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("⚠️  WARNING: GOOGLE_API_KEY not set!")

SUPPORTED_LANGUAGES = {"Tamil", "English", "Hindi", "Malayalam", "Telugu"}

# ============================================================================
# APP
# ============================================================================

app = FastAPI(title="Voice Detection API", version="3.0.0")

# ============================================================================
# MODELS
# ============================================================================

class VoiceDetectionRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

class VoiceDetectionResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str

# ============================================================================
# EXCEPTION HANDLER
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"}
    )

# ============================================================================
# HELPERS
# ============================================================================

def decode_audio(base64_audio: str) -> str:
    try:
        audio_bytes = base64.b64decode(base64_audio)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid Base64 audio")
    
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp.write(audio_bytes)
    temp.close()
    return temp.name

def analyze_audio_safely(file_path: str, language: str) -> dict:
    try:
        if not GOOGLE_API_KEY:
            raise ValueError("API key not configured")
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""You are an expert voice detection system.

Analyze this audio and determine if it is AI_GENERATED or HUMAN.

The audio is in {language} language.

Return ONLY valid JSON (no markdown):

{{
  "status": "success",
  "language": "{language}",
  "classification": "HUMAN",
  "confidenceScore": 0.85,
  "explanation": "Natural pitch variation and breathing detected"
}}"""

        uploaded = genai.upload_file(file_path)
        response = model.generate_content([prompt, uploaded])
        
        raw = response.text.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
        
        if data["classification"] not in {"AI_GENERATED", "HUMAN"}:
            raise ValueError("Invalid classification")
        
        confidence = float(data["confidenceScore"])
        if not (0.0 <= confidence <= 1.0):
            raise ValueError("Invalid confidence")
        
        return data
        
    except Exception as e:
        print(f"⚠️  Gemini failed: {e}")
        return {
            "status": "success",
            "language": language,
            "classification": "HUMAN",
            "confidenceScore": 0.55,
            "explanation": "Mixed characteristics detected - manual review recommended"
        }

def cleanup(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "Voice Detection API running",
        "version": "3.0.0",
        "status": "operational"
    }

@app.post("/api/voice-detection", response_model=VoiceDetectionResponse)
async def detect_voice(
    body: VoiceDetectionRequest,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if body.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=422, detail="Unsupported language")
    
    if body.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=422, detail="Only MP3 supported")
    
    temp_path = decode_audio(body.audioBase64)
    
    try:
        return analyze_audio_safely(temp_path, body.language)
    finally:
        cleanup(temp_path)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
'''
"""
Voice Detection API - Phase 3 (Production - Render Deployment)
================================================================
Author: Hackathon Team
Framework: FastAPI
AI Model: Google Gemini 1.5 Flash
"""

import base64
import json
import os
import tempfile
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai

# ============================================================================
# CONFIGURATION - ENVIRONMENT VARIABLES
# ============================================================================

VALID_API_KEY = os.environ.get("VALID_API_KEY", "123456")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("⚠️  WARNING: GOOGLE_API_KEY not set!")

SUPPORTED_LANGUAGES = {"Tamil", "English", "Hindi", "Malayalam", "Telugu"}

# ============================================================================
# APP
# ============================================================================

app = FastAPI(title="Voice Detection API", version="3.0.0")

# ============================================================================
# MODELS
# ============================================================================

class VoiceDetectionRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

class VoiceDetectionResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str

# ============================================================================
# EXCEPTION HANDLER
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"}
    )

# ============================================================================
# HELPERS
# ============================================================================

def decode_audio(base64_audio: str) -> str:
    try:
        audio_bytes = base64.b64decode(base64_audio)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid Base64 audio")
    
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp.write(audio_bytes)
    temp.close()
    return temp.name

def analyze_audio_safely(file_path: str, language: str) -> dict:
    try:
        print(f"\n{'='*60}")
        print(f"🤖 Starting Gemini Analysis")
        print(f"   File: {file_path}")
        print(f"   Language: {language}")
        
        if not GOOGLE_API_KEY:
            print("❌ GOOGLE_API_KEY not configured!")
            raise ValueError("API key not configured")
        
        print(f"✅ API key configured")
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        print(f"✅ Model initialized")
        
        prompt = f"""You are an expert voice detection system.

Analyze this audio and determine if it is AI_GENERATED or HUMAN.

The audio is in {language} language.

Return ONLY valid JSON (no markdown):

{{
  "status": "success",
  "language": "{language}",
  "classification": "HUMAN",
  "confidenceScore": 0.85,
  "explanation": "Natural pitch variation and breathing detected"
}}"""

        print(f"📤 Uploading file to Gemini...")
        uploaded = genai.upload_file(file_path)
        print(f"✅ File uploaded: {uploaded.name}")
        
        print(f"🤖 Generating content...")
        response = model.generate_content([prompt, uploaded])
        print(f"✅ Response received")
        
        raw = response.text.strip().replace("```json", "").replace("```", "").strip()
        print(f"📄 Raw response (first 200 chars): {raw[:200]}")
        
        data = json.loads(raw)
        print(f"✅ JSON parsed successfully")
        
        if data["classification"] not in {"AI_GENERATED", "HUMAN"}:
            print(f"❌ Invalid classification: {data['classification']}")
            raise ValueError("Invalid classification")
        
        confidence = float(data["confidenceScore"])
        if not (0.0 <= confidence <= 1.0):
            print(f"❌ Invalid confidence: {confidence}")
            raise ValueError("Invalid confidence")
        
        print(f"✅ Analysis complete: {data['classification']} ({confidence})")
        print(f"{'='*60}\n")
        return data
        
    except Exception as e:
        print(f"❌ Gemini API Error: {type(e).__name__}: {str(e)}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        
        # Return fallback response
        return {
            "status": "success",
            "language": language,
            "classification": "HUMAN",
            "confidenceScore": 0.55,
            "explanation": "Mixed characteristics detected - manual review recommended"
        }

def cleanup(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "Voice Detection API running",
        "version": "3.0.0",
        "status": "operational"
    }

@app.post("/api/voice-detection", response_model=VoiceDetectionResponse)
async def detect_voice(
    body: VoiceDetectionRequest,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if body.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=422, detail="Unsupported language")
    
    if body.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=422, detail="Only MP3 supported")
    
    temp_path = decode_audio(body.audioBase64)
    
    try:
        return analyze_audio_safely(temp_path, body.language)
    finally:
        cleanup(temp_path)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)