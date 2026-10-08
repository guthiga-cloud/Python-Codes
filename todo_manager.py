import json
import os

FILE_NAME = "tasks.json"

def load_tasks():
"""Load tasks from the JSON file."""
if not os.path.exists(FILE_NAME):
return []

```
try:
    with open(FILE_NAME, "r") as file:
        return json.load(file)
except (json.JSONDecodeError, FileNotFoundError):
    return []
```

def save_tasks(tasks):
"""Save tasks to the JSON file."""
with open(FILE_NAME, "w") as file:
json.dump(tasks, file, indent=4)

def show_tasks(tasks):
"""Display all tasks."""
if not tasks:
print("\nNo tasks found.")
return

```
print("\n===== YOUR TASKS =====")

for number, task in enumerate(tasks, start=1):
    status = "✓" if task["completed"] else " "
    print(f"{number}. [{status}] {task['title']}")
```

def add_task(tasks):
"""Add a new task."""
title = input("\nEnter a new task: ").strip()

```
if not title:
    print("Task cannot be empty.")
    return

tasks.append({
    "title": title,
    "completed": False
})

save_tasks(tasks)
print("Task added successfully!")
```

def complete_task(tasks):
"""Mark a task as completed."""
show_tasks(tasks)

```
if not tasks:
    return

try:
    number = int(input("\nEnter task number to complete: "))

    if 1 <= number <= len(tasks):
        tasks[number - 1]["completed"] = True
        save_tasks(tasks)
        print("Task marked as completed!")
    else:
        print("Invalid task number.")

except ValueError:
    print("Please enter a valid number.")
```

def delete_task(tasks):
"""Delete a task."""
show_tasks(tasks)

```
if not tasks:
    return

try:
    number = int(input("\nEnter task number to delete: "))

    if 1 <= number <= len(tasks):
        removed = tasks.pop(number - 1)
        save_tasks(tasks)
        print(f"Deleted: {removed['title']}")
    else:
        print("Invalid task number.")

except ValueError:
    print("Please enter a valid number.")
```

def main():
tasks = load_tasks()

```
while True:
    print("\n==========================")
    print("      TO-DO MANAGER")
    print("==========================")
    print("1. Show tasks")
    print("2. Add task")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Exit")

    choice = input("\nChoose an option: ").strip()

    if choice == "1":
        show_tasks(tasks)

    elif choice == "2":
        add_task(tasks)

    elif choice == "3":
        complete_task(tasks)

    elif choice == "4":
        delete_task(tasks)

    elif choice == "5":
        print("\nGoodbye! Keep coding.")
        break

    else:
        print("Invalid option. Please choose 1-5.")
```

if **name** == "**main**":
main()
