from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load API key
load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CommentRequest(BaseModel):
    comment: str

@app.get("/")
def root():
    return {"status": "API is running"}

@app.post("/comment")
async def analyze_comment(req: CommentRequest):

    if not req.comment.strip():
        raise HTTPException(status_code=400, detail="Comment cannot be empty")

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": "You are a sentiment analysis API. Return only JSON."
                },
                {
                    "role": "user",
                    "content": f"""
Analyze the sentiment of this comment.

Return strictly in JSON:
{{"sentiment":"positive|negative|neutral","rating":1-5}}

Comment: {req.comment}
"""
                }
            ]
        )

        # Extract text output safely
        text_output = response.output[0].content[0].text

        # Convert to dict
        result = json.loads(text_output)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
