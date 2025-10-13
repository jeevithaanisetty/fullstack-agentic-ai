from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY=os.getenv("GEMINI-API-KEY")

client=genai.Client(api_key=API_KEY)

app=FastAPI(title="TTS API")

class Text(BaseModel):
    text:str

@app.post("/summary")
async def summarize(data:Text):
    prompt=f"summarize this text in 2-3 sentences:\n {data.text}"
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    summary=response.strip()
    return {"summary":summary}
