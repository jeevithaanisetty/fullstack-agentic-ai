from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from openai import OpenAI

router=APIRouter()             #we have to define router.here apirouter recieves request and send it to required

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  #which we set in conda env

class TextInput(BaseModel):    #pydantic model for request/response
    text:str
    language:str="hi"          #providing default lang as hindi if not provided

@router.post("/prompt_chain")
async def prompt_chain(input:TextInput):
    
    Summary=client.chat.completions.create(
        model="gpt4",
        messages=[
            {"role":"system","content":"Summarize the following  text "},
            {"role":"user","content":input.text}
        ],
        temperature=0.4
    ).choices[0].message.content.strip()    # to remove unneccessary content except message in response 

    Grammer_check=client.chat.completions.create(
        model="gpt4",
        messages=[
            {"role":"system","content":"improve grammer and clarity of the following text"},
            {"role":"user","content":input.text}
        ],
        temperature=0.3
    ).choices[0].message.content.strip()   
    
    Translated_text=client.chat.completions.create(
        model="gpt4",
        messages=[
            {"role":"system","content":f"Translate the following text to {input.language}"},
            {"role":"user","content":input.text}
        ],
        temperature=0.3
    ).choices[0].message.content.strip()

    return {
        "Summary":Summary,
        "Grammer_check":Grammer_check,
        "Translated_text":Translated_text
    }