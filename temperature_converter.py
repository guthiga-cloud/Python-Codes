def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit):
    celsius = fahrenheit_to_celsius(fahrenheit)
    return celsius_to_kelvin(celsius)


def kelvin_to_fahrenheit(kelvin):
    celsius = kelvin_to_celsius(kelvin)
    return celsius_to_fahrenheit(celsius)


def main():
    print("=" * 45)
    print("        TEMPERATURE CONVERTER")
    print("=" * 45)

    while True:
        print("\nChoose a conversion:")
        print("1. Celsius to Fahrenheit")
        print("2. Fahrenheit to Celsius")
        print("3. Celsius to Kelvin")
        print("4. Kelvin to Celsius")
        print("5. Fahrenheit to Kelvin")
        print("6. Kelvin to Fahrenheit")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        if choice == "7":
            print("\nThank you for using Temperature Converter!")
            break

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid choice. Please select 1-7.")
            continue

        try:
            temperature = float(input("Enter the temperature: "))

            if choice == "1":
                result = celsius_to_fahrenheit(temperature)
                print(f"\n{temperature:.2f}°C = {result:.2f}°F")

            elif choice == "2":
                result = fahrenheit_to_celsius(temperature)
                print(f"\n{temperature:.2f}°F = {result:.2f}°C")

            elif choice == "3":
                result = celsius_to_kelvin(temperature)
                print(f"\n{temperature:.2f}°C = {result:.2f}K")

            elif choice == "4":
                result = kelvin_to_celsius(temperature)
                print(f"\n{temperature:.2f}K = {result:.2f}°C")

            elif choice == "5":
                result = fahrenheit_to_kelvin(temperature)
                print(f"\n{temperature:.2f}°F = {result:.2f}K")

            elif choice == "6":
                result = kelvin_to_fahrenheit(temperature)
                print(f"\n{temperature:.2f}K = {result:.2f}°F")

        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()