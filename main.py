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
# EXCEPTION HANDLER old
# ============================================================================
'''
@app.exception_handler(Exception)

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"}
    )'''

# ============================================================================
# EXCEPTION HANDLERS new
# ============================================================================

from fastapi.exceptions import HTTPException as FastAPIHTTPException

# Handle expected API errors (401, 422, etc.)
@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": str(exc.detail)
        }
    )

# Handle unexpected crashes (500)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        }
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
        print("🤖 Starting Gemini Inline Analysis")

        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not configured")

        model = genai.GenerativeModel("models/gemini-2.5-flash")

        prompt = f"""You are an expert voice detection system.

Analyze this MP3 audio and determine if it is AI_GENERATED or HUMAN.

The audio language is {language}.

Respond ONLY in valid JSON:

{{
  "status": "success",
  "language": "{language}",
  "classification": "HUMAN",
  "confidenceScore": 0.85,
  "explanation": "Natural pitch variation and breathing detected"
}}"""

        # 🔥 CRITICAL CHANGE: INLINE AUDIO (NO UPLOAD)
        with open(file_path, "rb") as f:
            audio_bytes = f.read()

        response = model.generate_content([
            prompt,
            {
                "mime_type": "audio/mp3",
                "data": audio_bytes
            }
        ])

        raw = response.text.strip().replace("```json", "").replace("```", "").strip()
        print(f"📄 Model response: {raw[:200]}")

        data = json.loads(raw)

        if data["classification"] not in {"AI_GENERATED", "HUMAN"}:
            raise ValueError("Invalid classification")

        confidence = float(data["confidenceScore"])
        if not (0.0 <= confidence <= 1.0):
            raise ValueError("Invalid confidence score")

        print(f"✅ Gemini success: {data['classification']} ({confidence})")
        print(f"{'='*60}\n")

        return data
    
    except Exception as e:
        print(f"❌ Gemini failed: {type(e).__name__}: {str(e)}")

        # Do NOT fake a classification — return an error
        raise HTTPException(
            status_code=500,
            detail="Audio analysis failed"
        )

            
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
        raise HTTPException(status_code=401, detail="Invalid API key or malformed request")
    
    if body.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=422, detail="Unsupported language")
    
    if body.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=422, detail="Invalid API key or malformed request")
    
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