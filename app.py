from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def load_and_process_data():
    df = pd.read_csv('data/food_waste.csv', parse_dates=['Date'])
    df['Month'] = df['Date'].dt.strftime('%B')
    df['Week'] = df['Date'].dt.isocalendar().week

    monthly_data = df.groupby('Month')['Food_Waste_kg'].sum().sort_values()
    weekly_data = df.groupby('Week')['Food_Waste_kg'].sum()

    best_month = monthly_data.idxmin()
    worst_month = monthly_data.idxmax()

    return df, monthly_data, weekly_data, best_month, worst_month

def generate_graphs(monthly_data, weekly_data):
    if not os.path.exists('static'):
        os.makedirs('static')

    # Monthly bar chart
    plt.figure(figsize=(10,5))
    monthly_data.plot(kind='bar', color='green')
    plt.title('Monthly Food Waste')
    plt.ylabel('Waste (kg)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/monthly_bar.png')
    plt.close()

    # Weekly pie chart
    plt.figure(figsize=(6,6))
    weekly_data.plot(kind='pie', autopct='%1.1f%%')
    plt.title('Weekly Food Waste Distribution')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('static/weekly_pie.png')
    plt.close()

@app.route('/')
def dashboard():
    df, monthly_data, weekly_data, best_month, worst_month = load_and_process_data()
    generate_graphs(monthly_data, weekly_data)

    problems = [
        "Overproduction of food",
        "Poor inventory management",
        "Lack of awareness in staff"
    ]
    solutions = [
        "Cook as per demand forecasts",
        "Track inventory and use FIFO",
        "Train staff in waste reduction"
    ]

    return render_template(
        'dashboard.html',
        best_month=best_month,
        worst_month=worst_month,
        problems=problems,
        solutions=solutions
    )

if __name__ == '__main__':
    app.run(debug=True)
