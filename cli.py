import argparse
from word_counter import WordCounter

def main():
    parser = argparse.ArgumentParser(description='Word Counter Tool for Anthropic')
    parser.add_argument('input', help='Text file to analyze')
    parser.add_argument('--top-words', type=int, help='Show top N most frequent words')
    parser.add_argument('--analyze', action='store_true', 
                       help='Perform detailed analysis using Claude')
    
    args = parser.parse_args()
    
    counter = WordCounter()
    
    try:
        stats = counter.count_from_file(args.input)
        with open(args.input, 'r') as file:
            text = file.read()
        
        print("\nFile Statistics:")
        print(f"Total Words: {stats['word_count']}")
        print(f"Total Characters: {stats['char_count']}")
        print(f"Total Lines: {stats['line_count']}")
        print(f"Unique Words: {stats['unique_words']}")
        
        if args.top_words:
            print(f"\nTop {args.top_words} most frequent words:")
            freq = counter.get_word_frequency(args.top_words)
            for word, count in freq.items():
                print(f"{word}: {count}")
                
        if args.analyze:
            try:
                analysis = counter.analyze_text_with_claude(text)
                print("\nClaude Analysis:")
                print(analysis['claude_analysis'])
            except ValueError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Analysis failed: {e}")
                
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main() 