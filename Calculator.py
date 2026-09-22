import tkinter as tk
import math


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        self.expression = ""

        self.display = tk.Entry(
            root,
            font=("Arial", 28),
            justify="right",
            bd=10,
            relief=tk.FLAT
        )

        self.display.pack(
            padx=15,
            pady=20,
            fill="x",
            ipady=15
        )

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill="both", expand=True)

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ("AC", 1, 0),
            ("⌫", 1, 1),
            ("(", 1, 2),
            (")", 1, 3),

            ("7", 2, 0),
            ("8", 2, 1),
            ("9", 2, 2),
            ("/", 2, 3),

            ("4", 3, 0),
            ("5", 3, 1),
            ("6", 3, 2),
            ("*", 3, 3),

            ("1", 4, 0),
            ("2", 4, 1),
            ("3", 4, 2),
            ("-", 4, 3),

            ("0", 5, 0),
            (".", 5, 1),
            ("%", 5, 2),
            ("+", 5, 3),

            ("√", 6, 0),
            ("^", 6, 1),
            ("+/-", 6, 2),
            ("=", 6, 3)
        ]

        for text, row, column in buttons:
            button = tk.Button(
                self.button_frame,
                text=text,
                font=("Arial", 18),
                command=lambda value=text: self.button_click(value)
            )

            button.grid(
                row=row,
                column=column,
                padx=5,
                pady=5,
                sticky="nsew"
            )

        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)

        for i in range(1, 7):
            self.button_frame.grid_rowconfigure(i, weight=1)

    def button_click(self, value):

        if value == "AC":
            self.expression = ""
            self.update_display()

        elif value == "⌫":
            self.expression = self.expression[:-1]
            self.update_display()

        elif value == "=":
            self.calculate()

        elif value == "√":
            self.square_root()

        elif value == "^":
            self.expression += "**"
            self.update_display()

        elif value == "+/-":
            self.toggle_sign()

        elif value == "%":
            self.percentage()

        else:
            self.expression += value
            self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    def calculate(self):
        try:
            result = eval(
                self.expression,
                {"__builtins__": None},
                {"math": math}
            )

            self.expression = str(result)
            self.update_display()

        except:
            self.expression = "Error"
            self.update_display()

    def square_root(self):
        try:
            result = math.sqrt(float(self.expression))
            self.expression = str(result)
            self.update_display()

        except:
            self.expression = "Error"
            self.update_display()

    def percentage(self):
        try:
            result = float(self.expression) / 100
            self.expression = str(result)
            self.update_display()

        except:
            self.expression = "Error"
            self.update_display()

    def toggle_sign(self):
        try:
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression

            self.update_display()

        except:
            self.expression = "Error"
            self.update_display()


root = tk.Tk()

calculator = Calculator(root)

root.mainloop()