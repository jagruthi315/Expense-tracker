import pandas as pd
import matplotlib.pyplot as plt


def monthly_trend(df):
    if df.empty:
        print("No data")
        return

    s = (
        -df[df.amount < 0]
        .groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    if s.empty:
        print("No expense data")
        return

    plt.figure(figsize=(8, 4))
    plt.plot(s["month"], s["amount"])
    plt.xticks(rotation=45)
    plt.title("Monthly Spend")
    plt.tight_layout()
    plt.show()


def category_donut(df, month):

    s = (
        -df[(df.amount < 0) & (df["month"] == month)]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    if s.empty:
        print("No category data for this month")
        return

    plt.figure(figsize=(5, 5))
    plt.pie(s.values, labels=s.index, wedgeprops={"width": 0.5})
    plt.title(f"Category Split — {month}")
    plt.tight_layout()
    plt.show()