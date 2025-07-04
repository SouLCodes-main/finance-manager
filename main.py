import pandas as pd 
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt
import os

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["Date", "Amount", "Category", "Description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
            print(f"Created new CSV file: {cls.CSV_FILE}")
    @classmethod
    def add_entry(cls, date, amount, category, description):
        print(f"[DEBUG] Writing to: {os.path.abspath(cls.CSV_FILE)}")
        new_entry = {
            'Date': date,
            'Amount': amount,
            'Category': category,
            'Description': description
        }
        print(f"Adding entry: {new_entry}")  # Debug print
        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        # Handle mixed date formats automatically
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if filtered_df.empty:
            print('No transactions found for the given date range.')
        else:
            print(f"Transactions from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}:")
            print(filtered_df.to_string(index=False))
            
            total_income = filtered_df[filtered_df['Category'] == 'Income']['Amount'].sum()
            total_expenses = filtered_df[(filtered_df['Category'] == 'Expenses') | (filtered_df['Category'] == 'Expense')]['Amount'].sum()
            print("\nSummary:")
            print(f"Total Income: INR {total_income:.2f}")
            print(f"Total Expenses: INR {total_expenses:.2f}")
            print(f"Net Savings: INR {total_income - total_expenses:.2f}")

            return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date (DD/MM/YYYY) or press Enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)
    print("Entry added successfully!")

def plot_transactions(df):
    df.set_index('Date', inplace=True)

    income_df = (df[df['Category'] == 'Income'].resample('D').sum().reindex(df.index, fill_value=0))
    expenses_df = (df[(df['Category'] == 'Expenses') | (df['Category'] == 'Expense')].resample('D').sum().reindex(df.index, fill_value=0))


    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df['Amount'], label='Income', color='green')
    plt.plot(expenses_df.index, expenses_df['Amount'], label='Expenses', color='red')
    plt.xlabel('Date')
    plt.ylabel('Amount (INR)')
    plt.title('Income and Expenses')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add a New Transaction")
        print("2. View Transactions")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            add()
        elif choice == '2':
            start_date = input("Enter start date (DD/MM/YYYY): ")
            end_date = input("Enter end date (DD/MM/YYYY): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot the transactions? (y/n): ").lower() == 'y':
                plot_transactions(df)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    



