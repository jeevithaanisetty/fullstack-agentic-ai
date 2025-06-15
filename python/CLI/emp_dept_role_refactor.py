import json
import os

DEPARTMENTS_JSON="department.json"
ROLES_JSON="roles.json"
EMPLOYEES_JSON="employees.json"

def save_to_json(data,file):
    with open(file,"w") as f:
        json.dump(data,f,indent=4)


def load_from_json(file):
    if not os.path.exists(file):
        return []
    with open(file,"r") as f:
       return json.load(f)
    
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

class Role:         
    def __init__(self, role_id,role_name):
        self.role_id=role_id
        self.role_name=role_name
    def to_dict(self):
        return vars(self) 
    def __str__(self):
        return f"Department {self.role_id} - {self.role_name}"
    
    @classmethod
    def add_role(cls):
        role_id=input("enter role_id:")
        role_name=input("enter role_name:")
        
        roles=load_from_json(ROLES_JSON)
        role=Role(role_id,role_name).to_dict()
        roles.append(role)
        save_to_json(roles,ROLES_JSON)
    
    def list_roles():          
        roles=load_from_json(ROLES_JSON)
        print("\033[92m\nAvailable roles")
        for r in roles:
            print(f"{r['role_id']} : {r['role_name']}")
        print("\033[0m")
    
    def delete_role():
        role_id=input("enter role_id:")
        roles=load_from_json(ROLES_JSON)
        new_list=list(filter(lambda r:r['role_id']!=role_id, roles))
        save_to_json(new_list,ROLES_JSON)
        print(f"employee with {role_id} as role_id is deleted")


    
    
def menu():
    while True:
        print("\n===========EMPLOYEE SYSTEM========")
        print("1.Add Department")
        print("2. List department")
        print("3.add_roles")
        print("4.list_roles")
        print("5.add employee")
        print("6.list employee")
        print("7.delete employee")
        print("8.delete departments")
        print("9.delete role")
        print("0.Exit")

        choice=input("choose an option:")
        
        if choice=="1": Department.add_department()
        elif choice=="2": Department.list_departments()
        elif choice=="3": Role.add_role()
        elif choice=="4": Role.list_roles()
        elif choice=="5": Employee.add_employee()
        elif choice=="6": Employee.list_employees()
        elif choice=="7": Employee.delete_employee()
        elif choice=="8": Role.delete_role()
        elif choice=="9": Department.delete_department()
        elif choice=="0": print("\033[92m\nexiting........\033[0m") ;break  
        else: print("\033[91minvalid choice\033[0m")

if __name__=='__main__':
    menu()


