# 📖 **A COMPLETE ARTICLE ABOUT DECORATORS,GENERATORS,DICTIONARY,LIST,LAMBDA - CRUD CONSOLE AND API APPLICATION**
This article shows the complete information about the decorators,generators,dictionary,list and lambda and also a simple CRUD application using all these.And ideal for Python learners who want to connect core programming features with real-world project building. It combines theoretical depth with practical implementations, helping readers level up both their coding and software development skills

## **Overview**:
This comprehensive article provides a practical and beginner-to-advanced level guide to essential Python programming concepts and real-world application development. The article is divided into two major parts:

**Core Python Concepts**:
+ **Decorators** – Learn how to modify or enhance the behavior of functions using decorators.
+ **Generators** – Understand how to create memory-efficient iterators using the yield statement.
+ **Dictionaries & Lists** – Deep dive into Python’s most versatile built-in data structures with hands-on examples.
+ **Lambda Functions** – Master anonymous functions for writing concise, functional-style code.

**CRUD Application (Console & API)**:

**Console Application** – Step-by-step building of a CRUD (Create, Read, Update, Delete) app using Python, demonstrating real-time usage of the above concepts.

**API Application** – Extend the CRUD app with a RESTful API using frameworks like Flask or FastAPI, allowing external access and integration.

# 1️⃣DECORATORS
## What is Decorator?
A **Decorator** is a special function that takes another function and extends or alters its behavior without explicitly modifying it.
In other words, a decorator wraps a function to add some functionality before or after the original function runs.

## Need of Decorators 

+ **Code Reusability** :
    Instead of writing the same extra functionality (like logging, access control, timing) inside multiple functions, decorators let you write it once and apply it wherever needed.

+ **Separation of Concerns** :
    Decorators help you separate core logic of a function from auxiliary concerns like debugging, authentication, or validation, keeping code cleaner and easier to maintain.

+ **Enhancing or Modifying Behavior Without Changing Code** :
    You can add features or modify how a function works without touching the original function's code — which is especially useful for code you don’t want to or can’t modify (like third-party libraries).

+ **Consistent Application of Functionality**:
    Using decorators ensures that cross-cutting concerns (like caching, logging, etc.) are applied consistently across many functions, reducing the risk of forgetting to add them.

+ **Cleaner and More Readable Code** :
   Using @decorator syntax is cleaner and more expressive than manually wrapping functions, making the intent clear.

### Example 1.1🖋️:
simple program for a decorator

```python
def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        print("Hello !")
        result = original_function(*args, **kwargs)
        print("How are you?")
        return result
    return wrapper_function

@decorator_function
def greet(name):
    print(f"{name}!")

greet("Sri")
```

## Types of Decorators 

1. **Function Decorators**
2. **Class Decorators**
3. **Method Decorators**
4. **Built-in Decorators**

### 1. **Function Decorators** 

A function decorator in Python is a function that modifies or enhances another function without changing its actual code. It "wraps" a function, adding extra behavior before or after the original function runs.

#### example 🖋️:
`revise example 1.1`

### 2. **Class Decorators**

It takes a class as input and returns either the same class (possibly modified) or a new class.

#### Example 1.2🖋️ :

```python 
def simple_decorator(cls):
    def say_hello(self):
        print(f"Hello from {self.__class__.__name__}!")
    cls.say_hello = say_hello
    return cls

@simple_decorator
class MyClass:
    def __init__(self, name):
        self.name = name

    def show_name(self):
        print(f"My name is {self.name}")

obj = MyClass("Alice")
obj.show_name()   # My name is Alice
obj.say_hello()   # Hello from MyClass!
```
### 3. **Method decorators**

These decorate methods inside a class. They receive the method function and return a modified or wrapped version.

#### Example 1.3 🖋️:

```python 
def simple_decorator(method):
    def wrapper(self):
        print("Good Morning!")
        method(self)
        print("BYE!")
    return wrapper

class MyClass:
    @simple_decorator
    def greet(self):
        print("Hello!")

obj = MyClass()
obj.greet()
```

### 4. **Built-in Decorators**
There are some built-in decorators in pytthon. Those are

+ **a. @classmethod**
+ **b. @staticmethod**
+ **c. @property**

### a.@classmethod

In Python, **@classmethod** is a decorator used to define a method that is bound to the class and not the instance of the class.The method receives the class itself (cls) as the first argument instead of an instance (self).

##### Example 1.4🖋️:
```python
class Practice:
    a = 0  # cls var

    def __init__(self,b): 
        self.b = b

    @classmethod
    def get_var(cls):   #we can access cls var just by cls.
        cls.a += 1
        print(cls(a))
```

