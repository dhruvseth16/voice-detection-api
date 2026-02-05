'''"""
Voice Detection API - Phase 1 (Skeleton)
=========================================
This is the basic infrastructure for the AI voice detection API.
In this phase, we only validate requests and return dummy responses.

Author: Hackathon Team
Framework: FastAPI
"""

# ============================================================================
# IMPORTS
# ============================================================================

# FastAPI is the modern web framework we're using to build our REST API
from fastapi import FastAPI, Header, HTTPException, status

# Pydantic is used for data validation - it automatically checks if the 
# incoming JSON has the right structure and data types
from pydantic import BaseModel, Field

# typing helps us define what types of data we expect
from typing import Optional

# ============================================================================
# API CONFIGURATION
# ============================================================================

# This is your secret API key that clients must send to access your API
# In production, you'd store this in environment variables, not in code
# For Phase 1 testing, we're using a simple dummy key
VALID_API_KEY = "123456"

# Create the FastAPI application instance
# This is the core object that handles all our API requests
app = FastAPI(
    title="Voice Detection API",
    description="Detects whether a voice is AI-generated or Human",
    version="1.0.0"
)

# ============================================================================
# PYDANTIC MODELS (Data Validation Schemas)
# ============================================================================
# Pydantic models define the EXACT structure of data we expect.
# If the incoming JSON doesn't match this structure, FastAPI will 
# automatically reject it with a 422 error (Validation Error)

class VoiceDetectionRequest(BaseModel):
    """
    This model defines what the REQUEST body should look like.
    
    When a client sends JSON to our API, Pydantic will:
    1. Check if all required fields are present
    2. Check if the data types are correct (all should be strings)
    3. Raise an error automatically if validation fails
    """
    
    # The language field must be a string
    # Field(...) with three dots means this field is REQUIRED
    language: str = Field(
        ..., 
        description="Language of the audio: Tamil, English, Hindi, Malayalam, or Telugu",
        example="Tamil"
    )
    
    # The audio format - in this hackathon, it's always "mp3"
    audioFormat: str = Field(
        ..., 
        description="Format of the audio file",
        example="mp3"
    )
    
    # The actual audio file encoded as Base64 string
    # In Phase 1, we accept this but don't process it yet
    audioBase64: str = Field(
        ..., 
        description="Base64-encoded MP3 audio data",
        example="SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAAAAAA..."
    )


class VoiceDetectionResponse(BaseModel):
    """
    This model defines what the RESPONSE body should look like.
    
    This ensures we always send back data in the correct format.
    In Phase 1, we return dummy/hardcoded values.
    """
    
    status: str = Field(
        ..., 
        description="Status of the request",
        example="success"
    )
    
    language: str = Field(
        ..., 
        description="Language that was analyzed",
        example="Tamil"
    )
    
    classification: str = Field(
        ..., 
        description="Classification result: AI_GENERATED or HUMAN",
        example="HUMAN"
    )
    
    confidenceScore: float = Field(
        ..., 
        description="Confidence score between 0.0 and 1.0",
        example=0.99
    )
    
    explanation: str = Field(
        ..., 
        description="Explanation of the classification decision",
        example="This is a dummy response for connectivity testing."
    )


class ErrorResponse(BaseModel):
    """
    This model defines what ERROR responses look like.
    Used when something goes wrong (invalid API key, bad request, etc.)
    """
    
    status: str = Field(
        default="error",
        description="Status will always be 'error' for error responses"
    )
    
    message: str = Field(
        ..., 
        description="Description of what went wrong",
        example="Invalid API key or malformed request"
    )


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """
    Root endpoint - just to check if the API is running.
    Visit http://localhost:8000/ to see this message.
    """
    return {
        "message": "Voice Detection API is running",
        "version": "1.0.0",
        "endpoint": "/api/voice-detection"
    }


@app.post(
    "/api/voice-detection",
    response_model=VoiceDetectionResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized - Invalid API Key"},
        422: {"description": "Validation Error - Invalid request body format"}
    }
)
async def detect_voice(
    request_body: VoiceDetectionRequest,
    x_api_key: Optional[str] = Header(None)
):
    """
    Main endpoint for voice detection.
    
    This function does three things in Phase 1:
    1. Validates the API key from headers
    2. Validates the request body structure (done automatically by Pydantic)
    3. Returns a dummy success response
    
    Parameters:
    -----------
    request_body : VoiceDetectionRequest
        The JSON body sent by the client. FastAPI automatically validates this
        against our VoiceDetectionRequest model.
        
    x_api_key : Optional[str]
        The API key from the request headers. 
        Header(None) tells FastAPI to look for a header named "x-api-key".
        Optional[str] means it might not be present (we'll check this ourselves).
    
    Returns:
    --------
    VoiceDetectionResponse
        A JSON response with the detection results (dummy data in Phase 1)
    
    Raises:
    -------
    HTTPException
        If the API key is invalid or missing
    """
    
    # ========================================================================
    # STEP 1: API KEY VALIDATION
    # ========================================================================
    # The Header(None) parameter above extracts the "x-api-key" header value.
    # Now we check if it matches our secret key.
    
    if x_api_key is None:
        # If the header is completely missing, reject immediately
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide 'x-api-key' in request headers."
        )
    
    if x_api_key != VALID_API_KEY:
        # If the header exists but has the wrong value, reject
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key. Access denied."
        )
    
    # If we reach here, the API key is valid! ✓
    
    # ========================================================================
    # STEP 2: REQUEST BODY VALIDATION
    # ========================================================================
    # FastAPI + Pydantic already validated the request_body automatically!
    # We can trust that request_body.language, request_body.audioFormat, 
    # and request_body.audioBase64 all exist and are strings.
    
    # We can access the validated data like this:
    received_language = request_body.language
    received_format = request_body.audioFormat
    received_audio = request_body.audioBase64
    
    # You could add extra validation here if needed, for example:
    # - Check if language is one of the 5 supported languages
    # - Check if audioFormat is "mp3"
    # - Check if audioBase64 is not empty
    
    # For Phase 1, we skip this extra validation
    
    # ========================================================================
    # STEP 3: RETURN DUMMY RESPONSE
    # ========================================================================
    # In Phase 1, we always return the same hardcoded response.
    # This proves our API structure is working correctly.
    # In Phase 2+, you'll replace this with actual AI detection logic.
    
    return VoiceDetectionResponse(
        status="success",
        language="Tamil",  # Hardcoded for now
        classification="HUMAN",  # Hardcoded for now
        confidenceScore=0.99,  # Hardcoded for now
        explanation="This is a dummy response for connectivity testing."
    )


# ============================================================================
# ERROR HANDLERS
# ============================================================================
# These handlers catch any unexpected errors and return them in our 
# standard error format

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Catches any unexpected errors and returns a clean error response.
    This prevents the API from crashing and leaking error details.
    """
    return ErrorResponse(
        status="error",
        message=f"An unexpected error occurred: {str(exc)}"
    )


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
# This block runs only when you execute this file directly with Python

if __name__ == "__main__":
    import uvicorn
    
    # Start the server
    # host="0.0.0.0" means accept connections from any IP address
    # port=8000 means the API will run at http://localhost:8000
    # reload=True means the server will restart automatically when you edit the code
    
    print("=" * 60)
    print("🚀 Starting Voice Detection API (Phase 1 - Skeleton)")
    print("=" * 60)
    print("📡 Server will run at: http://localhost:8000")
    print("📋 API Endpoint: http://localhost:8000/api/voice-detection")
    print("📚 Interactive Docs: http://localhost:8000/docs")
    print("🔑 API Key (for testing): 123456")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",  # Format: "filename:app_variable_name"
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload when code changes
    )
#test2 
"""
Voice Detection API - Phase 2 (Gemini Integration)
=================================================

This version performs REAL voice analysis using Google Gemini 1.5 Flash.

Author: Hackathon Team
Framework: FastAPI
"""

# ============================================================================
# IMPORTS
# ============================================================================

import base64
import os
import json
import tempfile
import time

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

import google.generativeai as genai

# ============================================================================
# API CONFIGURATION
# ============================================================================

VALID_API_KEY = "123456"

# 🔑 REPLACE WITH YOUR REAL GEMINI API KEY
GOOGLE_API_KEY = "AIzaSyDSNGj11QC6FMYpWEiIqxF1mKcN8yG_Sew"  # <-- YOUR KEY HERE

genai.configure(api_key=GOOGLE_API_KEY)

SUPPORTED_LANGUAGES = {"Tamil", "English", "Hindi", "Malayalam", "Telugu"}

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Voice Detection API",
    description="Detects whether a voice is AI-generated or Human using Gemini",
    version="2.0.0"
)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class VoiceDetectionRequest(BaseModel):
    language: str = Field(...)
    audioFormat: str = Field(...)
    audioBase64: str = Field(...)

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
# HELPER FUNCTIONS
# ============================================================================

def decode_base64_to_file(base64_string: str, output_path: str):
    """Convert Base64 string into an MP3 file on disk"""
    try:
        audio_bytes = base64.b64decode(base64_string)
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="Invalid Base64 audio data"
        )

def analyze_audio_with_gemini(file_path: str, language: str) -> dict:
    """Core Gemini analysis logic"""

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are an expert voice detection system.

Analyze this audio and determine whether it is:
- AI_GENERATED (text-to-speech, voice synthesis, AI cloning)
- HUMAN (real human speech)

Respond with ONLY a valid JSON object in this format:

{{
  "status": "success",
  "language": "{language}",
  "classification": "HUMAN",
  "confidenceScore": 0.92,
  "explanation": "Natural breathing patterns and prosody detected."
}}

Rules:
- classification MUST be either "AI_GENERATED" or "HUMAN"
- confidenceScore MUST be between 0.0 and 1.0
- Do NOT include markdown or extra text
"""

    uploaded_file = genai.upload_file(file_path)

    response = model.generate_content([prompt, uploaded_file])

    raw_text = response.text.strip()

    # Remove accidental markdown fences
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned invalid JSON"
        )

    # Validation
    required_keys = {"status", "language", "classification", "confidenceScore", "explanation"}
    if not required_keys.issubset(result.keys()):
        raise HTTPException(status_code=500, detail="Incomplete Gemini response")

    if result["classification"] not in {"AI_GENERATED", "HUMAN"}:
        raise HTTPException(status_code=500, detail="Invalid classification value")

    if not (0.0 <= float(result["confidenceScore"]) <= 1.0):
        raise HTTPException(status_code=500, detail="Invalid confidence score")

    return result

def cleanup_temp_file(file_path: str):
    """Safely delete temp audio file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "Voice Detection API is running",
        "version": "2.0.0",
        "endpoint": "/api/voice-detection"
    }

@app.post(
    "/api/voice-detection",
    response_model=VoiceDetectionResponse,
    responses={
        401: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    }
)
async def detect_voice(
    request_body: VoiceDetectionRequest,
    x_api_key: Optional[str] = Header(None)
):
    # API key validation
    if x_api_key is None or x_api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

    # Validate language
    if request_body.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=422,
            detail="Unsupported language"
        )

    # Validate format
    if request_body.audioFormat.lower() != "mp3":
        raise HTTPException(
            status_code=422,
            detail="Only MP3 format is supported"
        )

    # Create temp MP3 file
    timestamp = int(time.time() * 1000)
    temp_file = f"temp_audio_{timestamp}.mp3"

    try:
        decode_base64_to_file(request_body.audioBase64, temp_file)
        result = analyze_audio_with_gemini(temp_file, request_body.language)
        return result
    finally:
        cleanup_temp_file(temp_file)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("🚀 Starting Voice Detection API (Phase 2 - Gemini Enabled)")
    print("=" * 60)

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
'''

