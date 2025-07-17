# DECORATORS

    A decorator is a special function that takes another function and extends or alters its behavior without explicitly modifying it.

    In other words, a decorator wraps a function to add some functionality before or after the original function runs.

## Need of Decorators 

+ Code Reusability :
    Instead of writing the same extra functionality (like logging, access control, timing) inside multiple functions, decorators let you write it once and apply it wherever needed.

+ Separation of Concerns :
    Decorators help you separate core logic of a function from auxiliary concerns like debugging, authentication, or validation, keeping code cleaner and easier to maintain.

+ Enhancing or Modifying Behavior Without Changing Code :
    You can add features or modify how a function works without touching the original function's code — which is especially useful for code you don’t want to or can’t modify (like third-party libraries).

+ Consistent Application of Functionality:
    Using decorators ensures that cross-cutting concerns (like caching, logging, etc.) are applied consistently across many functions, reducing the risk of forgetting to add them.

+ Cleaner and More Readable Code :
   Using @decorator syntax is cleaner and more expressive than manually wrapping functions, making the intent clear.

### Example 1.1:
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

1. Function Decorators
2. Class Decorators
3. Method Decorators
4. Built-in Decorators

### 1. Function Decorators 

    A decorator in Python is a function that modifies or enhances another function without changing its actual code. It "wraps" a function, adding extra behavior before or after the original function runs.

#### example :

```python
revise example 1.1
```

### Class Decorators 

    It takes a class as input and returns either the same class (possibly modified) or a new class.

#### Example 1.2 :

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
### Method decorators 

    These decorate methods inside a class. They receive the method function and return a modified or wrapped version.

#### Example 1.3 :

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

### Built-in Decorators
    There are some built-in decorators in pytthon. Those are
+ @classmethod
+ @statismethod
+ @property

#### @classmethod

    In Python, @classmethod is a decorator used to define a method that is bound to the class and not the instance of the class.The method receives the class itself (cls) as the first argument instead of an instance (self).

##### Example 1.4
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

#### @staticmethod
    
    Defines a method that doesn't take self or cls as the first argument.It means it doesn't depends on the class and instances.

##### Example 1.5
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

#### @property

    This behaves like a normal method but always inside the class. We can call it just like an object/attribute it means no paranthesis needed.

###### Example 1.6
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



# GENERATORS

    A Python generator is a special kind of function that uses the yield keyword to return an iterator, producing values one at a time and conserving memory by not storing the entire sequence at once.

## Need of Generators

+ Memory-efficient: Values are generated one at a time.
+ Lazy evaluation: Values are only computed when needed.
+ Great for streaming data or working with large datasets.

## How Genrators work internally 

+ When a generator function is called, it returns a generator object, not the actual result.
+ The function pauses at each yield, saving the state until the next call.
+ You can resume execution using next() or by iterating with a for loop.

### Example 2.1
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

### Example 2.2
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
# LAMBDA 

    A lambda function is a small anonymous function (i.e., a function without a name).It can take any number of arguments but only one expression.The expression is evaluated and returned automatically.

### Syntax
```python
lambda arguments: expression
```
arguments: input parameters (like in a normal function)
expression: a single expression whose result is returned

### Example 3.1

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
+ Often used with functions like map(), filter(), sorted(), and reduce().

### Lambda with map

#### Syntax
    map(lambda x: expression, iterable)

##### Example 3.2
```python
no_list = [1, 2, 3, 4, 5]

# Square each number
squares = list(map(lambda x: x**2, no_list))
print(squares)  # [1, 4, 9, 16, 25]
```

### Lambda with filter

##### syntax
    filter(lambda x:expression, iterable)

##### Example 3.3
```python
# Filter even numbers
evens = list(filter(lambda x: x % 2 == 0, no_list))
print(evens)  # [2, 4]
```
### Lambda with sorted 

##### Syntax
    sorted(iterable, key=lambda x:expression)

##### Example 3.4
```python 
nums = [1, 2, 3, 4, 5]

# Sort nums in descending order using lambda as key
sorted_desc = sorted(nums, key=lambda x: -x)

print(sorted_desc)
# Output: [5, 4, 3, 2, 1]
```

### Lambda with reduce

##### syntax
    reduce(lambda x, y: expression, iterable)

##### Example 3.5
```python
from functools import reduce

nums = [1, 2, 3, 4, 5]

sum_all = reduce(lambda x, y: x + y, nums)
print(sum_all)
# Output: 15
```

# DICTIONARY

    A Python dictionary is a built-in data structure that stores data in key-value pairs. It is a collection that is: 
+ Ordered (as of Python 3.7):
    The order in which items are added to the dictionary is preserved. In earlier versions of Python, dictionaries were unordered.
+ Changeable (Mutable):
    You can add, remove, or modify key-value pairs after the dictionary has been created.
+ Does not allow duplicate keys:
    Each key within a dictionary must be unique. If you attempt to add a key that already exists, its corresponding value will be updated. Values, however, can be duplicated.
    Key Characteristics:

## Key Characteristics

+ Key-Value Pairs:
    Data is stored as pairs, where each unique "key" maps to a "value."
+ Curly Braces:
    Dictionaries are defined using curly braces {}. Key-value pairs are separated by commas, and keys and values within a pair are separated by a colon (:).
