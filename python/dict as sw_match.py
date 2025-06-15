day=input("enter today:")
weak_day={
           "mon":"work started",
           "tue":"work hard",
           "wed":"work hard",
           "thu":"work hard",
           "fri":"work work work",
           "sat":"one day to go",
           "sun":"work ended tdy is holiday"

         }.get(day,"enter correct day!")          #here get is for safe reading gives no err when inp is wrng
                                                   #o/p will be none when inp is wrng
                                                   #we can give default exp message without any err
print(weak_day)

#Example 2-------------------------------------------------------------------------------------------
# match case

day = input("enter week:")

match day:
    case "Monday":
        print("Start of the work week.")
    case "Tuesday":
        print("Second day grind.")
    case "Wednesday":
        print("Hump day!")
    case "Thursday":
        print("Almost there.")
    case "Friday":
        print("Weekend is coming!")
    case "Saturday" | "Sunday":
        print("It's the weekend! 🎉")
    case _:
        print("Invalid day.")
