import random


def get_random_quote():
    quotes = [
        "Success is the sum of small efforts repeated every day.",
        "The best way to predict the future is to create it.",
        "Don't stop when you're tired. Stop when you're done.",
        "Every expert was once a beginner.",
        "Great things take time and consistent effort.",
        "Code, test, learn, and improve.",
        "Your only limit is the one you set for yourself.",
        "Failure is not the opposite of success. It is part of success.",
        "Small progress is still progress.",
        "The secret of getting ahead is getting started."
    ]

    return random.choice(quotes)


def display_quote():
    quote = get_random_quote()

    print("\n" + "=" * 55)
    print("                 RANDOM QUOTE")
    print("=" * 55)
    print(f"\n\"{quote}\"")
    print("\n" + "=" * 55)


def main():
    print("=" * 55)
    print("              RANDOM QUOTE GENERATOR")
    print("=" * 55)

    while True:
        print("\nChoose an option:")
        print("1. Generate a random quote")
        print("2. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            display_quote()

        elif choice == "2":
            print("\nThank you for using Random Quote Generator!")
            break

        else:
            print("\nInvalid choice. Please select 1 or 2.")


if __name__ == "__main__":
    main()