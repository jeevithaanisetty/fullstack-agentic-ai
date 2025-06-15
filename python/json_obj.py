



import json

class user:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def dict_data(self):
        return {"name":self.name,"age":self.age}
    def save_file(self,filename):
        with open(filename,"w") as f:
            json.dump(self.dict_data(),f)
    @classmethod
    def load_file(cls,filename):
        with open (filename,"r") as f:
            data=json.load(f)
        return cls(**data)

User=user("sam",15)
User.save_file("sam.json")
 
USER=user.load_file("sam.json")
print({USER.name} ,{USER.age})





