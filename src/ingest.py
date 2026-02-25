import pandas as pd
import sqlite3
from pathlib import Path

# ✅ Resolve DB path correctly
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "expenses.db"


# =========================
# AUTO CATEGORY LOGIC
# =========================
def auto_category(description):
    description = description.lower()

    if any(word in description for word in ["uber", "ola", "metro", "petrol", "fuel"]):
        return "Transport"
    elif any(word in description for word in ["swiggy", "zomato", "restaurant", "cafe"]):
        return "Food"
    elif any(word in description for word in ["amazon", "flipkart", "shopping"]):
        return "Shopping"
    elif any(word in description for word in ["salary", "income"]):
        return "Income"
    elif any(word in description for word in ["rent"]):
        return "Rent"
    else:
        return "Other"


# =========================
# READ CSV
# =========================
def read_bank_csv(file, account, date_col="Date", desc_col="Description", amt_col="Amount"):

    if hasattr(file, "read"):
        df = pd.read_csv(file)
    else:
        df = pd.read_csv(file)

    df["tx_date"] = pd.to_datetime(df[date_col], errors="coerce")
    df["description"] = df[desc_col].astype(str).str.strip()
    df["amount"] = pd.to_numeric(df[amt_col], errors="coerce")
    df["account"] = account

    df = df.dropna(subset=["tx_date", "amount"])

    # ✅ Add month column for graphs
    df["month"] = df["tx_date"].dt.strftime("%Y-%m")

    # ✅ Auto category
    df["category"] = df["description"].apply(auto_category)

    return df[["tx_date", "description", "amount", "account", "month", "category"]]


# =========================
# INSERT DATA
# =========================
def upsert_transactions(df, db_path=DB_PATH):

    if df.empty:
        return 0

    init_db()

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for _, row in df.iterrows():

        # Insert category if not exists
        cur.execute("INSERT OR IGNORE INTO categories(name) VALUES (?)", (row["category"],))

        # Get category id
        cur.execute("SELECT id FROM categories WHERE name=?", (row["category"],))
        category_id = cur.fetchone()[0]

        # Insert transaction
        cur.execute("""
            INSERT INTO transactions (tx_date, description, amount, account, category_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            row["tx_date"].strftime("%Y-%m-%d"),
            row["description"],
            row["amount"],
            row["account"],
            category_id
        ))

    con.commit()
    con.close()

    return len(df)


# =========================
# INIT DB
# =========================
def init_db(db_path=DB_PATH):

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tx_date TEXT,
        description TEXT,
        amount REAL,
        account TEXT,
        category_id INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    con.commit()
    con.close()


if __name__ == "__main__":
    init_db()
    print("✅ Database Ready")