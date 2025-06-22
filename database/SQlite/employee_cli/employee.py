import sqlite3

conn=sqlite3.connect("employee.db")
cursor=conn.cursor()

class Employee:
    def __init__(self,name,age,email,emp_id,dob):
        self.name=name
        self.age=age
        self.email=email
        self.emp_id=emp_id
        self.dob=dob
    
    def __str__(self):
        return(f"name:{self.name} age:{self.age} email:{self.email} emp_id:{self.emp_id} dob:{self.dob}")
    
    def to_tuple(self): #sql db data will be in tuple format(while saving obj to db conv is imp)
        return (
                self.name,
                self.age,
                self.email,
                self.emp_id,
                self.dob
        )
    
def load_employees():
    try:
        # with sqlite3.connect("employee.db") as conn:
        #     cursor = conn.cursor()
        cursor.execute("SELECT name,age,email,emp_id,dob FROM Employees")
        rows = cursor.fetchall()
        return [Employee(name,age,email,emp_id,dob) for name,age,email,emp_id,dob in rows]
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    
def save_to_db(data):
    #with open("employee.db") as f:---->can't open sql db as a file so we have to use sqlite3.connect
    # with sqlite3.connect("employee.db") as conn:
    #     cursor=conn.cursor()
    cursor.execute("""
    create table if not exists Employees(
        Name text not null,
        Age integer not null,
        Email text unique not null,
        Emp_id integer unique primary key,
        Dob text not null
    )
    """)
    cursor.execute("insert into Employees(name,age,email,emp_id,dob) values(?,?,?,?,?)",data.to_tuple())
    conn.commit()
    
def get_all_employees():
    employees=load_employees()
    for emp in employees:
        print(emp)

def del_all_employees():  # delete table--->drop
    cursor.execute("drop table Employees")
    conn.commit()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")# to show table after clear
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])
    print("All Employees deleted successfully")

def add_employees():
    name=input("enter name: ")
    age=int(input("enter age:"))
    email=input("enter email: ")
    emp_id=int(input("enter emp_id: "))
    dob=input("enter dateofbirth: ")
    employee=Employee(name,age,email,emp_id,dob)
    save_to_db(employee)
    print(f"Employee with name {name} added successfully")

def delete_employee():
    email=input("enter email id:") # unique-so only specified will be del
    cursor.execute("delete from Employees where email= ? ",(email,))  #if i do email=email it'll always gives true
    conn.commit()
    if cursor.rowcount>0:    # rowcount-->how many rows effected by last operation
        print(f"employee with email_id {email} deleted successfully")
    else:
        print("email not found")

def get_employee_by_emp_id():
    emp_id=int(input("enter emp_id: "))
    cursor.execute("select * from Employees where emp_id=?",(emp_id,))
    employee=cursor.fetchall()
    print(f"--------------------------------------------------\n{employee}\n------------------------------------------------------")


def menu():
    while True:
        print("***********Employee CLI**********")
        print("1.List Employees")
        print("2.Add Employees ")
        print("3.Delete Employees")
        print("4.Search employee by employee id : ")
        print("5.delete all employees")
        print("6.Exit")
        choice=int(input("enter your choice from above 1-4: "))

        if choice==1:
            get_all_employees()
        elif choice==2:
            add_employees()
        elif choice==3:
            delete_employee()
        elif choice==4:
            get_employee_by_emp_id()
        elif choice==5:
            del_table()
        elif choice==6:
            print("Exiting the employee cli application......")
            break
        else:
            print("invalid option select from 1-5 only....")
if __name__=="__main__":
    menu()