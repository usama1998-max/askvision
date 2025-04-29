# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

llm = openai.OpenAI(
    api_key=os.getenv("TOGETHERAI_API_KEY"),
    base_url="https://api.together.xyz/v1"
)


class ChatRequest(BaseModel):
    prompt: str
    image: str


@app.get("/")
async def home():
    return {"message": "AskVision Extention!"}


@app.post("/chat/")
async def chat(request: ChatRequest):
    print(request)
    try:
        response = llm.chat.completions.create(
            model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",

            messages=[
                {"role": "system", "content": """Answer the question of the following user"""},
                {"role": "user", "content": [
                    {"type": "text", "text": request.prompt},
                    {"type": "image_url", "image_url": {"url": request.image}}
                ]}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
