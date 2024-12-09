from typing import Dict, List, Optional
import re
from pathlib import Path
import os
from dotenv import load_dotenv
from anthropic import Anthropic

class WordCounter:
    def __init__(self):
        self.word_count = 0
        self.char_count = 0
        self.line_count = 0
        self.word_frequency: Dict[str, int] = {}
        
        # Load environment variables
        load_dotenv()
        
        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            self.anthropic_client = Anthropic(api_key=api_key)
        else:
            self.anthropic_client = None

    def count_from_text(self, text: str) -> Dict[str, int]:
        """Count words from a string of text."""
        # Reset counters
        self.word_count = 0
        self.char_count = 0
        self.line_count = 0
        self.word_frequency.clear()

        # Count lines
        self.line_count = len(text.splitlines())

        # Count characters (excluding whitespace)
        self.char_count = len(''.join(text.split()))

        # Count words and their frequency
        words = re.findall(r'\b\w+\b', text.lower())
        self.word_count = len(words)
        
        for word in words:
            self.word_frequency[word] = self.word_frequency.get(word, 0) + 1

        return self.get_statistics()

    def count_from_file(self, file_path: str) -> Dict[str, int]:
        """Count words from a file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with path.open('r', encoding='utf-8') as file:
            text = file.read()
            return self.count_from_text(text)

    def get_statistics(self) -> Dict[str, int]:
        """Return the current statistics."""
        return {
            'word_count': self.word_count,
            'char_count': self.char_count,
            'line_count': self.line_count,
            'unique_words': len(self.word_frequency)
        }

    def get_word_frequency(self, top_n: Optional[int] = None) -> Dict[str, int]:
        """Return word frequency dictionary, optionally limited to top N words."""
        if top_n is None:
            return self.word_frequency
        
        sorted_words = sorted(self.word_frequency.items(), 
                            key=lambda x: x[1], 
                            reverse=True)
        return dict(sorted_words[:top_n]) 

    def analyze_text_with_claude(self, text: str) -> Dict[str, any]:
        """Analyze text using Claude to get additional insights."""
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured. Please check your .env file.")
        
        prompt = f"""Analyze the following text and provide insights about:
        1. Main topics or themes
        2. Writing style and tone
        3. Key entities mentioned
        4. Sentiment analysis
        
        Text to analyze:
        {text}
        
        Please provide the analysis in a structured format."""
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            return {
                'claude_analysis': response.content[0].text,
                'basic_stats': self.count_from_text(text)
            }
        except Exception as e:
            raise Exception(f"Error calling Anthropic API: {str(e)}")

    def anthropic_analyze(self, text: str) -> dict:
        """Simple interface for Anthropic to analyze text."""
        try:
            # Get basic stats
            stats = self.count_from_text(text)
            
            # Return in a simple format
            return {
                "basic_stats": {
                    "word_count": stats['word_count'],
                    "char_count": stats['char_count'],
                    "line_count": stats['line_count'],
                    "unique_words": stats['unique_words']
                }
            }
        except Exception as e:
            return {"error": str(e)}

    def __call__(self, input_dict: dict) -> dict:
        """Make the class callable with the exact format Anthropic uses."""
        if not isinstance(input_dict, dict) or 'text' not in input_dict:
            return {"error": "Input must be a dictionary with a 'text' key"}
            
        stats = self.count_from_text(input_dict['text'])
        return stats