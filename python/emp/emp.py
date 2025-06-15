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

@handle_exception
def load_data(filename):
    with open(filename,"r") as f:
        return json.load(f) 
    logging.info("data loaded successfully")   ,200
        
@handle_exception
def save_data(filename,data):
    with open(filename,"w") as f:
        json.dumps(data,f,indent=4)
        logging.info(f'saved json file successfully'),200

@handle_exception
def find_by_employee_dept(employee_data,department_name):
    result=[]

    for emp in employee_data:
        if emp["department"]==department_name:
            result.append(emp)
    print(f"emp belongs to {department_name} dept is :{result}")

    result=list(filter(lambda emp:emp["department"]==department_name,employee_data))
    print(f"using filter and lambda :{result}")

    result=[emp for emp in employee_data if emp["department"]==department_name ]
    print(f"using list comprehention result is :{result}")

@handle_exception
def find_by_active_project(employee_data):
    result=[]

    for emp in employee_data:
        for p in emp.get("projects",[]):
            if p["status"]=="active":
                result.append(emp)
                break
    print(f"employees with active projects are:{result}")

    result=[emp for emp in employee_data if any(p["status"]=="active" for p in emp.get("projects",[]))]
    print(f"using list comprehention emp with active projects are:{result}")

@handle_exception
def max_emp_in_dept_count(employee_data):
    dept_count={}
    for emp in employee_data:
        dept_name=emp["department"]
        dept_count[dept_name]=dept_count.get(dept_name,0)+1
    max_emp=max(dept_count)
    print(f"department having max no of employees is:{max_emp}  ")

@handle_exception
def unique_depts(employee_data):
    unique=set(emp["department"] for emp in employee_data)
    print(unique)

@handle_exception
def id_name(employee_data):
   result=((emp["emp_id"],emp["department"]) for emp in employee_data )   #lazy generator so use list/set then u no need next
   print(next(result))
   print(next(result))
    
if __name__=="__main__":

  employee_data=load_data(DATA_JSON)
#   find_by_employee_dept(employee_data,"tech")
#   find_by_active_project(employee_data)
# max_emp_in_dept_count(employee_data)
# unique_depts(employee_data)
# id_name(employee_data)