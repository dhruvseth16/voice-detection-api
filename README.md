# Voice Detection API - Phase 1 Setup Guide

## 📋 What This Is

This is the **skeleton/infrastructure** for your AI voice detection API. It doesn't do actual voice detection yet—it just validates requests and returns dummy responses to prove the API structure works.

## 🚀 Quick Start Guide

### Step 1: Install Dependencies

Open your terminal in the folder containing `main.py` and run:

```bash
pip install -r requirements.txt
```

**What this does:** Installs FastAPI, Uvicorn, and Pydantic.

### Step 2: Start the Server

Run this command:

```bash
python main.py
```

**OR** you can also use:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**What this does:** Starts your API server at `http://localhost:8000`

You should see output like:
```
🚀 Starting Voice Detection API (Phase 1 - Skeleton)
📡 Server will run at: http://localhost:8000
📋 API Endpoint: http://localhost:8000/api/voice-detection
🔑 API Key (for testing): 123456
```

### Step 3: Test Your API

Keep the server running and open a **new terminal window**.

#### Test 1: Check if API is Running

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "message": "Voice Detection API is running",
  "version": "1.0.0",
  "endpoint": "/api/voice-detection"
}
```

#### Test 2: Test WITHOUT API Key (Should Fail)

```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -d '{
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": "SUQzBAAAAAAAI1RTU0U="
  }'
```

**Expected Response:** 401 Unauthorized error

#### Test 3: Test WITH WRONG API Key (Should Fail)

```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: wrong_key" \
  -d '{
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": "SUQzBAAAAAAAI1RTU0U="
  }'
```

**Expected Response:** 401 Unauthorized error

#### Test 4: Test WITH CORRECT API Key (Should Succeed) ✅

```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: 123456" \
  -d '{
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAAAAAA"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "HUMAN",
  "confidenceScore": 0.99,
  "explanation": "This is a dummy response for connectivity testing."
}
```

#### Test 5: Test with MISSING Fields (Should Fail)

```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: 123456" \
  -d '{
    "language": "Tamil"
  }'
```

**Expected Response:** 422 Validation Error (missing required fields)

## 🌐 Interactive Documentation

FastAPI automatically generates interactive API documentation!

Visit these URLs in your browser while the server is running:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

You can test your API directly from these pages without using curl!

## 📁 File Structure

```
your-project-folder/
├── main.py              # Your API code
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔑 API Key for Phase 1 Testing

- **API Key:** `123456`
- **Header Name:** `x-api-key`

⚠️ **Important:** In production, you'll use a real secret key stored in environment variables, not hardcoded in the code!

## 📝 Request Format

```json
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU2LjM2LjEwMAAAAAAA..."
}
```

## ✅ Response Format (Success)

```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "HUMAN",
  "confidenceScore": 0.99,
  "explanation": "This is a dummy response for connectivity testing."
}
```

## ❌ Response Format (Error)

```json
{
  "status": "error",
  "message": "Invalid API key or malformed request"
}
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"
**Solution:** Run `pip install -r requirements.txt`

### "Address already in use"
**Solution:** Another program is using port 8000. Either:
- Stop the other program, OR
- Change the port in `main.py` (line with `port=8000`)

### "Connection refused"
**Solution:** Make sure the server is running before testing

## 📦 What's Included in Phase 1

✅ FastAPI server setup  
✅ POST endpoint at `/api/voice-detection`  
✅ API key authentication via `x-api-key` header  
✅ Request validation using Pydantic models  
✅ Proper error handling (401, 422 errors)  
✅ Dummy success response  
✅ Interactive documentation  

## 🚧 What's NOT Included Yet (Future Phases)

❌ Actual AI voice detection logic  
❌ Audio file processing  
❌ Base64 decoding  
❌ Language-specific analysis  
❌ Real confidence score calculation  

## 🎯 Next Steps for Phase 2

Once Phase 1 is working, you'll:
1. Add audio processing libraries (librosa, pydub)
2. Decode Base64 audio
3. Extract audio features
4. Implement ML model for detection
5. Calculate real confidence scores
6. Add language-specific logic

## 💡 Tips

- The server auto-reloads when you save changes to `main.py`
- Use the `/docs` page to test without writing curl commands
- Read the comments in `main.py` to understand each part
- Keep the API key simple for Phase 1; you'll improve security later

## 📞 Support

If you encounter issues:
1. Check that Python 3.7+ is installed
2. Make sure all dependencies are installed
3. Read the error messages carefully
4. Check the terminal where the server is running for logs

Good luck with your hackathon! 🎉
