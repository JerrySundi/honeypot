import re
from typing import Dict, List, Tuple


class ScamDetector:
    """Detect scam intent in messages"""
    
    def __init__(self):
        # High-confidence scam indicators
        self.urgent_keywords = [
            'urgent', 'immediately', 'now', 'today', 'hurry',
            'quick', 'fast', 'asap', 'right now'
        ]
        
        self.threat_keywords = [
            'blocked', 'suspended', 'closed', 'locked', 'frozen',
            'cancelled', 'terminated', 'action required', 'expired',
            'deactivated', 'disabled'
        ]
        
        self.financial_keywords = [
            'bank account', 'credit card', 'debit card', 'account number',
            'upi', 'payment', 'transfer', 'money', 'rupees', 'rs.',
            'verify payment', 'send money', 'pay now'
        ]
        
        self.authority_keywords = [
            'bank', 'government', 'police', 'officer', 'official',
            'rbi', 'income tax', 'customs', 'cyber cell', 'legal',
            'court', 'penalty', 'fine'
        ]
        
        self.personal_info_keywords = [
            'otp', 'cvv', 'pin', 'password', 'user id', 'username',
            'date of birth', 'aadhar', 'pan card', 'card number'
        ]
        
        self.prize_keywords = [
            'congratulations', 'winner', 'won', 'prize', 'reward',
            'lottery', 'lucky', 'selected', 'claim', 'gift'
        ]
        
        # Scam patterns
        self.scam_patterns = [
            r'send\s+(?:rs\.?|rupees|₹)\s*\d+',
            r'account\s+(?:will be|has been)\s+blocked',
            r'verify\s+(?:your|the)\s+(?:account|payment|transaction)',
            r'click\s+(?:here|this|the\s+link)',
            r'share\s+(?:your|the)\s+otp',
            r'won\s+(?:rs\.?|rupees|₹)\s*\d+',
        ]
    
    def detect(self, message: str, conversation_history: List[Dict] = None) -> Tuple[bool, float, str]:
        """
        Detect if a message is a scam attempt
        
        Args:
            message: Current message text
            conversation_history: Previous messages in conversation
            
        Returns:
            Tuple of (is_scam, confidence_score, reason)
        """
        if not message:
            return False, 0.0, "Empty message"
        
        message_lower = message.lower()
        score = 0.0
        reasons = []
        
        # Check for urgent language (weight: 0.2)
        urgent_count = sum(1 for kw in self.urgent_keywords if kw in message_lower)
        if urgent_count > 0:
            score += 0.2
            reasons.append(f"Urgent language detected ({urgent_count} keywords)")
        
        # Check for threats (weight: 0.25)
        threat_count = sum(1 for kw in self.threat_keywords if kw in message_lower)
        if threat_count > 0:
            score += 0.25
            reasons.append(f"Threatening language ({threat_count} keywords)")
        
        # Check for financial requests (weight: 0.2)
        financial_count = sum(1 for kw in self.financial_keywords if kw in message_lower)
        if financial_count > 0:
            score += 0.2
            reasons.append(f"Financial keywords ({financial_count} found)")
        
        # Check for authority impersonation (weight: 0.15)
        authority_count = sum(1 for kw in self.authority_keywords if kw in message_lower)
        if authority_count > 0:
            score += 0.15
            reasons.append(f"Authority impersonation ({authority_count} keywords)")
        
        # Check for personal info requests (weight: 0.3)
        personal_info_count = sum(1 for kw in self.personal_info_keywords if kw in message_lower)
        if personal_info_count > 0:
            score += 0.3
            reasons.append(f"Requesting personal info ({personal_info_count} items)")
        
        # Check for prize scams (weight: 0.2)
        prize_count = sum(1 for kw in self.prize_keywords if kw in message_lower)
        if prize_count > 0:
            score += 0.2
            reasons.append(f"Prize scam indicators ({prize_count} keywords)")
        
        # Check for scam patterns (weight: 0.3 per match)
        for pattern in self.scam_patterns:
            if re.search(pattern, message_lower):
                score += 0.3
                reasons.append(f"Scam pattern matched: {pattern}")
        
        # Cap score at 1.0
        score = min(score, 1.0)
        
        # Determine if it's a scam (threshold: 0.4)
        is_scam = score >= 0.4
        
        # Create reason string
        reason = "; ".join(reasons) if reasons else "No scam indicators"
        
        return is_scam, score, reason
    
    def get_scam_category(self, message: str) -> str:
        """Categorize the type of scam"""
        message_lower = message.lower()
        
        if any(kw in message_lower for kw in self.prize_keywords):
            return "PRIZE_SCAM"
        elif any(kw in message_lower for kw in self.personal_info_keywords):
            return "CREDENTIAL_THEFT"
        elif 'otp' in message_lower:
            return "OTP_SCAM"
        elif any(kw in message_lower for kw in self.threat_keywords):
            return "THREAT_BASED_SCAM"
        elif any(kw in message_lower for kw in self.financial_keywords):
            return "FINANCIAL_FRAUD"
        else:
            return "GENERAL_SCAM"
