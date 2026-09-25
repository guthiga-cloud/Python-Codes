def is_valid_email(email):
    # Remove spaces from the beginning and end
    email = email.strip()

    # Check if there is exactly one @ symbol
    if email.count("@") != 1:
        return False

    # Split the email into username and domain
    username, domain = email.split("@")

    # Username cannot be empty
    if not username:
        return False

    # Domain cannot be empty
    if not domain:
        return False

    # Domain must contain a dot
    if "." not in domain:
        return False

    # Username and domain should not start or end with a dot
    if username.startswith(".") or username.endswith("."):
        return False

    if domain.startswith(".") or domain.endswith("."):
        return False

    # Domain should have something after the final dot
    extension = domain.split(".")[-1]

    if not extension:
        return False

    # Check for spaces
    if " " in email:
        return False

    return True


def main():
    print("=" * 40)
    print("        EMAIL VALIDATOR")
    print("=" * 40)

    while True:
        email = input("\nEnter an email address: ")

        if is_valid_email(email):
            print("✓ Valid email address")
        else:
            print("✗ Invalid email address")

        choice = input("\nDo you want to check another email? (yes/no): ")

        if choice.lower() != "yes":
            print("\nThank you for using Email Validator!")
            break


if __name__ == "__main__":
    main()