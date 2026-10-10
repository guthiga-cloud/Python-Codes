
import json
import os

FILE_NAME = "contacts.json"


def load_contacts():
    if not os.path.exists(FILE_NAME):
        return {}

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Could not load contacts.")
        return {}


def save_contacts(contacts):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


def add_contact(contacts):
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email (optional): ").strip()

    if not name or not phone:
        print("Name and phone are required.")
        return

    contacts[name] = {
        "phone": phone,
        "email": email or "N/A"
    }

    save_contacts(contacts)
    print(f"Contact '{name}' added successfully!")


def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    print("\n===== CONTACTS =====")

    for name, details in sorted(contacts.items()):
        print(f"Name: {name}")
        print(f"Phone: {details['phone']}")
        print(f"Email: {details['email']}")
        print("-" * 25)


def search_contact(contacts):
    query = input("Enter name to search: ").strip().lower()

    matches = [
        (name, details)
        for name, details in contacts.items()
        if query and query in name.lower()
    ]

    if matches:
        for name, details in matches:
            print(f"{name} | {details['phone']} | "
                  f"{details['email']}")
    else:
        print("No matching contacts found.")


def delete_contact(contacts):
    name = input("Enter exact name to delete: ").strip()

    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        print(f"Contact '{name}' deleted.")
    else:
        print("Contact not found.")


def main():
    contacts = load_contacts()

    while True:
        print("\n===== CONTACT BOOK =====")
        print("1. Add contact")
        print("2. View contacts")
        print("3. Search contact")
        print("4. Delete contact")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            print("Goodbye! Keep coding.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
