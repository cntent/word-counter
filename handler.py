import json
from word_counter import WordCounter

def handle_request(event, context):
    # Parse the incoming GitHub webhook payload
    try:
        payload = json.loads(event['body'])
        text = payload.get('text', '')
        include_analysis = payload.get('include_analysis', False)
        top_n_words = payload.get('top_n_words', None)
        
        counter = WordCounter()
        result = counter.analyze_text_with_claude(text) if include_analysis else counter.count_from_text(text)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 