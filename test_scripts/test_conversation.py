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
    
    # Advanced scammer messages with complex patterns and obfuscation
    scammer_messages = [
        # Turn 1: Urgent bank alert
        "URGENT ALERT! Your HDFC bank account has been temporarily suspended due to KYC pending. Update now!",
        
        # Turn 2: Multiple contact methods
        "Dear customer, call our helpline at 91-8765432109 or WhatsApp 7654321098 immediately to reactivate.",
        
        # Turn 3: Mixed payment options with obfuscated data
        "To verify, send ₹100 to UPI: verify2024@paytm or account no. 1234 5678 9012 3456 (HDFC Bank)",
        
        # Turn 4: Email and website phishing
        "Confirm your details at www . verifybank . com or email us at support@verifybank.in with your PAN details",
        
        # Turn 5: IFSC code and complex account details
        "Transfer funds to A/C: 50100123456789, IFSC: HDFC0001234, branch Koramangala. UPI also accepted: merchant2024@ybl",
        
        # Turn 6: Shortened URL and urgency
        "ACT NOW! Visit bit.ly/verify2024 to prevent account closure. Last 2 hours remaining!",
        
        # Turn 7: Multiple UPI formats
        "Payment methods: 9876543210@paytm OR wallet2024@phonepe OR 8765432109@gpay - choose any one!",
        
        # Turn 8: Obfuscated phone with alternate formats
        "Contact: +91 9876-543-210 or 08765432109 for instant activation. Don't delay!",
        
        # Turn 9: Credit card fraud attempt
        "Your credit card ending 1234 has unauthorized transaction. Share CVV to block: support 2024 @ gmail . com",
        
        # Turn 10: OTP phishing with multiple channels
        "We sent OTP to your mobile. Share it on WhatsApp +919876543210 or call 7654321098 to verify immediately",
        
        # Turn 11: Fake refund with account details
        "Congratulations! ₹5000 refund approved. Account: 60123456789012, IFSC: SBIN0012345. Share OTP to process.",
        
        # Turn 12: Prize scam with contact info
        "You WON ₹50,000! Claim at claimprize.online/winner2024 or contact winner@lottery-india.com, call 8765432109",
        
        # Turn 13: Mixed language and symbols
        "Aap ke account mein problem hai! Send money: 7654321098@paytm ya call karein +91-8765-432-109 turant!",
        
        # Turn 14: Government impersonation
        "Income Tax Department alert! Pay pending tax ₹10,000 to govt-payment@paytm or visit incometax-refund.tk",
        
        # Turn 15: Final pressure with all details
        "LAST WARNING! Send to: A/C 70200123456789, IFSC ICIC0001234, UPI: final2024@okicici, OR call 9876543210 NOW!"
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
    """Run a quick 5-message test with challenging patterns"""
    
    session_id = str(uuid.uuid4())
    conversation_history = []
    
    print("\n🧪 QUICK TEST - 5 Advanced Messages\n")
    
    messages = [
        "URGENT! Your ICICI account suspended. Contact 9876543210 immediately!",
        "Verify at secure-bank . com or UPI: verify@paytm with ₹100",
        "Account details: 50100234567890, IFSC: ICIC0001234 needed",
        "Email proof to support@bank-verify.in or call 08765432109",
        "Last chance! Visit bit.ly/verify or WhatsApp 7654321098 NOW!"
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
    
    print("✅ Quick test completed!")


def run_full_test():
    """Run the full 15-message advanced test"""
    return run_test_conversation()


if __name__ == "__main__":
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║      HONEYPOT SCAM DETECTOR - ADVANCED TEST SUITE           ║
╚══════════════════════════════════════════════════════════════╝

Select test mode:
1. Full Test (15 advanced messages) - Complete scam simulation
2. Quick Test (5 messages) - Fast verification  
3. Exit

Tests include detection of:
  ✓ UPI IDs (multiple formats & providers)
  ✓ Bank account numbers & IFSC codes
  ✓ Phone numbers (various formats)
  ✓ Email addresses
  ✓ Phishing URLs (including obfuscated & shortened)
  ✓ Suspicious keywords

""")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        run_full_test()
    elif choice == "2":
        run_quick_test()
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

