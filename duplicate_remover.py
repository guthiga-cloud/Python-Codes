
def remove_duplicates(items):
    # Create an empty list for unique values
    unique_items = []

    # Loop through every item
    for item in items:

        # Add the item only if it is not already present
        if item not in unique_items:
            unique_items.append(item)

    return unique_items


def main():
    print("=" * 45)
    print("          DUPLICATE REMOVER")
    print("=" * 45)

    while True:
        user_input = input("\nEnter numbers separated by commas: ")

        try:
            # Convert input into a list of numbers
            numbers = [int(num.strip()) for num in user_input.split(",")]

            # Remove duplicates
            unique_numbers = remove_duplicates(numbers)

            print("\nOriginal List:")
            print(numbers)

            print("\nList Without Duplicates:")
            print(unique_numbers)

            print(f"\nOriginal Items: {len(numbers)}")
            print(f"Unique Items: {len(unique_numbers)}")
            print(f"Duplicates Removed: {len(numbers) - len(unique_numbers)}")

        except ValueError:
            print("Invalid input! Please enter numbers separated by commas.")
            continue

        choice = input("\nDo you want to try again? (yes/no): ")

        if choice.lower() != "yes":
            print("\nThank you for using Duplicate Remover!")
            break


if __name__ == "__main__":
    main()