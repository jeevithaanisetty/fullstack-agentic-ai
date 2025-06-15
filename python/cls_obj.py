# class car:
#     wheels=4    #cls level var
#     def __init__(self,clr,year,speed):  #attributes(instance)
#         self.clr=clr
#         self.year=year
#         self.speed=speed
#         print(f"car is in {self.clr} colour ")
        
    
#     def move(self):
#         print( f"car is moving with a speed of {self.speed} kmph")
# vehicle=car("red",2020,110)
# vehicle.move()



class srimani:
    age=4
    mother_toungue="telugu"
    def __init__(self,school:str,city:str,mother:str):
        self.school=school
        self.city=city
        self.mother=mother
        print(f"sri is {self.mother}'s first child")
    def study(self,standard:str):
        self.standard=standard
        return f"sri studying {standard} in {self.school} school"
    def tution(self,time:int):
        self.time=time
        return f"tution starts at time {time} PM"
class mukundh:
    age=1.5
    mother_tounge="telugu"
    def __init__(self,school:str,city:str,mother:str):
        self.school=school
        self.city=city
        self.mother=mother
        print(f"sri is {self.mother}'s second child")
    def study(self,standard:str):
        self.standard=standard
        print( f"sri studying {standard} in {self.school} school")
    def tution(self,time:int):
        self.time=time
        print (f"tution starts at time {time} PM")
        
kid1=srimani("rainbow","hyderabad","jeevana")
print(kid1.study("nursary"))
print(kid1.tution(6))

kid2=mukundh("RAGA","guntur","jeevana")
kid2.study("playschool")
kid2.tution(5)

