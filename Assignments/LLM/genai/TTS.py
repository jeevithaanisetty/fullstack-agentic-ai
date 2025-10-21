#text to speech
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY=os.getenv("GEMINI-API-KEY")
# or genai.configure(api_key="")
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

""" 
model=genai.GenerativeModel("gemini-2.5-pro")
response=model.generate_content("Summarize.......{data.text}") 
     or
response=model.generate.content(
"summarize {data.text}",
"temparature"=0.3,
"top_p"=0.8,
"max_output_tokens"=300,
"candidate_count"=1
)

"""