# volume_calculator.py
# Calculate volume of different 3D shapes

import math

def main():
    print("=== VOLUME CALCULATIONS ===\n")
    
    # Cube volume
    side = 5.0
    cube_volume = side ** 3
    print(f"1. Cube (Side = {side}): Volume = {cube_volume:.2f} cubic units")
    
    # Sphere volume
    radius = 4.5
    sphere_volume = (4/3) * math.pi * radius ** 3
    print(f"2. Sphere (Radius = {radius}): Volume = {sphere_volume:.2f} cubic units")
    
    # Cylinder volume
    cyl_radius = 3.0
    cyl_height = 10.0
    cylinder_volume = math.pi * cyl_radius ** 2 * cyl_height
    print(f"3. Cylinder (Radius = {cyl_radius}, Height = {cyl_height}): Volume = {cylinder_volume:.2f} cubic units")
    
    # Cone volume
    cone_radius = 3.0
    cone_height = 9.0
    cone_volume = (1/3) * math.pi * cone_radius ** 2 * cone_height
    print(f"4. Cone (Radius = {cone_radius}, Height = {cone_height}): Volume = {cone_volume:.2f} cubic units")
    
    # Rectangular Prism volume
    length = 8.0
    width = 4.0
    height = 6.0
    prism_volume = length * width * height
    print(f"5. Rectangular Prism (L = {length}, W = {width}, H = {height}): Volume = {prism_volume:.2f} cubic units")

if __name__ == "__main__":
    main()
