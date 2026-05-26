# mean_calculator.py
# Calculate mean/average of 8 subjects with grade calculation

def main():
    # 8 subject marks
    marks = [85, 90, 78, 92, 88, 76, 95, 89]
    subjects = ["Math", "Science", "English", "History", 
                "Geography", "Computer", "Physics", "Chemistry"]
    
    print("=== SUBJECT MARKS ===")
    total = 0
    
    for i, subject in enumerate(subjects):
        print(f"{subject}: {marks[i]}")
        total += marks[i]
    
    mean = total / len(marks)
    
    print(f"\nTotal Marks: {total}")
    print(f"Number of Subjects: {len(marks)}")
    print(f"Mean (Average) Marks: {mean:.2f}")
    
    # Grade calculation
    if mean >= 90:
        grade = 'A'
    elif mean >= 80:
        grade = 'B'
    elif mean >= 70:
        grade = 'C'
    elif mean >= 60:
        grade = 'D'
    else:
        grade = 'F'
    
    print(f"Grade: {grade}")

if __name__ == "__main__":
    main()
