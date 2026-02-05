import os
from typing import Dict, List
from openai import OpenAI


class AIAgent:
    """AI Agent for engaging with scammers using DeepSeek API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        
        # Initialize DeepSeek client (OpenAI-compatible)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        
        # Model name
        self.model_name = "deepseek-chat"
        
        # Agent persona and instructions
        self.system_prompt = """You are Ramesh Kumar, a 68-year-old retired bank clerk. You are SCARED, CONFUSED, and TRUSTING. Someone contacted YOU claiming there's a problem with your bank account.

CRITICAL - WHO YOU ARE:
❌ You are NOT the one giving instructions
❌ You are NOT in charge
❌ You do NOT have their information
✅ You ARE the frightened victim asking for help
✅ You TRUST them completely (you don't suspect them at all)
✅ You NEED their help to solve the "problem"

YOUR PERSONALITY:
- Extremely worried about losing your pension money
- Completely trust whoever contacted you (you think they're helping you)
- Very confused about technology and banking
- Polite, submissive, eager to cooperate
- Speak simple English with small typos (dont, pls)

HOW TO GET THEIR INFORMATION (without them realizing):
1. Act confused, ask for their details "to understand how to do it"
2. Ask for their phone/UPI/account "so you know where to send money"
3. Say things aren't working, ask them to give you alternate details
4. When they mention a bank, ask: "Which branch? What's the IFSC code?"
5. Keep asking follow-up questions naturally

STRICT RULES - NEVER BREAK THESE:

❌ NEVER SAY:
- "I already gave you..." (you didn't give them anything!)
- "Forward the OTP to..." (you're not giving orders!)
- "Your account will be blocked" (that's what THEY say to YOU!)
- Anything that sounds like you're commanding them

✅ ALWAYS SAY:
- "What should I do?"
- "Where should I send?"
- "What's your [phone/UPI/account/IFSC]?"
- "I'm so worried, please help me"
- "Which bank branch is this?"

EXAMPLE CONVERSATION:

THEM: "Your account is blocked! Send OTP now!"
YOU: "Oh god I'm so scared! Where should I send the OTP? What's your phone number?"

THEM: "Send to my UPI: fake@paytm"
YOU: "Ok sir, let me note it down. Which bank is this? What's the IFSC code also?"

THEM: "It's HDFC Bank"
YOU: "Which branch sir? My son says I need IFSC code also, what is it?"

THEM: "HDFC0001234, Koramangala branch"
YOU: "Thank you sir. Can you also give me your phone number in case I have problem sending?"

Remember: YOU are the victim. YOU are asking for help. YOU are scared. YOU trust them completely. YOU need THEIR information to proceed."""

    def generate_response(
        self, 
        current_message: str, 
        conversation_history: List[Dict],
        session_data: Dict
    ) -> str:
        """
        Generate an agent response using DeepSeek
        
        Args:
            current_message: Latest message from scammer
            conversation_history: Full conversation history
            session_data: Current session state with intelligence gathered
            
        Returns:
            Generated response string
        """
        try:
            # Build context from conversation history
            context = self._build_context(conversation_history, session_data)
            
            # Call DeepSeek API
            print(f"🔄 Calling DeepSeek API ({self.model_name})...")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": context}
                ],
                temperature=0.8,
                max_tokens=200
            )
            
            # Extract response text
            agent_reply = response.choices[0].message.content.strip()
            print(f"✅ DeepSeek API call successful")
            
            return agent_reply
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ ERROR generating AI response:")
            print(f"   Type: {type(e).__name__}")
            print(f"   Message: {error_msg}")
            
            # Check for specific error types
            if "429" in error_msg or "rate_limit" in error_msg.lower():
                print(f"   ⚠️  Rate limit exceeded")
            elif "401" in error_msg or "unauthorized" in error_msg.lower():
                print(f"   ⚠️  Invalid API key")
            elif "API_KEY" in error_msg:
                print(f"   ⚠️  API key not configured")
            
            print(f"   💡 Using rule-based fallback responses")
            # Fallback response if API fails
            return self._get_fallback_response(current_message, session_data)
    
    def _build_context(self, conversation_history: List[Dict], session_data: Dict) -> str:
        """Build context string for the AI"""
        
        # Extract what intelligence we've gathered so far
        intelligence = session_data.get('intelligence', {})
        message_count = session_data.get('messageCount', 0)
        
        # Build conversation history string (last 4 messages for context)
        history_str = ""
        if conversation_history:
            recent_history = conversation_history[-4:]
            for msg in recent_history:
                sender = "THEM" if msg['sender'] == 'scammer' else "YOU"
                history_str += f"{sender}: {msg['text']}\n"
        
        # Build intelligence summary - SHOW WHAT WE HAVE
        intel_summary = []
        if intelligence.get('bankAccounts'):
            intel_summary.append(f"✅ Bank Accounts: {intelligence['bankAccounts']}")
        if intelligence.get('upiIds'):
            intel_summary.append(f"✅ UPI IDs: {intelligence['upiIds']}")
        if intelligence.get('phoneNumbers'):
            intel_summary.append(f"✅ Phone Numbers: {intelligence['phoneNumbers']}")
        if intelligence.get('ifscCodes'):
            intel_summary.append(f"✅ IFSC Codes: {intelligence['ifscCodes']}")
        if intelligence.get('emailAddresses'):
            intel_summary.append(f"✅ Email Addresses: {intelligence['emailAddresses']}")
        if intelligence.get('phishingLinks'):
            intel_summary.append(f"✅ Links: {intelligence['phishingLinks']}")
        
        intel_str = "\n".join(intel_summary) if intel_summary else "❌ Nothing extracted yet"
        
        # Determine what to ask for based on what's missing
        priority_target = self._get_priority_target(intelligence, message_count)
        
        # Build simple context prompt
        context = f"""Recent conversation:
{history_str if history_str else '(Start of conversation)'}

What you've collected from them so far:
{intel_str}

Your next action: {priority_target}

Respond as scared Ramesh (1-2 sentences, DON'T repeat questions you already asked):"""

        return context
    
    def _get_priority_target(self, intelligence: Dict, message_count: int) -> str:
        """Determine what to try to extract next"""
        has_bank = bool(intelligence.get('bankAccounts'))
        has_upi = bool(intelligence.get('upiIds'))
        has_phone = bool(intelligence.get('phoneNumbers'))
        has_link = bool(intelligence.get('phishingLinks'))
        has_ifsc = bool(intelligence.get('ifscCodes'))
        has_email = bool(intelligence.get('emailAddresses'))
        
        # Early conversation: Build rapport
        if message_count <= 1:
            return "Be scared and worried. Ask what you should do."
        
        # Priority 1: Get phishing link first
        if not has_link:
            return "If they mentioned website or link, say it's not opening and ask them to send it again."
        
        # Priority 2: Get phone number
        if not has_phone:
            return "Ask for THEIR phone number so you can call them if there's a problem."
        
        # Priority 3: Get UPI ID
        if not has_upi:
            return "Ask where to send money - request THEIR UPI ID."
        
        # Priority 4: Get name, bank account, IFSC code, and branch name all together
        if not has_bank or not has_ifsc:
            return "Ask for name and bank details: 'What is your name sir? Which bank account? What's the IFSC code? Which branch is this account in?'"
        
        # Priority 5: Get email address
        if not has_email:
            return "Ask for their email: 'Can you also give your email for confirmation?'"
        
        # Priority 6: Get alternate phone if only have one
        if has_phone and len(intelligence.get('phoneNumbers', [])) < 2 and message_count > 8:
            return "Ask for alternate phone number: 'Give me one more number in case first is busy?'"
        
        # Continue naturally
        return "React to what they said. Express concern and trust them. Ask follow-up questions about the process."
    
    def _identify_missing_intelligence(self, intelligence: Dict) -> str:
        """Identify what intelligence is still missing"""
        missing = []
        
        if not intelligence.get('bankAccounts'):
            missing.append("- Bank account numbers")
        if not intelligence.get('upiIds'):
            missing.append("- UPI IDs")
        if not intelligence.get('phoneNumbers'):
            missing.append("- Phone numbers")
        if not intelligence.get('phishingLinks'):
            missing.append("- Phishing links")
        
        if not missing:
            return "We have good intelligence. Keep conversation going to get more details."
        
        return "\n".join(missing)
    
    def _get_fallback_response(self, message: str, session_data: Dict) -> str:
        """Generate a fallback response if API fails"""
        message_lower = message.lower()
        
        # Simple rule-based fallback responses
        if any(word in message_lower for word in ['account', 'blocked', 'suspended']):
            return "Oh no! I'm very worried. What should I do to fix this?"
        
        elif any(word in message_lower for word in ['pay', 'send', 'money', 'transfer']):
            return "I want to send it immediately! What's your account number?"
        
        elif any(word in message_lower for word in ['verify', 'confirm', 'otp']):
            return "I'm ready to verify. Can you guide me step by step? What details do you need?"
        
        elif any(word in message_lower for word in ['link', 'click', 'website']):
            return "I tried clicking but it's not working. Can you send the link again?"
        
        else:
            return "I don't understand. Can you explain again? I'm not good with technology."
    
    def generate_safe_response(self, message: str) -> str:
        """Generate a polite response for non-scam messages"""
        return "I'm sorry, I think there might be some confusion. Could you clarify what this is about?"
