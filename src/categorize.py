# import re, sqlite3, pandas as pd

# RULES = {
#   "Groceries": [r"big bazaar|reliance fresh|d-mart|grocery|supermart"],
#   "Food": [r"swiggy|zomato|restaurant|cafe|coffee"],
#   "Transport": [r"uber|ola|metro|fuel|petrol|diesel|bus"],
#   "Bills & Utilities": [r"electric|water|wifi|broadband|mobile recharge|dth"],
#   "Shopping": [r"amazon|flipkart|myntra|ajio"],
#   "Entertainment": [r"netflix|amazon prime|spotify|cinema|bookmyshow"],
#   "Income": [r"salary|payout|refund|reimbursement"]
# }

# def classify(desc):
#     d = desc.lower()
#     for cat, pats in RULES.items():
#         if any(re.search(p, d) for p in pats):
#             return cat
#     return "Uncategorized"

# # ⭐ ADD THIS FUNCTION (pytest expects it)
# def categorize_transaction(description: str) -> str:
#     return classify(description)

# def run(db_path="db/expenses.db"):
#     con = sqlite3.connect(db_path)
#     df = pd.read_sql_query(
#         "SELECT id, description, amount FROM transactions WHERE category_id IS NULL", con
#     )
#     cats = pd.read_sql_query("SELECT id,name FROM categories", con)
#     name_to_id = dict(zip(cats["name"], cats["id"]))

#     # ensure base categories exist
#     for name in RULES.keys() | {"Uncategorized"}:
#         if name not in name_to_id:
#             con.execute("INSERT INTO categories(name) VALUES(?)",(name,))
#             con.commit()

#     cats = pd.read_sql_query("SELECT id,name FROM categories", con)
#     name_to_id = dict(zip(cats["name"], cats["id"]))

#     for row in df.itertuples():
#         cat = "Income" if row.amount > 0 else classify(row.description)
#         con.execute(
#             "UPDATE transactions SET category_id=? WHERE id=?",
#             (name_to_id[cat], row.id)
#         )

#     con.commit()
#     con.close()

# if __name__ == "__main__":
#     run()

import re
import sqlite3
import pandas as pd

# ✅ Correct DB path (same folder as script)
DB_PATH = "expenses.db"

# =========================
# 📚 Category Rules (Expanded)
# =========================
RULES = {
    "Groceries": [r"big bazaar", r"reliance", r"d[- ]?mart", r"grocery", r"supermarket", r"kirana"],
    "Food": [r"swiggy", r"zomato", r"restaurant", r"cafe", r"coffee", r"eatery", r"pizza", r"burger"],
    "Transport": [r"uber", r"ola", r"metro", r"fuel", r"petrol", r"diesel", r"bus", r"auto", r"rapido"],
    "Bills & Utilities": [r"electric", r"electricity", r"water", r"wifi", r"broadband", r"mobile", r"recharge", r"dth", r"gas bill"],
    "Shopping": [r"amazon", r"flipkart", r"myntra", r"ajio", r"meesho", r"shop", r"store"],
    "Entertainment": [r"netflix", r"prime", r"spotify", r"cinema", r"bookmyshow", r"hotstar", r"youtube", r"concert", r"movie"],
    "Health": [r"hospital", r"clinic", r"pharmacy", r"medicine", r"doctor", r"apollo", r"medplus"],
    "Education": [r"course", r"udemy", r"coursera", r"college", r"school", r"fees", r"exam"],
    "Travel": [r"flight", r"train", r"irctc", r"hotel", r"oyo", r"booking", r"trip"],
    "Rent": [r"rent", r"landlord", r"lease"],
    "Personal Care": [r"salon", r"spa", r"cosmetics", r"parlor", r"beauty"],
    "Income": [r"salary", r"payout", r"refund", r"reimbursement", r"bonus", r"credited", r"freelance", r"payment"],
}

# =========================
# 🔍 Classification Logic
# =========================
def classify(description: str, amount: float) -> str:
    if not description:
        return "Uncategorized"

    # Income first
    if amount > 0:
        return "Income"

    d = description.lower()

    for category, patterns in RULES.items():
        for pattern in patterns:
            if re.search(pattern, d):
                return category

    return "Uncategorized"

# pytest helper
def categorize_transaction(description: str) -> str:
    return classify(description, -1)

# =========================
# 🗄️ Apply Categorization to DB
# =========================
def run():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Ensure categories exist
    cur.execute("SELECT id, name FROM categories")
    existing = dict(cur.fetchall())

    for category in list(RULES.keys()) + ["Uncategorized"]:
        if category not in existing.values():
            cur.execute("INSERT INTO categories (name) VALUES (?)", (category,))
    con.commit()

    # Reload categories
    cur.execute("SELECT id, name FROM categories")
    name_to_id = {name: cid for cid, name in cur.fetchall()}

    # Fetch uncategorized transactions
    df = pd.read_sql_query(
        "SELECT id, description, amount FROM transactions WHERE category_id IS NULL",
        con
    )

    print(f"Found {len(df)} uncategorized transactions")

    updated = 0

    for row in df.itertuples():
        category = classify(row.description, row.amount)
        cat_id = name_to_id.get(category, name_to_id["Uncategorized"])

        cur.execute(
            "UPDATE transactions SET category_id=? WHERE id=?",
            (cat_id, row.id),
        )
        updated += 1

    con.commit()
    con.close()

    print(f"✅ Categorized {updated} transactions successfully!")

if __name__ == "__main__":
    run()