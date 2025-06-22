import sqlite3

conn=sqlite3.connect("student.db")
cursor=conn.cursor()

students=[
    ("mukundh",6),
    ("vani",10),
    ("ravi",4),
    ("sasi",7),
    ("ramya",9)
]

cursor.execute("""
                create table if not exists students(
                                                    id integer primary key autoincrement,
                                                    name text not null,
                                                    age text 
               )
""")

cursor.executemany("insert into students (name,age) values(?,?)",students)
conn.commit()
 
cursor.execute("select * from students")
rows=cursor.fetchall()
print("before deletion")#----->due to fast script excecution u may not get this print in o/p so for clarification to sym say this
for row in rows:
    print(row)

#clear table data
cursor.execute("delete from students") 
conn.commit()
#after del see table 
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")# to show table after clear
tables = cursor.fetchall()
for table in tables:
    print(table[0])

conn.close()


#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") --->shows table data
#cursor.execute("drop table students")--->del table
#cursor.execute("delete from students")---->clear table data  