# 🎯 QUICK START - Deploy in 10 Minutes

## Step-by-Step Deployment Guide

---

## 🚀 FASTEST METHOD: Render.com

### ⏱️ Total Time: 10 minutes

---

### STEP 1: Prepare Your Code (2 minutes)

```bash
# 1. Navigate to your project
cd j:\honeypot-scam-detector

# 2. Generate a secure API key
python -c "import secrets; print('sk_' + secrets.token_urlsafe(32))"
```

**Copy the output** - this is your secure API key!
Example: `sk_Xy7pLm9Kj4Qw3Rt8Zn2Bv6Hf1Cd5Gh0`

---

### STEP 2: Push to GitHub (3 minutes)

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Ready for deployment"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/honeypot-scam-detector.git
git branch -M main
git push -u origin main
```

---

### STEP 3: Deploy on Render (5 minutes)

1. **Go to Render:** https://dashboard.render.com/

2. **Sign up/Login** (use GitHub account for easy connection)

3. **Click "New +" → "Web Service"**

4. **Connect Your Repository:**
   - Click "Connect account" for GitHub
   - Select your `honeypot-scam-detector` repository
   - Click "Connect"

5. **Render Auto-Configuration:**
   - Render will detect your `render.yaml` file
   - Everything is pre-configured! ✅

6. **Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable"
   
   Add these 4 variables:
   
   ```
   Name: DEEPSEEK_API_KEY
   Value: sk-b586e61a3a1a4e3ab2cde7737711a249
   
   Name: API_SECRET_KEY
   Value: sk_Xy7pLm9Kj4Qw3Rt8Zn2Bv6Hf1Cd5Gh0  ← YOUR SECURE KEY
   
   Name: SECRET_KEY
   Value: django-insecure-change-this-to-something-random-123456
   
   Name: GUVI_CALLBACK_URL
   Value: https://hackathon.guvi.in/api/updateHoneyPotFinalResult
   ```

7. **Click "Create Web Service"**

8. **Wait for Deployment** (3-5 minutes)
   - Watch the build logs
   - ✅ When you see "Your service is live", you're done!

---

### STEP 4: Get Your API Details

**Your API Endpoint:**
```
https://honeypot-scam-detector.onrender.com/api/honeypot
```
*(Render will show you the exact URL)*

**Your API Key:**
```
sk_Xy7pLm9Kj4Qw3Rt8Zn2Bv6Hf1Cd5Gh0
```
*(The one you generated in Step 1)*

---

### STEP 5: Test Your API (1 minute)

Open PowerShell/Terminal and run:

```powershell
# Test with WRONG key (should fail)
curl -X POST https://honeypot-scam-detector.onrender.com/api/honeypot `
  -H "Content-Type: application/json" `
  -H "x-api-key: wrong_key" `
  -d '{}'
```

**Expected:** `{"status":"error","message":"Invalid API key"}` ✅

```powershell
# Test with CORRECT key (should work)
curl -X POST https://honeypot-scam-detector.onrender.com/api/honeypot `
  -H "Content-Type: application/json" `
  -H "x-api-key: sk_Xy7pLm9Kj4Qw3Rt8Zn2Bv6Hf1Cd5Gh0" `
  -d '{
    "sessionId": "test-001",
    "message": {
      "sender": "scammer",
      "text": "URGENT! Your account blocked. Send money to 9876543210@paytm now!",
      "timestamp": "2026-02-05T10:00:00Z"
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English"
    }
  }'
```

**Expected:** `{"status":"success","reply":"Oh no! What should I do?..."}` ✅

---

## 📋 COPY THIS FOR GUVI SUBMISSION

```
===============================================
HONEYPOT SCAM DETECTOR - SUBMISSION DETAILS
===============================================

API ENDPOINT URL:
https://honeypot-scam-detector.onrender.com/api/honeypot

AUTHENTICATION METHOD:
HTTP Header: x-api-key

