import re
from datetime import datetime

class EmotionDetector:
    def __init__(self):
        self.emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'awesome', 'wonderful', 'amazing', 'fantastic', 'good', 'smile', 'laugh'],
            'sad': ['sad', 'depressed', 'down', 'upset', 'cry', 'terrible', 'awful', 'bad', 'disappointed', 'hurt'],
            'angry': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'hate', 'stupid', 'idiot', 'damn'],
            'anxious': ['worried', 'nervous', 'scared', 'afraid', 'anxious', 'stress', 'panic', 'fear'],
            'confused': ['confused', 'lost', 'dont understand', "don't get", 'unclear', 'what', 'how', 'why'],
            'tired': ['tired', 'exhausted', 'sleepy', 'fatigue', 'worn out', 'drained'],
            'excited': ['excited', 'thrilled', 'pumped', 'eager', 'cant wait', "can't wait"]
        }
    
    def detect_emotion(self, text):
        """Detect primary emotion from user text"""
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = emotion_scores[primary_emotion] / len(text.split()) * 10
            return primary_emotion, min(confidence, 1.0)
        
        return 'neutral', 0.5
    
    def get_empathetic_response(self, emotion, confidence):
        """Generate empathetic response based on emotion"""
        responses = {
            'happy': [
                "That's wonderful to hear! I'm glad you're feeling good.",
                "Your happiness is contagious! What's making you so happy?",
                "I love your positive energy! Keep that smile going."
            ],
            'sad': [
                "I'm sorry you're feeling down. I'm here to listen if you want to talk.",
                "It sounds like you're going through a tough time. How can I help?",
                "I understand you're feeling sad. Sometimes talking helps."
            ],
            'angry': [
                "I can sense you're frustrated. Let's work through this together.",
                "It sounds like something really bothered you. Want to tell me about it?",
                "I hear your frustration. Let me try to help you with this."
            ],
            'anxious': [
                "I can tell you're feeling worried. Let's take this step by step.",
                "It's okay to feel anxious. I'm here to help you through this.",
                "Take a deep breath. We can figure this out together."
            ],
            'confused': [
                "I can see this is confusing. Let me try to explain it more clearly.",
                "No worries about being confused. Let's break this down together.",
                "I understand this might be unclear. Let me help clarify."
            ],
            'tired': [
                "You sound exhausted. Make sure you're getting enough rest.",
                "It seems like you need a break. Take care of yourself.",
                "Being tired can make everything harder. How can I help?"
            ],
            'excited': [
                "I can feel your excitement! That's amazing!",
                "Your enthusiasm is wonderful! Tell me more!",
                "I love your energy! What's got you so excited?"
            ]
        }
        
        import random
        if emotion in responses:
            return random.choice(responses[emotion])
        
        return "I'm here to help you with whatever you need."