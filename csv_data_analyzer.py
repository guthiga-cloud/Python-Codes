
import csv
import os
from statistics import mean

FILE_NAME = "sales_data.csv"


def create_sample_file():
    """Create sample sales data if the file does not exist."""
    if os.path.exists(FILE_NAME):
        return

    sample_data = [
        ["Product", "Sales"],
        ["Laptop", 75000],
        ["Phone", 35000],
        ["Headphones", 4500],
        ["Keyboard", 3000],
        ["Monitor", 18000],
    ]

    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(sample_data)


def load_sales():
    """Read sales records from the CSV file."""
    records = []

    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    product = row["Product"].strip()
                    amount = float(row["Sales"])

                    if product and amount >= 0 and amount < float("inf"):
                        records.append({
                            "product": product,
                            "sales": amount
                        })
                except (ValueError, KeyError, TypeError):
                    print(f"Skipping invalid record: {row}")

    except OSError as error:
        print(f"Could not read the file: {error}")

    return records


def analyze_sales(records):
    """Calculate sales statistics."""
    if not records:
        print("No valid sales records found.")
        return

    amounts = [record["sales"] for record in records]
    total = sum(amounts)
    average = mean(amounts)

    highest = max(records, key=lambda record: record["sales"])
    lowest = min(records, key=lambda record: record["sales"])

    print("\n========== SALES REPORT ==========")
    print(f"Products analyzed: {len(records)}")
    print(f"Total sales: KES {total:,.2f}")
    print(f"Average sales: KES {average:,.2f}")
    print(
        f"Highest sale: {highest['product']} "
        f"(KES {highest['sales']:,.2f})"
    )
    print(
        f"Lowest sale: {lowest['product']} "
        f"(KES {lowest['sales']:,.2f})"
    )
    print("==================================")


def show_records(records):
    """Display all valid sales records."""
    if not records:
        print("No records to display.")
        return

    print("\nProduct                 Sales (KES)")
    print("-" * 38)

    for record in records:
        print(
            f"{record['product']:<22} "
            f"{record['sales']:>12,.2f}"
        )


def main():
    create_sample_file()
    records = load_sales()

    while True:
        print("\n====== CSV DATA ANALYZER ======")
        print("1. View sales records")
        print("2. Analyze sales")
        print("3. Reload CSV file")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            show_records(records)
        elif choice == "2":
            analyze_sales(records)
        elif choice == "3":
            records = load_sales()
            print(f"Loaded {len(records)} valid records.")
        elif choice == "4":
            print("Thanks for coding. Keep your streak alive!")
            break
        else:
            print("Invalid option. Choose between 1 and 4.")


if __name__ == "__main__":
    main()
