# area_calculator.py
# Calculate area of different shapes

import math

def main():
    print("=== AREA CALCULATIONS ===\n")
    
    # Circle area
    radius = 7.5
    circle_area = math.pi * radius ** 2
    print(f"1. Circle (Radius = {radius}): Area = {circle_area:.2f} sq units")
    
    # Rectangle area
    length = 12.5
    width = 8.5
    rectangle_area = length * width
    print(f"2. Rectangle (Length = {length}, Width = {width}): Area = {rectangle_area:.2f} sq units")
    
    # Triangle area
    base = 10.0
    height = 6.0
    triangle_area = 0.5 * base * height
    print(f"3. Triangle (Base = {base}, Height = {height}): Area = {triangle_area:.2f} sq units")
    
    # Square area
    side = 9.0
    square_area = side ** 2
    print(f"4. Square (Side = {side}): Area = {square_area:.2f} sq units")
    
    # Trapezoid area
    base1 = 8.0
    base2 = 12.0
    trap_height = 5.0
    trapezoid_area = 0.5 * (base1 + base2) * trap_height
    print(f"5. Trapezoid (Base1 = {base1}, Base2 = {base2}, Height = {trap_height}): Area = {trapezoid_area:.2f} sq units")

if __name__ == "__main__":
    main()
