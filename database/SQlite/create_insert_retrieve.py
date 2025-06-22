import sqlite3   # built_in module

# Connect to a database (it will be created if it doesn't exist)
conn = sqlite3.connect("school.db")
cursor = conn.cursor()   #The cursor is like your hand — it lets you write notes, ask questions, and grab books (data).When you're done, you close() your hand and exit the library (conn.close()).

# 1. Create a table                             #cursor.execute() sends your SQL query (like SELECT, INSERT, CREATE TABLE) to the database engine.without excecute ntg will happen
cursor.execute("""                                      
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    grade TEXT
)
""")

# 2. Insert data
cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("Alice", 14, "8th")) #? is a placeholder for a value.Handles special characters (like quotes or symbols in names)
cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("Bob", 15, "9th"))

conn.commit()#When you modify the database with INSERT, UPDATE, or DELETE to save changes you have to say conn.commit

# 3. Query data/retrieve/request
cursor.execute("SELECT * FROM students") #it'll auto.. gives rows even if u don't mention
#cursor.execute("SELECT name, age FROM students") ---> to select perticular columns only
rows = cursor.fetchall()# to get one fetchone(),to fetch first n rows fetchmany(n)
for row in rows:
    print(row)

conn.close()  # after picking what we want we exit library.

#-----------------Practice--------------------------------------------------------------------------------------------

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Books")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        title TEXT,
        year_published INTEGER
    )
""")

n = int(input("Enter number of books to be inserted: "))

for i in range(n):
    print(f"\nBook {i+1}")
    author = input("  Enter author: ")
    title = input("  Enter title: ")
    year_published = int(input("  Enter year: "))

    cursor.execute(
        "INSERT INTO Books (author, title, year_published) VALUES (?, ?, ?)",
        (author, title, year_published)
    )
conn.commit()

cursor.execute("SELECT * FROM Books")
rows = cursor.fetchall()

print("\nBooks in database:")
for row in rows:
    print(row)

conn.close()



