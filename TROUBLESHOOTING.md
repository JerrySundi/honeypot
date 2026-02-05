# Troubleshooting Guide

## Issue: Fallback Responses Being Used Instead of LLM

### Root Cause
The Gemini API is returning **429 RESOURCE_EXHAUSTED** errors because the API quota has been exceeded. This causes the system to fall back to rule-based responses instead of using the AI agent.

### Error Details
```
429 RESOURCE_EXHAUSTED
You exceeded your current quota, please check your plan and billing details.
Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests
```

### Solutions

#### Option 1: Wait for Quota Reset ⏰
The free tier quota typically resets daily. Wait 24 hours and try again.

#### Option 2: Try Alternative Models 🔄
Different Gemini models may have separate quotas. Set environment variable:
```bash
# In PowerShell
$env:GEMINI_MODEL="gemini-1.5-flash"
# Or
$env:GEMINI_MODEL="gemini-1.5-pro"
```

Or update `.env` file:
```
GEMINI_MODEL=gemini-1.5-flash
```

#### Option 3: Get New API Key 🔑
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new project
3. Generate a new API key
4. Update `.env` file with new key

#### Option 4: Upgrade to Paid Tier 💳
For production use, consider upgrading to a paid plan with higher quotas.

### Testing API Connection

#### Test if API key is loaded:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"
```

#### Test API call:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); from google import genai; client = genai.Client(api_key=os.getenv('GEMINI_API_KEY')); response = client.models.generate_content(model='gemini-1.5-flash', contents='Hello'); print(response.text)"
```

### Enhanced Error Logging
The system now provides detailed error messages when API calls fail:
- ✅ Success: "Gemini API call successful"
- ❌ Rate limit: "Rate limit exceeded - API quota exhausted"
- ❌ Auth error: "Invalid API key"
- 🔄 Fallback: "Trying fallback model..."

### Monitoring
Check the console output when running tests. You'll now see:
```
🔄 Calling Gemini API (gemini-2.0-flash)...
❌ ERROR generating AI response:
   Type: ClientError
   ⚠️  Rate limit exceeded - API quota exhausted for gemini-2.0-flash
   💡 Trying fallback model...
   🔄 Trying gemini-1.5-flash...
```

### Prevention
1. **Monitor Usage**: Check [Google AI Studio Quotas](https://ai.dev/rate-limit)
2. **Implement Caching**: Cache common responses to reduce API calls
3. **Rate Limiting**: Add delays between requests
4. **Upgrade Plan**: Use paid tier for production workloads

### Current Model Fallback Chain
1. `gemini-2.0-flash` (primary)
2. `gemini-2.0-flash-lite` (fallback 1)
3. `gemini-2.5-flash` (fallback 2)
4. `gemini-exp-1206` (fallback 3)
5. Rule-based responses (final fallback)

### Quota Status
**Current Status**: ❌ **ALL FREE TIER QUOTAS EXHAUSTED**

The API key has hit the free tier daily limit for:
- `generativelanguage.googleapis.com/generate_content_free_tier_requests` (limit: 0)
- Multiple models affected: gemini-2.0-flash, gemini-2.0-flash-lite, etc.

**Estimated Reset**: Quotas typically reset at midnight UTC (check [usage dashboard](https://ai.dev/rate-limit))

### Immediate Solutions

#### 1. Wait for Reset (Recommended for Testing) ⏰
- Free tier quotas reset daily
- Wait 24 hours from first request
- Check quota at: https://ai.dev/rate-limit

#### 2. Get a New API Key (Quick Fix) 🔑
If you need immediate access:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a NEW project (different from current one)
3. Generate API key for new project
4. Update `.env` file:
   ```
   GEMINI_API_KEY="your-new-api-key-here"
   ```
5. Restart Django server

#### 3. Upgrade to Paid Tier (Production) 💳
- Higher rate limits
- No daily quota restrictions
- Better for production use
- Visit: https://ai.google.dev/pricing
