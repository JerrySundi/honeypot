# 🚀 Deployment Guide - Honeypot Scam Detector

## 📋 Overview

This guide explains how to deploy your honeypot application and provide the required credentials for submission.

---

## 🔐 API Authentication

### How It Works

The application uses **API Key authentication** via HTTP headers for security:

1. **API Endpoint**: `POST /api/honeypot`
2. **Authentication Header**: `x-api-key: YOUR_API_KEY`
3. **Content-Type**: `application/json`

### API Key Configuration

Your API key is stored in the `.env` file:

```bash
API_SECRET_KEY=sk_test_123456789
```

**⚠️ IMPORTANT FOR SUBMISSION:**
- When deploying to production, **change this to a secure random key**
- Use a key generator: `python -c "import secrets; print('sk_' + secrets.token_urlsafe(32))"`
- Never commit your production API key to Git

### Security Flow

```
1. Client Request → 2. Extract x-api-key Header → 3. Validate Against API_SECRET_KEY
                                                    ↓
4. Return 401 Unauthorized ← Validation Failed ← 
                                                    ↓
5. Process Request ← Validation Success ←
```

---

## 🌐 Deployment Options

### Option 1: Render.com (Recommended - Free Tier Available)

#### Step 1: Prepare for Deployment

1. Create `render.yaml` in your project root:

```yaml
services:
  - type: web
    name: honeypot-scam-detector
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py migrate
    startCommand: gunicorn honeypot_project.wsgi:application
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DEEPSEEK_API_KEY
        sync: false
      - key: API_SECRET_KEY
        sync: false
      - key: SECRET_KEY
        sync: false
      - key: DEBUG
        value: False
      - key: ALLOWED_HOSTS
        value: "*"
      - key: GUVI_CALLBACK_URL
        value: https://hackathon.guvi.in/api/updateHoneyPotFinalResult
```

2. Update `requirements.txt` to include gunicorn:

```txt
Django==4.2.7
djangorestframework==3.14.0
python-dotenv==1.0.0
requests==2.31.0
gunicorn==21.2.0
```

#### Step 2: Deploy to Render

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click **"New +" → "Web Service"**
4. Connect your GitHub repository
5. Render will auto-detect your `render.yaml`
6. Add environment variables in Render dashboard:
   - `DEEPSEEK_API_KEY` = your_deepseek_key
   - `API_SECRET_KEY` = sk_YOUR_SECURE_KEY_HERE
   - `SECRET_KEY` = django_secret_key
7. Click **"Create Web Service"**

#### Step 3: Get Your Endpoint URL

After deployment completes:
- Your API endpoint: `https://your-app-name.onrender.com/api/honeypot`
- Your API key: The value you set for `API_SECRET_KEY`

---

### Option 2: Railway.app (Recommended - $5 Free Credit)

#### Step 1: Prepare for Deployment

1. Create `Procfile` in your project root:

```
web: gunicorn honeypot_project.wsgi:application --bind 0.0.0.0:$PORT
```

2. Create `runtime.txt`:

```
python-3.11.0
```

#### Step 2: Deploy to Railway

