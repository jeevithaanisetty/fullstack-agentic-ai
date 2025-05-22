
import json
import logging
from datetime  import datetime
from functools import wraps
from flask import Flask,request,jsonify

logging.basicConfig (
    filename = 'employee.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

logging = logging.getLogger(__name__)

def handle_exceptions(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:
            logging.info(f"Executing: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error while Executing: {func.__name__} : {e}")
    return wrapper

app= Flask(__name__)

@app.route("/")
def hello():
    return("hello viewer!")

data_file="employees_details.json"


class Project:
    def __init__(self, project_id, name,status):
        self.project_id = project_id 
        self.name = name
        self.status = status

    def to_dict(self):
        return {
            "project_id":self.project_id, 
            "name":self.name,
            "status":self.status
        }
    def from_dict(data):
        return[
            data["project_id"],
            data["name"],
            data["status"]
        ]

class Employee:
    def __init__(self, emp_id, name, department,salary,designation, location,dob, projects):
        self.emp_id =  emp_id
        self.name = name 
        self.department = department
        self.salary = salary
        self.designation =  designation
        self.location = location
        self.dob = dob
        self.projects = [ Project(**p) for p in projects]

    def to_dict(self):
       return {
           "emp_id":self.emp_id, 
            "name":self.name, 
            "department":self.department,
            "salary":self.salary,
            "designation":self.designation, 
            "location":self.location,
            "dob":self.dob, 
            "projects":[p.to_dict() for p in self.projects]         # converting each project object to a dictionary
        }
    
    def from_dict(data):
        return [
                data["emp_id"],
                data["name"],
                data["department"],
                data["salary"],
                data["designation"],
                data["location"],
                data["dob"],
                data["projects"]
        ]

    def is_on_bench(self):
        return len(self.projects) == 0 

    def has_project_with_status(self, status):
            return any (p.status == status for p in self.projects)
    
    def get_age (self):
        birth_date = datetime.strptime(self.dob, "%Y-%m-%d")
        return (datetime.now() - birth_date).days // 365

@handle_exceptions
@app.route("/employees")
def list_employees():
    result=[emp.to_dict() for emp in employees]
    return jsonify(result)

@handle_exceptions
@app.route("/bench",methods=["GET"])
def bench_employees():
    employees_on_bench=[emp.to_dict() for emp in employees if emp.is_on_bench()]
    return jsonify(employees_on_bench)

@handle_exceptions
@app.route("/active_project")
def with_active_project():
    result=[emp.to_dict() for emp in employees if emp.has_project_with_status("active")]
    return jsonify(result)

@handle_exceptions
@app.route("/completed_project")
def with_completed_project():
    result=[emp.to_dict() for emp in employees if emp.has_project_with_status("completed")]
    return jsonify(result)

@handle_exceptions
@app.route("/find_by_dept",methods=["POST"])
def find_by_department():
    data=request.get_json()
    department=data.get("department")
    result=[emp.to_dict() for emp in employees if emp.department==department]
    return jsonify(result)

@handle_exceptions
@app.route("/find_by_designation",methods=["POST"])
def find_by_designation():
    data=request.get_json()
    designation=data.get("designation")
    result=[emp.to_dict() for emp in employees if emp.designation==designation]
    return jsonify(result)

@handle_exceptions
@app.route("/find_by_location",methods=["POST"])
def find_by_location():
    data=request.get_json()
    location=data.get("location")
    result=[emp.to_dict() for emp in employees if emp.location==location]
    return jsonify(result)

@handle_exceptions
@app.route("/find_by_salary",methods=["POST"])
def find_by_salary():
    data=request.get_json()
    min_salary=data.get("minimum_salary")
    max_salary=data.get("maximum_salary")
    result=[emp.to_dict() for emp in employees if min_salary<=emp.salary>=max_salary]
    return jsonify(result)

@handle_exceptions
@app.route("/find_age_in_between",methods=["POST"])
def find_emp_by_age():
    data=request.get_json()
    min_age=data.get("minimum_age")
    max_age=data.get("maximum_age")
    result=[emp.to_dict() for emp in employees if min_age<=emp.get_age()>=max_age]
    return jsonify(result)

@handle_exceptions
@app.route("/find_by_above_age",methods=["POST"])
def find_emp_by_above_age():
    data=request.get_json()
    age=data.get("age")
    result=[emp.to_dict() for emp in employees if emp.get_age()>=age]
    return jsonify(result)

@handle_exceptions
@app.route("/find_by_project_name",methods=["POST"])
def find_by_project():
    data=request.get_json()
    name=data.get("name")
    result=[emp.to_dict() for emp in employees for p in emp.projects if p.name==name ]
    return jsonify(result)

@handle_exceptions
@app.route("/employee_count_per_dept")
def employees_per_department():
    dept_count = {}
    for emp in employees:
        dept_count[emp.department] = dept_count.get(emp.department, 0) + 1
    for dept, count in dept_count.items():
        return (f"{dept}:{count}")

@handle_exceptions
def load_employees(data):
    with open (data, 'r') as f:
        employees  = json.load(f)
        return [Employee(**emp) for emp in  employees]
    
employees=load_employees(data_file)

if __name__== "__main__":
    app.run(debug=True)
    

      
