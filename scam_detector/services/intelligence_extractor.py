import re
from typing import Dict, List


class IntelligenceExtractor:
    """Extract scam-related intelligence from messages with advanced pattern detection"""
    
    def __init__(self):
        self.scam_keywords = [
            'urgent', 'immediately', 'verify', 'blocked', 'suspended',
            'confirm', 'update', 'expired', 'action required', 'click here',
            'account', 'bank', 'payment', 'transfer', 'upi', 'otp',
            'prize', 'winner', 'congratulations', 'claim', 'reward',
            'kyc', 'aadhar', 'pan', 'cvv', 'pin', 'password', 'security',
            'refund', 'cashback', 'credit', 'debit', 'loan', 'emi'
        ]
        
        # Extended UPI providers (including all major banks and wallets)
        self.upi_providers = [
            'paytm', 'phonepe', 'googlepay', 'gpay', 'ybl', 'axl',
            'ibl', 'okaxis', 'okhdfcbank', 'okicici', 'oksbi', 'airtel',
            'amazonpay', 'freecharge', 'mobikwik', 'jio', 'whatsapp',
            'okbank', 'okmybank', 'mybank', 'pnb', 'boi', 'citi',
            'hsbc', 'kotak', 'federal', 'rbl', 'yes', 'idbi', 'indus'
        ]
        
        # Email domains commonly used by scammers
        self.suspicious_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'protonmail.com', 'mail.com', 'yandex.com'
        ]
    
    def extract_from_message(self, text: str) -> Dict[str, List[str]]:
        """
        Extract all intelligence from a single message with enhanced detection
        
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
            "emailAddresses": self._extract_emails(text),
            "ifscCodes": self._extract_ifsc_codes(text),
            "suspiciousKeywords": self._extract_keywords(text)
        }
        
        return intelligence
    
    def _extract_bank_accounts(self, text: str) -> List[str]:
        """Extract bank account numbers with improved patterns"""
        accounts = set()
        
        # Remove common separators for easier matching
        clean_text = text.replace('-', ' ').replace('_', ' ')
        
        # Pattern 1: 16-digit cards (debit/credit cards)
        pattern1 = r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b'
        matches1 = re.findall(pattern1, clean_text)
        for m in matches1:
            clean = re.sub(r'\s', '', m)
            if len(clean) == 16 and not self._is_phone_number(clean):
                accounts.add(clean)
        
        # Pattern 2: Bank account numbers (9-18 digits)
        # Must not be phone numbers
        pattern2 = r'\b\d{9,18}\b'
        matches2 = re.findall(pattern2, text)
        for acc in matches2:
            if 9 <= len(acc) <= 18 and not self._is_phone_number(acc):
                # Additional check: account numbers often have consistent digit patterns
                accounts.add(acc)
        
        # Pattern 3: Account numbers with "A/C", "account", "acc" keywords nearby
        pattern3 = r'(?:account|acc|a/c|ac|acct)[\s\:\-]*(\d{9,18})'
        matches3 = re.findall(pattern3, text, re.IGNORECASE)
        for acc in matches3:
            if not self._is_phone_number(acc):
                accounts.add(acc)
        
        return list(accounts)
    
    def _extract_upi_ids(self, text: str) -> List[str]:
        """Extract UPI IDs with enhanced pattern detection"""
        upi_ids = set()
        
        # Pattern 1: Catch all @something patterns (user@anything)
        # Key logic: If there's NO dot after @, it's a UPI ID
        # If there IS a dot after @, it's an email (handled separately)
        pattern1 = r'\b[\w\.\-]+@[\w\-]+\b'
        matches = re.findall(pattern1, text.lower())
        
        for match in matches:
            domain = match.split('@')[1] if '@' in match else ''
            # UPI IDs don't have dots in the domain part
            # Emails do (gmail.com, yahoo.com, etc.)
            if '.' not in domain:
                upi_ids.add(match)
            # Also accept known UPI providers even with dots
            elif any(provider in domain for provider in self.upi_providers):
                upi_ids.add(match)
        
        # Pattern 2: UPI IDs mentioned with keywords
        pattern2 = r'(?:upi|vpa|payment)[\s\:\-]*(?:id)?[\s\:\-]*([\w\.\-]+@[\w\-]+)'
        matches2 = re.findall(pattern2, text, re.IGNORECASE)
        for m in matches2:
            domain = m.split('@')[1] if '@' in m else ''
            if '.' not in domain:
                upi_ids.add(m.lower())
        
        # Pattern 3: Phone number based UPI (10digits@anything)
        pattern3 = r'\b[6-9]\d{9}@[\w\-]+\b'
        matches3 = re.findall(pattern3, text.lower())
        upi_ids.update(matches3)
        
        return list(upi_ids)
    
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
        """Extract phone numbers with comprehensive Indian format detection"""
        phone_numbers = set()
        
        # Pattern 1: +91 with various separators
        pattern1 = r'\+91[\s\-]?[6-9]\d{4}[\s\-]?\d{5}'
        matches1 = re.findall(pattern1, text)
        for phone in matches1:
            clean = re.sub(r'[\s\-]', '', phone)
            phone_numbers.add(clean)
        
        # Pattern 2: 91 without + sign
        pattern2 = r'\b91[\s\-]?[6-9]\d{9}\b'
        matches2 = re.findall(pattern2, text)
        for phone in matches2:
            clean = '+' + re.sub(r'[\s\-]', '', phone)
            phone_numbers.add(clean)
        
        # Pattern 3: 10 digits starting with 6-9 (standalone)
        pattern3 = r'(?<!\d)[6-9]\d{9}(?!\d)'
        matches3 = re.findall(pattern3, text)
        for phone in matches3:
            normalized = '+91' + phone
            phone_numbers.add(normalized)
        
        # Pattern 4: With leading 0
        pattern4 = r'\b0[6-9]\d{9}\b'
        matches4 = re.findall(pattern4, text)
        for phone in matches4:
            clean = phone[1:]  # Remove leading 0
            normalized = '+91' + clean
            phone_numbers.add(normalized)
        
        # Pattern 5: Phone numbers with keywords
        pattern5 = r'(?:call|contact|phone|mobile|whatsapp|number)[\s\:\-]*(\+?91[\s\-]?[6-9]\d{9}|\+?[6-9]\d{9})'
        matches5 = re.findall(pattern5, text, re.IGNORECASE)
        for phone in matches5:
            clean = re.sub(r'[\s\-]', '', phone)
            if not clean.startswith('+'):
                if clean.startswith('91'):
                    clean = '+' + clean
                else:
                    clean = '+91' + clean
            phone_numbers.add(clean)
        
        return list(phone_numbers)
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs including obfuscated and shortened links"""
        urls = set()
        
        # Pattern 1: Standard http(s):// URLs
        pattern1 = r'https?://[^\s<>"{}|\\^`\[\]]+'
        matches1 = re.findall(pattern1, text, re.IGNORECASE)
        urls.update(matches1)
        
        # Pattern 2: www. links without protocol
        pattern2 = r'www\.[^\s<>"{}|\\^`\[\]]+'
        matches2 = re.findall(pattern2, text, re.IGNORECASE)
        urls.update(matches2)
        
        # Pattern 3: Common URL patterns without www or http
        # e.g., domain.com/path
        pattern3 = r'\b[\w\-]+\.(?:com|net|org|in|co\.in|info|xyz|tk|ml|ga|cf|gq|online|site|club)/[^\s<>"{}|\\^`\[\]]*'
        matches3 = re.findall(pattern3, text, re.IGNORECASE)
        urls.update(matches3)
        
        # Pattern 4: Shortened URLs (bit.ly, tinyurl, etc.)
        pattern4 = r'\b(?:bit\.ly|tinyurl\.com|goo\.gl|ow\.ly|short\.link|t\.co|rb\.gy)/[\w\-]+'
        matches4 = re.findall(pattern4, text, re.IGNORECASE)
        urls.update(matches4)
        
        # Pattern 5: URLs mentioned with keywords
        pattern5 = r'(?:visit|click|open|go to|link|url)[\s\:\-]*((?:https?://)?[\w\-]+\.[\w\-\.]+(?:/[\w\-\./?%&=]*)?)'
        matches5 = re.findall(pattern5, text, re.IGNORECASE)
        urls.update(matches5)
        
        # Pattern 6: Obfuscated URLs with spaces (e.g., "google . com")
        pattern6 = r'([\w\-]+)\s*\.\s*(com|net|org|in|co\.in)'
        matches6 = re.findall(pattern6, text, re.IGNORECASE)
        for domain, tld in matches6:
            urls.add(f"{domain}.{tld}")
        
        return list(urls)
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses"""
        emails = set()
        
        # Pattern 1: Standard email format
        pattern1 = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches1 = re.findall(pattern1, text)
        emails.update(m.lower() for m in matches1)
        
        # Pattern 2: Email with keywords
        pattern2 = r'(?:email|mail|e-mail)[\s\:\-]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
        matches2 = re.findall(pattern2, text, re.IGNORECASE)
        emails.update(m.lower() for m in matches2)
        
        # Filter out UPI IDs that look like emails
        filtered_emails = set()
        for email in emails:
            domain = email.split('@')[1] if '@' in email else ''
            # Only keep if not a UPI provider
            if not any(provider in domain for provider in self.upi_providers):
                filtered_emails.add(email)
        
        return list(filtered_emails)
    
    def _extract_ifsc_codes(self, text: str) -> List[str]:
        """Extract IFSC codes (Indian bank codes)"""
        ifsc_codes = set()
        
        # IFSC format: 4 letters + 0 + 6 alphanumeric characters
        # Example: SBIN0001234
        pattern1 = r'\b[A-Z]{4}0[A-Z0-9]{6}\b'
        matches1 = re.findall(pattern1, text.upper())
        ifsc_codes.update(matches1)
        
        # Pattern 2: IFSC mentioned with keywords
        pattern2 = r'(?:ifsc|ifsc code|bank code)[\s\:\-]*([A-Z]{4}0[A-Z0-9]{6})'
        matches2 = re.findall(pattern2, text, re.IGNORECASE)
        ifsc_codes.update(m.upper() for m in matches2)
        
        return list(ifsc_codes)
    
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
            "emailAddresses": [],
            "ifscCodes": [],
            "suspiciousKeywords": []
        }
    
    def merge_intelligence(self, existing: Dict, new: Dict) -> Dict:
        """Merge new intelligence with existing, removing duplicates"""
        merged = {}
        
        for key in existing.keys():
            combined = existing[key] + new.get(key, [])
            merged[key] = list(set(combined))  # Remove duplicates
        
        return merged