### b.**@staticmethod**

Defines a method that doesn't take self or cls as the first argument.It means it doesn't depends on the class and instances.

#### Example 1.5🖋️:
```python
    class Practice:
    a = 0  # cls var

    def __init__(self,b): 
        self.b = b

    @classmethod
    def get_var(cls):      # we can access cls var just by cls.
        cls.a += 1
        print(cls(a))

    @staticmethod          #no need to create instance
    def add(x, y):
        print(x + y)
```

### c.**@property**

This behaves like a normal method but always inside the class. We can call it just like an object/attribute it means no paranthesis needed.

###### Example 1.6🖋️:
```python
class employee:
    com_name="zennial_pro"
    def __init__(self,name,hourly_rate):
        self.name=name
        self.hourly_rate=hourly_rate
        self.hours_worked=0
    
    def log_hours(self,hours):
        self.hours_worked +=hours
    @property                        
    def salary(self):
        return self.hours_worked * self.hourly_rate
emp=employee("ram",500)
emp.log_hours(5)

print(emp.salary)  
```
---
# 2️⃣GENERATORS
## What is GEnerator?
A Python **Generator** is a special kind of function that uses the yield keyword to return an iterator, producing values one at a time and conserving memory by not storing the entire sequence at once.

## Need of Generators

+ Memory-efficient: Values are generated one at a time.
+ Lazy evaluation: Values are only computed when needed.
+ Great for streaming data or working with large datasets.

## How Genrators work internally 

+ When a generator function is called, it returns a generator object, not the actual result.
+ The function pauses at each yield, saving the state until the next call.
+ You can resume execution using next() or by iterating with a for loop.

### Example 2.1🖋️:
using yeild and next

```python
def even_numbers(limit): 
    num = 0
    while num <= limit:
        if num % 2 == 0:
            yield num
        num += 1

#generator object
gen = even_numbers(10)

# Use next() to get values manually
print(next(gen))  # 0
print(next(gen))  # 2
print(next(gen))  # 4
print(next(gen))  # 6
print(next(gen))  # 8
print(next(gen))  # 10
print(next(gen))  # Raises StopIteration
```
### Example 2.2🖋️:
to get all values without using next() manually use for loop

```python
a = (x**2 for x in [1, 2, 3])  # generator expression
for val in a:
    print(val)
```
or you can convert the generator to a list, which will exhaust the generator and collect all its values:

```python
all_values = list(a)
print(all_values)

```
---
# 3️⃣LAMBDA 
## What is Lambda?
A lambda function is a small anonymous function (i.e., a function without a name).It can take any number of arguments but only one expression.The expression is evaluated and returned automatically.

### Syntax
`lambda arguments: expression`

arguments: input parameters (like in a normal function)
expression: a single expression whose result is returned

### Example 3.1🖋️:

```python
# Normal function to add 10 to a number
def add(x):
    return x + 10

# Equivalent lambda function
add= lambda x: x + 10

print(add(5))  # Output: 15
```
## Use cases of lambda
+ When you need a small function for a short period of time.
+ Often used with functions like **map()**, **filter()**, **sorted()**, and **reduce()**.

### Lambda with map
The map() function applies a given function to each item in an iterable (like a list) and returns a map object (an iterator).
+ map(func, iterable): Applies func to each item in iterable.
#### Syntax
`map(lambda x: expression, iterable)`

##### Example 3.2🖋️:
```python
no_list = [1, 2, 3, 4, 5]

# Square each number
squares = list(map(lambda x: x**2, no_list))
print(squares)  # [1, 4, 9, 16, 25]
```
### Lambda with filter
The filter() function constructs an iterator from elements of an iterable for which a function returns True.
+ filter(func, iterable): Filters items in iterable for which func returns True.
##### syntax
`filter(lambda x:expression, iterable)`

##### Example 3.3🖋️:
```python
# Filter even numbers
evens = list(filter(lambda x: x % 2 == 0, no_list))
print(evens)  # [2, 4]
```
### Lambda with sorted 
+ sorted(iterable, key=..., reverse=...)
+ sorted() returns a new sorted list.
+ You can use a lambda function for custom sorting using the key argument.
##### Syntax
`sorted(iterable, key=lambda x:expression)`

##### Example 3.4🖋️:
```python 
nums = [1, 2, 3, 4, 5]

# Sort nums in descending order using lambda as key
sorted_desc = sorted(nums, key=lambda x: -x)

print(sorted_desc)
# Output: [5, 4, 3, 2, 1]
```
### Lambda with reduce
The reduce() function applies a function cumulatively to the items of an iterable (like a list), reducing it to a single value.
+ reduce(func, iterable) (in functools): Applies func cumulatively to the items in iterable.

