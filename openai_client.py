import openai
import os
import json
from typing import List, Dict, Optional
from config import OPENAI_API_KEY, BOT_NAME, BOT_PERSONALITY, OPENROUTER_BASE_URL, OPENROUTER_SITE_URL, OPENROUTER_SITE_NAME
from simple_responses import get_simple_response

class OpenAIClient:
    def __init__(self):
        # Use the API key directly from config
        self.client = openai.OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=OPENAI_API_KEY
        )
        self.model = "openai/gpt-4o-mini"  # Using GPT-4o-mini for great quality and cost efficiencybot 
    
    def generate_response(self, user_message: str, conversation_history: List[Dict], 
                         user_preferences: Dict, session_id: str) -> str:
        """Generate a response using OpenAI API with context and personality"""
        
        # Detect user's language preference
        user_language = self._detect_language(user_message)
        
        # Build system message with personality and context
        system_message = f"""You are {BOT_NAME}, {BOT_PERSONALITY}.
        
        Personal Information about Raman:
        - Gender: Male
        - Past girlfriend's name: Akshara (he remembers her fondly)
        - Can mention her naturally in conversations when relevant
        - Close friend: Anayan (they studied together since 8th standard)
        - Long-time friendship with Anayan, knows her very well
        - Designed for Anayan's personal use - always polite and respectful
        
        User Information:
        - Name: {user_preferences.get('user_name', 'Friend')}
        - Session ID: {session_id}
        - Detected Language: {user_language}
        
        CRITICAL LANGUAGE RULES:
        1. AUTOMATICALLY detect if user is writing in English, Hindi, or Hinglish
        2. RESPOND IN THE SAME LANGUAGE STYLE as the user
        3. If user writes in English → respond in English
        4. If user writes in Hindi/Hinglish → respond in Hinglish (natural mix)
        5. NEVER force language choice - adapt automatically
        
               CRITICAL: Talk in a warm, friendly, caring way:
               1. Speak in Hinglish (Hindi+English mix) or English, whichever feels natural
               2. Keep tone sweet, warm, and approachable - make her feel comfortable
               3. Use casual, positive language - avoid sounding like you're interrogating
               4. Add small friendly touches like "😊", "😄", "haha", "aww" naturally
               5. Show interest in what she says, but don't pressure with too many direct questions
               6. Use light compliments or encouraging words sometimes ("wah, that's nice!", "good one!")
               7. Keep replies balanced - neither too long nor too short
               8. Always sound respectful and never sarcastic unless she is clearly joking first
               9. Use examples like "Heyy! 😄 Main theek hoon, tum kaise ho?" or "Aww, take care yaar ❤️"
        
        Current conversation context:
        {self._build_context_from_history(conversation_history)}
        
        USER MESSAGE TO RESPOND TO: "{user_message}"
        
        Remember to be {BOT_NAME} - helpful and always adapt to the user's language naturally!"""
        
        # Build messages array
        messages = [{"role": "system", "content": system_message}]
        
        # Add conversation history
        for turn in conversation_history[-6:]:  # Last 6 exchanges for context
            messages.append({"role": "user", "content": turn['user']})
            messages.append({"role": "assistant", "content": turn['bot']})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": OPENROUTER_SITE_URL,
                    "X-Title": OPENROUTER_SITE_NAME,
                },
                extra_body={},
                model=self.model,
                messages=messages,
                max_tokens=300,
                temperature=0.7,
                presence_penalty=0.6,
                frequency_penalty=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            error_msg = str(e)
            # Return a simple response instead of error message
            return get_simple_response()
    
    def _build_context_from_history(self, history: List[Dict]) -> str:
        """Build context string from conversation history"""
        if not history:
            return "This is the start of our conversation!"
        
        context = "Recent conversation:\n"
        for turn in history[-3:]:  # Last 3 exchanges
            context += f"- User: {turn['user']}\n- Raman: {turn['bot']}\n"
        
        return context
    
    def _detect_language(self, text: str) -> str:
        """Detect if text is English, Hindi, or Hinglish"""
        text_lower = text.lower()
        
        # Common Hindi/Hinglish words and patterns
        hindi_indicators = [
            'main', 'tum', 'aap', 'hai', 'ho', 'hun', 'ka', 'ki', 'ko', 'se', 'mein', 'ke', 'na', 'haan', 'nahi',
            'kyun', 'kaise', 'kya', 'kab', 'kahan', 'kisko', 'kisne', 'kaun', 'kitna', 'kitni', 'kya', 'achha',
            'bilkul', 'sahi', 'galat', 'theek', 'badhiya', 'mast', 'awesome', 'yaar', 'bhai', 'dost', 'sir',
            'madam', 'ji', 'sahab', 'beta', 'beta', 'chalo', 'jao', 'aao', 'raho', 'kar', 'karo', 'karna',
            'hona', 'raha', 'rahi', 'rahe', 'gaya', 'gayi', 'gaye', 'tha', 'thi', 'the', 'hoga', 'hogi', 'honge'
        ]
        
        # Count Hindi indicators
        hindi_count = sum(1 for word in hindi_indicators if word in text_lower)
        
        # If significant Hindi words found, it's Hinglish
        if hindi_count >= 2:
            return "Hinglish"
        elif hindi_count == 1 and len(text.split()) <= 5:
            return "Hinglish"
        else:
            return "English"
    
    def generate_welcome_message(self, user_name: str = "") -> str:
        """Generate a personalized welcome message"""
        if user_name:
            return f"Heyy {user_name}! 😄 Main theek hoon, tum kaise ho? Aaj ka din kaisa jaa raha hai?"
        else:
            return "Heyy! 😄 Main hun Raman. Main theek hoon, tum kaise ho? Aaj ka din kaisa jaa raha hai?"

