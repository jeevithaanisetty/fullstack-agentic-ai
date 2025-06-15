from functools import wraps
import json
import logging

logging.basicConfig(
    filename='emp_info.log',
    level= logging.INFO,
    format=" %(asctime)s  -  %(levelname)s  -  %(message)s  "
    )

DATA_JSON="emp.json"

def handle_exception(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
       try:
           logging.info(f"loading data from file {func.__name__}")
           return func(*args,**kwargs)
       except Exception as e:
           logging.info(f"exception occured in file {func.__name__}")
    return wrapper  

class Employee:
    def __init__(self,emp_id,name,department,projects):
        self.emp_id=emp_id
        self.name=name
        self.department=department
        self.projects=projects

    def to_dict(self):
        return{
            "emp_id":self.emp_id,
            "name":self.name,
            "department":self.department,
            "projects":self.projects

        }
    @staticmethod
    def from_dict(emp_dict):
        return{
               emp_dict["emp_id"],
               emp_dict["name"],
               emp_dict["department"],
               emp_dict["projects"]
        }
    @handle_exception
    def has_active_project(self):
        for project in self.projects:
            if project["status"]=="active":
                return True
        return False
        
@handle_exception
def load_data(filename):
    with open(filename,"r") as f:
        raw= json.load(f) 
        return [Employee.from_dict(emp) for emp in raw ]
    logging.info("data loaded successfully")   ,200
        
@handle_exception
def save_data(filename,data):
    with open(filename,"w") as f:
        json.dumps(data,f,indent=4)
        logging.info(f'saved json file successfully'),200

def main():
    
    employees=load_data(DATA_JSON)
    #emp=Employee("123de43","sai","sales",{"project_name":"agentic ai","status":"active"})
    for emp in employees:
       if emp.has_active_project():
           print(f"{emp.name} have an active project")
       else:
           print(f"{emp.name} has no active projects")
           
if __name__=="__main__":
    main()