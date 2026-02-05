import requests
import json
from typing import Dict
from django.conf import settings


def send_final_callback(session_data: Dict) -> bool:
    """
    Send final results to GUVI evaluation endpoint
    
    Args:
        session_data: Complete session data
        
    Returns:
        Boolean indicating success
    """
    callback_url = settings.GUVI_CALLBACK_URL
    
    if not callback_url:
        print("⚠️  GUVI_CALLBACK_URL not configured, skipping callback")
        return False
    
    payload = {
        "sessionId": session_data["sessionId"],
        "scamDetected": session_data["scamDetected"],
        "totalMessagesExchanged": session_data["messageCount"],
        "extractedIntelligence": session_data["intelligence"],
        "agentNotes": generate_agent_notes(session_data)
    }
    
    # Print the complete JSON payload in formatted form
    print("\n" + "="*80)
    print("📤 FINAL CALLBACK TO GUVI ENDPOINT")
    print("="*80)
    print(f"🌐 URL: {callback_url}")
    print(f"\n📦 COMPLETE JSON PAYLOAD:")
    print("-"*80)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("-"*80 + "\n")
    
    try:
        response = requests.post(
            callback_url,
            json=payload,
            timeout=10
        )
        
        response.raise_for_status()
        print(f"✅ Callback successful! Status: {response.status_code}")
        if response.text:
            print(f"📥 Response from GUVI: {response.text}")
        print("="*80 + "\n")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Callback failed: {str(e)}")
        print("="*80 + "\n")
        return False


def generate_agent_notes(session_data: Dict) -> str:
    """Generate summary notes about the scammer interaction"""
    intelligence = session_data.get('intelligence', {})
    message_count = session_data.get('messageCount', 0)
    scam_category = session_data.get('scamCategory', 'UNKNOWN')
    
    notes_parts = []
    
    # Scam type
    notes_parts.append(f"Scam Type: {scam_category}")
    
    # Engagement summary
    notes_parts.append(f"Engaged for {message_count} messages")
    
    # Intelligence summary
    intel_summary = []
    if intelligence.get('bankAccounts'):
        intel_summary.append(f"{len(intelligence['bankAccounts'])} bank account(s)")
    if intelligence.get('upiIds'):
        intel_summary.append(f"{len(intelligence['upiIds'])} UPI ID(s)")
    if intelligence.get('phoneNumbers'):
        intel_summary.append(f"{len(intelligence['phoneNumbers'])} phone number(s)")
    if intelligence.get('phishingLinks'):
        intel_summary.append(f"{len(intelligence['phishingLinks'])} phishing link(s)")
    
    if intel_summary:
        notes_parts.append(f"Extracted: {', '.join(intel_summary)}")
    else:
        notes_parts.append("No critical intelligence extracted")
    
    # Tactics observed
    keywords = intelligence.get('suspiciousKeywords', [])
    if keywords:
        top_keywords = ', '.join(keywords[:5])
        notes_parts.append(f"Tactics: {top_keywords}")
    
    return ". ".join(notes_parts)


def validate_api_key(provided_key: str) -> bool:
    """Validate the API key from request header"""
    expected_key = settings.API_SECRET_KEY
    return provided_key == expected_key
