from pydantic import BaseModel

class usercreate(BaseModel):
    email:str     #Emailstr
    password:str

