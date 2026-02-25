from src.ingest import read_bank_csv
from src.categorize import categorize_transaction
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# load data
file_path = Path("tests/sample.csv")
df = read_bank_csv(file_path, account="Test")

# apply categorization
df["Category"] = df["description"].apply(categorize_transaction)

print(df.head())
print("\nTotal spending:", df["amount"].sum())
print("\nCategory summary:")
print(df.groupby("Category")["amount"].sum())

# ensure date column is datetime
df["tx_date"] = pd.to_datetime(df["tx_date"])

# 🔹 Category totals
category_totals = df.groupby("Category")["amount"].sum().abs()

# -----------------------------
# 1️⃣ BAR CHART
# -----------------------------
plt.figure()
category_totals.plot(kind="bar")
plt.title("Spending by Category")
plt.ylabel("Amount")

# -----------------------------
# 2️⃣ PIE CHART (only if >1 category)
# -----------------------------
if len(category_totals) > 1:
    plt.figure()
    category_totals.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Spending Distribution by Category")
    plt.ylabel("")

# -----------------------------
# 3️⃣ DAILY TREND LINE CHART
# -----------------------------
daily_spending = df.groupby("tx_date")["amount"].sum().abs()

if len(daily_spending) > 1:
    plt.figure()
    daily_spending.plot(kind="line", marker="o")
    plt.title("Daily Spending Trend")
    plt.xlabel("Date")
    plt.ylabel("Amount Spent")
    plt.xticks(rotation=45)

# -----------------------------
# 4️⃣ MONTHLY TREND
# -----------------------------
monthly_spending = df.resample("M", on="tx_date")["amount"].sum().abs()

if len(monthly_spending) > 1:
    plt.figure()
    monthly_spending.plot(kind="line", marker="o")
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount Spent")
    plt.xticks(rotation=45)

# 🔥 Show all charts together
plt.show()