+ Keys must be immutable:
    Keys can be any immutable data type (e.g., strings, numbers, tuples). Lists and other mutable objects cannot be used as keys.
+ Values can be any data type:
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

    You can create a dictionary using curly braces {} with key-value pairs separated by colons (:).

##### Example 4.1
```python
my_dict = {"name": "John", "age": 30, "country": "London"}
print(my_dict)
# You can create a dictionary by using dict() constructor
my_dict = dict(name="John", age=30, country="London")
print(my_dict)

```
### Dictionary Comprehension

    It’s a compact syntax for creating dictionaries by looping over an iterable and defining keys and values on the fly.

##### syntax
```python
{key_expression: value_expression for item in iterable}
```
##### Example 4.2
```python
squares = {x: x**2 for x in range(5)}
print(squares)
```

## Accessing values in a dictionary
    You access values by using their keys inside square brackets [] or with the get() method.

##### Example 4.3
```python
my_dict = {"name": "Alice", "city": "Mumbai"}
print(my_dict["name"]) 
print(my_dict.get("name"))
print(my_dict.get("name","jeevana")) #providing a default value
```
## Adding or Updating Values
    Add a new key-value pair or update an existing key by assigning a value to that key.Using update() also you can update a dict.

##### Example 4.4

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

+ del keyword removes a key-value pair by key
+ pop(key) removes and returns the value of a key
+ popitem() removes and returns the last inserted key-value pair
+ clear() removes all items in the dictionary

##### Example 4.5

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

    You can loop through a Dictionary using keys(),values(),items().

#### keys()
    Returns a view of all the keys in the dictionary.

##### Example 4.6
```python

my_dict = {"name": "Alice", "age": 25, "city": "Mumbai"}
print(my_dict.keys())  # dict_keys(['name', 'age', 'city'])

# loop through keys
for key in my_dict:
    print(key)

```
#### values()
    Returns a view of all the values in the dictionary.

##### Example 4.7
```python

my_dict = {"name": "Alice", "age": 25, "city": "Mumbai"}
print(my_dict.values())  # dict_values(['Alice', 25, 'NY'])

#loop through values
for value in my_dict:
    print(values)

```
#### items()
    Returns a view of all the items(key-value pairs) in the dictionary.

##### Example 4.8
```python

my_dict = {"name": "Alice", "age": 25, "city": "Mumbai"}
print(my_dict.items())  # dict_items([('name', 'Alice'), ('age', 25), ('city', 'NY')])

# loop through items
for key ,value in my_dict.items:
    print(key,":",value)
```

# LIST

    In Python, a list is a fundamental, built-in data structure used to store an ordered, mutable collection of items. Lists are highly versatile and can contain items of different data types within the same list.

## Key characteristics of Python lists:
+ Ordered:
    Items in a list maintain their insertion order and can be accessed by their index (position), starting from 0 for the first element.
+ Changeable (Mutable):
    You can modify, add, or remove items from a list after it has been created. 
+ Allow Duplicates:
    Lists can contain multiple instances of the same value.
+ Heterogeneous:
    A single list can store items of various data types, such as integers, strings, floats, booleans, and even other lists.

## Creating a List 

Lists are created by enclosing a comma-separated sequence of items within square brackets [].
Python

#### Example 5.1

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

#### Example 5.2
```python
fruits = ['apple', 'banana', 'cherry']
print(fruits[0])  
print(fruits[2])  
```
## Updating or changing list items

Assign a new value to a specific index.

#### Example 5.3
```python
fruits = ['apple', 'banana', 'cherry']
fruits[1] = 'orange'
print(fruits)  # Output: ['apple', 'orange', 'cherry']
```
## Adding or Appending items to a list

   using append() we can add new values to a list at the end. By using insert() we can add values at a specific index.

#### Example 5.4

```python 
fruits = ['apple', 'banana']
fruits.append('grape')
print(fruits)  # Output: ['apple', 'banana', 'grape']
fruits.insert(1,"papaya")
print(fruits)  # Output: ['apple', 'papaya','banana', 'grape']
```
## Removing or Deleting items from a list

    remove() is used to delete the first occurrence of the item..pop() is used to remove and return the last item, or item at specific index.

#### Example 5.5

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
By using .sort() we can sort the list in ascending order by default

### acsending
#### Example 5.6
```python
numbers = [4, 1, 3, 2]
numbers.sort()
print(numbers)  # Output: [1, 2, 3, 4]
```
### descending
#### Example 5.7
```python
numbers = [4, 1, 3, 2]
numbers.sort(reverse=True)
print(numbers)  # Output: [4,3,2,1]
```
## Reversing a List

By using reverse() we can print a reversed list
#### Example 5.8
```python 
fruits = ['apple', 'banana', 'cherry']
fruits.reverse()
print(fruits)  # Output: ['cherry', 'banana', 'apple']
```
## looping through a List

#### Example 5.9
```python
fruits = ['apple', 'banana', 'cherry']
for fruit in fruits:
    print(fruit)
```
## List Comprehension
    A shorthand way to create a list using a loop in one line
### Example 
```python
squares = [x**2 for x in range(5)]
print(squares)  # Output: [0, 1, 4, 9, 16]
```


















