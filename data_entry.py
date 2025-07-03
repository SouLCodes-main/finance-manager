from datetime import datetime
from multiprocessing import Value
from sre_parse import CATEGORIES

CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime("%d/%m/%Y")
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return get_date(prompt, allow_default)



def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        return amount
    except ValueError as e:
        print(f"Error: {e}")
        return get_amount()


def get_category():
    category = input("Enter the category ('I' for income, 'E' for expense): ")
    if category.upper() in CATEGORIES:
        return CATEGORIES[category.upper()]

    print("Invalid category. Please enter 'I' for income or 'E' for expense.")
    return get_category()

def get_description():
    return input("Enter the description: ")

