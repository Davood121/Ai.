# -*- coding: utf-8 -*-
"""
Advanced AI Assistant System v2.0
Upgraded with enhanced performance, better error handling, and advanced features
"""

import ollama
import threading
import json
import os
import time
import asyncio
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache, wraps
from typing import Dict, List, Optional, Tuple

# Core AI modules
from human_voice import HumanVoice
from common_sense import CommonSense
from emotion_detector import EmotionDetector
from learning_system import LearningSystem
from personality_system import PersonalitySystem
from context_memory import ContextMemory
from web_search_live import LiveWebSearch
from news_system import NewsSystem


class TerminalAI:
    """Advanced AI Assistant with enhanced capabilities and performance optimizations"""
    
    def __init__(self):
        # Core configuration
        self.knowledge_file = "ai_knowledge.json"
        self.conversation_context = []
        self.conversation_memory = []
        self.current_language = "english"
        self.debug_mode = False
        
        # Initialize core AI components
        self._initialize_ai_components()
        
        # Performance optimizations
        self._setup_performance_optimizations()
        
        # Load initial data
        self._load_initial_data()
        
        print("🤖 Advanced AI System v2.0 Initialized Successfully!")
    
    def _initialize_ai_components(self):
        """Initialize all AI components with error handling"""
        try:
            self.voice = HumanVoice()
            self.common_sense = CommonSense()
            self.emotion_detector = EmotionDetector()
            self.learning_system = LearningSystem()
            self.personality_system = PersonalitySystem()
            self.context_memory = ContextMemory()
            self.web_search = LiveWebSearch()
            self.news_system = NewsSystem()
            
            # Translation service (simplified)
            self.translation_service = self._create_translation_service()
            
        except Exception as e:
            print(f"⚠️ Component initialization error: {e}")
    
    def _create_translation_service(self):
        """Create simplified translation service"""
        class SimpleTranslation:
            def __init__(self):
                self.current_language = "english"
            
            def translate_response(self, text, target_lang):
                # Simplified translation - in real implementation, use proper translation API
                return text
        
        return SimpleTranslation()
    
    def _setup_performance_optimizations(self):
        """Setup performance optimizations"""
        self.executor = ThreadPoolExecutor(max_workers=6, thread_name_prefix="AI-Worker")
        self.response_cache = {}
        self.search_cache = {}
        self.cache_ttl = 3600  # 1 hour
        self.last_cache_clear = datetime.now()
        self.max_cache_size = 1000
        
        # Performance metrics
        self.performance_stats = {
            "total_queries": 0,
            "cache_hits": 0,
            "search_requests": 0,
            "average_response_time": 0
        }
    
    def _load_initial_data(self):
        """Load initial knowledge and data"""
        self.load_knowledge()
        self._clear_old_cache()

    def speak(self, text, language=None):
        """Enhanced voice output with performance optimization"""
        if not text or len(text.strip()) == 0:
            return
        
        # Optimize text for speech
        optimized_text = self._optimize_text_for_speech(text)
        
        # Run in background thread to avoid blocking
        future = self.executor.submit(self.voice.speak, optimized_text)
        return future
    
    def _optimize_text_for_speech(self, text: str) -> str:
        """Optimize text for better speech synthesis"""
        # Remove excessive punctuation
        text = text.replace("...", ". ")
        text = text.replace("!!", "!")
        text = text.replace("??", "?")
        
        # Limit length for better speech flow
        if len(text) > 500:
            sentences = text.split(". ")
            text = ". ".join(sentences[:3]) + "."
        
        return text

    def _clear_old_cache(self):
        """Enhanced cache management with size limits"""
        now = datetime.now()
        
        # Clear by TTL
        if (now - self.last_cache_clear).total_seconds() > self.cache_ttl:
            self.response_cache.clear()
            self.search_cache.clear()
            self.last_cache_clear = now
            print("🗑️ Cache cleared (TTL expired)")
        
        # Clear by size limit
        if len(self.response_cache) > self.max_cache_size:
            # Keep only recent 50% of cache
            items = list(self.response_cache.items())
            self.response_cache = dict(items[-self.max_cache_size//2:])
            print("🗑️ Cache optimized (size limit)")
    
    def get_performance_stats(self) -> Dict:
        """Get current performance statistics"""
        cache_hit_rate = (self.performance_stats["cache_hits"] / 
                         max(self.performance_stats["total_queries"], 1)) * 100
        
        return {
            **self.performance_stats,
            "cache_hit_rate": f"{cache_hit_rate:.1f}%",
            "cache_size": len(self.response_cache),
            "search_cache_size": len(self.search_cache)
        }

    def search_web(self, query: str) -> str:
        """Enhanced web search with intelligent caching and optimization"""
        start_time = time.time()
        
        # Clean and optimize query
        clean_query = self._clean_search_query(query)
        cache_key = clean_query.lower()[:100]  # Limit key length
        
        # Check cache first
        if cache_key in self.search_cache:
            self.performance_stats["cache_hits"] += 1
            return self.search_cache[cache_key]
        
        # Perform search
        try:
            self.performance_stats["search_requests"] += 1
            result = self.web_search.search_web(clean_query)
            
            # Cache successful results
            if result and "error" not in result.lower():
                self.search_cache[cache_key] = result
            
            # Update performance stats
            search_time = time.time() - start_time
            self._update_response_time(search_time)
            
            return result
            
        except Exception as e:
            print(f"⚠️ Search error: {e}")
            return f"I couldn't search for '{clean_query}' right now, but I can provide general information."
    
    def _clean_search_query(self, query: str) -> str:
        """Clean and optimize search query"""
        # Extract main question from context
        if "Current question:" in query:
            query = query.split("Current question:")[-1].strip()
        
        # Remove conversation context
        if "Conversation context:" in query:
            query = query.split("Conversation context:")[0].strip()
        
        # Limit query length
        words = query.split()
        if len(words) > 10:
            query = " ".join(words[:10])
        
        return query.strip()
    
    def _update_response_time(self, response_time: float):
        """Update average response time statistics"""
        current_avg = self.performance_stats["average_response_time"]
        total_queries = self.performance_stats["total_queries"]
        
        if total_queries == 0:
            self.performance_stats["average_response_time"] = response_time
        else:
            # Calculate rolling average
            self.performance_stats["average_response_time"] = (
                (current_avg * total_queries + response_time) / (total_queries + 1)
            )
    

    
    def get_ai_response(self, prompt: str, context: str = "", show_thinking: bool = False) -> str:
        """Enhanced AI response with better error handling and optimization"""
        start_time = time.time()
        
        try:
            # Update query count
            self.performance_stats["total_queries"] += 1
            
            # Check cache first
            cache_key = self._generate_cache_key(prompt, context)
            if cache_key in self.response_cache:
                self.performance_stats["cache_hits"] += 1
                return self.response_cache[cache_key]
            
            # Prepare optimized prompt
            system_prompt = self._get_system_prompt()
            full_prompt = self._prepare_full_prompt(prompt, context)
            
            # Get AI response with timeout
            response = self._call_ollama_with_timeout(system_prompt, full_prompt)
            
            if response:
                # Cache successful response
                self.response_cache[cache_key] = response
                
                # Update performance stats
                response_time = time.time() - start_time
                self._update_response_time(response_time)
                
                return response
            else:
                return self._get_fallback_response(prompt)
                
        except Exception as e:
            print(f"⚠️ AI Response Error: {e}")
            return self._get_fallback_response(prompt)
    
    def _generate_cache_key(self, prompt: str, context: str) -> str:
        """Generate optimized cache key"""
        combined = f"{prompt}:{context}"
        return combined.lower()[:100]  # Limit key length
    
    def _get_system_prompt(self) -> str:
        """Get optimized system prompt based on current personality"""
        personality_info = self.personality_system.get_current_personality_info()
        
        base_prompt = (
            "You are a helpful AI assistant. Respond naturally and conversationally. "
            "For greetings, respond with simple greetings. For questions, provide clear and accurate answers. "
        )
        
        personality_prompt = f"Your personality is {personality_info['name']} - {personality_info['style']}. "
        
        return base_prompt + personality_prompt
    
    def _prepare_full_prompt(self, prompt: str, context: str) -> str:
        """Prepare optimized full prompt"""
        if context and len(context.strip()) > 0:
            # Limit context length to prevent token overflow
            if len(context) > 1000:
                context = context[:1000] + "..."
            
            return (
                f"Based on this information: {context}\n\n"
                f"Question: {prompt}\n\n"
                f"Provide a helpful response in 2-3 sentences."
            )
        else:
            return prompt
    
    def _call_ollama_with_timeout(self, system_prompt: str, full_prompt: str, timeout: int = 30) -> Optional[str]:
        """Call Ollama with timeout handling"""
        try:
            response = ollama.chat(
                model='llama3.2',
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': full_prompt}
                ],
                stream=False,
                options={'timeout': timeout}
            )
            
            return response['message']['content'].strip()
            
        except Exception as e:
            print(f"⚠️ Ollama call failed: {e}")
            return None
    
    def _get_fallback_response(self, prompt: str) -> str:
        """Get fallback response when AI is unavailable"""
        fallback_responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "how are you": "I'm doing well, thank you! How are you?",
            "thanks": "You're welcome! Happy to help!",
            "bye": "Goodbye! Have a great day!"
        }
        
        prompt_lower = prompt.lower().strip()
        
        for key, response in fallback_responses.items():
            if key in prompt_lower:
                return response
        
        return "I'm having trouble processing that right now. Could you please try again or rephrase your question?"
    
    def summarize(self, text: str) -> str:
        """Enhanced text summarization"""
        if len(text) < 100:
            return text  # No need to summarize short text
        
        prompt = f"Summarize this concisely in 2-3 sentences: {text[:1000]}"  # Limit input length
        return self.get_ai_response(prompt)
    
    def save_to_memory(self, query: str, response: str):
        """Enhanced memory saving with error handling"""
        try:
            # Save to conversation memory
            self.conversation_memory.append({
                'question': query,
                'answer': response,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep memory manageable
            if len(self.conversation_memory) > 15:
                self.conversation_memory = self.conversation_memory[-10:]
                
        except Exception as e:
            if self.debug_mode:
                print(f"⚠️ Memory save error: {e}")
    
    def get_recent_memory(self) -> str:
        """Get recent conversation memory"""
        try:
            if hasattr(self, 'context_memory'):
                return self.context_memory.get_relevant_context("general")
            else:
                # Fallback to conversation context
                if self.conversation_context:
                    return self.conversation_context[-1]
                return ""
        except Exception as e:
            if self.debug_mode:
                print(f"⚠️ Memory retrieval error: {e}")
            return ""
    
    def resolve_pronouns(self, query: str) -> str:
        """Enhanced pronoun resolution with better context handling"""
        try:
            # Get recent conversation context
            if len(self.conversation_context) == 0:
                return query
            
            # Check for pronouns
            pronouns = {'it', 'that', 'this', 'they', 'them', 'he', 'she', 'his', 'her'}
            query_words = set(query.lower().split())
            
            if pronouns.intersection(query_words):
                # Get last relevant context
                recent_context = self.conversation_context[-1] if self.conversation_context else ""
                if recent_context:
                    return f"Previous context: {recent_context}\nCurrent question: {query}"
            
            return query
            
        except Exception as e:
            if self.debug_mode:
                print(f"⚠️ Pronoun resolution error: {e}")
            return query
    
    def load_knowledge(self):
        """Enhanced knowledge loading with error handling"""
        try:
            if os.path.exists(self.knowledge_file):
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    self.knowledge = json.load(f)
                print(f"📚 Loaded {len(self.knowledge)} knowledge items")
            else:
                self.knowledge = {}
                print("📚 Initialized new knowledge base")
        except Exception as e:
            print(f"⚠️ Knowledge loading error: {e}")
            self.knowledge = {}
    
    def save_knowledge(self, query: str, answer: str):
        """Enhanced knowledge saving with error handling"""
        try:
            key = query.lower()[:100]  # Limit key length
            self.knowledge[key] = {
                'answer': answer,
                'timestamp': datetime.now().isoformat(),
                'usage_count': self.knowledge.get(key, {}).get('usage_count', 0) + 1
            }
            
            # Save to file with error handling
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            if self.debug_mode:
                print(f"⚠️ Knowledge save error: {e}")
    
    def needs_search(self, query: str) -> bool:
        """Enhanced intelligent search decision with better accuracy"""
        query_lower = query.lower().strip()
        
        # Immediate skip patterns (high confidence)
        immediate_skip = [
            'hello', 'hi', 'hey', 'thanks', 'thank you', 'bye', 'goodbye',
            'how are you', 'what can you do', 'who are you', 'good morning',
            'good evening', 'nice', 'great', 'okay', 'yes', 'no', 'sure',
            'alright', 'fine', 'cool', 'awesome', 'perfect'
        ]
        
        if any(skip in query_lower for skip in immediate_skip):
            return False
        
        # Command-based queries (don't search)
        command_patterns = [
            'personality', 'memory stats', 'voice test', 'breaking news',
            'news', 'search live', 'ask me a question', 'quiz me'
        ]
        
        if any(cmd in query_lower for cmd in command_patterns):
            return False
        
        # High-priority search triggers (always search)
        priority_triggers = [
            'current', 'latest', 'recent', 'today', 'now', '2024', '2025',
            'breaking', 'live', 'real-time', 'up-to-date'
        ]
        
        if any(trigger in query_lower for trigger in priority_triggers):
            return True
        
        # Specific information requests (search)
        info_requests = [
            'price of', 'cost of', 'statistics', 'population', 'rate',
            'weather in', 'temperature', 'forecast', 'news about',
            'best colleges', 'best hospitals', 'best restaurants',
            'deaths in', 'mortality', 'crime rate', 'happened in'
        ]
        
        if any(req in query_lower for req in info_requests):
            return True
        
        # Location-based queries (search)
        location_indicators = ['near me', 'in my area', 'pincode', 'pin code']
        if any(loc in query_lower for loc in location_indicators):
            return True
        
        # Basic knowledge (don't search)
        basic_knowledge = [
            'what is love', 'what is life', 'what is happiness',
            'what is water', 'what is fire', 'what is human',
            'bones in human', 'human bones'
        ]
        
        if any(basic in query_lower for basic in basic_knowledge):
            return False
        
        # Default: search for questions, don't search for statements
        return '?' in query or query_lower.startswith(('what', 'how', 'when', 'where', 'why', 'who'))
    
    def extract_pincode_from_query(self, query: str) -> Optional[str]:
        """Extract pincode from query with validation"""
        import re
        pincode_match = re.search(r'\b\d{6}\b', query)
        if pincode_match:
            pincode = pincode_match.group()
            # Basic validation for Indian pincodes
            if pincode.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')):
                return pincode
        return None
    
    def enhance_query_with_location(self, query: str) -> Tuple[str, Optional[Dict]]:
        """Enhanced location-based query optimization"""
        pincode = self.extract_pincode_from_query(query)
        if pincode:
            # Simplified location enhancement without external dependencies
            base_query = query.replace(f"pin code {pincode}", "").replace(f"pincode {pincode}", "")
            base_query = base_query.replace("near me", "").strip()
            
            # Create location-enhanced query
            enhanced_query = f"{base_query} near {pincode} India"
            location_info = {"pincode": pincode, "enhanced": True}
            
            return enhanced_query, location_info
        
        return query, None
    
    def smart_response(self, query: str) -> str:
        """Enhanced intelligent response system with optimized performance"""
        start_time = time.time()
        
        try:
            # Determine if search is needed
            if self.needs_search(query):
                return self._handle_search_response(query, start_time)
            else:
                return self._handle_direct_response(query, start_time)
                
        except Exception as e:
            print(f"⚠️ Smart response error: {e}")
            return self._get_fallback_response(query)
    
    def _handle_search_response(self, query: str, start_time: float) -> str:
        """Handle responses that require web search"""
        print("🔍 Searching for latest information...")
        
        # Enhance query with location if needed
        enhanced_query, location_info = self.enhance_query_with_location(query)
        
        if location_info and self.debug_mode:
            print(f"📍 Enhanced query: {enhanced_query}")
        
        # Perform search
        search_results = self.search_web(enhanced_query)
        
        if not search_results or "error" in search_results.lower():
            print("⚠️ Search failed, using AI knowledge")
            return self._handle_direct_response(query, start_time)
        
        # Prepare context-aware prompt
        enhanced_prompt = self._create_search_prompt(query, location_info)
        
        # Get AI response
        raw_response = self.get_ai_response(enhanced_prompt, search_results[:1200])
        
        # Apply enhancements
        response = self.enhance_ai_response(query, raw_response)
        
        # Apply translation if needed
        response = self._apply_translation(response)
        
        # Save to memory
        self.save_enhanced_memory(query, response)
        
        # Update conversation context
        self._update_conversation_context(query, response)
        
        return response
    
    def _handle_direct_response(self, query: str, start_time: float) -> str:
        """Handle responses using AI knowledge without search"""
        # Get memory context
        memory_context = self.context_memory.get_relevant_context(query)
        
        # Prepare prompt
        if memory_context and self._should_add_memory_context(query):
            context_prompt = f"Conversation context: {memory_context}\nCurrent question: {query}"
        else:
            context_prompt = query
        
        # Get AI response
        raw_response = self.get_ai_response(context_prompt)
        
        # Apply enhancements
        response = self.enhance_ai_response(query, raw_response)
        
        # Apply translation if needed
        response = self._apply_translation(response)
        
        # Save to memory
        self.save_enhanced_memory(query, response)
        
        # Update conversation context
        self._update_conversation_context(query, response)
        
        return response
    
    def _create_search_prompt(self, query: str, location_info: Optional[Dict]) -> str:
        """Create optimized search prompt"""
        base_prompt = (
            f"Using the latest search results provided, give current 2025 information about: {query}. "
            f"Focus on recent data and current trends. Avoid outdated information."
        )
        
        if location_info:
            base_prompt += f" Location context: {location_info.get('pincode', 'N/A')}"
        
        return base_prompt
    
    def _apply_translation(self, response: str) -> str:
        """Apply translation if needed"""
        try:
            if (hasattr(self.translation_service, 'current_language') and 
                self.translation_service.current_language != 'english'):
                return self.translation_service.translate_response(
                    response, self.translation_service.current_language
                )
        except Exception as e:
            if self.debug_mode:
                print(f"⚠️ Translation error: {e}")
        
        return response
    
    def _update_conversation_context(self, query: str, response: str):
        """Update conversation context efficiently"""
        self.conversation_context.append(f"Q: {query} A: {response}")
        
        # Keep context manageable
        if len(self.conversation_context) > 20:
            self.conversation_context = self.conversation_context[-15:]
    
    def enhance_ai_response(self, query: str, raw_response: str) -> str:
        """Enhanced AI response processing with intelligent filtering"""
        try:
            # 1. Emotion detection (selective)
            emotion, confidence = self.emotion_detector.detect_emotion(query)
            
            # 2. Add empathy only for strong emotions
            if confidence > 0.85:  # Even higher threshold for less intrusion
                empathy = self.emotion_detector.get_empathetic_response(emotion, confidence)
                raw_response = f"{empathy} {raw_response}"
            
            # 3. Apply personality (always)
            response = self.personality_system.apply_personality_to_response(raw_response)
            
            # 4. Common sense check (only when needed)
            if self._needs_common_sense_check(query, response):
                response = self.common_sense.enhance_with_common_sense(query, response)
            
            # 5. Memory context (very selective)
            if self._should_add_memory_context(query):
                context = self.context_memory.get_relevant_context(query)
                if context:
                    response = f"Based on our conversation, {response}"
            
            # 6. Learning integration
            personalized = self.learning_system.get_personalized_response(query)
            if personalized and len(personalized) < len(response):
                response = personalized
            
            return response.strip()
            
        except Exception as e:
            print(f"⚠️ Enhancement error: {e}")
            return raw_response
    
    def _needs_common_sense_check(self, query: str, response: str) -> bool:
        """Determine if common sense check is needed"""
        # Safety keywords
        safety_keywords = ['dangerous', 'harmful', 'illegal', 'unsafe', 'hurt', 'damage']
        
        # Logic issue indicators
        logic_keywords = ['impossible', 'never', 'always', 'can\'t', 'unable']
        
        query_lower = query.lower()
        response_lower = response.lower()
        
        # Check for safety concerns
        if any(word in response_lower for word in safety_keywords):
            return True
        
        # Check for physical impossibilities
        impossible_queries = ['fly without', 'breathe underwater', 'time travel', 'live forever']
        if any(impossible in query_lower for impossible in impossible_queries):
            return True
        
        return False
    
    def _should_add_memory_context(self, query: str) -> bool:
        """Determine if memory context should be added"""
        memory_triggers = [
            'remember', 'earlier', 'before', 'previous', 'last time',
            'you said', 'we talked', 'mentioned', 'discussed'
        ]
        
        return any(trigger in query.lower() for trigger in memory_triggers)
    

    
    def save_enhanced_memory(self, query: str, response: str):
        """Enhanced memory saving with error handling and optimization"""
        try:
            # Save to memory systems (async for performance)
            memory_futures = [
                self.executor.submit(self.save_to_memory, query, response),
                self.executor.submit(self.save_knowledge, query, response),
                self.executor.submit(self.context_memory.add_to_session_memory, query, response),
                self.executor.submit(self.context_memory.add_to_long_term_memory, query, response),
                self.executor.submit(self.learning_system.learn_from_conversation, query, response)
            ]
            
            # Don't wait for completion to avoid blocking
            # Futures will complete in background
            
        except Exception as e:
            print(f"⚠️ Memory save error: {e}")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        try:
            performance = self.get_performance_stats()
            memory_stats = self.context_memory.get_memory_stats()
            learning_stats = self.learning_system.get_learning_stats()
            personality_info = self.personality_system.get_current_personality_info()
            
            return {
                "status": "operational",
                "performance": performance,
                "memory": memory_stats,
                "learning": learning_stats,
                "personality": personality_info,
                "language": self.current_language,
                "components": {
                    "voice": "active",
                    "search": "active",
                    "emotion_detection": "active",
                    "learning": "active"
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

def main():
    """Enhanced main function with better error handling and features"""
    try:
        ai = TerminalAI()
        
        print("🤖 Advanced AI Assistant System v2.0")
        print("=" * 60)
        print("🎆 Upgraded with enhanced performance and features!")
        print("")
        
        print("📝 BASIC COMMANDS:")
        print("  quit                    - Exit application")
        print("  status                  - System status overview")
        print("  🔍 SEARCH & INFO:")
        print("  news                    - Latest news headlines")
        print("  🧠 MEMORY & LEARNING:")
        print("  memory stats            - View memory statistics")
        
        print("\n" + "=" * 50)
        
        try:
            current_personality = ai.personality_system.get_current_personality_info()
            print(f"🎭 Personality: {current_personality['name']} ({current_personality['style']})")
            print(f"🧠 Features: Emotion Detection • Learning • Memory • Voice • Search")
            print(f"🚀 Performance: Optimized caching and async processing")
            print("\n💬 Type any command or just start chatting!")
        except Exception as e:
            print(f"⚠️ Initialization warning: {e}")
            print("\n💬 System ready - you can start chatting!")
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() == 'quit':
                    print("👋 Goodbye! Thanks for using the AI Assistant!")
                    ai.executor.shutdown(wait=False)
                    break
                
                elif user_input.lower() == 'status':
                    status = ai.get_system_status()
                    print(f"\n📊 System Status:")
                    print(f"Status: {status['status']}")
                    if 'performance' in status:
                        print(f"Performance: {status['performance']['cache_hit_rate']} cache hit rate")
                    if 'memory' in status:
                        print(f"Memory: {status['memory']['total_conversations']} conversations")
                
                elif user_input.lower() == 'news':
                    news = ai.news_system.get_latest_news()
                    print(f"\n{news}")
                    ai.speak("Here are the latest news headlines.")
                    
                elif user_input.lower() == 'memory stats':
                    stats = ai.context_memory.get_memory_stats()
                    learning_stats = ai.learning_system.get_learning_stats()
                    print(f"\nMemory Statistics:")
                    print(f"Session conversations: {stats['session_conversations']}")
                    print(f"Total conversations: {stats['total_conversations']}")
                    print(f"Learning items: {learning_stats['total_knowledge_items']}")
                
                else:
                    start_time = time.time()
                    response = ai.smart_response(user_input)
                    response_time = time.time() - start_time
                    
                    print("\n🤖 AI:")
                    print(response)
                    
                    if ai.debug_mode:
                        print(f"\n🕰️ Response time: {response_time:.2f}s")
                    
                    ai.speak(response)
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Thanks for using the AI Assistant!")
                ai.executor.shutdown(wait=False)
                break
            except Exception as e:
                print(f"⚠️ Unexpected error: {e}")
                if ai.debug_mode:
                    import traceback
                    traceback.print_exc()
    
    except Exception as e:
        print(f"⚠️ System startup error: {e}")
        print("Please check your installation and try again.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"⚠️ System startup error: {e}")
        print("Please check your installation and try again.")