# Program to determine the maximum between two user-entered numbers
a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))

if a > b:
    print(f"Maximum = {a}")
elif b > a:
    print(f"Maximum = {b}")
else:
    print("Both numbers are equal.")
