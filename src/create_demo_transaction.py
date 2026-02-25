import pandas as pd
import random
from datetime import datetime, timedelta

descriptions = {
    "Food": ["Swiggy order", "Zomato lunch", "Cafe coffee", "Restaurant dinner"],
    "Transport": ["Uber ride", "Ola trip", "Metro recharge", "Petrol pump"],
    "Shopping": ["Amazon purchase", "Flipkart order", "Clothing store", "Grocery shopping"],
    "Rent": ["House rent"],
    "Utilities": ["Electricity bill", "Water bill", "Mobile recharge", "Internet bill"],
    "Entertainment": ["Movie ticket", "Netflix subscription", "Concert pass"],
    "Income": ["Salary credit", "Freelance payment"]
}

rows = []
start_date = datetime(2024, 11, 1)

for i in range(100):
    category = random.choice(list(descriptions.keys()))
    description = random.choice(descriptions[category])
    date = start_date + timedelta(days=random.randint(0, 120))

    if category == "Income":
        amount = random.randint(20000, 60000)
    elif category == "Rent":
        amount = -random.randint(8000, 15000)
    else:
        amount = -random.randint(100, 3000)

    rows.append([date.strftime("%Y-%m-%d"), description, amount])

df = pd.DataFrame(rows, columns=["Date", "Description", "Amount"])
df.to_csv("demo_transactions.csv", index=False)

print("✅ demo_transactions.csv created!")