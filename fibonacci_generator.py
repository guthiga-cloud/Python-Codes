def generate_fibonacci(number_of_terms):
    sequence = []

    first = 0
    second = 1

    for _ in range(number_of_terms):
        sequence.append(first)

        next_number = first + second
        first = second
        second = next_number

    return sequence


def main():
    print("=" * 45)
    print("         FIBONACCI GENERATOR")
    print("=" * 45)

    while True:
        try:
            number = int(input("\nHow many Fibonacci numbers do you want? "))

            if number <= 0:
                print("Please enter a number greater than 0.")
                continue

            fibonacci_sequence = generate_fibonacci(number)

            print("\nFibonacci Sequence:")
            print(", ".join(map(str, fibonacci_sequence)))

        except ValueError:
            print("Please enter a valid whole number.")
            continue

        choice = input("\nGenerate another sequence? (yes/no): ")

        if choice.lower() != "yes":
            print("\nThank you for using Fibonacci Generator!")
            break


if __name__ == "__main__":
    main()