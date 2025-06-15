
#lambda along with map filter reduce

#map:to iterate

def square(x):
    return x**2
squares=list(map(square,[1,2,3,4]))     #using functions without lambda
print(squares)
    

list_num=[1,2,3,4,5,6]      #using lambda along with map
sq=list(map(lambda x:x**2,list_num))
print(sq)


#filter
list_num=[1,2,3,4,5,6,7,8,9,10]
even_num=list(filter(lambda x:x%2==0,list_num))   #filter is used to filter required ones
print(even_num)

#inc eacah no by 1 in the list
list_num=[1,2,3,4]
updated=list(map(lambda x:x+1,list_num))
print(updated)

#reduce

from functools import reduce
list_num=[1,2,3,4,5]
sum= reduce(lambda x,y:x+y,list_num)
print(sum)