### syntax
`reduce(lambda x, y: expression, iterable)`

##### Example 3.5🖋️:
```python
from functools import reduce

nums = [1, 2, 3, 4, 5]

sum_all = reduce(lambda x, y: x + y, nums)
print(sum_all)
# Output: 15
```
---
# 4️⃣DICTIONARY
## What is a Dictionary?
A Python **Dictionary** is a built-in data structure that stores data in key-value pairs. It is a collection that is: 
+ **Ordered** (as of Python 3.7):
    The order in which items are added to the dictionary is preserved. In earlier versions of Python, dictionaries were unordered.
+ **Changeable (Mutable)**:
    You can add, remove, or modify key-value pairs after the dictionary has been created.
+ **Does not allow duplicate keys**:
    Each key within a dictionary must be unique. If you attempt to add a key that already exists, its corresponding value will be updated. Values, however, can be duplicated.
    Key Characteristics:

## Key Characteristics

+ **Key-Value Pairs**:
    Data is stored as pairs, where each unique "key" maps to a "value."
+ **Curly Braces**:
    Dictionaries are defined using curly braces {}. Key-value pairs are separated by commas, and keys and values within a pair are separated by a colon (:).
+ **Keys must be immutable**:
    Keys can be any immutable data type (e.g., strings, numbers, tuples). Lists and other mutable objects cannot be used as keys.
+ **Values can be any data type**:
    Values can be of any type, including other dictionaries, lists, or custom objects.

## Syntax

```python 
dict_1 = {
    "key1": "value1",
    "key2": "value2",
    "key3": "value3"
}
```
## Creating a Dictionary
You can create a dictionary using curly braces **{}** with key-value pairs separated by colons **:**.

### Example 4.1🖋️:
```python
my_dict = {"name": "John", "age": 30, "country": "London"}
print(my_dict)
# You can create a dictionary by using dict() constructor
my_dict = dict(name="John", age=30, country="London")
print(my_dict)
```
### Dictionary Comprehension
It’s a compact syntax for creating dictionaries by looping over an iterable and defining keys and values on the fly.

### syntax
`{key_expression: value_expression for item in iterable}`

#### Example 4.2🖋️:
```python
squares = {x: x**2 for x in range(5)}
print(squares)
```
## Accessing values in a dictionary
You access values by using their keys inside square brackets **[]** or with the **get()** method.

### Example 4.3🖋️:
```python
my_dict = {"name": "Alice", "city": "Mumbai"}
print(my_dict["name"]) 
print(my_dict.get("name"))
print(my_dict.get("name","jeevana")) #providing a default value
```
## Adding or Updating Values
Add a new key-value pair or update an existing key by assigning a value to that key.Using **update()** also you can update a dict.

### Example 4.4🖋️:

```python
my_dict = {"name": "Alice", "city": "Mumbai"}
# Adding a new key-value pair
my_dict["age"] = 24

# Updating an existing key
my_dict["name"] = jeevitha

print(my_dict)

# using update()
my_dict.update({"age": 26, "country": "India"})
print(my_dict)  # {'name': 'Alice', 'age': 26, 'city': 'NY'}

```
## Removing Items
+ **del** keyword removes a key-value pair by key
+ **pop(key)** removes and returns the value of a key
+ **popitem()** removes and returns the last inserted key-value pair
+ **clear()** removes all items in the dictionary

### Example 4.5🖋️:
```python
my_dict = {"name": "John", "age": 30, "city": "Mumbai"}

# Using del
del my_dict["city"]

# Using pop
age = my_dict.pop("age")
print("Removed age:", age)

# Using popitem
last_item = my_dict.popitem()
print("Removed last item:", last_item)

print(my_dict)

my_dict.clear()
print(my_dict)  # Output: {}

```

## Looping through a Dictionary
You can loop through a Dictionary using **keys()**,**values()**,**items()**.

### keys()
Returns a view of all the keys in the dictionary.

#### Example 4.6🖋️:
```python
my_dict = {"name": "Alice", "age": 25, "city": "Mumbai"}
print(my_dict.keys())  # dict_keys(['name', 'age', 'city'])

# loop through keys
for key in my_dict:
    print(key)
```
### values()
Returns a view of all the values in the dictionary.

