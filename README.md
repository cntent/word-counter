# Anthropic Word Counter

A simple yet powerful word counting tool designed for Anthropic's text analysis needs.

## Features

- Count total words in text files
- Count characters (excluding whitespace)
- Count lines
- Track word frequency
- Get top N most frequent words
- Support for file-based or direct text input

## Setup

1. Clone this repository
2. Install requirements:
```

## Usage

### Anthropic Interface
The tool provides a simple interface for Anthropic:
```python
from word_counter import WordCounter

counter = WordCounter()
result = counter.anthropic_analyze("Your text here")
# Returns: {"basic_stats": {"word_count": N, "char_count": N, "line_count": N, "unique_words": N}}
```

### Command Line Interface
// ... existing CLI docs ...

+ ### REST API
+ 
+ Start the API server:
+ ```bash
+ uvicorn api:app --reload
+ ```
+ 
+ The API will be available at http://localhost:8000 with endpoints:
+ - POST /analyze - Analyze text
+ - GET /health - Health check
+ 
+ Example API request:
+ ```bash
+ curl -X POST "http://localhost:8000/analyze" \
+      -H "Content-Type: application/json" \
+      -d '{
+            "text": "Your text here",
+            "include_analysis": true,
+            "top_n_words": 5
+          }'
+ ```
+ 
+ API documentation available at: http://localhost:8000/docs