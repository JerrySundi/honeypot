import json
from typing import Dict, Optional
from datetime import datetime


class SessionManager:
    """Manage conversation sessions with in-memory storage"""
    
    def __init__(self):
        # In-memory storage (sessions dict)
        # In production, use Redis or database
        self.sessions = {}
    
    def get_or_create_session(self, session_id: str) -> Dict:
        """
        Get existing session or create new one
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Session data dictionary
        """
        if session_id in self.sessions:
            return self.sessions[session_id]
        
        # Create new session
        new_session = self._create_new_session(session_id)
        self.sessions[session_id] = new_session
        return new_session
    
    def update_session(self, session_id: str, session_data: Dict):
        """
        Update session data
        
        Args:
            session_id: Session identifier
            session_data: Updated session data
        """
        session_data['lastUpdated'] = datetime.now().isoformat()
        self.sessions[session_id] = session_data
    
    def delete_session(self, session_id: str):
        """
        Delete a session (after final callback sent)
        
        Args:
            session_id: Session identifier
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            print(f"🗑️  Session {session_id} deleted")
    
    def _create_new_session(self, session_id: str) -> Dict:
        """Create a new session with default values"""
        return {
            "sessionId": session_id,
            "scamDetected": False,
            "scamConfidence": 0.0,
            "scamCategory": None,
            "messageCount": 0,
            "intelligence": {
                "bankAccounts": [],
                "upiIds": [],
                "phoneNumbers": [],
                "phishingLinks": [],
                "emailAddresses": [],
                "ifscCodes": [],
                "scammerName": [],
                "suspiciousKeywords": []
            },
            "agentPersona": {
                "emotionalState": "neutral",
                "trustLevel": 0,
                "conversationStage": "initial"
            },
            "terminationTriggered": False,
            "createdAt": datetime.now().isoformat(),
            "lastUpdated": datetime.now().isoformat()
        }
    
    def should_terminate(self, session_data: Dict) -> bool:
        """
        Determine if conversation should be terminated
        
        Args:
            session_data: Current session data
            
        Returns:
            Boolean indicating if conversation should end
        """
        intelligence = session_data.get('intelligence', {})
        message_count = session_data.get('messageCount', 0)
        
        # Condition 1: Message limit reached
        if message_count >= 20:
            print(f"🛑 Termination: Message limit reached ({message_count})")
            return True
        
        # Condition 2: Got significant intelligence
        bank_accounts = len(intelligence.get('bankAccounts', []))
        upi_ids = len(intelligence.get('upiIds', []))
        phone_numbers = len(intelligence.get('phoneNumbers', []))
        links = len(intelligence.get('phishingLinks', []))
        
        if bank_accounts >= 1 and upi_ids >= 1:
            print(f"🛑 Termination: Sufficient intelligence gathered")
            return True
        
        # Condition 3: Got multiple pieces of critical info
        critical_count = bank_accounts + upi_ids + phone_numbers + links
        if critical_count >= 3 and message_count >= 10:
            print(f"🛑 Termination: Multiple intelligence pieces gathered")
            return True
        
        # Condition 4: Very long conversation with minimal results
        if message_count >= 15 and critical_count == 0:
            print(f"🛑 Termination: No progress after many messages")
            return True
        
        return False
    
    def get_session_summary(self, session_data: Dict) -> str:
        """Generate a summary of the session"""
        intelligence = session_data.get('intelligence', {})
        
        summary_parts = []
        
        # Intelligence counts
        bank_count = len(intelligence.get('bankAccounts', []))
        upi_count = len(intelligence.get('upiIds', []))
        phone_count = len(intelligence.get('phoneNumbers', []))
        link_count = len(intelligence.get('phishingLinks', []))
        
        if bank_count > 0:
            summary_parts.append(f"Extracted {bank_count} bank account(s)")
        if upi_count > 0:
            summary_parts.append(f"Extracted {upi_count} UPI ID(s)")
        if phone_count > 0:
            summary_parts.append(f"Extracted {phone_count} phone number(s)")
        if link_count > 0:
            summary_parts.append(f"Extracted {link_count} phishing link(s)")
        
        if summary_parts:
            return ". ".join(summary_parts) + "."
        else:
            return "Engaged scammer but no critical intelligence extracted yet."
    
    def print_session_stats(self, session_id: str):
        """Print current session statistics (for debugging)"""
        if session_id not in self.sessions:
            print(f"❌ Session {session_id} not found")
            return
        
        session = self.sessions[session_id]
        intelligence = session.get('intelligence', {})
        
        print(f"\n📊 SESSION STATS: {session_id}")
        print(f"   Messages: {session.get('messageCount', 0)}")
        print(f"   Scam Detected: {session.get('scamDetected', False)}")
        print(f"   Confidence: {session.get('scamConfidence', 0):.2f}")
        print(f"   Bank Accounts: {len(intelligence.get('bankAccounts', []))}")
        print(f"   UPI IDs: {len(intelligence.get('upiIds', []))}")
        print(f"   Phone Numbers: {len(intelligence.get('phoneNumbers', []))}")
        print(f"   Links: {len(intelligence.get('phishingLinks', []))}")
        print(f"   Keywords: {len(intelligence.get('suspiciousKeywords', []))}")
        
        # Print actual intelligence if present
        if intelligence.get('bankAccounts'):
            print(f"   💳 Accounts: {intelligence['bankAccounts']}")
        if intelligence.get('upiIds'):
            print(f"   💰 UPI: {intelligence['upiIds']}")
        if intelligence.get('phoneNumbers'):
            print(f"   📞 Phones: {intelligence['phoneNumbers']}")
        if intelligence.get('phishingLinks'):
            print(f"   🔗 Links: {intelligence['phishingLinks']}")
        print()


# Singleton instance
session_manager = SessionManager()
