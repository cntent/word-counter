from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from word_counter import WordCounter

app = FastAPI(title="Word Counter API")

class WordCountRequest(BaseModel):
    text: str
    include_analysis: bool = False
    top_n_words: Optional[int] = None

@app.post("/analyze")
async def analyze_text(request: WordCountRequest) -> Dict[str, Any]:
    counter = WordCounter()
    
    try:
        # Get basic stats
        stats = counter.count_from_text(request.text)
        
        # Prepare response
        response = {
            "basic_stats": stats,
            "word_frequency": counter.get_word_frequency(request.top_n_words)
        }
        
        # Add Claude analysis if requested
        if request.include_analysis and counter.anthropic_client:
            analysis = counter.analyze_text_with_claude(request.text)
            response["claude_analysis"] = analysis["claude_analysis"]
            
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 