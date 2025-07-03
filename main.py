import pandas as pd 
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description

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
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            'Date': date,
            'Amount': amount,
            'Category': category,
            'Description': description
        }
        with open(cls.CSV_FILE, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if filtered_df.empty:
            print('No transactions found for the given date range.')
        else:
            print(f"Transactions from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}:")
            print(filtered_df.to_string(index=False, formatters={'Date': lambda x: x.strftime('%d/%m/%Y')}))
            
            total_income = filtered_df[filtered_df['category'] == 'Income']['Amount'].sum()
            total_expenses = filtered_df[filtered_df['category'] != 'Income']['Amount'].sum()
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
            CSV.get_transactions(start_date, end_date)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    



