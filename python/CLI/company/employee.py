
from utils.helper_methods import save_to_json,load_from_json
import os

#EMPLOYEES_JSON="employees.json"
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
EMPLOYEES_JSON=os.path.join(BASE_DIR,"employees.json")

class Employee:         
    def __init__(self, emp_id,emp_name):
        self.emp_id=emp_id
        self.emp_name=emp_name
    def to_dict(self):
        return vars(self) 
    def __str__(self):
        return f"Department {self.emp_id} - {self.emp_name}"
    
    @classmethod
    def add_employee(cls):
        emp_id=input("enter emp_id:")
        emp_name=input("enter emp_name:")
        
        employees=load_from_json(EMPLOYEES_JSON)
        employee=Employee(emp_id,emp_name).to_dict()
        employees.append(employee)
        save_to_json(employees,EMPLOYEES_JSON)
    
    def list_employees():          
        employees=load_from_json(EMPLOYEES_JSON)
        print("\033[92m\nemployees..........")
        for e in employees:
            print(f"{e['emp_id']} : {e['emp_name']}")
        print("\033[0m")

    def delete_employee():
        emp_id=input("enter employee_id:")
        employees=load_from_json(EMPLOYEES_JSON)
        new_list=list(filter(lambda e:e['emp_id']!=emp_id, employees))
        save_to_json(new_list,EMPLOYEES_JSON)
        print(f"employee with {emp_id} as emp_id is deleted")
