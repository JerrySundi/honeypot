import re
from typing import Dict, List


class IntelligenceExtractor:
    """Extract scam-related intelligence from messages"""
    
    def __init__(self):
        self.scam_keywords = [
            'urgent', 'immediately', 'verify', 'blocked', 'suspended',
            'confirm', 'update', 'expired', 'action required', 'click here',
            'account', 'bank', 'payment', 'transfer', 'upi', 'otp',
            'prize', 'winner', 'congratulations', 'claim', 'reward'
        ]
        
        # Common UPI providers in India
        self.upi_providers = [
            'paytm', 'phonepe', 'googlepay', 'gpay', 'ybl', 'axl',
            'ibl', 'okaxis', 'okhdfcbank', 'okicici', 'oksbi', 'airtel'
        ]
    
    def extract_from_message(self, text: str) -> Dict[str, List[str]]:
        """
        Extract all intelligence from a single message
        
        Args:
            text: Message text to analyze
            
        Returns:
            Dictionary with extracted intelligence
        """
        if not text:
            return self._empty_intelligence()
        
        intelligence = {
            "bankAccounts": self._extract_bank_accounts(text),
            "upiIds": self._extract_upi_ids(text),
            "phoneNumbers": self._extract_phone_numbers(text),
            "phishingLinks": self._extract_urls(text),
            "suspiciousKeywords": self._extract_keywords(text)
        }
        
        return intelligence
    
    def _extract_bank_accounts(self, text: str) -> List[str]:
        """Extract bank account numbers"""
        accounts = []
        
        # Pattern 1: 16-digit cards (4 groups of 4)
        pattern1 = r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        matches1 = re.findall(pattern1, text)
        for m in matches1:
            clean = m.replace(' ', '').replace('-', '')
            if not self._is_phone_number(clean):
                accounts.append(clean)
        
        # Pattern 2: Account numbers (11-18 digits, excluding phone numbers)
        pattern2 = r'\b\d{11,18}\b'
        matches2 = re.findall(pattern2, text)
        for acc in matches2:
            if not self._is_phone_number(acc):
                accounts.append(acc)
        
        # Remove duplicates
        return list(set(accounts))
    
    def _extract_upi_ids(self, text: str) -> List[str]:
        """Extract UPI IDs (format: user@provider)"""
        upi_ids = []
        
        # Pattern: word characters + @ + word characters
        pattern = r'\b[\w\.-]+@[\w\.-]+\b'
        matches = re.findall(pattern, text.lower())
        
        # Filter for known UPI providers
        for match in matches:
            if any(provider in match for provider in self.upi_providers):
                upi_ids.append(match)
        
        return list(set(upi_ids))
    
    def _is_phone_number(self, text: str) -> bool:
        """Check if a string is likely a phone number"""
        digits = re.sub(r'\D', '', text)
        # Indian phone numbers: 10 digits starting with 6-9
        if len(digits) == 10 and digits[0] in '6789':
            return True
        # With country code: +91 or 0091
        if len(digits) == 12 and digits[:2] == '91':
            return True
        return False
    
    def _extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers (Indian format)"""
        phone_numbers = set()  # Use set to avoid duplicates
        
        # Pattern 1: +91 followed by 10 digits
        pattern1 = r'\+91[-\s]?[6-9]\d{9}'
        matches1 = re.findall(pattern1, text)
        for phone in matches1:
            clean = re.sub(r'[-\s]', '', phone)
            phone_numbers.add(clean)
        
        # Pattern 2: 10 digits starting with 6-9 (not already captured)
        pattern2 = r'(?<!\+91)(?<!\d)[6-9]\d{9}(?!\d)'
        matches2 = re.findall(pattern2, text)
        for phone in matches2:
            # Only add if not already captured with +91
            normalized = '+91' + phone
            if normalized not in phone_numbers:
                phone_numbers.add(normalized)
        
        # Pattern 3: 0 followed by 10 digits
        pattern3 = r'\b0[6-9]\d{9}\b'
        matches3 = re.findall(pattern3, text)
        for phone in matches3:
            clean = phone[1:]  # Remove leading 0
            normalized = '+91' + clean
            phone_numbers.add(normalized)
        
        return list(phone_numbers)
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs (potential phishing links)"""
        # Pattern for http(s):// URLs
        pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        matches = re.findall(pattern, text)
        
        # Also catch www. links without protocol
        pattern2 = r'\bwww\.[^\s<>"{}|\\^`\[\]]+'
        matches2 = re.findall(pattern2, text)
        
        all_urls = matches + matches2
        return list(set(all_urls))
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract suspicious keywords"""
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in self.scam_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return list(set(found_keywords))
    
    def _empty_intelligence(self) -> Dict[str, List[str]]:
        """Return empty intelligence structure"""
        return {
            "bankAccounts": [],
            "upiIds": [],
            "phoneNumbers": [],
            "phishingLinks": [],
            "suspiciousKeywords": []
        }
    
    def merge_intelligence(self, existing: Dict, new: Dict) -> Dict:
        """Merge new intelligence with existing, removing duplicates"""
        merged = {}
        
        for key in existing.keys():
            combined = existing[key] + new.get(key, [])
            merged[key] = list(set(combined))  # Remove duplicates
        
        return merged
