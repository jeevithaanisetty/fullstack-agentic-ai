#They provide a way to define how objects of a class should behave with built-in operators and functions


class user:
    def __init__(self,name:str,id:int,projects_list):
        self.name=name                                  #we can also write self.any=name
        self.id=id
        self.projects_list=projects_list

        print(f"welcome {name}")
    def log_in(self,password:str):
        self.password=password
        print(f"your password is:{password}")
        return f"hi {self.name}! do you want to save your password"
    def __str__(self):
        return f"string rep of obj is:  {self.name} and {self.id}"
    def __repr__(self):
        return f"string rep of obj is:   {self.name} and {self.id}  "
    def __len__(self):
       # return len(self.name) 
       return len(self.projects_list) 
                                #return f"length of name is len(self.name)--->is error
    
guest_user=user("sri",121,["AI","JAVA","PYTHON"])
print(guest_user.log_in("hjgdsuyfgdh"))
print(str(guest_user))                                   #o/p=string rep of obj is: sri and 121                     (only method o/p)
print(repr(user("priya",153,["c","c++"])))               # o/p=welcome priya string rep of obj is: priya and 153     (both method and cls)
print(len(guest_user))







