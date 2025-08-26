from pydantic import BaseModel
from typing import List
 
class PollCreate(BaseModel):
    question: str
    options: List[str]
 
class Vote(BaseModel):
    poll_id:str
    option: int

class Poll(BaseModel):
    title:str
    description:str