1. Push your code to GitHub
2. Go to [Railway Dashboard](https://railway.app/)
3. Click **"New Project" → "Deploy from GitHub repo"**
4. Select your repository
5. Add environment variables:
   - `DEEPSEEK_API_KEY`
   - `API_SECRET_KEY`
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=*`
   - `GUVI_CALLBACK_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult`
6. Railway will auto-deploy

#### Step 3: Get Your Endpoint URL

- Your API endpoint: `https://your-app.railway.app/api/honeypot`
- Your API key: The value you set for `API_SECRET_KEY`

---

### Option 3: PythonAnywhere (Free Tier Available)

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Upload your project files
3. Configure WSGI settings
4. Set environment variables in `.env`
5. Restart the web app

---

### Option 4: ngrok (Quick Local Testing)

Perfect for **temporary testing** before full deployment:

```bash
# Terminal 1: Start Django server
python manage.py runserver

# Terminal 2: Start ngrok tunnel
ngrok http 8000
```

You'll get a public URL like: `https://abc123.ngrok.io`

**Your endpoint**: `https://abc123.ngrok.io/api/honeypot`

⚠️ **Note**: ngrok URLs change on every restart (unless you use paid version)

---

## 📤 Submission Information

### What to Submit to GUVI

When submitting your project, provide:

1. **API Endpoint URL**:
   ```
   https://your-deployed-app.onrender.com/api/honeypot
   ```

2. **API Key** (for authentication):
   ```
   sk_YOUR_SECURE_API_KEY_HERE
   ```

3. **Sample Request** (for testing):

```bash
curl -X POST https://your-deployed-app.onrender.com/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_YOUR_SECURE_API_KEY_HERE" \
  -d '{
    "sessionId": "test-session-001",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked! Send ₹10000 to verify.",
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

## 🧪 Testing Your Deployed API

### Test 1: Health Check (Wrong API Key)

```bash
curl -X POST https://your-app.onrender.com/api/honeypot \
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

### Test 2: Valid Request

```bash
curl -X POST https://your-app.onrender.com/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_YOUR_ACTUAL_KEY" \
  -d '{
    "sessionId": "test-001",
    "message": {
      "sender": "scammer",
      "text": "Urgent! Your account blocked. Call 9876543210",
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
  "reply": "Oh no! What should I do? I'm very worried!"
}
```

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change `API_SECRET_KEY` to a secure random value
- [ ] Change `SECRET_KEY` to a unique Django secret
- [ ] Set `DEBUG=False` in production
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Add HTTPS (most platforms provide this automatically)
- [ ] Never commit `.env` file to Git
- [ ] Keep your DeepSeek API key secure
- [ ] Rotate API keys if compromised

---

## 📊 Monitoring Your Deployment

### Check Logs

**Render**:
- Go to your service dashboard
- Click "Logs" tab
- Watch real-time logs

**Railway**:
- Go to your project
- Click "Deployments"
- View logs for each deployment

### Expected Log Output

```
============================================================
📨 INCOMING MESSAGE - Session: abc-123
   Sender: scammer
   Text: Your account will be blocked!
   History Length: 0
============================================================

🚨 SCAM DETECTED!
   Confidence: 0.85
   Category: THREAT_BASED_SCAM

🤖 AGENT RESPONSE: Oh my god! I'm so worried. What should I do?
```

---

## 🐛 Common Deployment Issues

### Issue 1: Application Error / 500 Error

**Cause**: Missing environment variables

**Solution**:
```bash
# Check all required env vars are set:
DEEPSEEK_API_KEY=sk_...
API_SECRET_KEY=sk_...
SECRET_KEY=django-...
DEBUG=False
ALLOWED_HOSTS=*
```

### Issue 2: "Invalid API key" on Valid Key

**Cause**: Mismatch between deployed env var and test key

**Solution**: Verify the exact API key in your deployment platform's environment variables

### Issue 3: CSRF Token Error

**Cause**: CSRF protection interfering with API

**Solution**: Already fixed! We added `@csrf_exempt` decorator to the view

### Issue 4: Database Migrations Error

**Cause**: SQLite database not initialized

**Solution**: Ensure build command includes:
```bash
python manage.py migrate
```

---

## 📋 Submission Template

Copy this template and fill in your details:

```
==============================================
GUVI HACKATHON SUBMISSION
Project: AI-Powered Honeypot Scam Detector
==============================================

API ENDPOINT:
https://your-app-name.onrender.com/api/honeypot

API KEY (x-api-key header):
sk_YOUR_SECURE_API_KEY_HERE

AUTHENTICATION METHOD:
HTTP Header: x-api-key

SAMPLE CURL REQUEST:
curl -X POST https://your-app-name.onrender.com/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_YOUR_SECURE_API_KEY_HERE" \
  -d '{
    "sessionId": "guvi-test-001",
    "message": {
      "sender": "scammer",
      "text": "URGENT! Your account blocked. Verify at http://fake-bank.com",
      "timestamp": "2026-02-05T10:00:00Z"
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English"
    }
  }'

DEPLOYMENT PLATFORM:
Render.com / Railway.app / PythonAnywhere

CALLBACK ENDPOINT CONFIGURED:
https://hackathon.guvi.in/api/updateHoneyPotFinalResult

==============================================
```

---

## 🎯 Quick Start Deployment (Render)

```bash
# 1. Install gunicorn
pip install gunicorn
pip freeze > requirements.txt

# 2. Create render.yaml (see above)

# 3. Push to GitHub
git add .
git commit -m "Prepare for deployment"
git push origin main

# 4. Deploy on Render
# - Connect GitHub repo
# - Add environment variables
# - Deploy!

# 5. Test your endpoint
curl -X POST https://your-app.onrender.com/api/honeypot \
  -H "x-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"test","message":{"sender":"scammer","text":"Test","timestamp":"2026-02-05T10:00:00Z"},"conversationHistory":[]}'
```

---

## 📞 Support

If you encounter issues:

1. Check deployment logs for errors
2. Verify all environment variables are set
3. Test locally first with `python manage.py runserver`
4. Use ngrok for quick testing before full deployment

---

**Good luck with your submission! 🚀**
