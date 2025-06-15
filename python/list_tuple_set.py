student_list=["ram","EEE","VIT"]
#student_tuple=tuple(student_list)         
#print(student_tuple)
student_list[2]="ECE"
print(student_list)
print(student_list.append("nrt"))
print(student_list.remove("EEE"))
print(student_list.sort())


#list duplicates can be del by set
list_1=[1,2,3,4,12,3,4,5,6,7,3,2,1,3,2,1,4,5,12,21]
dup_remove=set(list_1)
print(dup_remove)
print(max(list_1,key=lambda x:x)  )   
print(min(list_1,key=lambda x:x)) 
print(set(list(filter(lambda x:x%2==0,list_1))))
print(list(map(lambda x:x+2,list_1)))         #to remove dup add set()

set_1={1,2,5,7,12,3,13,4,17,8,9,21,7,2}
print(set_1 & dup_remove)
print(set_1 | dup_remove)
print(set_1 - dup_remove)

#another set ex
ex_set={1,2,3,2,1,3,2,3,4,5,6,7,8,8}
print(ex_set)                          #dup del
set1={"ram","sri","sai","sam",32,45,54,12,10,"priya"}
set2={"sam","ravi","balu",23,54,"sri"}
print(set1&set2)
print(set1|set2)
print(set1-set2)



#adding iems to list through loop
n=int(input("how many no u want to add:"))
list_2=[]
while(n!=0):
   a=int(input("add int item to list_2:"))
   if type(a)==int and a>0:
    list_2.append(a)
    n-=1
   else:print("can't add to list")
print(list_2)



#tuple items update 

tuple_1=(1,2,3,"sai","sam","ram")     #by REF we can modify
print(tuple_1[3])
#modify using list
my_list=list(tuple_1)
my_list[0]=100000                        #we can't use = in tuples so we need list or concatination to modify tuple items
my_list[4]="tom"
tuple_1=tuple(my_list)
print(tuple_1)
#modify using another tuple
tup=(1,0,8,"t","y","u")
tup_1=(tup,"r",5,9)          #((1,0,8,"t","y","u"),"r",5,9) tuple inside tuple  to get single tuple concat
print(tup_1)
tup_2=tup[:1]+(500,)+tup[2:]
print(tup_2)



