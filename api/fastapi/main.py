from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
import asyncio
import json
import os

DATAFILE="student.json"

app=FastAPI(title="My FastAPI",version="1.0.0",description="This API belongs to Student API application")

class Student:
    def __init__(self,name,roll_no,standard,dob,email):
        self.name=name
        self.roll_no=roll_no
        self.standard=standard
        self.dob=dob
        self.email=email

    def __str__(self):
        return (f"name:{self.name} , roll_no:{self.roll_no} , standard:{self.standard} , dob:{self.dob} , email:{self.email}")
    
    def to_dict(self):
        return vars(self)
    
class Details(BaseModel):
    name:str
    roll_no:str
    standard:int
    dob:str
    email:str=None

def save_to_json(data):
    with open(DATAFILE,"w") as f:
        json.dump([s.to_dict() for s in data],f,indent=4)

def load_from_json():
    if not os.path.exists(DATAFILE):
        return []
    with open(DATAFILE,"r") as f:
        students=json.load(f)
    return [Student(**s) for s in students]

@app.get("/")
async def hello():
    return {"message":"hello viewer ! "}

@app.post("/add_student")
async def add_student(data:Details):
    students=load_from_json()

    if any((s.roll_no==data.roll_no) for s in students):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f" student already exists with the roll number {data.roll_no}")
    
    student=Student(name=data.name,   #Student(name,roll_no,standard,dob,email)
        roll_no=data.roll_no,
        standard=data.standard,
        dob=data.dob,
        email=data.email)
    
    students.append(student)
    save_to_json(students)
    return {"mesage":"student added successfully..."}

@app.get("/list_students")
async def list_students():
    students=load_from_json()
    return [s.to_dict() for s in students]
    