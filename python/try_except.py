num=input("enter even no only.")

try:
    print(num%2==0)       #str can't perform  opr so err
except:
    print("enter correct:")          #until try raise err except will excecute
finally:
         if num%2==0:
            print("brilliant ")
         else:
            print("you entered is not even")
       #print(type(num)) to know what user enter