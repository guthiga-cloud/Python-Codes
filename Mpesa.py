# Install ipywidgets if not already
!pip install ipywidgets

from ipywidgets import Button, Password, FloatText, Label, VBox, HBox
from IPython.display import display
import hashlib

# -------------------
# M-Pesa Account Logic
# -------------------
class MpesaAccount:
    def __init__(self):
        self.balance = 0.0
        self.hashed_pin = None
        self.logged_in = False

    def set_pin(self, pin):
        if self.hashed_pin is None:
            self.hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
            return True
        return False

    def login(self, pin):
        if self.hashed_pin and hashlib.sha256(pin.encode()).hexdigest() == self.hashed_pin:
            self.logged_in = True
            return True
        return False

    def deposit(self, amount):
        if self.logged_in and amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if self.logged_in and 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def send(self, amount):
        return self.withdraw(amount)

# -------------------
# GUI with ipywidgets
# -------------------
account = MpesaAccount()

# Widgets
pin_input = Password(description='PIN:')
pin_button = Button(description='Login/Set PIN')
amount_input = FloatText(description='Amount:')
deposit_button = Button(description='Deposit')
withdraw_button = Button(description='Withdraw')
send_button = Button(description='Send Money')
check_button = Button(description='Check Balance')
message_label = Label(value='')
balance_label = Label(value='Balance: 0.0')

# Event handlers
def login_action(b):
    pin = pin_input.value
    if account.set_pin(pin):
        message_label.value = "✅ PIN set. Login again."
    elif account.login(pin):
        message_label.value = "✅ Login successful!"
    else:
        message_label.value = "❌ Incorrect PIN!"
    pin_input.value = ''

def deposit_action(b):
    amt = amount_input.value
    if account.deposit(amt):
        message_label.value = "✅ Deposit Successful"
        balance_label.value = f"Balance: {account.balance}"
    else:
        message_label.value = "❌ Deposit Failed"
    amount_input.value = 0.0

def withdraw_action(b):
    amt = amount_input.value
    if account.withdraw(amt):
        message_label.value = "✅ Withdrawal Successful"
        balance_label.value = f"Balance: {account.balance}"
    else:
        message_label.value = "❌ Withdrawal Failed"
    amount_input.value = 0.0

def send_action(b):
    amt = amount_input.value
    if account.send(amt):
        message_label.value = "✅ Money Sent"
        balance_label.value = f"Balance: {account.balance}"
    else:
        message_label.value = "❌ Send Failed"
    amount_input.value = 0.0

def check_action(b):
    balance_label.value = f"Balance: {account.balance}"
    message_label.value = "💰 Balance Displayed"

# Link buttons to functions
pin_button.on_click(login_action)
deposit_button.on_click(deposit_action)
withdraw_button.on_click(withdraw_action)
send_button.on_click(send_action)
check_button.on_click(check_action)

# Layout
vbox = VBox([
    HBox([pin_input, pin_button]),
    amount_input,
    HBox([deposit_button, withdraw_button, send_button]),
    check_button,
    message_label,
    balance_label
])

display(vbox)
