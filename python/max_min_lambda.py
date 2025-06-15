
x=int(input("enter a no:"))
square= lambda x :x**2
result=square(x)                    #square is a lambda func we have to call
print(result)

#example:2

list_num=[1,2,3,4,5,6,7,8,9,10]
sq=list(map(lambda x:x**2,list_num))   #without map err i.e iteration is not possible
print(f"squares list is :{sq}") 




student_list=[
{"name":"sri","marks":55,"age":18},
{"name":"mukundh","marks":54,"age":15},
{"name":"priya","marks":85,"age":25}
]
topper=max(student_list,key=lambda x:x["marks"])      #we can't directly call key as str i.e key=["marks"] err
avg_student=min(student_list,key=lambda x:x["marks"])
elder=max(student_list,key=lambda x:x["age"])
younger=min(student_list,key=lambda x:x["age"])
print(topper)
print(avg_student)
print(elder)
print(younger)