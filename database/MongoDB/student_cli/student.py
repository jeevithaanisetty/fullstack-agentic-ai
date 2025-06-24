import pymongo
from pymongo import MongoClient

client=pymongo.MongoClient("localhost",27017)
database=client["student"]
collection=database["student_details"]

class Student:
    def __init__(self,name,roll_no,dob,standard):
       self.name=name
       self.roll_no=roll_no
       self.dob=dob
       self.standard=standard
    def __str__(self):
        return (f"name:{self.name},age:{self.roll_no},dob:{self.dob},standard:{self.standard}")
    def to_dict(self):
        return vars(self)

def save_to_db(student_data):
    collection.insert_one(student_data)
    print("student added successfully......")

def load_from_db():
    students=collection.find()
    return [Student(s['name'], s['roll_no'], s['dob'], s['standard']) for s in students] # **student makes error due to _id

def add_student():
    name=input("enter name: ")
    roll_no=input("enter roll_no: ")
    dob=input("enter date of birth:")
    standard=input("enter standard:")
    student=Student(name,roll_no,dob,standard).to_dict()
    save_to_db(student)

def list_students():
    students=load_from_db()
    for student in students:
        print(student)

def delete_student():
    roll_no=input("enter roll_no : ")
    query={"roll_no":f"{roll_no}"}
    result=collection.delete_one(query)
    print(f"deleted student with roll no {roll_no} and deleted no of students are {result.deleted_count}")

def get_student_by_rollno():
    roll_no=input("enter roll_no : ")
    query={"roll_no":f"{roll_no}"}
    student=collection.find_one(query)
    print(student)

def menu():
    while True:
        print("\n=========== student CLI ============")
        print("1.Add Student")
        print("2.List students")
        print("3.Delete Student")
        print("4.Find student with roll_no")
        print("5.exit")
        choice=int(input("enter choice here: "))

        if choice==1:
            add_student()
        elif choice==2:
            list_students()
        elif choice==3:
            delete_student()
        elif choice==4:
            get_student_by_rollno()
        elif choice==5:
            print("Exiting the application..............")
            break
        else:
            print("Invalid choice try again with other choices from 1-5....")

if __name__=="__main__":
    menu()