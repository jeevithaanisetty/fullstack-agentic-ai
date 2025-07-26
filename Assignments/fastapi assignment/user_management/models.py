from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username:str
    firstname:str
    lastname:str
    dob:str
    doj:str
    password:str
    address:str
    comment: Optional[str]=None
    status:Optional[str]=None

class Login(BaseModel):
    username:str
    password:str

class ChangePassword(BaseModel):
    password:str
    new_password:str
    