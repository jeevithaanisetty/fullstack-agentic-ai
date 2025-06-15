import os
from utils.helper_methods import save_to_json,load_from_json

#DEPARTMENTS_JSON="department.json"
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DEPARTMENTS_JSON=os.path.join(BASE_DIR,"department.json")
    
class Department:         
    def __init__(self, dept_id,dept_name):
        self.dept_id=dept_id
        self.dept_name=dept_name
    def to_dict(self):
        return vars(self) 
    def __str__(self):
        return f"Department {self.dept_id} -{self.dept_name}"
    
    @classmethod
    def add_department(cls):
        dept_id=input("enter dept_id:")
        dept_name=input("enter dept_name:")
        
        departments=load_from_json(DEPARTMENTS_JSON)
        department=Department(dept_id,dept_name).to_dict()
        departments.append(department)
        save_to_json(departments,DEPARTMENTS_JSON)
    
    def list_departments():          
        departments=load_from_json(DEPARTMENTS_JSON)
        print("\033[92m\nAvailable departments")
        for d in departments:
            print(f"{d['dept_id']} : {d['dept_name']}")
        print("\033[0m")
    
    def delete_department():
        dept_id=input("enter dept_id:")
        departments=load_from_json(DEPARTMENTS_JSON)
        new_list=list(filter(lambda d:d['dept_id']!=dept_id, departments))
        save_to_json(new_list,DEPARTMENTS_JSON)
        print(f"employee with {dept_id} as dept_id is deleted")

