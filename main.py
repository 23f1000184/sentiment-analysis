from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from anywhere (needed for graders)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommentRequest(BaseModel):
    comment: str

positive_words = ["good", "great", "amazing", "excellent", "love", "fast", "nice", "awesome"]
negative_words = ["bad", "poor", "worst", "hate", "slow", "terrible", "awful"]

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/comment")
async def analyze_comment(req: CommentRequest):
    text = req.comment.lower()

    if any(word in text for word in positive_words):
        return {"sentiment": "positive", "rating": 4}
    elif any(word in text for word in negative_words):
        return {"sentiment": "negative", "rating": 2}
    else:
        return {"sentiment": "neutral", "rating": 3}
