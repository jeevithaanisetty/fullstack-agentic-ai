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
    
class Forgotted(BaseModel):
    subject:str

class Reset(BaseModel):
    username:str
    new_password:str
    confirm_password:str
    