#### Example 4.7🖋️:
```python
my_dict = {"name": "Alice", "age": 25, "city": "Mumbai"}
print(my_dict.values())  # dict_values(['Alice', 25, 'NY'])

#loop through values
for value in my_dict:
    print(values)

```
### items()
Returns a view of all the items(key-value pairs) in the dictionary.

#### Example 4.8🖋️:
```python
my_dict = {"name": "Alice", "age": 25, "city": "Mumbai"}
print(my_dict.items())  # dict_items([('name', 'Alice'), ('age', 25), ('city', 'NY')])

# loop through items
for key ,value in my_dict.items:
    print(key,":",value)
```
---
# 5️⃣LIST
## What is a List?
In Python, a list is a fundamental, built-in data structure used to store an ordered, mutable collection of items. Lists are highly versatile and can contain items of different data types within the same list.

## Key characteristics of Python lists:
+ **Ordered**:
    Items in a list maintain their insertion order and can be accessed by their index (position), starting from 0 for the first element.
+ **Changeable (Mutable)**:
    You can modify, add, or remove items from a list after it has been created. 
+ **Allow Duplicates**:
    Lists can contain multiple instances of the same value.
+ **Heterogeneous**:
    A single list can store items of various data types, such as integers, strings, floats, booleans, and even other lists.

## Creating a List 
Lists are created by enclosing a comma-separated sequence of items within square brackets **[]**.

#### Example 5.1🖋️:
```python
# An empty list
empty_list = []

# A list of integers
numbers = [1, 2, 3, 4, 5]

# A list of strings
fruits = ["apple", "banana", "cherry"]

# A list with mixed data types
mixed_list = ["hello", 123, True, 3.14]

# A nested list (list of lists)
nested_list = [[1, 2], [3, 4]]

# Or by using list() constructor
list_1=list((1,2,"a",0.2))

```
## Acessing list items
Use indexing to access elements (index starts at 0).

#### Example 5.2🖋️:
```python
fruits = ['apple', 'banana', 'cherry']
print(fruits[0])  
print(fruits[2])  
```
## Updating or changing list items
Assign a new value to a specific index.

#### Example 5.3🖋️:
```python
fruits = ['apple', 'banana', 'cherry']
fruits[1] = 'orange'
print(fruits)  # Output: ['apple', 'orange', 'cherry']
```
## Adding or Appending items to a list
By using **append()** we can add new values to a list at the end. By using insert() we can add values at a specific index.

#### Example 5.4🖋️:
```python 
fruits = ['apple', 'banana']
fruits.append('grape')
print(fruits)  # Output: ['apple', 'banana', 'grape']
fruits.insert(1,"papaya")
print(fruits)  # Output: ['apple', 'papaya','banana', 'grape']
```
## Removing or Deleting items from a list
**remove()** is used to delete the first occurrence of the item.**.pop()** is used to remove and return the last item, or item at specific index.

#### Example 5.5🖋️:
```python
fruits = ['apple', 'banana', 'apple','cherry']
fruits.remove('apple')
print(fruits)  # Output: ['banana', 'apple','cherry']

a = fruits.pop()
print(a)      # Output: cherry
print(fruits)    # Output: ['banana','apple']

b = fruits.pop(1)
print(b)    # Output: banana

```
## Sorting a List
By using **.sort()** we can sort the list in ascending order by default

### acsending
#### Example 5.6🖋️:
```python
numbers = [4, 1, 3, 2]
numbers.sort()
print(numbers)  # Output: [1, 2, 3, 4]
```
### descending
#### Example 5.7🖋️:
```python
numbers = [4, 1, 3, 2]
numbers.sort(reverse=True)
print(numbers)  # Output: [4,3,2,1]
```
## Reversing a List
By using **reverse()** we can print a reversed list

#### Example 5.8🖋️:
```python 
fruits = ['apple', 'banana', 'cherry']
fruits.reverse()
print(fruits)  # Output: ['cherry', 'banana', 'apple']
```
## looping through a List

#### Example 5.9🖋️:
```python
fruits = ['apple', 'banana', 'cherry']
for fruit in fruits:
    print(fruit)
```
## List Comprehension
A shorthand way to create a list using a loop in one line

### Example 🖋️:
```python
squares = [x**2 for x in range(5)]
print(squares)  # Output: [0, 1, 4, 9, 16]
```

---
# ✒️**CRUD CONSOLE APPLICATION**
See the below CRUD (create,remove,update,delete) console application which involves logging through decorators,code building with the use of dict,list,generators... etc.

