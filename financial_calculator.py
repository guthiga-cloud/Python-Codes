# financial_calculator.py
# Calculate financial metrics

def main():
    print("=== FINANCIAL CALCULATIONS ===\n")
    
    # Simple Interest
    principal = 10000.0
    rate = 5.5
    time = 3
    simple_interest = (principal * rate * time) / 100
    print("1. Simple Interest")
    print(f"   Principal: ${principal:.2f}, Rate: {rate}%, Time: {time} years")
    print(f"   Simple Interest: ${simple_interest:.2f}")
    print(f"   Total Amount: ${principal + simple_interest:.2f}\n")
    
    # Compound Interest
    compound_interest = principal * ((1 + rate/100) ** time) - principal
    total_amount = principal * ((1 + rate/100) ** time)
    print("2. Compound Interest (Annual Compounding)")
    print(f"   Principal: ${principal:.2f}, Rate: {rate}%, Time: {time} years")
    print(f"   Compound Interest: ${compound_interest:.2f}")
    print(f"   Total Amount: ${total_amount:.2f}\n")
    
    # EMI Calculation
    loan_amount = 500000.0
    annual_rate = 8.5
    months = 60
    monthly_rate = annual_rate / (12 * 100)
    emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
    print("3. EMI Calculator (Loan)")
    print(f"   Loan Amount: ${loan_amount:.2f}, Rate: {annual_rate}%, Tenure: {months} months")
    print(f"   Monthly EMI: ${emi:.2f}")
    print(f"   Total Payment: ${emi * months:.2f}")
    print(f"   Total Interest: ${(emi * months) - loan_amount:.2f}\n")
    
    # Profit/Loss Calculation
    cost_price = 750.0
    selling_price = 925.0
    profit_loss = selling_price - cost_price
    profit_loss_percent = (profit_loss / cost_price) * 100
    print("4. Profit/Loss Calculator")
    print(f"   Cost Price: ${cost_price:.2f}, Selling Price: ${selling_price:.2f}")
    if profit_loss > 0:
        print(f"   Profit: ${profit_loss:.2f} ({profit_loss_percent:.2f}%)")
    elif profit_loss < 0:
        print(f"   Loss: ${-profit_loss:.2f} ({-profit_loss_percent:.2f}%)")
    else:
        print("   No Profit, No Loss")
    
    # Discount Calculation
    original_price = 1200.0
    discount_percent = 15
    discount_amount = original_price * discount_percent / 100
    final_price = original_price - discount_amount
    print("\n5. Discount Calculator")
    print(f"   Original Price: ${original_price:.2f}")
    print(f"   Discount: {discount_percent}%")
    print(f"   Discount Amount: ${discount_amount:.2f}")
    print(f"   Final Price: ${final_price:.2f}")

if __name__ == "__main__":
    main()
