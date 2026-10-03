
import string


def check_password_strength(password):
    score = 0
    feedback = []

    # Check password length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should contain at least 8 characters.")

    # Check uppercase letters
    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    # Check lowercase letters
    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    # Check numbers
    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    # Check special characters
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("Add at least one special character.")

    # Determine password strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return strength, score, feedback


def main():
    print("=" * 45)
    print("       PASSWORD STRENGTH CHECKER")
    print("=" * 45)

    while True:
        password = input("\nEnter your password: ")

        strength, score, feedback = check_password_strength(password)

        print("\nPassword Analysis")
        print("-" * 45)
        print(f"Strength: {strength}")
        print(f"Score: {score}/5")

        if feedback:
            print("\nSuggestions for improvement:")
            for suggestion in feedback:
                print(f"- {suggestion}")
        else:
            print("\nExcellent! Your password meets all five checks.")

        choice = input("\nCheck another password? (yes/no): ")

        if choice.lower() != "yes":
            print("\nThank you for using Password Strength Checker!")
            break


if __name__ == "__main__":
    main()