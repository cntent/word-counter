import requests
import sys

def test_api():
    url = "http://localhost:8000/analyze"
    data = {
        "text": "The quick brown fox jumps over the lazy dog.",
        "include_analysis": True,
        "top_n_words": 5
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise exception for bad status codes
        print(response.json())
        return True
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server. Is it running?")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1) 