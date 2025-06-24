import json
import os

class Employee:
    def __init__(self,name,emp_id,salary,role):
        self.name=name
        self.emp_id=emp_id
        self.salary=salary
        self.role=role
    def __str__(self):
        return (f"name:{self.name},emp_id:{self.emp_id},salary:{self.salary},role:{self.role}")
    def to_dict(self):
        return vars(self)
    
def save_to_json(Employees):
    #employees.append(employee)
    with open(Datafile,"w") as f:
        json.dump([e.to_dict() for e in Employees],f,indent=4)

def load_from_json(datafile):
    if not os.path.exists(datafile):
        return []
    with open(datafile,"r")as f:
        employees=json.load(f)
    return [Employee(**e) for e in employees]

def add_employee():
    name=input("enter name : ")
    emp_id=input("enter employee id: ")
    salary=input("enter salary: ")
    role=input("enter role: ")
    employee=Employee(name,emp_id,salary,role)
    employees.append(employee)
    save_to_json(employees)
    print("employee added successfully........")

def list_employees():
    if not employees:
        print("no employee found...")
    for e in employees:
        print(e)

def delete_employee():
    emp_id=input("enter employee id: ")
    global employees    # we can only change global values like this
    employees=[e for e in employees if e.emp_id!=emp_id]
    save_to_json(employees)
    print("employee deleted successfully....")

def get_employee_by_emp_id():
    emp_id=input("enter employee id: ")
    employee=next((e for e in employees if e.emp_id==emp_id),None) #[e for e in emplo.....]-->gives list obj as output
    if employee:
        print(employee)
    else:
        print("No employee found with that ID.")

def menu():
    while True:
        print("1.Add Employee")
        print("2.List Employees")
        print("3.Delete employee")
        print("4.Get employee by employee_id")
        print("5.exit")
        choice=int(input("enter choice: "))
        if choice==1:
            add_employee()
        elif choice==2:
            list_employees()
        elif choice==3:
            delete_employee()
        elif choice==4:
            get_employee_by_emp_id()
        elif choice==5:
            print("Exiting the employee cli application....")
            break
        else:
            print("invalid choice try again later...")
if __name__=="__main__":
    Datafile="employees.json"
    employees=load_from_json(Datafile)
    menu() 

