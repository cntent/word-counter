import re

class WordCounter:
    def __call__(self, input_dict: dict) -> dict:
        """Count words in text."""
        if not isinstance(input_dict, dict) or 'text' not in input_dict:
            return {"error": "Input must be a dictionary with a 'text' key"}
            
        text = input_dict['text']
        words = re.findall(r'\b\w+\b', text.lower())
        return {"word_count": len(words)}