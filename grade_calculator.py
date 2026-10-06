def calculate_average(marks):
    return sum(marks) / len(marks)


def calculate_grade(average):
    if average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "E"


def get_performance(grade):
    performance = {
        "A": "Excellent",
        "B": "Very Good",
        "C": "Good",
        "D": "Needs Improvement",
        "E": "Fail"
    }

    return performance[grade]


def calculate_student_result(subjects):
    marks = list(subjects.values())

    average = calculate_average(marks)
    grade = calculate_grade(average)
    performance = get_performance(grade)

    return average, grade, performance


def main():
    print("=" * 50)
    print("          STUDENT GRADE CALCULATOR")
    print("=" * 50)

    while True:
        name = input("\nEnter student's name: ").strip()

        if not name:
            print("Please enter a student name.")
            continue

        subjects = {}

        print("\nEnter marks for each subject.")
        print("Marks must be between 0 and 100.")

        subject_names = [
            "Mathematics",
            "English",
            "Programming",
            "Database",
            "Computer Networks"
        ]

        for subject in subject_names:
            while True:
                try:
                    mark = float(input(f"Enter marks for {subject}: "))

                    if mark < 0 or mark > 100:
                        print("Marks must be between 0 and 100.")
                        continue

                    subjects[subject] = mark
                    break

                except ValueError:
                    print("Please enter a valid number.")

        average, grade, performance = calculate_student_result(subjects)

        print("\n" + "=" * 50)
        print("              STUDENT RESULTS")
        print("=" * 50)

        print(f"Student Name: {name}")

        print("\nSubject Marks")
        print("-" * 50)

        for subject, mark in subjects.items():
            print(f"{subject:<25} {mark:.2f}")

        print("-" * 50)
        print(f"Average:                   {average:.2f}")
        print(f"Grade:                     {grade}")
        print(f"Performance:               {performance}")

        print("=" * 50)

        choice = input("\nCalculate another student? (yes/no): ")

        if choice.lower() != "yes":
            print("\nThank you for using Student Grade Calculator!")
            break


if __name__ == "__main__":
    main()