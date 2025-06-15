#func decorator is used to modify the org func without changing it

def decorator(func):
    def wrapper():                    #u can use inside func name any other not only wrapper
        print("good morning!")       
        func()                     
        print("thank you for visit!")
    return wrapper

@decorator                            #befor user @decorator will excecute and goes to decorator
def user():
    print("hello!")
user()                                #calls user fnc first 



#



def employ_details(func):
    def wrapper(*args,**kwargs):
        print(f"employee belongs to {args} are:")
        func(*args,**kwargs)
        high_salary=max(employee,key=lambda x:x["salary"])
        print(f"highest salary in company is:{high_salary}")
    return wrapper   
employee=[
    {"name":"sam","dept":"IT","exp":5,"salary":100000},
    {"name":"ram","dept":"HR","exp":12,"salary":25000},
    {"name":"hari","dept":"pro","exp":4,"salary":50000},
    {"name":"hema","dept":"HR","exp":15,"salary":500000}
]


@employ_details
def employee_list(key,value):
   print(list(filter(lambda x:x[key]==value,employee)))

employee_list("dept","HR")
employee_list("name","ram")


