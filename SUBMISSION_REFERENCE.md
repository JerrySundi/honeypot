# 📋 SUBMISSION QUICK REFERENCE

## For GUVI Hackathon Submission

---

### 🔗 API Endpoint

```
POST https://[YOUR-DEPLOYED-URL]/api/honeypot
```

**Examples:**
- Render: `https://honeypot-scam-detector.onrender.com/api/honeypot`
- Railway: `https://honeypot-scam-detector.railway.app/api/honeypot`
- ngrok: `https://abc123.ngrok.io/api/honeypot`

---

### 🔐 Authentication

**Method:** HTTP Header Authentication

**Header Name:** `x-api-key`

**Header Value:** Your API Secret Key (from `.env` file)

**Default (change before deployment):** `sk_test_123456789`

**Example:**
```bash
-H "x-api-key: sk_test_123456789"
```

---

### 📤 Request Format

**Method:** POST

**Content-Type:** `application/json`

**Required Headers:**
- `x-api-key: YOUR_API_KEY`
- `Content-Type: application/json`

**Request Body Schema:**
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Message text here",
    "timestamp": "2026-02-05T10:00:00Z"
  },
  "conversationHistory": [
    {
      "sender": "scammer|user",
      "text": "Previous message",
      "timestamp": "2026-02-05T09:59:00Z"
    }
  ],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

---

### 📥 Response Format

**Success Response (200 OK):**
```json
{
  "status": "success",
  "reply": "AI agent's response message"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "error",
  "message": "Invalid API key"
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Invalid request format",
  "errors": { ... }
}
```

---

### 🧪 Complete Test Command

Replace `YOUR-DEPLOYED-URL` and `YOUR_API_KEY`:

```bash
curl -X POST https://YOUR-DEPLOYED-URL/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "sessionId": "guvi-test-001",
    "message": {
      "sender": "scammer",
      "text": "URGENT! Your account blocked. Send ₹10000 to 9876543210@paytm. Call +91-9876543210 now!",
      "timestamp": "2026-02-05T10:00:00Z"
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English",
      "locale": "IN"
    }
  }'
```

---

### 🎯 What Happens

1. **Authentication:** API validates the `x-api-key` header
2. **Scam Detection:** System analyzes message for scam patterns
3. **Intelligence Extraction:** Extracts bank accounts, UPI IDs, phone numbers, links
4. **AI Response:** DeepSeek generates human-like vulnerable response
5. **Session Tracking:** Maintains conversation state
6. **Termination:** After 15-20 messages or sufficient intelligence gathered
7. **Callback:** Sends final report to GUVI endpoint

---

### 📊 Intelligence Extracted

The system automatically extracts:

- **Bank Account Numbers:** 10-16 digit patterns
- **UPI IDs:** format: `id@provider`
- **Phone Numbers:** +91, 0, or 10-digit patterns
- **Phishing Links:** http/https URLs
- **Suspicious Keywords:** urgent, blocked, verify, OTP, etc.

---

### 🔄 Callback to GUVI

After conversation ends (15-20 messages or enough intelligence), system automatically sends:

**Endpoint:** `https://hackathon.guvi.in/api/updateHoneyPotFinalResult`

**Payload:**
```json
{
  "sessionId": "unique-session-id",
  "scamDetected": true,
  "totalMessagesExchanged": 15,
  "extractedIntelligence": {
    "bankAccounts": ["1234567890123456"],
    "upiIds": ["scammer@paytm"],
    "phoneNumbers": ["+91-9876543210"],
    "phishingLinks": ["http://fake-bank.com"],
    "suspiciousKeywords": ["urgent", "blocked", "verify"]
  },
  "agentNotes": "Scam Type: THREAT_BASED_SCAM. Engaged for 15 messages..."
}
```

---

### ⚙️ Environment Variables Required

For deployment, set these in your hosting platform:

```bash
# Required
DEEPSEEK_API_KEY=sk_your_deepseek_api_key
API_SECRET_KEY=sk_your_secure_random_key
SECRET_KEY=django_secret_key_here

# Production Settings
DEBUG=False
ALLOWED_HOSTS=*

# GUVI Integration
GUVI_CALLBACK_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult

# Optional (Redis for production)
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

### 🚀 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Deployed to Render/Railway/PythonAnywhere
- [ ] Environment variables configured
- [ ] `DEBUG=False` in production
- [ ] Secure `API_SECRET_KEY` generated
- [ ] Test with wrong API key (should get 401)
- [ ] Test with correct API key (should get AI response)
- [ ] Check server logs for scam detection
- [ ] Verify GUVI callback URL configured

---

### 📞 Quick Links

- **Deployment Guide:** See `DEPLOYMENT_GUIDE.md`
- **Testing Guide:** See `API_TESTING.md`
- **Main README:** See `README.md`
- **Test Script:** Run `python test_scripts/test_conversation.py`

---

### 🎓 For GUVI Submission Form

**Project Name:** AI-Powered Honeypot Scam Detector

**API Endpoint URL:**
```
https://[YOUR-APP].onrender.com/api/honeypot
```

**Authentication Method:** HTTP Header (`x-api-key`)

**API Key:**
```
sk_[YOUR-SECURE-KEY]
```

**Sample Test Command:**
```bash
curl -X POST https://[YOUR-APP].onrender.com/api/honeypot \
  -H "x-api-key: sk_[YOUR-KEY]" \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"test","message":{"sender":"scammer","text":"Urgent! Account blocked. Send money to 9876@paytm","timestamp":"2026-02-05T10:00:00Z"},"conversationHistory":[]}'
```

**Technologies Used:**
- Python 3.11
- Django 4.2
- Django REST Framework
- DeepSeek AI (via OpenAI SDK)
- Redis (session management)

**Key Features:**
- Multi-layer scam detection
- AI-powered conversational agent
- Automated intelligence extraction
- Session state management
- Autonomous termination detection
- GUVI callback integration

---

**Ready for submission! 🎉**
