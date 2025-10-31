import random
from datetime import datetime

class PersonalitySystem:
    def __init__(self):
        self.current_personality = "friendly"
        self.personalities = {
            "friendly": {
                "greeting": ["Hello there! How can I help you today?", "Hi! Great to see you!", "Hey! What's on your mind?"],
                "response_style": "warm and welcoming",
                "traits": ["helpful", "cheerful", "supportive"],
                "speech_patterns": ["I'd love to help!", "That sounds interesting!", "Great question!"]
            },
            
            "professional": {
                "greeting": ["Good day. How may I assist you?", "Hello. What can I help you with?", "Greetings. How can I be of service?"],
                "response_style": "formal and efficient",
                "traits": ["precise", "knowledgeable", "reliable"],
                "speech_patterns": ["I can provide information on", "According to my analysis", "The optimal solution would be"]
            },
            
            "funny": {
                "greeting": ["Hey there, human! Ready for some fun?", "Hello! I promise not to make too many bad jokes... maybe.", "Hi! Warning: Dad jokes may occur."],
                "response_style": "humorous and playful",
                "traits": ["witty", "playful", "entertaining"],
                "speech_patterns": ["That reminds me of a joke...", "Funny you should ask!", "Here's a fun fact:"]
            },
            
            "wise": {
                "greeting": ["Greetings, seeker of knowledge.", "Hello. What wisdom do you seek today?", "Welcome. I sense you have questions."],
                "response_style": "thoughtful and philosophical",
                "traits": ["contemplative", "insightful", "patient"],
                "speech_patterns": ["Consider this perspective:", "In my experience,", "Wisdom suggests that"]
            },
            
            "energetic": {
                "greeting": ["HEY THERE! Ready to tackle the day?", "Hello! I'm super excited to help!", "Hi! Let's make something awesome happen!"],
                "response_style": "enthusiastic and motivating",
                "traits": ["energetic", "motivational", "optimistic"],
                "speech_patterns": ["That's AMAZING!", "Let's do this!", "You've got this!"]
            }
        }
    
    def set_personality(self, personality_name):
        """Change AI personality"""
        if personality_name.lower() in self.personalities:
            self.current_personality = personality_name.lower()
            return True
        return False
    
    def get_personality_greeting(self):
        """Get greeting based on current personality"""
        personality = self.personalities[self.current_personality]
        return random.choice(personality["greeting"])
    
    def apply_personality_to_response(self, response):
        """Apply current personality style to response"""
        personality = self.personalities[self.current_personality]
        
        # Add personality-specific speech patterns
        if random.random() < 0.3:  # 30% chance to add personality flair
            pattern = random.choice(personality["speech_patterns"])
            response = pattern + " " + response
        
        # Modify response based on personality
        if self.current_personality == "funny":
            response = self.add_humor(response)
        elif self.current_personality == "professional":
            response = self.make_professional(response)
        elif self.current_personality == "energetic":
            response = self.add_energy(response)
        elif self.current_personality == "wise":
            response = self.add_wisdom(response)
        
        return response
    
    def add_humor(self, response):
        """Add humor to response"""
        jokes = [
            " (No pun intended... okay, maybe a little intended!)",
            " Speaking of which, why don't scientists trust atoms? Because they make up everything!",
            " That's what I call a 'byte' of information! Get it? Byte? I'll see myself out...",
        ]
        
        if random.random() < 0.2:  # 20% chance for joke
            response += random.choice(jokes)
        
        # Make response more playful
        response = response.replace("I think", "I reckon")
        response = response.replace("However", "But hey")
        
        return response
    
    def make_professional(self, response):
        """Make response more professional"""
        # Add formal language
        response = response.replace("I think", "I believe")
        response = response.replace("pretty good", "quite effective")
        response = response.replace("really", "particularly")
        
        # Add professional phrases
        professional_starters = [
            "Based on available information, ",
            "According to current data, ",
            "From a professional standpoint, "
        ]
        
        if random.random() < 0.3:
            response = random.choice(professional_starters) + response.lower()
        
        return response
    
    def add_energy(self, response):
        """Add energy and enthusiasm"""
        # Add exclamation marks
        if not response.endswith(('!', '?', '.')):
            response += "!"
        
        # Add energetic words
        response = response.replace("good", "AWESOME")
        response = response.replace("yes", "ABSOLUTELY YES")
        response = response.replace("I can", "I'd LOVE to")
        
        energetic_additions = [
            " Let's make it happen!",
            " This is going to be great!",
            " I'm excited to help with this!"
        ]
        
        if random.random() < 0.4:
            response += random.choice(energetic_additions)
        
        return response
    
    def add_wisdom(self, response):
        """Add wisdom and thoughtfulness"""
        wise_starters = [
            "In my contemplation, ",
            "Through careful consideration, ",
            "Reflecting on this matter, "
        ]
        
        wise_endings = [
            " Such is the nature of knowledge.",
            " This requires thoughtful consideration.",
            " Wisdom comes through understanding."
        ]
        
        if random.random() < 0.3:
            response = random.choice(wise_starters) + response.lower()
        
        if random.random() < 0.2:
            response += random.choice(wise_endings)
        
        return response
    
    def get_available_personalities(self):
        """Get list of available personalities"""
        return list(self.personalities.keys())
    
    def get_current_personality_info(self):
        """Get information about current personality"""
        personality = self.personalities[self.current_personality]
        return {
            "name": self.current_personality,
            "style": personality["response_style"],
            "traits": personality["traits"]
        }