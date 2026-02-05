# 🕵️ Honeypot Scam Detector

An AI-powered agentic honeypot system that detects scam messages and autonomously engages scammers to extract intelligence without revealing detection.

## 🎯 Features

- **Scam Detection**: Multi-layer detection using pattern matching and keyword analysis
- **AI Agent**: DeepSeek-powered conversational agent that pretends to be a vulnerable user
- **Intelligence Extraction**: Automatically extracts bank accounts, UPI IDs, phone numbers, and phishing links
- **Session Management**: Maintains conversation state across multiple turns
- **Automated Callback**: Sends final results to GUVI evaluation endpoint

## 📋 Prerequisites

- Python 3.8+
- DeepSeek API key
- pip (Python package manager)

## 🚀 Setup Instructions

### 1. Clone/Download the Project

```bash
cd honeypot-scam-detector
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Edit the `.env` file and add your DeepSeek API key:

```bash
# .env file
DEEPSEEK_API_KEY=your_actual_deepseek_api_key_here
API_SECRET_KEY=sk_test_123456789
DEBUG=True
```

**⚠️ IMPORTANT**: Replace `your_actual_deepseek_api_key_here` with your real DeepSeek API key!

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/honeypot`

## 🧪 Testing Locally

### Method 1: Using the Test Script (Recommended)

```bash
# Make the script executable (Linux/Mac)
chmod +x test_scripts/test_conversation.py

# Run the test script
python test_scripts/test_conversation.py
```

**Select test mode:**
- **Option 1**: Full conversation test (8 messages) - Simulates complete scam interaction
- **Option 2**: Quick test (3 messages) - Fast verification
- **Option 3**: Exit

### Method 2: Using cURL

```bash
# First message (start conversation)
curl -X POST http://localhost:8000/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_test_123456789" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "Your account will be blocked! Verify immediately.",
      "timestamp": "2026-01-31T10:00:00Z"
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English"
    }
  }'

# Second message (continue conversation)
curl -X POST http://localhost:8000/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: sk_test_123456789" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "Send ₹5000 to 9876543210@paytm to verify",
      "timestamp": "2026-01-31T10:01:00Z"
    },
    "conversationHistory": [
      {
        "sender": "scammer",
        "text": "Your account will be blocked! Verify immediately.",
        "timestamp": "2026-01-31T10:00:00Z"
      },
      {
        "sender": "user",
        "text": "Oh no! What should I do?",
        "timestamp": "2026-01-31T10:00:30Z"
      }
    ],
    "metadata": {
      "channel": "SMS",
      "language": "English"
    }
  }'
```

### Method 3: Using Postman

1. Import the requests from `test_scripts/sample_requests.json`
2. Set header: `x-api-key: sk_test_123456789`
3. Send POST requests to `http://localhost:8000/api/honeypot`

## 📊 Understanding the Output

### Console Logs

The server will display detailed logs:

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
   Reason: Threatening language (2 keywords); Urgent language detected

🔍 NEW INTELLIGENCE EXTRACTED:
   suspiciousKeywords: ['urgent', 'blocked', 'account']

🤖 AGENT RESPONSE: Oh my god! I'm so worried. What should I do?

📊 SESSION STATS: abc-123
   Messages: 3
   Scam Detected: True
   Confidence: 0.85
   Bank Accounts: 0
   UPI IDs: 1
   Phone Numbers: 1
   Links: 0
   💰 UPI: ['scammer@paytm']
   📞 Phones: ['+91-9876543210']
