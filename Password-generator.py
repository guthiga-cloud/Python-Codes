import tkinter as tk
from tkinter import messagebox
import string
import secrets


# ==============================
# PASSWORD GENERATOR FUNCTIONS
# ==============================

def generate_password():
    try:
        length = int(length_entry.get())

        if length < 4:
            messagebox.showerror(
                "Invalid Length",
                "Password length must be at least 4 characters."
            )
            return

        characters = ""

        if uppercase_var.get():
            characters += string.ascii_uppercase

        if lowercase_var.get():
            characters += string.ascii_lowercase

        if numbers_var.get():
            characters += string.digits

        if symbols_var.get():
            characters += string.punctuation

        if not characters:
            messagebox.showerror(
                "No Characters Selected",
                "Please select at least one character type."
            )
            return

        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid password length."
        )


def copy_password():
    password = password_entry.get()

    if not password:
        messagebox.showwarning(
            "No Password",
            "Generate a password first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard."
    )


def clear_password():
    password_entry.delete(0, tk.END)


# ==============================
# MAIN WINDOW
# ==============================

root = tk.Tk()

root.title("Password Generator")
root.geometry("500x550")
root.resizable(False, False)

root.configure(bg="#f4f6f8")


# ==============================
# TITLE
# ==============================

title_label = tk.Label(
    root,
    text="🔐 Password Generator",
    font=("Arial", 24, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

title_label.pack(pady=(30, 10))


subtitle_label = tk.Label(
    root,
    text="Create a strong and secure password",
    font=("Arial", 11),
    bg="#f4f6f8",
    fg="#6b7280"
)

subtitle_label.pack(pady=(0, 25))


# ==============================
# PASSWORD LENGTH
# ==============================

length_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

length_frame.pack(pady=5)


length_label = tk.Label(
    length_frame,
    text="Password Length:",
    font=("Arial", 12, "bold"),
    bg="#f4f6f8",
    fg="#374151"
)

length_label.pack(side=tk.LEFT, padx=10)


length_entry = tk.Entry(
    length_frame,
    width=8,
    font=("Arial", 12),
    justify="center"
)

length_entry.pack(side=tk.LEFT)

length_entry.insert(0, "16")


# ==============================
# CHARACTER OPTIONS
# ==============================

options_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

options_frame.pack(pady=20)


uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)


uppercase_check = tk.Checkbutton(
    options_frame,
    text="Uppercase Letters",
    variable=uppercase_var,
    font=("Arial", 11),
    bg="#f4f6f8",
    activebackground="#f4f6f8"
)

uppercase_check.grid(
    row=0,
    column=0,
    sticky="w",
    padx=20,
    pady=5
)


lowercase_check = tk.Checkbutton(
    options_frame,
    text="Lowercase Letters",
    variable=lowercase_var,
    font=("Arial", 11),
    bg="#f4f6f8",
    activebackground="#f4f6f8"
)

lowercase_check.grid(
    row=1,
    column=0,
    sticky="w",
    padx=20,
    pady=5
)


numbers_check = tk.Checkbutton(
    options_frame,
    text="Numbers",
    variable=numbers_var,
    font=("Arial", 11),
    bg="#f4f6f8",
    activebackground="#f4f6f8"
)

numbers_check.grid(
    row=0,
    column=1,
    sticky="w",
    padx=20,
    pady=5
)


symbols_check = tk.Checkbutton(
    options_frame,
    text="Special Characters",
    variable=symbols_var,
    font=("Arial", 11),
    bg="#f4f6f8",
    activebackground="#f4f6f8"
)

symbols_check.grid(
    row=1,
    column=1,
    sticky="w",
    padx=20,
    pady=5
)


# ==============================
# GENERATE BUTTON
# ==============================

generate_button = tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    font=("Arial", 13, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief=tk.FLAT,
    cursor="hand2",
    padx=20,
    pady=10
)

generate_button.pack(pady=20)


# ==============================
# PASSWORD DISPLAY
# ==============================

password_label = tk.Label(
    root,
    text="Generated Password",
    font=("Arial", 12, "bold"),
    bg="#f4f6f8",
    fg="#374151"
)

password_label.pack(pady=(5, 8))


password_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

password_frame.pack()


password_entry = tk.Entry(
    password_frame,
    width=35,
    font=("Arial", 14),
    justify="center",
    show=""
)

password_entry.pack(
    side=tk.LEFT,
    ipady=8
)


# ==============================
# ACTION BUTTONS
# ==============================

buttons_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

buttons_frame.pack(pady=20)


copy_button = tk.Button(
    buttons_frame,
    text="Copy",
    command=copy_password,
    font=("Arial", 11, "bold"),
    bg="#10b981",
    fg="white",
    activebackground="#059669",
    activeforeground="white",
    relief=tk.FLAT,
    cursor="hand2",
    padx=25,
    pady=8
)

copy_button.grid(
    row=0,
    column=0,
    padx=8
)


clear_button = tk.Button(
    buttons_frame,
    text="Clear",
    command=clear_password,
    font=("Arial", 11, "bold"),
    bg="#ef4444",
    fg="white",
    activebackground="#dc2626",
    activeforeground="white",
    relief=tk.FLAT,
    cursor="hand2",
    padx=25,
    pady=8
)

clear_button.grid(
    row=0,
    column=1,
    padx=8
)


# ==============================
# FOOTER
# ==============================

footer_label = tk.Label(
    root,
    text="Generated using Python secrets",
    font=("Arial", 9),
    bg="#f4f6f8",
    fg="#9ca3af"
)

footer_label.pack(
    side=tk.BOTTOM,
    pady=15
)


# ==============================
# START APPLICATION
# ==============================

root.mainloop()