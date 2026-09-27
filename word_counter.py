def count_words(text):
    # Remove unnecessary spaces
    text = text.strip()

    # Check if the user entered nothing
    if not text:
        return 0

    # Split the text into individual words
    words = text.split()

    # Return the number of words
    return len(words)


def count_characters(text):
    # Count characters excluding spaces
    return len(text.replace(" ", ""))


def main():
    print("=" * 40)
    print("          WORD COUNTER")
    print("=" * 40)

    while True:
        text = input("\nEnter a sentence or paragraph: ")

        words = count_words(text)
        characters = count_characters(text)

        print("\nResults")
        print("-" * 40)
        print(f"Number of words: {words}")
        print(f"Number of characters: {characters}")

        choice = input("\nDo you want to count another text? (yes/no): ")

        if choice.lower() != "yes":
            print("\nThank you for using Word Counter!")
            break


if __name__ == "__main__":
    main()