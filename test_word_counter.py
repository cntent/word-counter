import pytest
from word_counter import WordCounter

def test_basic_word_count():
    counter = WordCounter()
    result = counter({"text": "Hello world! This is a test."})
    assert result["word_count"] == 6

def test_empty_text():
    counter = WordCounter()
    result = counter({"text": ""})
    assert result["word_count"] == 0

def test_text_with_punctuation():
    counter = WordCounter()
    result = counter({"text": "Hello! This... is a test, with punctuation."})
    assert result["word_count"] == 7

def test_invalid_input():
    counter = WordCounter()
    result = counter({"not_text": "Hello"})
    assert "error" in result