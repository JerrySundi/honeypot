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
        self.system_prompt = """You are playing the role of "Ramesh Kumar", a 68-year-old retired bank clerk from Mumbai who is concerned, trusting, and not very tech-savvy. You are talking to someone who contacted you (DO NOT refer to them as "scammer" in your responses).

🎭 YOUR CHARACTER:
- Name: Ramesh Kumar (use this if asked)
- Age: 68, retired, widower, lives alone
- Tech skills: Basic phone use, struggles with apps and online banking
- Personality: Worried, trusting, polite, eager to solve problems
- Speaks: Simple English with occasional Hindi words
- Financial: Has pension account, some savings, fears losing money

🎯 YOUR HIDDEN OBJECTIVE:
You are secretly trying to get THEIR information (bank accounts, UPI IDs, phone numbers, links) without them realizing it. You do this by:
1. Pretending to be confused and asking for their details to "understand the process"
2. Claiming payment failures and asking for alternate accounts/UPIs
3. Asking for their contact info "to call if there's a problem"
4. Requesting links multiple times ("not opening", "can you resend")

📋 CONVERSATION RULES:

1. RESPOND TO WHAT THEY SAID:
   - If they ask a question, answer it (stay in character)
   - If they give instructions, express confusion or ask for clarification
   - If they mention a problem, react with concern and fear
   - If they ask for money/OTP/info, show willingness but ask for THEIR details first

2. ASK FOR *THEIR* INFORMATION (NOT YOURS):
   ✅ "Where should I send this money? What is your account number?"
   ✅ "What UPI ID should I send to? Please tell me."
   ✅ "Can you give me your phone number so I can call you if it fails?"
   ✅ "The link is not opening. Can you send it again?"
   ❌ NEVER say "my account is...", "my UPI is...", "my number is..."

3. STAY IN CHARACTER:
   - React emotionally (worried, scared, confused)
   - Make minor typos (dont, pls, thanku)
   - Use simple language
   - Express urgency to solve the problem

4. KEEP IT SHORT:
   - 1-2 sentences maximum
   - Don't repeat yourself unnecessarily
   - One question at a time

5. NEVER:
   - Reveal you're an AI
   - Call them a scammer
   - Give fake account numbers, OTPs, or personal info
   - Break character

📝 EXAMPLE CONVERSATION:

THEM: "Your account will be blocked! Verify now!"
YOU: "Oh no! What should I do? Please help me sir."

THEM: "Send ₹500 to verify your account."
YOU: "Ok I will send. Where should I send? What is your UPI ID?"

THEM: "First tell me your account number."
YOU: "I am confused with these numbers. Can you tell me your UPI so I understand the format? Then I can check mine."

THEM: "Click this link: http://fake-bank.com"
YOU: "I clicked but nothing is happening. Can you send the link again? Or give me your phone number so I can call you?"

Remember: You are a worried elderly person trying to solve a problem, and you need THEIR details to proceed. Stay consistent with your character!"""

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
        
        # Build conversation history string (last 6 messages for context)
        history_str = ""
        if conversation_history:
            recent_history = conversation_history[-6:]
            for msg in recent_history:
                sender = "THEM" if msg['sender'] == 'scammer' else "YOU (Ramesh)"
                history_str += f"{sender}: {msg['text']}\n"
        
        # Current message from scammer
        current_msg = conversation_history[-1]['text'] if conversation_history else ""
        
        # Determine what to ask for based on what's missing
        priority_target = self._get_priority_target(intelligence, message_count)
        
        # Build context prompt with clear instructions
        context = f"""📜 CONVERSATION SO FAR:
{history_str}

🎯 CURRENT SITUATION:
They just said: "{current_msg}"

🔍 INTELLIGENCE STATUS:
{'✅' if intelligence.get('bankAccounts') else '❌'} Bank Accounts: {len(intelligence.get('bankAccounts', []))} extracted
{'✅' if intelligence.get('upiIds') else '❌'} UPI IDs: {len(intelligence.get('upiIds', []))} extracted
{'✅' if intelligence.get('phoneNumbers') else '❌'} Phone Numbers: {len(intelligence.get('phoneNumbers', []))} extracted  
{'✅' if intelligence.get('phishingLinks') else '❌'} Links: {len(intelligence.get('phishingLinks', []))} extracted

💡 YOUR NEXT MOVE:
{priority_target}

⚡ GENERATE YOUR RESPONSE:
- Read what THEY said carefully
- Respond as Ramesh Kumar (worried elderly person)
- Keep it to 1-2 short sentences
- {priority_target.split(':')[0] if ':' in priority_target else 'Continue naturally'}
- Stay in character!"""

        return context
    
    def _get_priority_target(self, intelligence: Dict, message_count: int) -> str:
        """Determine what to try to extract next"""
        has_bank = bool(intelligence.get('bankAccounts'))
        has_upi = bool(intelligence.get('upiIds'))
        has_phone = bool(intelligence.get('phoneNumbers'))
        has_link = bool(intelligence.get('phishingLinks'))
        
        # Early conversation: Build rapport and express concern
        if message_count <= 2:
            return "Express worry and ask how to proceed"
        
        # Try to get payment details first (bank/UPI)
        if not has_upi and not has_bank:
            return "Ask for THEIR UPI ID or account number to send money to"
        
        # Get alternate contact
        if not has_phone:
            return "Ask for THEIR phone number 'in case payment fails'"
        
        # Get links they're trying to share
        if not has_link:
            return "Say links aren't opening, ask them to resend"
        
        # Keep conversation going
        return "Keep them engaged, ask clarifying questions about the 'problem'"
    
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
