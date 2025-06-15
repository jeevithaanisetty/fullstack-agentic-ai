age=int(input("enter your age:"))
if(age>18):
    print("you can vote!")
else:
    print("sorry! you must be a  major to vote.")



# age=int(input("enter age:"))
# if age>18:print("go and vote")
# else:print("go home")


n=int(input("how many no u want to add:"))
list_2=[]
while(n!=0):
   a=int(input("add int item to list_2:"))              #asking user to enter continuously
   if type(a)==int and a>0:
    list_2.append(a)
    n-=1
   else:print("can't add to list")
print(list_2)