from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/count-words")
async def count_words(input_data: TextInput):
    try:
        words = len(input_data.text.split())
        return {"word_count": words}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 