import sqlite3

class Student:
    def __init__(self,name,age):
        #self.id=id
        self.name=name
        self.age=age
    
    def __str__(self):
        return(f"name:{self.name} and age:{self.age}")

def get_students(): #loading students/data from sql-db
    conn=sqlite3.connect("school.db")
    cursor=conn.cursor()

    cursor.execute("select name,age from students")# unpacking may fail otherwise with select*from
    result=cursor.fetchall()

    conn.close()
    return [Student(name,age) for name,age in result]  #sql-tuple so can't use like **Students
# def get_students():
#     students = []
#     try:
#         with sqlite3.connect("school.db") as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT name, age FROM students")
#             rows = cursor.fetchall()
#             students = [Student(name, age) for name, age in rows]
#     except sqlite3.Error as e:
#         print(f"Database error: {e}")
#     return students

def list_students(Students):
    for student in Students:
        print(student)  # output could be --> name:Alice and age:14
                                        #     name:Bob and age:15

if __name__=="__main__":
    students=get_students()
    list_students(students)
    
#-->Student(name, age) — Works with tuples.
# --->Student(**row) — Works only if row is a dict-like object.
# --->Use conn.row_factory = sqlite3.Row to access column names and allow **.
# then--students = [Student(**dict(row)) for row in rows]
