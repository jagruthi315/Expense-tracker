# 📊 Expense Tracker (Python + SQLite + Streamlit)

A simple yet powerful Expense Tracker Web App built using Python, SQLite, and Streamlit that helps users record, categorize, and visualize their expenses through interactive dashboards.

This project demonstrates practical use of data handling, SQL queries, and data visualization in a real-world finance management tool.

## Features

✅ Add, view, and manage daily expenses

✅ Categorize expenses (Food, Travel, Bills, Shopping, etc.)

✅ Automatic total spending calculation

✅ Interactive charts for expense insights

✅ Category-wise analysis with Pie, Bar, and Line charts

✅ Lightweight database using SQLite (no external setup needed)

## 🛠️ Tech Stack

## Frontend

Streamlit – interactive web interface

## Backend

Python

Database

SQLite – local storage for transactions and categories

## Libraries Used

pandas – data manipulation

sqlite3 – database connectivity

streamlit – web app framework

📈 Visualizations

The dashboard provides multiple insights:

🥧 Pie Chart – category-wise expense distribution

📊 Bar Chart – comparison of spending across categories

📉 Line Chart – spending trend over time

## 📂 Project Structure
EXPENSE-TRACKER/
│
├── src/
|   ├── .gitignore
│   ├── __init__.py
│   ├── analyse.py
│   ├── app_streamlit.py
│   ├── budget.py
│   ├── categorize.py
│   ├── check_db.py
│   ├── create_demo_transactions.csv
│   ├── expenses.db
│   ├── ingest.py
│   ├── init_db.py
│   ├── models.py
│   ├── report.py
│
├── tests/
│   ├── sample.csv
│   ├── test_categorize.py
│   ├── test_ingest.py
│
├── requirements.txt
├── run_demo.py


## How to Run
### Clone the repository
git clone https://github.com/your-username/expense-tracker.git

###  Navigate to project folder expense tracker then 
cd src

###  Install dependencies
pip install -r requirements.txt

###  Run the app
streamlit run app_streamlit.py

## Learning Outcomes

This project helped in understanding:

✅ Building data apps with Streamlit

✅ Using SQL for data aggregation & analysis

✅ Structuring real-world Python projects

## 🌟 Future Improvements

User authentication

Monthly budget alerts

Export reports (PDF/CSV)

Cloud database integration

Mobile-friendly UI
