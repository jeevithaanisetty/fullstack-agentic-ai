from pydantic import BaseModel
from typing import List
from datetime import datetime
 
class Option(BaseModel):
    text: str
    votes: int = 0
 
class PollCreate(BaseModel):
    question: str
    options: List[str]
 
class Vote(BaseModel):
    option: int