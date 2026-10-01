import re


def is_valid_phone_number(phone):
    # Remove spaces and hyphens
    phone = phone.replace(" ", "").replace("-", "")

    # Kenyan local format: 07XXXXXXXX or 01XXXXXXXX
    local_pattern = r"^(07|01)\d{8}$"

    # Kenyan international format: +2547XXXXXXXX or +2541XXXXXXXX
    international_pattern = r"^\+254(7|1)\d{8}$"

    # Check local format
    if re.match(local_pattern, phone):
        return True

    # Check international format
    if re.match(international_pattern, phone):
        return True

    return False


def format_phone_number(phone):
    # Remove spaces and hyphens
    phone = phone.replace(" ", "").replace("-", "")

    # Convert local Kenyan number to international format
    if phone.startswith("0") and len(phone) == 10:
        phone = "+254" + phone[1:]

    return phone


def main():
    print("=" * 45)
    print("       KENYAN PHONE NUMBER VALIDATOR")
    print("=" * 45)

    while True:
        phone = input("\nEnter a Kenyan phone number: ")

        if is_valid_phone_number(phone):
            formatted_number = format_phone_number(phone)

            print("✓ Valid phone number")
            print(f"International format: {formatted_number}")
        else:
            print("✗ Invalid phone number")

        choice = input("\nCheck another number? (yes/no): ")

        if choice.lower() != "yes":
            print("\nThank you for using Phone Number Validator!")
            break


if __name__ == "__main__":
    main()