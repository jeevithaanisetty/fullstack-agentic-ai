import json
import os


class Student:
    def __init__(self, name,rank, dob, email,branch,fee_paid=None):
        self.name = name
        self.rank = rank
        self.dob = dob
        self.email = email
        self.branch=branch
        self.fee_paid=fee_paid
        

    def to_dict(self):
        return vars(self)

class Department:
    def __init__(self, department, no_of_seats, available_seats,fee):
        self.department = department
        self.no_of_seats = no_of_seats
        self.available_seats = available_seats
        self.fee=fee

    def to_dict(self):
        return vars(self)

def load_students(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        students = json.load(f)
        return [Student(**s) for s in students]

def load_departments(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        departments = json.load(f)
        return [Department(**d) for d in departments]

def save_students(students, file_name):
    with open(file_name, "w") as f:
        json.dump([s.to_dict() for s in students], f, indent=4)

def save_departments(departments, file_name):
    with open(file_name, "w") as f:
        json.dump([d.to_dict() for d in departments], f, indent=4)

def seat_allotment(Branch):
    for d in departments:
        if d.department.lower() == Branch.lower():
            if d.available_seats > 0:
                print("\nSeats are available. Enter your details.")
                name = input("\nEnter name: ")
                dob = input("Enter Date of Birth: ")
                rank = int(input("Enter rank: "))
                email = input("Enter email: ")
                branch=Branch
                if any (s.rank==rank or s.email==email for s in students):
                    print("\nCheck rank and mail.Student existed alredy with above details.")
                else:
                    student = Student(name, rank, dob, email,branch)
                    students.append(student)
                    save_students(students, student_file)       # saving student to college list after checking seats availability
                    d.available_seats -= 1                      # decrement of available seats after seat allocation
                    save_departments(departments, dept_file)    # saving change in available seats in departments
                    return f"\nStudent assigned to {branch} department"
            else:
                return f"\nNo available seats for {branch} department. Apply for other branches."
    return f"\nDepartment {branch} not found."

def Fee_pay():
    email = input("Enter your email: ").strip()
    for s in students:
        if s.email==email:
            print("\n***** Choose Payment Type *****")
            print("MANAGEMENT\nCOUNSELLING\n")
            option = input().upper()

    if option not in ["MANAGEMENT", "COUNSELLING"]:
        return "Invalid payment type selected."
    
    print("\n**** Choose Branch *****\nECE\nCSE\nEEE\nCIVIL\nMECH\n")
    choice = input().upper()

    for d in departments:
        if d.department.upper() == choice:
            
            fee_amount = d.fee[option.lower()]      #  similar to d.fee["management/counselling"]

            print(f"Fee for {option.lower()} is: {fee_amount}")
            amount = int(input("Enter amount to pay:"))
            s.fee_paid = amount
            save_students(students, student_file)

            remaining = fee_amount - amount
            return f"Amount of {amount} paid successfully. Remaining amount to be paid is {remaining}"

    return "Invalid branch selected."


def menu():
    while True:
        print("\n ******** STUDENT MENU ********")
        print("1. Seat Allotment")
        print("2. List Students")
        print("3.fee payment")
        print("4. Exit")
        choice = int(input("\nEnter option here: "))
        

        if choice == 1:
            print("\n*******Choose******:")
            print("MANAGEMENT\nCOUNSELLING\n")
            option=input()
            # Student Registration under management
            if option.upper()=="MANAGEMENT":
                print("\nSelect Branch:\nECE\nCSE\nEEE\nCIVIL\nMECH")
                branch_name=input("\n")
                result=seat_allotment(branch_name)
                print(result)
            #Stuednt registration under counselling    
            if option.upper()=="COUNSELLING":

                rank = int(input("Enter your rank: "))

                if rank > 150000:
                    print("Rank is not sufficient for seat allotment under counselling. Try under management.")
                elif 0 <= rank <= 40000:
                    print("Eligible branches:\nECE\nCSE\nEEE\nCIVIL\nMECH")
                    branch_name = input("****Choose Branch***** ")
                    result = seat_allotment(branch_name)
                    print(result)
                elif 40000 < rank <= 70000:
                    print("Eligible branches:\nEEE\nCIVIL\nMECH")
                    branch_name = input("\n******Choose Branch*****")
                    result = seat_allotment(branch_name)
                    print(result)
                elif 70000 < rank <= 150000:
                    print("Eligible branches:\nCIVIL\nMECH")
                    branch_name = input("\n******Choose Branch*****")
                    result = seat_allotment(branch_name)
                    print(result)

        elif choice == 2:
            for s in students:
                print(s.to_dict())

        elif choice==3:
            result=Fee_pay()
            print(result)

        elif choice == 4:
            print("\nExiting program.")
            break
        else:
            print("\nInvalid option. Please select from the menu.")


if __name__ == "__main__":
    student_file = "data/student.json"
    dept_file = "data/management.json"

    students = load_students(student_file)
    departments = load_departments(dept_file)

    menu()
