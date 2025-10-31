import pygame
import os
import time
import re
import random
from gtts import gTTS
import pyttsx3

class HumanVoice:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.voice_sample = r"C:\Users\shaik\Downloads\voice\download.wav"
        self.setup_human_voice()
    
    def setup_human_voice(self):
        """Setup human-like voice with natural settings"""
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            
            # Find most natural female voice
            for voice in voices:
                if any(word in voice.name.lower() for word in ['zira', 'hazel', 'eva']):
                    self.engine.setProperty('voice', voice.id)
                    break
            
            # Human-like speech settings
            self.engine.setProperty('rate', 175)  # Natural conversational speed
            self.engine.setProperty('volume', 0.95)
            
        except Exception as e:
            print(f"Voice setup error: {e}")
            self.engine = None
    
    def speak(self, text):
        """Human-like speech with natural flow"""
        # Add human conversational elements
        humanized_text = self.humanize_speech(text)
        
        # Add natural pauses and breathing
        speech_segments = self.add_natural_pauses(humanized_text)
        
        # Speak with human-like delivery
        return self.deliver_human_speech(speech_segments)
    
    def humanize_speech(self, text):
        """Make text more conversational and human-like"""
        # Add conversational fillers occasionally
        fillers = ["well", "you know", "actually", "I mean", "so"]
        
        # Add natural conversation starters
        if random.random() < 0.3:  # 30% chance
            starters = ["Well, ", "So, ", "Actually, ", "You know, "]
            text = random.choice(starters) + text.lower()
        
        # Add thinking pauses for complex responses
        if len(text) > 100:
            thinking_words = ["hmm", "let me think", "well"]
            if random.random() < 0.4:  # 40% chance for long responses
                text = random.choice(thinking_words) + "... " + text
        
        # Make responses more conversational
        text = text.replace("I am", "I'm")
        text = text.replace("you are", "you're")
        text = text.replace("cannot", "can't")
        text = text.replace("do not", "don't")
        text = text.replace("will not", "won't")
        
        # Add natural emphasis
        text = re.sub(r'\b(very|really|quite|extremely)\b', r'\\1', text)
        
        return text
    
    def add_natural_pauses(self, text):
        """Add natural breathing and thinking pauses"""
        segments = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                # Add breathing pause before longer sentences
                if len(sentence) > 50 and i > 0:
                    segments.append(("pause", "breath"))
                
                # Add thinking pause for complex ideas
                if any(word in sentence.lower() for word in ['because', 'however', 'therefore', 'although']):
                    segments.append(("pause", "think"))
                
                segments.append(("speech", sentence.strip()))
                
                # Add natural pause between sentences
                if i < len(sentences) - 1:
                    segments.append(("pause", "sentence"))
        
        return segments
    
    def deliver_human_speech(self, segments):
        """Deliver speech with human-like timing and pauses"""
        try:
            for segment_type, content in segments:
                if segment_type == "pause":
                    self.add_human_pause(content)
                elif segment_type == "speech":
                    self.speak_naturally(content)
            
            return True
            
        except Exception as e:
            print(f"Human speech error: {e}")
            return False
    
    def add_human_pause(self, pause_type):
        """Add natural human pauses"""
        if pause_type == "breath":
            time.sleep(0.4)  # Natural breathing pause
        elif pause_type == "think":
            time.sleep(0.6)  # Thinking pause
        elif pause_type == "sentence":
            time.sleep(0.3)  # Between sentences
    
    def speak_naturally(self, text):
        """Speak with natural human-like delivery"""
        try:
            # Adjust speech rate based on content
            if self.engine:
                # Slower for important information
                if any(word in text.lower() for word in ['important', 'remember', 'careful', 'attention']):
                    self.engine.setProperty('rate', 160)
                # Faster for casual conversation
                elif any(word in text.lower() for word in ['hello', 'hi', 'okay', 'sure', 'yes']):
                    self.engine.setProperty('rate', 190)
                else:
                    self.engine.setProperty('rate', 175)  # Normal conversational
                
                # Add slight volume variation for naturalness
                volume = 0.9 + (random.random() * 0.1)  # 0.9 to 1.0
                self.engine.setProperty('volume', volume)
                
                self.engine.say(text)
                self.engine.runAndWait()
                return True
            
            # Fallback to gTTS with human-like settings
            return self.natural_gtts(text)
            
        except Exception as e:
            print(f"Natural speech error: {e}")
            return False
    
    def natural_gtts(self, text):
        """Natural gTTS with human-like characteristics"""
        try:
            # Use gTTS with natural settings
            tts = gTTS(
                text=text,
                lang='en',
                slow=False,
                tld='com'  # More natural voice
            )
            
            temp_file = f"human_voice_{int(time.time())}.mp3"
            tts.save(temp_file)
            
            if os.path.exists(temp_file):
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(50)
                
                try:
                    os.unlink(temp_file)
                except:
                    pass
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Natural gTTS error: {e}")
            return False
    
    def add_personality_to_response(self, text):
        """Add personality and human-like responses"""
        # Add emotional responses
        if "?" in text:
            responses = ["That's a great question! ", "Interesting question. ", "Let me think about that. "]
            if random.random() < 0.4:
                text = random.choice(responses) + text
        
        # Add acknowledgments
        if any(word in text.lower() for word in ['thank', 'thanks']):
            responses = ["You're welcome! ", "No problem! ", "Happy to help! "]
            if random.random() < 0.5:
                text = random.choice(responses) + text
        
        return text

if __name__ == "__main__":
    voice = HumanVoice()
    test_text = "Hello! I'm your AI assistant. How can I help you today? I'm here to answer your questions and have a natural conversation with you."
    voice.speak(test_text)