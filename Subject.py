# Program to calculate average marks and assign a grade
print("Enter Marks Obtained in 5 Subjects:")

try:
    mark_one = int(input("Subject 1: "))
    mark_two = int(input("Subject 2: "))
    mark_three = int(input("Subject 3: "))
    mark_four = int(input("Subject 4: "))
    mark_five = int(input("Subject 5: "))

    total = mark_one + mark_two + mark_three + mark_four + mark_five
    average = total / 5

    print(f"Average = {average:.2f}")

    if 70 <= average <= 100:
        print("Your Grade is A")
    elif 60 <= average <= 69:
        print("Your Grade is B")
    elif 50 <= average <= 59:
        print("Your Grade is C")
    elif 40 <= average <= 49:
        print("Your Grade is D")
    elif 0 <= average <= 39:
        print("Your Grade is F")
    else:
        print("Invalid Input! Average out of expected range.")

except ValueError:
    print("Invalid input! Please enter numeric marks only.")
