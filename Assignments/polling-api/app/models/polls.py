from pydantic import BaseModel
from typing import List
 
class PollCreate(BaseModel):
    question: str
    options: List[str]
    summary:str | None=None
    related_info:list |None=None

class Vote(BaseModel):
    poll_id:str
    option: int

class Poll(BaseModel):
    title:str
    description:str

class Delete(BaseModel):
    Poll_Id:str
