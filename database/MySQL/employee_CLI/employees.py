import mysql.connector

conn=mysql.connector.connect(
    host="localhost",
    user="mukundh",
    password="jeevitha123@",
    database="employees"
)
if conn.is_connected():
    print("connection successful")
cursor=conn.cursor()
cursor.execute("create table if not exists Employees_info(id integer primary key auto_increment,name varchar(255),age varchar(20),emp_id varchar(20) unique ,email varchar(255) unique ,salary varchar(20))")
cursor.execute("use employees")
conn.commit()

# mysql -u root -p--->
# CREATE USER IF NOT EXISTS 'mukundh'@'localhost' IDENTIFIED BY 'jeevitha123@';
# ALTER USER 'mukundh'@'localhost' IDENTIFIED WITH mysql_native_password BY 'jeevitha123@';
# GRANT ALL PRIVILEGES ON employees.* TO 'mukundh'@'localhost';
# FLUSH PRIVILEGES;

class Employee:
    def __init__(self,name,age,emp_id,email,salary):
        self.name=name
        self.age=age
        self.emp_id=emp_id
        self.email=email
        self.salary=salary
    def __str__(self):
        return(f"name:{self.name},age:{self.age},emp_id:{self.emp_id},email:{self.email},salary:{self.salary}")
    def to_tuple(self):
        return(
            self.name,
            self.age,
            self.emp_id,
            self.email,
            self.salary)
    
def save_to_mysqldb(data):
    cursor.execute("insert into Employees_info(name,age,emp_id,email,salary) values(%s,%s,%s,%s,%s)",data.to_tuple())
    conn.commit()
    print(f"employee {data.name} saved successfully")

def load_from_mysqldb():
    cursor.execute("select name,age,emp_id,email,salary from Employees_info")
    employees=cursor.fetchall()
    return [Employee(name,age,emp_id,email,salary) for name,age,emp_id,email,salary in employees]

def add_employee():
    name=input("enter name: ")
    age=int(input("enter age: "))
    emp_id=input("enter emp_id: ")
    email=input("enter email: ")
    salary=int(input("enter salary: "))
    employee=Employee(name,age,emp_id,email,salary)
    save_to_mysqldb(employee) 

def get_employees():
    employees=load_from_mysqldb()
    for emp in employees:
        print(emp)

def delete_employee():
    emp_id=input("enter emp_id: ")
    cursor.execute("delete from Employees_info where emp_id=%s",(emp_id,))
    conn.commit()
    print(f"employee with employee id deleted successfully...")

def get_employee_by_email():
    email=input("enter email: ")
    cursor.execute("select * from Employees_info where email=%s",(email,))
    employee=cursor.fetchone()
    print(employee) 

def menu():
    while True:
        print("1.Add Employee")
        print("2.List Employees")
        print("3.Delete employee")
        print("4.Get employee by email")
        print("5.exit")
        choice=int(input("enter choice: "))
        
        if choice==1:
            add_employee()
        elif choice==2:
            get_employees()
        elif choice==3:
            delete_employee()
        elif choice==4:
            get_employee_by_email()
        elif choice==5:
            print("exiting the employee cli application..........")
            break
        else:
            print("invalid choice try again.......")
if __name__=="__main__":
    menu()











# CREATE USER IF NOT EXISTS 'mukundh'@'localhost' IDENTIFIED BY 'jeevitha123@';
# ALTER USER 'mukundh'@'localhost' IDENTIFIED WITH mysql_native_password BY 'jeevitha123@';
# GRANT ALL PRIVILEGES ON employees.* TO 'mukundh'@'localhost';
# FLUSH PRIVILEGES;