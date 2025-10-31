import json
import os
from datetime import datetime, timedelta

class ContextMemory:
    def __init__(self):
        self.memory_file = "context_memory.json"
        self.session_memory = []
        self.long_term_memory = {}
        self.load_memory()
    
    def load_memory(self):
        """Load long-term memory from file"""
        try:
            with open(self.memory_file, 'r') as f:
                self.long_term_memory = json.load(f)
        except:
            self.long_term_memory = {
                "conversations": [],
                "user_info": {},
                "topics": {},
                "relationships": {}
            }
    
    def save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.long_term_memory, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def add_to_session_memory(self, user_input, ai_response):
        """Add conversation to current session memory"""
        memory_item = {
            "user_input": user_input,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "session_id": self.get_current_session_id()
        }
        
        self.session_memory.append(memory_item)
        
        # Keep session memory manageable (last 20 exchanges)
        if len(self.session_memory) > 20:
            self.session_memory = self.session_memory[-20:]
    
    def add_to_long_term_memory(self, user_input, ai_response):
        """Add important conversations to long-term memory"""
        memory_item = {
            "user_input": user_input,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "importance": self.calculate_importance(user_input)
        }
        
        self.long_term_memory["conversations"].append(memory_item)
        
        # Extract and store important information
        self.extract_user_info(user_input)
        self.extract_topics(user_input)
        
        # Keep only important memories (last 100)
        if len(self.long_term_memory["conversations"]) > 100:
            # Sort by importance and keep top 100
            sorted_memories = sorted(
                self.long_term_memory["conversations"],
                key=lambda x: x.get("importance", 0),
                reverse=True
            )
            self.long_term_memory["conversations"] = sorted_memories[:100]
        
        self.save_memory()
    
    def calculate_importance(self, user_input):
        """Calculate importance score of conversation"""
        importance = 0
        text = user_input.lower()
        
        # Personal information is important
        if any(phrase in text for phrase in ["my name", "i am", "i live", "my age", "my job"]):
            importance += 5
        
        # Questions are moderately important
        if "?" in text:
            importance += 2
        
        # Emotional content is important
        if any(word in text for word in ["love", "hate", "sad", "happy", "angry", "excited"]):
            importance += 3
        
        # Requests for help are important
        if any(word in text for word in ["help", "please", "can you", "need"]):
            importance += 2
        
        # Length indicates complexity/importance
        if len(text.split()) > 10:
            importance += 1
        
        return importance
    
    def extract_user_info(self, user_input):
        """Extract and store user information"""
        text = user_input.lower()
        
        # Extract name
        if "my name is" in text:
            name = text.split("my name is")[-1].strip().split()[0]
            self.long_term_memory["user_info"]["name"] = name
        
        # Extract location
        if "i live in" in text or "i am from" in text:
            location = text.split("in" if "in" in text else "from")[-1].strip()
            self.long_term_memory["user_info"]["location"] = location
        
        # Extract age
        if "i am" in text and "years old" in text:
            try:
                age = int([word for word in text.split() if word.isdigit()][0])
                self.long_term_memory["user_info"]["age"] = age
            except:
                pass
        
        # Extract interests
        if "i like" in text or "i love" in text:
            interest = text.split("like" if "like" in text else "love")[-1].strip()
            if "interests" not in self.long_term_memory["user_info"]:
                self.long_term_memory["user_info"]["interests"] = []
            self.long_term_memory["user_info"]["interests"].append(interest)
    
    def extract_topics(self, user_input):
        """Extract and track conversation topics"""
        # Simple topic extraction based on keywords
        topics = {
            "technology": ["computer", "software", "ai", "robot", "internet", "phone"],
            "science": ["physics", "chemistry", "biology", "space", "research"],
            "entertainment": ["movie", "music", "game", "book", "tv", "show"],
            "food": ["eat", "food", "cook", "recipe", "restaurant", "meal"],
            "travel": ["travel", "trip", "vacation", "country", "city", "visit"],
            "work": ["job", "work", "career", "office", "business", "company"],
            "health": ["health", "exercise", "doctor", "medicine", "fitness"],
            "education": ["school", "study", "learn", "university", "course"]
        }
        
        text = user_input.lower()
        for topic, keywords in topics.items():
            if any(keyword in text for keyword in keywords):
                if topic not in self.long_term_memory["topics"]:
                    self.long_term_memory["topics"][topic] = 0
                self.long_term_memory["topics"][topic] += 1
    
    def get_relevant_context(self, current_input):
        """Get relevant context for current conversation"""
        context = []
        
        # Add recent session memory
        if self.session_memory:
            context.append("Recent conversation:")
            for memory in self.session_memory[-3:]:  # Last 3 exchanges
                context.append(f"You: {memory['user_input']}")
                context.append(f"AI: {memory['ai_response']}")
        
        # Add relevant user info
        if self.long_term_memory["user_info"]:
            user_info = []
            if "name" in self.long_term_memory["user_info"]:
                user_info.append(f"User's name: {self.long_term_memory['user_info']['name']}")
            if "location" in self.long_term_memory["user_info"]:
                user_info.append(f"Location: {self.long_term_memory['user_info']['location']}")
            
            if user_info:
                context.append("User information: " + ", ".join(user_info))
        
        return "\n".join(context) if context else ""
    
    def get_current_session_id(self):
        """Get current session identifier"""
        return datetime.now().strftime("%Y%m%d_%H")
    
    def search_memory(self, query):
        """Search through memory for relevant information"""
        results = []
        query_lower = query.lower()
        
        # Search conversations
        for conv in self.long_term_memory["conversations"]:
            if query_lower in conv["user_input"].lower() or query_lower in conv["ai_response"].lower():
                results.append(conv)
        
        return results[-5:]  # Return last 5 relevant results
    
    def get_memory_stats(self):
        """Get memory statistics"""
        return {
            "session_conversations": len(self.session_memory),
            "total_conversations": len(self.long_term_memory["conversations"]),
            "user_info_items": len(self.long_term_memory["user_info"]),
            "topics_discussed": len(self.long_term_memory["topics"]),
            "most_discussed_topic": max(self.long_term_memory["topics"].items(), key=lambda x: x[1])[0] if self.long_term_memory["topics"] else "None"
        }