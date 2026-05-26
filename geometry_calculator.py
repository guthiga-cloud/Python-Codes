# geometry_calculator.py
# Calculate various geometry properties

import math

def main():
    print("=== GEOMETRY CALCULATIONS ===\n")
    
    # Pythagorean Theorem
    side_a = 3.0
    side_b = 4.0
    hypotenuse = math.sqrt(side_a ** 2 + side_b ** 2)
    print("1. Pythagorean Theorem")
    print(f"   Side A: {side_a}, Side B: {side_b}")
    print(f"   Hypotenuse: {hypotenuse:.2f}\n")
    
    # Distance between two points
    x1, y1 = 2.0, 3.0
    x2, y2 = 5.0, 7.0
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    print("2. Distance Formula")
    print(f"   Point 1: ({x1}, {y1})")
    print(f"   Point 2: ({x2}, {y2})")
    print(f"   Distance: {distance:.2f} units\n")
    
    # Slope of a line
    if x2 - x1 != 0:
        slope = (y2 - y1) / (x2 - x1)
        print("3. Slope of Line")
        print(f"   Points ({x1},{y1}) and ({x2},{y2})")
        print(f"   Slope: {slope:.2f}\n")
    else:
        print("3. Slope: Undefined (vertical line)\n")
    
    # Perimeter of shapes
    print("4. Perimeter Calculations")
    rect_length = 10.0
    rect_width = 6.0
    rect_perimeter = 2 * (rect_length + rect_width)
    print(f"   Rectangle (L={rect_length}, W={rect_width}): Perimeter = {rect_perimeter:.2f}")
    
    circle_radius = 5.0
    circumference = 2 * math.pi * circle_radius
    print(f"   Circle (Radius={circle_radius}): Circumference = {circumference:.2f}\n")
    
    # Quadratic Equation Solver
    a, b, c = 1, -5, 6
    discriminant = b**2 - 4*a*c
    print("5. Quadratic Equation Solver")
    print(f"   Equation: {a}x² + {b}x + {c} = 0")
    
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        print(f"   Real and Different Roots: {root1:.2f}, {root2:.2f}")
    elif discriminant == 0:
        root = -b / (2*a)
        print(f"   Real and Equal Roots: {root:.2f}")
    else:
        real_part = -b / (2*a)
        imaginary_part = math.sqrt(-discriminant) / (2*a)
        print(f"   Complex Roots: {real_part:.2f} ± {imaginary_part:.2f}i")

if __name__ == "__main__":
    main()
