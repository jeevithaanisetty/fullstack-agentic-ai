import mysql.connector

conn_root= mysql.connector.connect(
        host="localhost",
        user="root",
        password="jeevitha123@",
        #database="student"
    )
if conn_root.is_connected():
    print("\nConnected successfully......\n")

cursor_root = conn_root.cursor()

#u should have to create user before connecting to it
cursor_root.execute("CREATE USER IF NOT EXISTS 'sri'@'localhost' IDENTIFIED BY 'jeevitha123@';")
cursor_root.execute("CREATE DATABASE IF NOT EXISTS student;")

cursor_root.execute("GRANT ALL PRIVILEGES ON student.* TO 'sri'@'localhost';")
cursor_root.execute("FLUSH PRIVILEGES;")
conn_root.commit()

conn = mysql.connector.connect(
        host="localhost",
        user="sri",
        password="jeevitha123@",
        database="student"
    )
cursor=conn.cursor()
if conn.is_connected():
    print("user connected successfully......")

cursor.execute("create table if not exists student_info(id integer primary key auto_increment,name text,roll_no text,unique(roll_no(255)))")
cursor.execute("insert into student_info(name,roll_no)values(%s,%s)",("raghu","B123"))
conn.commit()
cursor.execute("select* from student_info")
rows=cursor.fetchall()   
print("\nstudent_info......") 
for row in rows:
    print(row)

cursor.execute("SHOW PROCESSLIST;") # Show current MySQL process list--->to see user connection
print("\nMySQL Process List:")
for row in cursor.fetchall():
    print(row)

conn.close()