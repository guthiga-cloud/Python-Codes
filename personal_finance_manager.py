
import sqlite3
from datetime import datetime
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "finance.db"


def connect_db():
    """Connect to SQLite and create the transactions table."""
    connection = sqlite3.connect(DB_FILE)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL
                CHECK(transaction_type IN ('income', 'expense')),
            description TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            category TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    connection.commit()
    return connection


def add_transaction(connection, transaction_type):
    """Record income or an expense."""
    description = input("Description: ").strip()
    category = input("Category: ").strip() or "Other"

    if not description:
        print("Description cannot be empty.")
        return

    try:
        amount = round(float(input("Amount (KES): ")), 2)

        if not 0 < amount < float("inf"):
            print("Enter a valid positive amount.")
            return
    except ValueError:
        print("Enter a valid numeric amount.")
        return

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        connection.execute(
            """
            INSERT INTO transactions
            (transaction_type, description, amount, category, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (transaction_type, description, amount, category, created_at)
        )
        connection.commit()
        print(f"{transaction_type.title()} recorded successfully!")
    except sqlite3.Error as error:
        print(f"Database error: {error}")


def view_transactions(connection):
    """Display all saved transactions."""
    cursor = connection.execute("""
        SELECT id, transaction_type, description, amount,
               category, created_at
        FROM transactions
        ORDER BY id DESC
    """)
    transactions = cursor.fetchall()

    if not transactions:
        print("No transactions recorded yet.")
        return

    print("\n========== TRANSACTION HISTORY ==========")

    for item in transactions:
        transaction_id, kind, description, amount, category, date = item
        sign = "+" if kind == "income" else "-"

        print(
            f"#{transaction_id} | {date} | {kind.upper()} | "
            f"{description} | {category} | "
            f"{sign}KES {amount:,.2f}"
        )


def show_balance(connection):
    """Calculate income, expenses, and net balance."""
    cursor = connection.execute("""
        SELECT
            COALESCE(SUM(CASE
                WHEN transaction_type = 'income' THEN amount
                ELSE 0 END), 0),
            COALESCE(SUM(CASE
                WHEN transaction_type = 'expense' THEN amount
                ELSE 0 END), 0)
        FROM transactions
    """)

    income, expenses = cursor.fetchone()
    balance = income - expenses

    print("\n========== FINANCIAL SUMMARY ==========")
    print(f"Total income:   KES {income:,.2f}")
    print(f"Total expenses: KES {expenses:,.2f}")
    print(f"Net balance:    KES {balance:,.2f}")


def category_summary(connection):
    """Summarize expenses by category."""
    cursor = connection.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE transaction_type = 'expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    results = cursor.fetchall()

    if not results:
        print("No expenses available for analysis.")
        return

    print("\n========== EXPENSE CATEGORIES ==========")

    for category, total in results:
        print(f"{category}: KES {total:,.2f}")


def main():
    try:
        connection = connect_db()
    except sqlite3.Error as error:
        print(f"Could not open database: {error}")
        return

    try:
        while True:
            print("\n====== PERSONAL FINANCE MANAGER ======")
            print("1. Add income")
            print("2. Add expense")
            print("3. View transactions")
            print("4. View financial summary")
            print("5. Expenses by category")
            print("6. Exit")

            choice = input("Choose an option (1-6): ").strip()

            if choice == "1":
                add_transaction(connection, "income")
            elif choice == "2":
                add_transaction(connection, "expense")
            elif choice == "3":
                view_transactions(connection)
            elif choice == "4":
                show_balance(connection)
            elif choice == "5":
                category_summary(connection)
            elif choice == "6":
                print("Your records are saved. Goodbye!")
                break
            else:
                print("Invalid choice. Select 1-6.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