API KEY:
sk_Xy7pLm9Kj4Qw3Rt8Zn2Bv6Hf1Cd5Gh0

TEST COMMAND (Windows PowerShell):
curl -X POST https://honeypot-scam-detector.onrender.com/api/honeypot `
  -H "Content-Type: application/json" `
  -H "x-api-key: sk_Xy7pLm9Kj4Qw3Rt8Zn2Bv6Hf1Cd5Gh0" `
  -d '{
    "sessionId": "guvi-test",
    "message": {
      "sender": "scammer",
      "text": "Urgent! Account blocked. Send ₹10000 to 9876@paytm",
      "timestamp": "2026-02-05T10:00:00Z"
    },
    "conversationHistory": []
  }'

FEATURES:
- AI-powered scam detection
- Autonomous honeypot agent (DeepSeek)
- Intelligence extraction (bank accounts, UPI, phone numbers)
- Session management
- Automatic GUVI callback integration

TECH STACK:
- Python 3.11
- Django 4.2
- Django REST Framework
- DeepSeek AI
- Deployed on Render.com

===============================================
```

---

## 🔍 Check Your Deployment

### View Logs in Render:

1. Go to your Render dashboard
2. Click on your service
3. Click "Logs" tab
4. Send a test request
5. You should see:

```
============================================================
📨 INCOMING MESSAGE - Session: test-001
   Sender: scammer
   Text: URGENT! Your account blocked...
============================================================

🚨 SCAM DETECTED!
   Confidence: 0.90
   Category: THREAT_BASED_SCAM

🔍 NEW INTELLIGENCE EXTRACTED:
   upiIds: ['9876543210@paytm']

🤖 AGENT RESPONSE: Oh no! What should I do?
```

✅ **If you see this, your API is working perfectly!**

---

## 🆘 TROUBLESHOOTING

### Problem: "Application failed to start"

**Solution:** Check environment variables in Render dashboard
- Verify all 4 variables are set
- No typos in variable names
- DEEPSEEK_API_KEY must start with `sk-`

### Problem: "Invalid API key" when testing

**Solution:** Copy the exact API key from your Render environment variables
- Check for extra spaces
- Must match exactly

### Problem: "DeepSeek API error"

**Solution:** 
1. Check your DeepSeek API key is valid
2. Verify you have API credits
3. Check DeepSeek service status

---

## ⚡ ALTERNATIVE: Quick Test with ngrok (No Deployment)

If you just want to test quickly without deploying:

```bash
# Terminal 1
python manage.py runserver

# Terminal 2  
ngrok http 8000
```

Use the ngrok URL (e.g., `https://abc123.ngrok.io/api/honeypot`)

⚠️ **Note:** ngrok URL changes every restart!

---

## 📚 Full Documentation

For more details, see:
- [`IMPLEMENTATION_EXPLAINED.md`](IMPLEMENTATION_EXPLAINED.md) - Complete explanation
- [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) - Detailed deployment options
- [`API_TESTING.md`](API_TESTING.md) - Testing guide
- [`SUBMISSION_REFERENCE.md`](SUBMISSION_REFERENCE.md) - Quick reference
- [`API_FLOW_DIAGRAM.md`](API_FLOW_DIAGRAM.md) - Visual diagrams

---

## ✅ CHECKLIST

Before submitting:

- [ ] Deployed to Render/Railway
- [ ] Generated secure API key
- [ ] Set all environment variables
- [ ] Tested with wrong API key (gets 401 error)
- [ ] Tested with correct API key (gets AI response)
- [ ] Checked logs show scam detection
- [ ] Copied API endpoint URL
- [ ] Copied API key
- [ ] Ready to submit to GUVI!

---

**You're ready to submit! 🎉**

**Time spent: 10 minutes**
**Result: Production-ready AI honeypot API**

**Good luck with your hackathon submission! 🚀**
