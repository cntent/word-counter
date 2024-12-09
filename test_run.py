from word_counter import WordCounter

# Create counter
counter = WordCounter()

# Test cases
tests = [
    {"text": "Hello world! This is a test."},
    {"text": ""},
    {"text": "Hello! This... is a test, with punctuation."},
    {"not_text": "Hello"}  # Invalid input
]

# Run tests
print("Running manual tests:")
print("-" * 40)
for test in tests:
    print(f"\nInput: {test}")
    result = counter(test)
    print(f"Result: {result}")

print("\n" + "-" * 40) 