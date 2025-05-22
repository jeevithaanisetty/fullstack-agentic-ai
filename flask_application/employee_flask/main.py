from flask import Flask,request,jsonify
from app.utils.decorator import handle_exceptions,logging
from app.service.employee_services import employees,bench_employees
from app.model.employee import Employee
from app.utils.logger import get_logger

# Initializing logger
logger = get_logger('employees.main')

# Creating an app flask application
app= Flask(__name__)

# listing all employees
@handle_exceptions
@app.route("/employees")
def list_employees():
        result=[emp.to_dict() for emp in employees]
        logger.info("employees loaded successfully")
        return jsonify(result)

# Searching employees who are on bench
@handle_exceptions
@app.route("/bench",methods=["GET"])
def employees_on_bench():
        result=bench_employees()
        logger.info("employees on bench loaded successfully")
        return jsonify(result)

# Searching employee by project status
@handle_exceptions
@app.route("/employee/project_status",methods=["POST"])
def find_by_project_status():
    data=request.get_json()
    status=data.get("status")
    result=[emp.to_dict() for emp in employees if emp.has_project_with_status(status)]
    logger.info(f"found employee with {status}")
    return jsonify(result)

# Searching employee by department
@handle_exceptions
@app.route("/find_by_dept",methods=["POST"])
def find_by_department():
    data=request.get_json()
    department=data.get("department")
    result=[emp.to_dict() for emp in employees if emp.department==department]
    logger.info(f"employees belongs to {department} dept are found")
    return jsonify(result)

# Searching employee by designation
@handle_exceptions
@app.route("/employee/designation",methods=["POST"])
def find_by_designation():
    data=request.get_json()
    designation=data.get("designation")
    result=[emp.to_dict() for emp in employees if emp.designation==designation]
    logger.info(f"employees belongs to {designation} role are found")
    return jsonify(result)

# Searching employee by location
@handle_exceptions
@app.route("/employee/location",methods=["POST"])
def find_by_location():
    data=request.get_json()
    location=data.get("location")
    result=[emp.to_dict() for emp in employees if emp.location==location]
    logger.info(f"employees belongs to {location} are found")
    return jsonify(result)

# Searching employee having salary in between x and  y
@handle_exceptions
@app.route("/employee/salary",methods=["POST"])
def find_by_salary():
    data=request.get_json()
    min_salary=data.get("minimum_salary")
    max_salary=data.get("maximum_salary")
    result=[emp.to_dict() for emp in employees if min_salary<=emp.salary>=max_salary]
    logger.info(f"employees having salary in between {min_salary} ,{max_salary} are found")
    return jsonify(result)

# Searching employee having age in between x and y
@handle_exceptions
@app.route("/employee/age_in_between",methods=["POST"])
def find_emp_by_age():
    data=request.get_json()
    min_age=data.get("minimum_age")
    max_age=data.get("maximum_age")
    result=[emp.to_dict() for emp in employees if min_age<=emp.get_age()>=max_age]
    logger.info(f"employees with age in between {min_age} and {max_age} are found")
    return jsonify(result)

# Searching employee having age above x
@handle_exceptions
@app.route("/employee/above_age",methods=["POST"])
def find_emp_by_above_age():
    data=request.get_json()
    age=data.get("age")
    result=[emp.to_dict() for emp in employees if emp.get_age()>=age]
    logger.info(f"employees having age more than {age} are found")
    return jsonify(result)

# Searching employee by porject name
@handle_exceptions
@app.route("/find_by_project_name",methods=["POST"])
def find_by_project():
    data=request.get_json()
    name=data.get("name")
    result=[emp.to_dict() for emp in employees for p in emp.projects if p.name==name ]
    logger.info(f"employees belongs to {name} project are found")
    return jsonify(result)

# A simple "/" call to know the health of flask application
@app.route("/")
def hello():
    return("hello viewer!")

if __name__== "__main__":
    # Running app flask application on localserver
    app.run(debug=True)