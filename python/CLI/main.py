
from company.employee import Employee                  
from company.department import Department
from company.role import Role
#from examples import __init__
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


