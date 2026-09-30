import random


def generate_number():
    return random.randint(1, 100)


def check_guess(guess, secret_number):
    if guess < secret_number:
        return "Too low!"
    elif guess > secret_number:
        return "Too high!"
    else:
        return "Correct!"


def play_game():
    secret_number = generate_number()
    attempts = 0

    print("\nI'm thinking of a number between 1 and 100.")

    while True:
        try:
            guess = int(input("Enter your guess: "))

            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100.")
                continue

            attempts += 1

            result = check_guess(guess, secret_number)
            print(result)

            if guess == secret_number:
                print(f"🎉 You got it in {attempts} attempts!")
                break

        except ValueError:
            print("Please enter a valid whole number.")


def main():
    print("=" * 45)
    print("        NUMBER GUESSING GAME")
    print("=" * 45)

    while True:
        play_game()

        choice = input("\nDo you want to play again? (yes/no): ")

        if choice.lower() != "yes":
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()