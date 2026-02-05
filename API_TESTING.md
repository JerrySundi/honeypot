# 🧪 API Testing Guide

## Quick Test Your Deployed API

### Step 1: Test Authentication (Should Fail)

This tests that the API key authentication is working:

```bash
curl -X POST https://YOUR-APP-URL.onrender.com/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: wrong_key" \
  -d '{}'
```

**Expected Response** (401 Unauthorized):
```json
{
  "status": "error",
  "message": "Invalid API key"
}
```

✅ If you get this response, authentication is working correctly!

---

### Step 2: Test Scam Detection (Should Succeed)

This tests the full scam detection and AI response:

```bash
curl -X POST https://YOUR-APP-URL.onrender.com/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_ACTUAL_API_KEY" \
  -d '{
    "sessionId": "test-session-001",
    "message": {
      "sender": "scammer",
      "text": "URGENT! Your bank account will be blocked today. Send ₹10000 to 9876543210@paytm to verify immediately!",
      "timestamp": "2026-02-05T10:00:00Z"
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English"
    }
  }'
```

**Expected Response** (200 OK):
```json
{
  "status": "success",
  "reply": "Oh my goodness! I'm so scared! What should I do? Should I really send money?"
}
```

✅ If you get a worried/compliant response, the AI agent is working!

---

### Step 3: Continue Conversation

Send a follow-up message to extract more intelligence:

```bash
curl -X POST https://YOUR-APP-URL.onrender.com/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_ACTUAL_API_KEY" \
  -d '{
    "sessionId": "test-session-001",
    "message": {
      "sender": "scammer",
      "text": "Yes! Send money now to UPI scammer@paytm or account 1234567890123456 at HDFC Bank. Call +91-9876543210 for help.",
      "timestamp": "2026-02-05T10:01:00Z"
    },
    "conversationHistory": [
      {
        "sender": "scammer",
        "text": "URGENT! Your bank account will be blocked today.",
        "timestamp": "2026-02-05T10:00:00Z"
      },
      {
        "sender": "user",
        "text": "Oh my goodness! I'm so scared! What should I do?",
        "timestamp": "2026-02-05T10:00:30Z"
      }
    ],
    "metadata": {
      "channel": "SMS",
      "language": "English"
    }
  }'
```

**Expected Response** (200 OK):
```json
{
  "status": "success",
  "reply": "I want to send the money right now! Should I use the UPI or the bank account number?"
}
```

✅ If you get this response, intelligence extraction is working!

---

## 🔍 Check Server Logs

In your deployment platform (Render/Railway), check the logs to see:

```
============================================================
📨 INCOMING MESSAGE - Session: test-session-001
   Sender: scammer
   Text: URGENT! Your bank account will be blocked today...
   History Length: 0
============================================================

🚨 SCAM DETECTED!
   Confidence: 0.95
   Category: THREAT_BASED_SCAM
   Reason: Threatening language (3 keywords); Urgent language detected; Financial request detected

🔍 NEW INTELLIGENCE EXTRACTED:
   upiIds: ['9876543210@paytm']
   suspiciousKeywords: ['urgent', 'blocked', 'verify', 'account', 'bank']

🤖 AGENT RESPONSE: Oh my goodness! I'm so scared! What should I do?

📊 SESSION STATS: test-session-001
   Messages: 1
   Scam Detected: True
   Confidence: 0.95
   Bank Accounts: 0
   UPI IDs: 1
   Phone Numbers: 0
   Links: 0
```

---

## 📋 For GUVI Submission

Replace placeholders with your actual values:

**API Endpoint:**
```
https://your-app-name.onrender.com/api/honeypot
```

**API Key (for x-api-key header):**
```
sk_YOUR_SECURE_API_KEY_HERE
```

**Test Command:**
```bash
curl -X POST https://your-app-name.onrender.com/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_YOUR_SECURE_API_KEY_HERE" \
  -d '{
    "sessionId": "guvi-evaluation-001",
    "message": {
      "sender": "scammer",
      "text": "Your account is locked! Click http://fake-bank.com and enter OTP to unlock. Call 9876543210 now!",
      "timestamp": "2026-02-05T10:00:00Z"
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English"
    }
  }'
```

---

## ✅ Success Criteria

Your API is working correctly if:

1. ❌ Wrong API key → Returns 401 Unauthorized
2. ✅ Valid API key + Scam message → Returns AI response
3. 📊 Server logs show scam detection and intelligence extraction
4. 📤 After ~15-20 messages, callback sent to GUVI endpoint

---

## 🐛 Troubleshooting

### "Invalid API key" with correct key

**Solution:** Check environment variables in your deployment platform match exactly

### "Connection refused" or timeout

**Solution:** Make sure your app is running and the URL is correct

### "Internal server error"

**Solution:** Check server logs for Python errors. Usually missing environment variables:
- DEEPSEEK_API_KEY
- API_SECRET_KEY
- SECRET_KEY

---

**Ready to test! 🚀**
