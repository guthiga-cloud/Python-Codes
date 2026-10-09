
import json
from pathlib import Path
from datetime import date

FILE_NAME = Path("expenses.json")


def load_expenses():
    if not FILE_NAME.exists():
        return []

    try:
        with FILE_NAME.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        print("Expense file has an invalid format.")
        return []

    except (json.JSONDecodeError, OSError):
        print("Could not read saved expenses.")
        return []


def save_expenses(expenses):
    with FILE_NAME.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def add_expense(expenses):
    title = input("Expense description: ").strip()

    if not title:
        print("Description cannot be empty.")
        return

    try:
        amount = float(input("Amount spent (KES): "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    expense = {
        "title": title,
        "amount": round(amount, 2),
        "date": date.today().isoformat()
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense saved successfully!")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- EXPENSE HISTORY ---")

    for number, expense in enumerate(expenses, start=1):
        print(
            f"{number}. {expense['date']} | "
            f"{expense['title']} | "
            f"KES {expense['amount']:.2f}"
        )


def show_summary(expenses):
    total = sum(item["amount"] for item in expenses)

    print("\n--- EXPENSE SUMMARY ---")
    print(f"Number of expenses: {len(expenses)}")
    print(f"Total spent: KES {total:.2f}")

    if expenses:
        average = total / len(expenses)
        print(f"Average expense: KES {average:.2f}")


def main():
    expenses = load_expenses()

    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Show summary")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            print("Keep coding. See you tomorrow!")
            break
        else:
            print("Invalid choice. Select 1-4.")


if __name__ == "__main__":
    main()