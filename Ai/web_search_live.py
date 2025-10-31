import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class LiveWebSearch:
    def __init__(self):
        self.search_engines = {
            "duckduckgo": "https://duckduckgo.com/html/?q=",
            "bing": "https://www.bing.com/search?q="
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_web(self, query, max_results=5):
        """Search the web for current information"""
        try:
            # Use DuckDuckGo for privacy-friendly search
            results = self.search_duckduckgo(query, max_results)
            
            if not results:
                # Fallback to Bing if DuckDuckGo fails
                results = self.search_bing(query, max_results)
            
            return self.format_search_results(results, query)
            
        except Exception as e:
            print(f"Web search error: {e}")
            return f"I couldn't search the web right now, but I can help with general information about {query}."
    
    def search_duckduckgo(self, query, max_results):
        """Search using DuckDuckGo"""
        try:
            url = f"https://duckduckgo.com/html/?q={query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                # Extract search results
                for result in soup.find_all('div', class_='result')[:max_results]:
                    title_elem = result.find('a', class_='result__a')
                    snippet_elem = result.find('a', class_='result__snippet')
                    
                    if title_elem and snippet_elem:
                        results.append({
                            'title': title_elem.get_text().strip(),
                            'snippet': snippet_elem.get_text().strip(),
                            'url': title_elem.get('href', '')
                        })
                
                return results
            
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
        
        return []
    
    def search_bing(self, query, max_results):
        """Search using Bing (fallback)"""
        try:
            # Simple Bing search implementation
            url = f"https://www.bing.com/search?q={query}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                results = []
                
                # Extract Bing results (simplified)
                for result in soup.find_all('li', class_='b_algo')[:max_results]:
                    title_elem = result.find('h2')
                    snippet_elem = result.find('p')
                    
                    if title_elem and snippet_elem:
                        results.append({
                            'title': title_elem.get_text().strip(),
                            'snippet': snippet_elem.get_text().strip(),
                            'url': ''
                        })
                
                return results
            
        except Exception as e:
            print(f"Bing search error: {e}")
        
        return []
    
    def format_search_results(self, results, query):
        """Format search results into readable text"""
        if not results:
            return f"I couldn't find current web results for '{query}', but I can provide general information."
        
        formatted = f"Here's what I found about '{query}':\n\n"
        
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   {result['snippet']}\n\n"
        
        formatted += f"This information was found from live web search on {datetime.now().strftime('%Y-%m-%d %H:%M')}."
        
        return formatted
    
    def get_news(self, topic="latest news"):
        """Get latest news about a topic"""
        news_query = f"{topic} news today"
        return self.search_web(news_query, max_results=3)
    
    def get_current_info(self, topic):
        """Get current information about any topic"""
        current_query = f"{topic} 2024 latest current information"
        return self.search_web(current_query, max_results=4)
    
    def fact_check(self, statement):
        """Fact-check a statement using web search"""
        fact_query = f"fact check {statement} true false"
        return self.search_web(fact_query, max_results=3)
    
    def get_weather_web(self, location):
        """Get weather information from web"""
        weather_query = f"weather {location} today current"
        return self.search_web(weather_query, max_results=2)
    
    def search_how_to(self, task):
        """Search for how-to information"""
        how_to_query = f"how to {task} step by step guide"
        return self.search_web(how_to_query, max_results=3)