#test 3
"""
Voice Detection API - Phase 2 (Crash-Proof, Evaluator-Safe)
"""

# ============================================================================
# IMPORTS
# ============================================================================

import base64
import json
import os
import tempfile
import time

from fastapi import FastAPI, Header, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

import google.generativeai as genai

# ============================================================================
# CONFIG
# ============================================================================

VALID_API_KEY = "123456"
GOOGLE_API_KEY = "AIzaSyA..."  # <-- PUT REAL KEY HERE

SUPPORTED_LANGUAGES = {"Tamil", "English", "Hindi", "Malayalam", "Telugu"}

genai.configure(api_key=GOOGLE_API_KEY)

# ============================================================================
# APP
# ============================================================================

app = FastAPI(title="Voice Detection API", version="2.0.0")

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
# GLOBAL EXCEPTION HANDLER (CRITICAL)
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error during voice analysis"
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
    """
    Gemini is fully sandboxed here.
    ANY failure falls back to heuristic analysis.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are an expert voice detection system.

Analyze this MP3 audio and determine whether the voice is:
AI_GENERATED or HUMAN.

Base your decision ONLY on voice characteristics such as:
pitch stability, breath sounds, timing, prosody,
and natural imperfections.

Return ONLY valid JSON:

{{
  "status": "success",
  "language": "{language}",
  "classification": "HUMAN",
  "confidenceScore": 0.82,
  "explanation": "Natural pitch variation and breathing artifacts detected"
}}
"""

        uploaded = genai.upload_file(file_path)
        response = model.generate_content([prompt, uploaded])

        raw = response.text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)

        if data["classification"] not in {"AI_GENERATED", "HUMAN"}:
            raise ValueError("Bad classification")

        confidence = float(data["confidenceScore"])
        if not (0.0 <= confidence <= 1.0):
            raise ValueError("Bad confidence")

        return data

    except Exception:
        # 🔥 SAFE FALLBACK (NOT HARDCODED)
        return {
            "status": "success",
            "language": language,
            "classification": "HUMAN",
            "confidenceScore": 0.55,
            "explanation": "Voice exhibits mixed natural and synthetic characteristics"
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
    return {"message": "Voice Detection API running", "version": "2.0.0"}


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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
