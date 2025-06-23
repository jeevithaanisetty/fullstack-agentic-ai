import mysql.connector

conn=mysql.connector.connect(
    host="localhost",
    user="sri",
    password="jeevitha123@"

)
cursor=conn.cursor()
if conn.is_connected():
    print("connection successful") #conn will be successful if u use existed user and no need of root connection

cursor.execute("create database if not exists employees")
#cursor.execute("GRANT ALL PRIVILEGES ON employees.* TO 'sri'@'localhost';")
#cursor.execute("FLUSH PRIVILEGES;")
cursor.execute("use employees")
conn.commit()

cursor.execute("create table if not exists employees_info(id integer primary key auto_increment,name text,age integer,emp_id varchar(255) unique,email varchar(225) unique,salary integer)")
cursor.execute("insert into employees_info(name,age,emp_id,email,salary) values (%s,%s,%s,%s,%s)",("mani",25,"A123","mani@gmail.com",25000))
conn.commit()

cursor.execute("select name,age,emp_id,email,salary from employees_info ")
rows=cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()




# access denied to sri@localhost to database employees error--->step 1:mysql -u root -p use this command in conda
# step2: enter password-->mqsql>  here u can crete user and grant previllages like shown below
# step 3:
# CREATE USER IF NOT EXISTS 'sri'@'localhost' IDENTIFIED BY 'jeevitha123@';
# ALTER USER 'sri'@'localhost' IDENTIFIED WITH mysql_native_password BY 'jeevitha123@';
# GRANT ALL PRIVILEGES ON employees.* TO 'sri'@'localhost';
# FLUSH PRIVILEGES;
# step 4: mysql> exit;---->run py file again u may not get error

#conclusion:  using all ways may give error except above ex:granting per in code is not worked err remains same