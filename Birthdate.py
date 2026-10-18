# Program to calculate age based on year of birth and current year
try:
    birth_year = int(input("Enter the year of birth: "))
    current_year = int(input("Enter the current year: "))

    if birth_year > current_year:
        print("Invalid input. Birth year cannot be greater than current year.")
    else:
        age = current_year - birth_year
        print(f"You are {age} years old.")
        print(f"Age = {age}")
        print("My age = %d" % age)

except ValueError:
    print("Invalid input. Please enter valid years as integers.")