```python
import json
import os
import logging

logging.basicConfig (
    filename = 'employee.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

logging = logging.getLogger(__name__)

def handle_exceptions(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:
            logging.info(f"Executing: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error while Executing: {func.__name__} : {e}")
    return wrapper

class Employee:
    def __init__(self,name,emp_id,salary,role):
        self.name=name
        self.emp_id=emp_id
        self.salary=salary
        self.role=role
    def __str__(self):
        return (f"name:{self.name},emp_id:{self.emp_id},salary:{self.salary},role:{self.role}")
    def to_dict(self):
        return vars(self)
    
def save_to_json(Employees):
    with open(Datafile,"w") as f:
        json.dump([e.to_dict() for e in Employees],f,indent=4)

def load_from_json(datafile):
    if not os.path.exists(datafile):
        return []
    with open(datafile,"r")as f:
        employees=json.load(f)
    return [Employee(**e) for e in employees]

def add_employee():
    name=input("enter name : ")
    emp_id=input("enter employee id: ")
    salary=input("enter salary: ")
    role=input("enter role: ")
    employee=Employee(name,emp_id,salary,role)
    employees.append(employee)
    save_to_json(employees)
    print("employee added successfully........")

def list_employees():
    if not employees:
        print("no employee found...")
    for e in employees:
        print(e)

def delete_employee():
    emp_id=input("enter employee id: ")
    global employees    # we can only change global values like this
    employees=[e for e in employees if e.emp_id!=emp_id]
    save_to_json(employees)
    print("employee deleted successfully....")

def get_employee_by_emp_id():
    emp_id=input("enter employee id: ")
    employee=next((e for e in employees if e.emp_id==emp_id),None) #[e for e in emplo.....]-->list
    if employee:
        print(employee)
    else:
        print("No employee found with that ID.")

def menu():
    while True:
        print("1.Add Employee")
        print("2.List Employees")
        print("3.Delete employee")
        print("4.Get employee by employee_id")
        print("5.exit")
        choice=int(input("enter choice: "))
        if choice==1:
            add_employee()
        elif choice==2:
            list_employees()
        elif choice==3:
            delete_employee()
        elif choice==4:
            get_employee_by_emp_id()
        elif choice==5:
            print("Exiting the employee cli application....")
            break
        else:
            print("invalid choice try again later...")
if __name__=="__main__":
    Datafile="employees.json"
    employees=load_from_json(Datafile)
    menu() 
```
# ✒️**CRUD API APPLICATION**
The below example is a CRUD flask api application.
```python
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory employee storage
employees = []
id_counter = 1

logging.basicConfig (
    filename = 'employee.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

logging = logging.getLogger(__name__)

def handle_exceptions(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        try:
            logging.info(f"Executing: {func.__name__}")
            return func(*args, **kwargs)
        except Exception as e:
            logging.exception(f"Error while Executing: {func.__name__} : {e}")
    return wrapper

# CREATE employee
@app.route('/employees', methods=['POST'])
def create_employee():
    global id_counter
    data = request.get_json()
    name = data.get('name')
    position = data.get('position')

    if not name or not position:
        return jsonify({'error': 'Name and position are required'}), 400

    employee = {'id': id_counter, 'name': name, 'position': position}
    employees.append(employee)
    id_counter += 1

    return jsonify(employee), 201

# READ all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

# READ single employee
@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    return jsonify(employee)

# UPDATE employee
@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    employee['name'] = data.get('name', employee['name'])
    employee['position'] = data.get('position', employee['position'])

    return jsonify(employee)

# DELETE employee
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    global employees
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404

    employees = [emp for emp in employees if emp['id'] != employee_id]
    return jsonify({'message': 'Employee deleted', 'employee': employee})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
```
## 📋INTERVIEW QUESTIONS
### **Decorators**
1.What is a decorator in Python and why is it used?

2.Explain the difference between function decorators and method decorators.

3.What does the @ symbol mean in Python?

4.What are some real-world use cases for decorators?

5.What is the difference between @staticmethod, @classmethod, and @property?
### **Generators**
1.What is the difference between a generator and a regular function?

2.How does yield differ from return?

3.Why are generators memory-efficient?

4.What is a generator expression? How is it different from a list comprehension?
### **Dictionary**
1.What makes dictionaries in Python efficient for lookups?

2.How do dict.get() and dict[] differ?

3.Explain dictionary comprehension and its use cases.

4.How do you merge two dictionaries in Python?
### **Lambda**
1.What is a lambda function and how is it different from a regular function?

2.What are the limitations of lambda functions in Python?

3.How can you use map(), filter(), and reduce() with lambda functions?
### **List**
1.What are the main differences between lists and tuples?

2.How does Python handle list mutability?

3.What happens when you sort a list with mixed data types?











