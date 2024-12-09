import pytest
from word_counter import WordCounter

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
    counter = WordCounter()
    assert counter.anthropic_client is None
    
    # Test with API key (requires setting ANTHROPIC_API_KEY in environment)
    import os
    os.environ['ANTHROPIC_API_KEY'] = 'dummy_key_for_testing'
    counter = WordCounter()
    assert counter.anthropic_client is not None

def test_claude_analysis():
    counter = WordCounter()
    if counter.anthropic_client:  # Only run if API key is configured
        text = "The quick brown fox jumps over the lazy dog. This classic pangram has been used for typing practice."
        analysis = counter.analyze_text_with_claude(text)
        
        assert 'claude_analysis' in analysis
        assert 'basic_stats' in analysis
        assert analysis['basic_stats']['word_count'] == 14

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
    assert result["basic_stats"]["word_count"] == 14
    assert result["basic_stats"]["unique_words"] == 13
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