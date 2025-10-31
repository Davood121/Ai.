import json
import os
from datetime import datetime

class LearningSystem:
    def __init__(self):
        self.knowledge_file = "ai_learned_knowledge.json"
        self.user_preferences = "user_preferences.json"
        self.conversation_patterns = "conversation_patterns.json"
        self.load_learned_data()
    
    def load_learned_data(self):
        """Load previously learned information"""
        try:
            with open(self.knowledge_file, 'r') as f:
                self.learned_knowledge = json.load(f)
        except:
            self.learned_knowledge = {}
        
        try:
            with open(self.user_preferences, 'r') as f:
                self.preferences = json.load(f)
        except:
            self.preferences = {}
        
        try:
            with open(self.conversation_patterns, 'r') as f:
                self.patterns = json.load(f)
        except:
            self.patterns = {}
    
    def learn_from_conversation(self, user_input, ai_response, user_feedback=None):
        """Learn from each conversation"""
        timestamp = datetime.now().isoformat()
        
        # Learn user preferences
        self.extract_preferences(user_input)
        
        # Learn conversation patterns
        self.analyze_conversation_pattern(user_input, ai_response)
        
        # Store successful responses
        if user_feedback == "good" or any(word in user_input.lower() for word in ['thanks', 'good', 'great', 'perfect']):
            self.store_successful_response(user_input, ai_response)
        
        self.save_learned_data()
    
    def extract_preferences(self, user_input):
        """Extract user preferences from conversation"""
        text = user_input.lower()
        
        # Favorite things
        if "my favorite" in text or "i like" in text or "i love" in text:
            if "color" in text:
                colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black', 'white']
                for color in colors:
                    if color in text:
                        self.preferences['favorite_color'] = color
            
            if "food" in text:
                foods = ['pizza', 'burger', 'pasta', 'rice', 'chicken', 'fish', 'salad']
                for food in foods:
                    if food in text:
                        self.preferences['favorite_food'] = food
        
        # Personal info
        if "my name is" in text:
            name = text.split("my name is")[-1].strip().split()[0]
            self.preferences['name'] = name
        
        if "i am from" in text or "i live in" in text:
            location = text.split("from" if "from" in text else "in")[-1].strip()
            self.preferences['location'] = location
    
    def analyze_conversation_pattern(self, user_input, ai_response):
        """Analyze and learn conversation patterns"""
        input_type = self.classify_input_type(user_input)
        
        if input_type not in self.patterns:
            self.patterns[input_type] = []
        
        self.patterns[input_type].append({
            'input': user_input,
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only recent patterns (last 10)
        if len(self.patterns[input_type]) > 10:
            self.patterns[input_type] = self.patterns[input_type][-10:]
    
    def classify_input_type(self, user_input):
        """Classify the type of user input"""
        text = user_input.lower()
        
        if any(word in text for word in ['hello', 'hi', 'hey', 'good morning']):
            return 'greeting'
        elif '?' in text:
            return 'question'
        elif any(word in text for word in ['thanks', 'thank you', 'bye', 'goodbye']):
            return 'closing'
        elif any(word in text for word in ['help', 'can you', 'please']):
            return 'request'
        else:
            return 'general'
    
    def store_successful_response(self, user_input, ai_response):
        """Store responses that worked well"""
        key = user_input.lower()[:50]  # Use first 50 chars as key
        
        if key not in self.learned_knowledge:
            self.learned_knowledge[key] = []
        
        self.learned_knowledge[key].append({
            'response': ai_response,
            'success_count': 1,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_personalized_response(self, user_input):
        """Get personalized response based on learned data"""
        # Check for similar previous successful responses
        key = user_input.lower()[:50]
        
        if key in self.learned_knowledge:
            best_response = max(self.learned_knowledge[key], 
                              key=lambda x: x.get('success_count', 0))
            return best_response['response']
        
        # Use preferences to personalize
        if self.preferences.get('name'):
            return f"Hi {self.preferences['name']}! " + self.get_contextual_response(user_input)
        
        return None
    
    def get_contextual_response(self, user_input):
        """Get response based on learned patterns"""
        input_type = self.classify_input_type(user_input)
        
        if input_type in self.patterns and self.patterns[input_type]:
            # Use most recent successful pattern
            recent_pattern = self.patterns[input_type][-1]
            return f"Based on our previous conversations, {recent_pattern['response']}"
        
        return "Let me help you with that."
    
    def save_learned_data(self):
        """Save all learned data to files"""
        try:
            with open(self.knowledge_file, 'w') as f:
                json.dump(self.learned_knowledge, f, indent=2)
            
            with open(self.user_preferences, 'w') as f:
                json.dump(self.preferences, f, indent=2)
            
            with open(self.conversation_patterns, 'w') as f:
                json.dump(self.patterns, f, indent=2)
        except Exception as e:
            print(f"Error saving learned data: {e}")
    
    def get_learning_stats(self):
        """Get statistics about what AI has learned"""
        return {
            'total_knowledge_items': len(self.learned_knowledge),
            'user_preferences': len(self.preferences),
            'conversation_patterns': len(self.patterns),
            'preferences': self.preferences
        }