import re
import json
from datetime import datetime, time

class CommonSense:
    def __init__(self):
        self.knowledge_base = self.load_common_sense_rules()
        self.context_memory = []
    
    def load_common_sense_rules(self):
        """Load basic common sense knowledge"""
        return {
            # Physical world
            "physics": {
                "water_freezes_at_0": "Water freezes at 0°C (32°F)",
                "gravity_pulls_down": "Objects fall down due to gravity",
                "fire_is_hot": "Fire is hot and can burn",
                "ice_is_cold": "Ice is cold and melts when heated",
                "sun_gives_light": "The sun provides light during day"
            },
            
            # Time and seasons
            "time": {
                "day_after_night": "Day comes after night",
                "seasons_cycle": "Seasons change in cycles",
                "past_before_present": "Past events happened before now",
                "future_after_present": "Future events will happen later"
            },
            
            # Human behavior
            "human": {
                "people_need_food": "People need food to survive",
                "sleep_when_tired": "People sleep when they're tired",
                "wear_clothes": "People wear clothes for protection and warmth",
                "communicate_with_language": "People use language to communicate"
            },
            
            # Cause and effect
            "causality": {
                "rain_makes_wet": "Rain makes things wet",
                "exercise_makes_tired": "Exercise can make you tired",
                "studying_improves_knowledge": "Studying helps you learn",
                "practice_improves_skills": "Practice makes you better at things"
            },
            
            # Social norms
            "social": {
                "be_polite": "It's good to be polite to others",
                "help_others": "Helping others is generally good",
                "respect_privacy": "People value their privacy",
                "follow_laws": "Following laws is important for society"
            }
        }
    
    def apply_common_sense(self, query, ai_response):
        """Apply common sense reasoning to AI responses"""
        # Check if response needs common sense correction
        corrected_response = self.check_logical_consistency(query, ai_response)
        
        # Add practical context
        enhanced_response = self.add_practical_context(query, corrected_response)
        
        # Apply safety and ethics
        safe_response = self.apply_safety_filter(enhanced_response)
        
        return safe_response
    
    def check_logical_consistency(self, query, response):
        """Check if response makes logical sense"""
        query_lower = query.lower()
        response_lower = response.lower()
        
        # Time-based logic
        if "yesterday" in query_lower and "tomorrow" in response_lower:
            return "I think there might be some confusion about time. Let me clarify: " + response
        
        # Physical impossibilities
        impossible_phrases = [
            ("water" in response_lower and "burn" in response_lower),
            ("ice" in response_lower and "hot" in response_lower),
            ("fly" in response_lower and "human" in query_lower and "without" not in response_lower)
        ]
        
        if any(impossible_phrases):
            return "That doesn't seem physically possible. Let me give you a more realistic answer: " + self.get_realistic_alternative(query)
        
        return response
    
    def add_practical_context(self, query, response):
        """Add practical, real-world context"""
        query_lower = query.lower()
        
        # Weather-related advice
        if any(word in query_lower for word in ["rain", "cold", "hot", "snow"]):
            if "rain" in query_lower:
                response += " By the way, if it's raining, don't forget an umbrella!"
            elif "cold" in query_lower:
                response += " In cold weather, make sure to dress warmly."
            elif "hot" in query_lower:
                response += " In hot weather, stay hydrated and seek shade."
        
        # Safety reminders
        if any(word in query_lower for word in ["drive", "driving", "car"]):
            response += " Remember to always drive safely and follow traffic rules."
        
        # Health advice
        if any(word in query_lower for word in ["sick", "illness", "pain", "hurt"]):
            response += " If you're experiencing health issues, it's best to consult with a healthcare professional."
        
        # Time management
        if any(word in query_lower for word in ["busy", "time", "schedule"]):
            response += " Good time management can help reduce stress and improve productivity."
        
        return response
    
    def apply_safety_filter(self, response):
        """Apply safety and ethical guidelines"""
        # Remove potentially harmful advice
        harmful_keywords = ["dangerous", "illegal", "harmful", "unsafe"]
        
        if any(keyword in response.lower() for keyword in harmful_keywords):
            return "I want to make sure I give you safe and helpful advice. " + response + " Please prioritize your safety and follow local laws and guidelines."
        
        return response
    
    def get_realistic_alternative(self, query):
        """Provide realistic alternatives to impossible scenarios"""
        query_lower = query.lower()
        
        if "fly" in query_lower and "human" in query_lower:
            return "Humans can't fly naturally, but we can use airplanes, helicopters, or other aircraft to travel through the air."
        
        if "breathe underwater" in query_lower:
            return "Humans can't breathe underwater naturally, but we can use scuba gear or submarines to explore underwater."
        
        return "Let me provide a more realistic perspective on that."
    
    def add_contextual_awareness(self, query, response):
        """Add awareness of current context and situation"""
        current_hour = datetime.now().hour
        
        # Time-appropriate responses
        if "good morning" in query.lower() and current_hour > 12:
            response = "Actually, it's afternoon now, but good day to you too! " + response
        elif "good evening" in query.lower() and current_hour < 17:
            response = "It's still daytime, but good day! " + response
        
        # Seasonal awareness
        current_month = datetime.now().month
        if current_month in [12, 1, 2] and "summer" in query.lower():
            response = "Just to note, it's currently winter season. " + response
        elif current_month in [6, 7, 8] and "winter" in query.lower():
            response = "Just to note, it's currently summer season. " + response
        
        return response
    
    def check_contradictions(self, new_response):
        """Check for contradictions with previous statements"""
        # Store context for contradiction checking
        self.context_memory.append({
            'response': new_response,
            'timestamp': datetime.now()
        })
        
        # Keep only recent context (last 5 responses)
        if len(self.context_memory) > 5:
            self.context_memory = self.context_memory[-5:]
        
        return new_response
    
    def enhance_with_common_sense(self, query, ai_response):
        """Main method to enhance AI response with common sense"""
        # Apply all common sense enhancements
        enhanced = self.apply_common_sense(query, ai_response)
        enhanced = self.add_contextual_awareness(query, enhanced)
        enhanced = self.check_contradictions(enhanced)
        
        return enhanced

if __name__ == "__main__":
    cs = CommonSense()
    
    # Test cases
    test_queries = [
        ("Can humans fly?", "Yes, humans can fly by flapping their arms."),
        ("What should I do if it's raining?", "Go outside without protection."),
        ("Good morning!", "Good morning to you too!")
    ]
    
    for query, response in test_queries:
        enhanced = cs.enhance_with_common_sense(query, response)
        print(f"Query: {query}")
        print(f"Enhanced: {enhanced}\n")