```

### API Response

```json
{
  "status": "success",
  "reply": "I want to send the money right now! What's your account number?"
}
```

### Final Callback (to GUVI)

When conversation ends, the system sends:

```json
{
  "sessionId": "abc-123",
  "scamDetected": true,
  "totalMessagesExchanged": 15,
  "extractedIntelligence": {
    "bankAccounts": ["1234567890123456"],
    "upiIds": ["scammer@paytm"],
    "phoneNumbers": ["+91-9876543210"],
    "phishingLinks": ["http://fake-bank.com"],
    "suspiciousKeywords": ["urgent", "blocked", "verify"]
  },
  "agentNotes": "Scam Type: THREAT_BASED_SCAM. Engaged for 15 messages. Extracted: 1 bank account(s), 1 UPI ID(s), 1 phone number(s), 1 phishing link(s). Tactics: urgent, blocked, verify, account, payment"
}
```

## 🔧 Configuration

### Termination Conditions

The conversation automatically ends when:
- **20 messages** exchanged
- **Significant intelligence** gathered (1+ bank accounts AND 1+ UPI IDs)
- **Multiple pieces** of intelligence (3+ items) after 10+ messages
- **No progress** after 15+ messages with no intelligence

### Adjusting Settings

Edit `honeypot_project/settings.py`:

```python
# Session settings
SESSION_TIMEOUT_MINUTES = 60
MAX_MESSAGES_PER_SESSION = 20
```

### Disabling GUVI Callback (for local testing)

In `.env`:
```bash
GUVI_CALLBACK_URL=
```

Or comment it out to prevent callback attempts during local testing.

## 📁 Project Structure

```
honeypot-scam-detector/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (API keys)
├── README.md                     # This file
│
├── honeypot_project/             # Django project settings
│   ├── settings.py               # Configuration
│   ├── urls.py                   # URL routing
│   └── wsgi.py                   # WSGI config
│
├── scam_detector/                # Main application
│   ├── views.py                  # API endpoint
│   ├── serializers.py            # Request/response validation
│   ├── urls.py                   # App URL routing
│   │
│   ├── services/                 # Core business logic
│   │   ├── scam_detector.py     # Scam detection engine
│   │   ├── intelligence_extractor.py  # Extract intel from messages
│   │   ├── ai_agent.py          # DeepSeek AI agent
│   │   └── session_manager.py   # Session state management
│   │
│   └── utils/                    # Helper functions
│       └── helpers.py            # Callback & validation utils
│
└── test_scripts/                 # Testing tools
    ├── test_conversation.py      # Automated test script
    └── sample_requests.json      # Sample API requests
```

## 🔍 How It Works

### 1. Scam Detection
- **Pattern Matching**: Checks for urgent language, threats, financial requests
- **Keyword Analysis**: Identifies scam indicators (blocked, verify, OTP, etc.)
- **Confidence Scoring**: Multi-factor scoring system (0.0 - 1.0)

### 2. AI Agent Engagement
- **Persona**: Pretends to be a 65-year-old, tech-naive person
- **Goals**: Extract bank accounts, UPI IDs, phone numbers, phishing links
- **Tactics**: Shows willingness to comply, asks clarifying questions
- **Natural Behavior**: Makes typos, shows emotion, asks for help

### 3. Intelligence Extraction
- **Real-time Extraction**: Analyzes every scammer message
- **Pattern Recognition**: Regex patterns for accounts, UPIs, phones, URLs
- **Accumulation**: Merges intelligence across conversation turns

### 4. Conversation Flow
```
Incoming Message
    ↓
Load/Create Session
    ↓
Extract Intelligence
    ↓
Detect Scam → Yes → AI Agent Response
    ↓            No ↘ Safe Response
Check Termination
    ↓
Save Session / Send Callback
```

## 🐛 Troubleshooting

### API Key Error
```
Error: Invalid API key
```
**Solution**: Check that `x-api-key` header matches `API_SECRET_KEY` in `.env`

### DeepSeek API Error
```
Error generating AI response
```
**Solution**: 
1. Verify your DeepSeek API key in `.env`
2. Check your API quota/credits
3. Ensure internet connection

### Import Errors
```
ModuleNotFoundError: No module named 'rest_framework'
```
**Solution**: 
```bash
pip install -r requirements.txt
```

### Port Already in Use
```
Error: That port is already in use
```
**Solution**: Use a different port:
```bash
python manage.py runserver 8001
```

## 📝 API Documentation

### Endpoint
```
POST /api/honeypot
```

### Headers
```
x-api-key: YOUR_API_KEY
Content-Type: application/json
```

### Request Body
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "sender": "scammer",
    "text": "Message text",
    "timestamp": "2026-01-31T10:00:00Z"
  },
  "conversationHistory": [
    {
      "sender": "scammer",
      "text": "Previous message",
      "timestamp": "2026-01-31T09:59:00Z"
    }
  ],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

### Response
```json
{
  "status": "success",
  "reply": "Agent's response message"
}
```

## 🚀 Deployment (for GUVI submission)

### Option 1: Deploy to Render/Railway
1. Push code to GitHub
2. Connect to Render/Railway
3. Add environment variables
4. Deploy

### Option 2: Use ngrok (Quick local deployment)
```bash
# Start Django server
python manage.py runserver

# In another terminal, start ngrok
ngrok http 8000
```

Use the ngrok URL (e.g., `https://abc123.ngrok.io/api/honeypot`) for GUVI testing.

## 📞 Support

For issues or questions:
1. Check the console logs for detailed error messages
2. Review the session statistics output
3. Test with the provided test script first
4. Verify your DeepSeek API key is valid

## 📄 License

This project is created for the GUVI Hackathon - AI for Fraud Detection & User Safety.

---

**Built with ❤️ using Django, DeepSeek AI, and Python**
