def is_palindrome(text):
    # Remove spaces and convert to lowercase
    text = text.replace(" ", "").lower()

    # Reverse the text
    reversed_text = text[::-1]

    # Check if the text is the same forwards and backwards
    return text == reversed_text


def main():
    print("=" * 40)
    print("       PALINDROME CHECKER")
    print("=" * 40)

    while True:
        text = input("\nEnter a word or phrase: ")

        if is_palindrome(text):
            print(f"✓ '{text}' is a palindrome.")
        else:
            print(f"✗ '{text}' is not a palindrome.")

        choice = input("\nDo you want to check another? (yes/no): ")

        if choice.lower() != "yes":
            print("\nThank you for using Palindrome Checker!")
            break


if __name__ == "__main__":
    main()