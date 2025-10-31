import requests
import json
from datetime import datetime, timedelta

class NewsSystem:
    def __init__(self):
        # Free news APIs (no key required)
        self.news_sources = {
            "newsapi_free": "https://newsapi.org/v2/top-headlines?country=us&apiKey=demo",
            "rss_feeds": [
                "https://feeds.bbci.co.uk/news/rss.xml",
                "https://rss.cnn.com/rss/edition.rss"
            ]
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_latest_news(self, category="general", count=5):
        """Get latest news headlines"""
        try:
            # Try multiple sources
            news = self.get_news_from_web_search(category, count)
            
            if not news:
                news = self.get_fallback_news(category)
            
            return self.format_news(news, category)
            
        except Exception as e:
            print(f"News error: {e}")
            return "I'm having trouble getting the latest news right now. Please try again later."
    
    def get_news_from_web_search(self, category, count):
        """Get news using web search"""
        try:
            from web_search_live import LiveWebSearch
            
            search = LiveWebSearch()
            
            # Search for recent news
            if category == "general":
                query = "latest news today headlines"
            else:
                query = f"latest {category} news today"
            
            results = search.search_web(query, max_results=count)
            
            # Convert search results to news format
            news_items = []
            if "Here's what I found" in results:
                lines = results.split('\n')
                current_item = {}
                
                for line in lines:
                    if line.strip() and line[0].isdigit():
                        if current_item:
                            news_items.append(current_item)
                        current_item = {'title': line.strip()}
                    elif line.strip() and 'title' in current_item:
                        current_item['description'] = line.strip()
                
                if current_item:
                    news_items.append(current_item)
            
            return news_items
            
        except Exception as e:
            print(f"Web search news error: {e}")
            return []
    
    def get_fallback_news(self, category):
        """Fallback news when APIs fail"""
        fallback_news = {
            "general": [
                {"title": "Technology Advances Continue", "description": "Latest developments in AI and technology sector"},
                {"title": "Global Economic Updates", "description": "Current market trends and economic indicators"},
                {"title": "Climate and Environment", "description": "Recent environmental news and climate updates"}
            ],
            "technology": [
                {"title": "AI Development Progress", "description": "New breakthroughs in artificial intelligence"},
                {"title": "Tech Industry Updates", "description": "Latest from major technology companies"},
                {"title": "Cybersecurity News", "description": "Recent cybersecurity developments and threats"}
            ],
            "science": [
                {"title": "Scientific Discoveries", "description": "Recent research and scientific breakthroughs"},
                {"title": "Space Exploration", "description": "Latest news from space agencies and missions"},
                {"title": "Medical Research", "description": "New developments in healthcare and medicine"}
            ]
        }
        
        return fallback_news.get(category, fallback_news["general"])
    
    def format_news(self, news_items, category):
        """Format news items for display"""
        if not news_items:
            return f"No {category} news available at the moment."
        
        formatted = f"📰 Latest {category.title()} News ({datetime.now().strftime('%Y-%m-%d %H:%M')}):\n\n"
        
        for i, item in enumerate(news_items[:5], 1):
            title = item.get('title', 'No title')
            description = item.get('description', 'No description available')
            
            formatted += f"{i}. {title}\n"
            formatted += f"   {description}\n\n"
        
        formatted += "Note: News information is gathered from various sources and updated regularly."
        
        return formatted
    
    def get_news_by_topic(self, topic):
        """Get news about specific topic"""
        try:
            from web_search_live import LiveWebSearch
            
            search = LiveWebSearch()
            query = f"{topic} news latest updates today"
            
            results = search.search_web(query, max_results=4)
            
            if results and "Here's what I found" in results:
                return f"📰 Latest news about {topic}:\n\n{results}"
            else:
                return f"I couldn't find recent news about {topic}. Try searching for a more specific topic."
                
        except Exception as e:
            return f"Error getting news about {topic}: {e}"
    
    def get_breaking_news(self):
        """Get breaking news alerts"""
        try:
            from web_search_live import LiveWebSearch
            
            search = LiveWebSearch()
            query = "breaking news alerts today urgent"
            
            results = search.search_web(query, max_results=3)
            
            if results:
                return f"🚨 Breaking News:\n\n{results}"
            else:
                return "No breaking news alerts at the moment."
                
        except Exception as e:
            return f"Error getting breaking news: {e}"
    
    def get_local_news(self, location):
        """Get local news for specific location"""
        try:
            from web_search_live import LiveWebSearch
            
            search = LiveWebSearch()
            query = f"{location} local news today headlines"
            
            results = search.search_web(query, max_results=4)
            
            if results:
                return f"📍 Local news for {location}:\n\n{results}"
            else:
                return f"Couldn't find local news for {location}."
                
        except Exception as e:
            return f"Error getting local news: {e}"
    
    def get_news_categories(self):
        """Get available news categories"""
        return [
            "general", "technology", "science", "health", 
            "business", "sports", "entertainment", "politics"
        ]