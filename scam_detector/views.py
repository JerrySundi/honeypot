from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .serializers import HoneypotRequestSerializer, HoneypotResponseSerializer
from .services.scam_detector import ScamDetector
from .services.intelligence_extractor import IntelligenceExtractor
from .services.ai_agent import AIAgent
from .services.session_manager import session_manager
from .utils.helpers import validate_api_key, send_final_callback


@method_decorator(csrf_exempt, name='dispatch')
class HoneypotAPIView(APIView):
    """
    Main API endpoint for the honeypot system
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scam_detector = ScamDetector()
        self.intelligence_extractor = IntelligenceExtractor()
        self.ai_agent = AIAgent(api_key=settings.DEEPSEEK_API_KEY)
    
    def post(self, request):
        """
        Handle incoming message and generate response
        """
        # 1. Validate API Key
        api_key = request.headers.get('x-api-key')
        if not api_key or not validate_api_key(api_key):
            return Response(
                {
                    "status": "error",
                    "message": "Invalid API key"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # 2. Validate request data
        serializer = HoneypotRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "status": "error",
                    "message": "Invalid request format",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        session_id = validated_data['sessionId']
        current_message = validated_data['message']
        conversation_history = validated_data.get('conversationHistory', [])
        
        print(f"\n{'='*60}")
        print(f"📨 INCOMING MESSAGE - Session: {session_id}")
        print(f"   Sender: {current_message['sender']}")
        print(f"   Text: {current_message['text']}")
        print(f"   History Length: {len(conversation_history)}")
        print(f"{'='*60}\n")
        
        try:
            # 3. Load or create session
            session_data = session_manager.get_or_create_session(session_id)
            
            # 4. Update message count
            session_data['messageCount'] += 1
            
            # 5. Extract intelligence from scammer's message
            new_intelligence = self.intelligence_extractor.extract_from_message(
                current_message['text']
            )
            
            # Merge with existing intelligence
            existing_intelligence = session_data['intelligence']
            session_data['intelligence'] = self.intelligence_extractor.merge_intelligence(
                existing_intelligence,
                new_intelligence
            )
            
            # Log extracted intelligence
            if any(new_intelligence.values()):
                print("🔍 NEW INTELLIGENCE EXTRACTED:")
                for key, values in new_intelligence.items():
                    if values:
                        print(f"   {key}: {values}")
            
            # 6. Detect scam (if not already detected)
            if not session_data['scamDetected']:
                is_scam, confidence, reason = self.scam_detector.detect(
                    current_message['text'],
                    conversation_history
                )
                
                session_data['scamDetected'] = is_scam
                session_data['scamConfidence'] = confidence
                
                if is_scam:
                    session_data['scamCategory'] = self.scam_detector.get_scam_category(
                        current_message['text']
                    )
                    print(f"🚨 SCAM DETECTED!")
                    print(f"   Confidence: {confidence:.2f}")
                    print(f"   Category: {session_data['scamCategory']}")
                    print(f"   Reason: {reason}")
            
            # 7. Generate response
            if session_data['scamDetected']:
                # Use AI agent for scam conversations
                agent_response = self.ai_agent.generate_response(
                    current_message['text'],
                    conversation_history,
                    session_data
                )
            else:
                # Safe response for non-scam messages
                agent_response = self.ai_agent.generate_safe_response(
                    current_message['text']
                )
            
            print(f"🤖 AGENT RESPONSE: {agent_response}\n")
            
            # 8. Check termination conditions
            should_end = session_manager.should_terminate(session_data)
            
            if should_end and not session_data.get('terminationTriggered'):
                session_data['terminationTriggered'] = True
                
                # Print final session stats
                session_manager.print_session_stats(session_id)
                
                # Send final callback to GUVI
                if session_data['scamDetected']:
                    callback_success = send_final_callback(session_data)
                    if callback_success:
                        print("✅ Final callback sent successfully")
                    else:
                        print("⚠️  Final callback failed or disabled")
                
                # Clean up session
                session_manager.delete_session(session_id)
            else:
                # Save updated session
                session_manager.update_session(session_id, session_data)
                
                # Print current stats
                if session_data['messageCount'] % 3 == 0:  # Every 3 messages
                    session_manager.print_session_stats(session_id)
            
            # 9. Return response
            return Response(
                {
                    "status": "success",
                    "reply": agent_response
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return Response(
                {
                    "status": "error",
                    "message": f"Internal server error: {str(e)}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
