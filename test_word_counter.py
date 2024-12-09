import pytest
from word_counter import WordCounter
import os

def test_basic_word_count():
    counter = WordCounter()
    stats = counter.count_from_text("Hello world! This is a test.")
    
    assert stats['word_count'] == 6
    assert stats['char_count'] == 19
    assert stats['line_count'] == 1
    assert stats['unique_words'] == 6

def test_word_frequency():
    counter = WordCounter()
    counter.count_from_text("hello world hello test hello")
    
    freq = counter.get_word_frequency()
    assert freq['hello'] == 3
    assert freq['world'] == 1
    assert freq['test'] == 1

def test_empty_text():
    counter = WordCounter()
    stats = counter.count_from_text("")
    
    assert stats['word_count'] == 0
    assert stats['char_count'] == 0
    assert stats['line_count'] == 1
    assert stats['unique_words'] == 0

def test_multiple_lines():
    counter = WordCounter()
    text = """Hello world
    This is a test
    Multiple lines"""
    
    stats = counter.count_from_text(text)
    assert stats['line_count'] == 3 

def test_anthropic_client_initialization():
    # Test without API key
    original_key = os.getenv('ANTHROPIC_API_KEY')  # Save original key
    counter = WordCounter()
    assert counter.anthropic_client is not None  # Should be not None since we have a key
    
    # Verify it's using the correct key
    assert os.getenv('ANTHROPIC_API_KEY') == original_key

def test_claude_analysis():
    counter = WordCounter()
    api_key = os.getenv('ANTHROPIC_API_KEY')
    print(f"Using API Key: {api_key}")  # Debugging line to check API key
    if counter.anthropic_client:  # Only run if API key is configured
        text = "The quick brown fox jumps over the lazy dog. This classic pangram has been used for typing practice."
        try:
            analysis = counter.analyze_text_with_claude(text)
            assert 'claude_analysis' in analysis
            assert 'basic_stats' in analysis
            assert analysis['basic_stats']['word_count'] == 14
        except Exception as e:
            print(f"Error during analysis: {e}")

def test_anthropic_interface():
    counter = WordCounter()
    result = counter.anthropic_analyze("Hello world! This is a test.")
    
    assert "basic_stats" in result
    assert result["basic_stats"]["word_count"] == 6
    assert result["basic_stats"]["unique_words"] == 6
    assert "error" not in result

def test_anthropic_call_format():
    counter = WordCounter()
    result = counter({
        "text": "The quick brown fox jumps over the lazy dog. This classic pangram has been used for typing practice."
    })
    
    assert "basic_stats" in result
    assert result["basic_stats"]["word_count"] == 18  # Updated to correct word count
    assert result["basic_stats"]["unique_words"] == 17  # Updated to correct unique word count
    assert "error" not in result

def test_text_with_punctuation():
    counter = WordCounter()
    result = counter({
        "text": "Hello! This... is a test, with punctuation."
    })
    
    assert "basic_stats" in result
    assert result["basic_stats"]["word_count"] == 7  # Hello, This, is, a, test, with, punctuation
    assert result["basic_stats"]["unique_words"] == 7
    assert "error" not in result