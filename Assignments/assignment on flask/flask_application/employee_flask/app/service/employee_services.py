from app.utils.decorator import handle_exceptions
from flask import Flask,request,jsonify
from app.model.employee import Employee
import json

app=Flask(__name__)

data_file="app/data/employees_details.json"

# loading all employees
@handle_exceptions
def load_employees():
    with open (data_file, 'r') as f:
        employees  = json.load(f)
        return [Employee(**emp) for emp in  employees]     

employees=load_employees()

# finding employees who are on bench
def bench_employees():
    return [emp.to_dict() for emp in employees if emp.is_on_bench()]

# finding employee with active project
def with_active_project():
    return [emp.to_dict() for emp in employees if emp.has_project_with_status("active")]

# finding employee with completed project
def with_completed_project():
    return [emp.to_dict() for emp in employees if emp.has_project_with_status("completed")]
    
# counting employees in each department
@handle_exceptions
def employees_per_department():
    dept_count = {}
    for emp in employees:
        dept_count[emp.department] = dept_count.get(emp.department, 0) + 1
    for dept, count in dept_count.items():
        result=next(f"{dept}:{count}")
        return result
