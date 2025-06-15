# class employee:
#     com_name="zennial_pro"
#     def __init__(self,name,hourly_rate):
#         self.name=name
#         self.hourly_rate=hourly_rate
#         self.hours_worked=0
    
#     def log_hours(self,hours):
#         self.hours_worked +=hours
#     @property                           #without this we can't call salary(we can set and get)
#     def salary(self):
#         return self.hours_worked * self.hourly_rate
# emp=employee("ram",500)
# emp.log_hours(5)

# print(emp.salary)

# Example !:------------------------------------------------------------------
class Practice:
    a = 0  # cls var

    def __init__(self,b): 
        self.b = b

    @classmethod
    def get_var(cls):   #we can access cls var just by cls.
        cls.a += 1
        print(cls(a))

    @staticmethod          #no need to create instance
    def add(x, y):
        print(x + y)

# Example 2:---------------------------------------------------------------------------------------

class Car:
    wheels = 4  # class variable

    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    @classmethod #Can access and modify class state.
    def with_default_model(cls, brand):
        return cls(brand, 'Standard')

    @staticmethod #Does not take self or cls as the first argument.
    def is_motor_vehicle():
        return True

# Creating object using class method
car1 = Car.with_default_model("Toyota")
print(car1.brand, car1.model)  # Output: Toyota Standard -->we can acccess cls var here model

# Using static method
print(Car.is_motor_vehicle())  # Output: True











class college:
    college_rating=5
    college_name="NEC"
    def __init__(self,dept,fee):
        self.a=dept
        self.b=fee
    def fest(self,venue,entry):
        self.c=venue
        self.d=entry
        print(f"venue:{venue}    entry:{entry}")
    @classmethod
    def rating(cls):
        return (f"rating of {cls.college_name} is {cls.college_rating}")     #without @clsmethod and cls. we can access cls instances
    @staticmethod
    def expo(project:str):                                                    #without ststicmethod err
        return f"{project} got first prize"

institute=college("cse",100000)
institute.fest("narasaraopet",200)
print(institute.rating())
print(institute.expo("electric_vehicle"))