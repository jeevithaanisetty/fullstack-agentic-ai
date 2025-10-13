from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from openai import OpenAI
from functools import wraps
import os
import logging

logging.basicConfig(
    filename="prompt_chain.log",
    level= logging.INFO,
    format= "%(asctime)s [%(levelname)s]   %(message)s ")

def handle_exceptions(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:
            logging.info(f"Executing: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error while Executing: {func.__name__} : {e}")
    return wrapper

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
    logging.info("summarized the input_text successfully")

    Grammer_check=client.chat.completions.create(
        model="gpt4",
        messages=[
            {"role":"system","content":"improve grammer and clarity of the following text"},
            {"role":"user","content":input.text}
        ],
        temperature=0.3
    ).choices[0].message.content.strip()
    logging.info("grammer fixed for the given input_text")   
    
    Translated_text=client.chat.completions.create(
        model="gpt4",
        messages=[
            {"role":"system","content":f"Translate the following text to {input.language}"},
            {"role":"user","content":input.text}
        ],
        temperature=0.3
    ).choices[0].message.content.strip()
    logging.info(f"input_text is translated to {input.language}successfully.if not check content carefullyand correct")

    return {
        "Summary":Summary,
        "Grammer_check":Grammer_check,
        "Translated_text":Translated_text
    }