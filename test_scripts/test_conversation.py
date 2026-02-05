#!/usr/bin/env python3
"""
Test script to simulate scam conversations locally
"""
import requests
import json
import time
from datetime import datetime
import uuid


# Configuration
API_URL = "http://localhost:8000/api/honeypot"
API_KEY = "sk_test_123456789"


def send_message(session_id, sender, text, conversation_history):
    """Send a message to the honeypot API"""
    
    payload = {
        "sessionId": session_id,
        "message": {
            "sender": sender,
            "text": text,
            "timestamp": datetime.now().isoformat() + "Z"
        },
        "conversationHistory": conversation_history,
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None


def run_test_conversation():
    """Run a test conversation simulating a scam"""
    
    session_id = str(uuid.uuid4())
    conversation_history = []
    
    print("=" * 80)
    print("🧪 STARTING TEST CONVERSATION")
    print(f"📝 Session ID: {session_id}")
    print("=" * 80)
    print()
    
    # Define scammer messages (simulating a typical bank fraud scam)
    scammer_messages = [
        "Your bank account will be blocked today due to suspicious activity!",
        "You need to verify your account immediately by sending ₹5000 to my account.",
        "Send the money to account number 9876543210 at HDFC Bank.",
        "Or you can use UPI. My UPI ID is scammer123@paytm",
        "Call me at +91-9876543210 if you have any issues with the transfer.",
        "Click this link to verify: http://fake-bank-verify.com/account",
        "Why are you delaying? Your account will be permanently closed!",
        "Send the OTP you receive to confirm the transaction.",
    ]
    
    for i, scammer_text in enumerate(scammer_messages):
        print(f"\n{'─' * 80}")
        print(f"💬 Turn {i + 1}")
        print(f"{'─' * 80}")
        
        # Scammer sends message
        print(f"\n🦹 SCAMMER: {scammer_text}")
        
        # Send to API
        response = send_message(session_id, "scammer", scammer_text, conversation_history)
        
        if not response:
            print("❌ Failed to get response, stopping conversation")
            break
        
        # Get agent reply
        if response.get('status') == 'success':
            agent_reply = response.get('reply', '')
            print(f"🤖 AGENT: {agent_reply}")
            
            # Update conversation history
            conversation_history.append({
                "sender": "scammer",
                "text": scammer_text,
                "timestamp": datetime.now().isoformat() + "Z"
            })
            
            conversation_history.append({
                "sender": "user",
                "text": agent_reply,
                "timestamp": datetime.now().isoformat() + "Z"
            })
            
        else:
            print(f"❌ Error: {response.get('message', 'Unknown error')}")
            break
        
        # Small delay between messages
        time.sleep(1)
    
    print("\n" + "=" * 80)
    print("✅ TEST CONVERSATION COMPLETED")
    print("=" * 80)
    print()
    print("💡 Check the server logs to see:")
    print("   - Scam detection results")
    print("   - Intelligence extracted")
    print("   - Session statistics")
    print("   - Final callback status")
    print()


def run_quick_test():
    """Run a quick 3-message test"""
    
    session_id = str(uuid.uuid4())
    conversation_history = []
    
    print("\n🧪 QUICK TEST - 3 Messages\n")
    
    messages = [
        "Your account has been blocked! Verify immediately.",
        "Send ₹1000 to 1234567890@paytm to unblock.",
        "Call +91-9999999999 for help."
    ]
    
    for msg in messages:
        print(f"SCAMMER: {msg}")
        response = send_message(session_id, "scammer", msg, conversation_history)
        
        if response and response.get('status') == 'success':
            reply = response.get('reply')
            print(f"AGENT: {reply}\n")
            
            conversation_history.append({
                "sender": "scammer",
                "text": msg,
                "timestamp": datetime.now().isoformat() + "Z"
            })
            conversation_history.append({
                "sender": "user",
                "text": reply,
                "timestamp": datetime.now().isoformat() + "Z"
            })
        
        time.sleep(0.5)


if __name__ == "__main__":
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║           HONEYPOT SCAM DETECTOR - TEST SCRIPT               ║
╚══════════════════════════════════════════════════════════════╝

Select test mode:
1. Full conversation test (8 messages)
2. Quick test (3 messages)
3. Exit

""")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        run_test_conversation()
    elif choice == "2":
        run_quick_test()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")
