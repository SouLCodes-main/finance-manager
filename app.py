from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from datetime import datetime
import plotly
import json
import os

app = Flask(__name__)

CSV_FILE = "finance_data.csv"
COLUMNS = ["Date", "Amount", "Category", "Description"]

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)

def add_entry(date, amount, category, description):
    initialize_csv()
    new_entry = {
        'Date': date,
        'Amount': float(amount),
        'Category': category,
        'Description': description
    }
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def get_transactions(start_date=None, end_date=None):
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=COLUMNS)
    
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        return df
        
    df['Date'] = pd.to_datetime(df['Date'])
    
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    # Ensure Date column remains as datetime
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def get_summary(df):
    if df.empty:
        return {'income': 0, 'expenses': 0, 'savings': 0}
    
    total_income = df[df['Category'] == 'Income']['Amount'].sum()
    total_expenses = df[df['Category'] == 'Expenses']['Amount'].sum()
    net_savings = total_income - total_expenses
    
    return {
        'income': round(total_income, 2),
        'expenses': round(total_expenses, 2),
        'savings': round(net_savings, 2)
    }

def create_plot(df):
    if df.empty:
        return {}

    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    income_df = df[df['Category'] == 'Income'].copy()
    expenses_df = df[df['Category'] == 'Expenses'].copy()
    
    data = [
        {
            'x': income_df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'y': income_df['Amount'].tolist(),
            'type': 'scatter',
            'name': 'Income',
            'line': {'color': '#4CAF50'}
        },
        {
            'x': expenses_df['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'y': expenses_df['Amount'].tolist(),
            'type': 'scatter',
            'name': 'Expenses',
            'line': {'color': '#f44336'}
        }
    ]
    
    return json.dumps(data)

@app.route('/')
def index():
    df = get_transactions()
    summary = get_summary(df)
    plot_data = create_plot(df)
    transactions = df.sort_values('Date', ascending=False).head(5).to_dict('records')
    return render_template('index.html', 
                         summary=summary, 
                         plot_data=plot_data,
                         recent_transactions=transactions)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        add_entry(date, amount, category, description)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/transactions')
def transactions():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    df = get_transactions(start_date, end_date)
    transactions = df.sort_values('Date', ascending=False).to_dict('records')
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    initialize_csv()
    app.run(debug=True)