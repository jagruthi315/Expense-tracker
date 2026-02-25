# import sqlite3
# import pandas as pd
# from pathlib import Path

# # ✅ Locate database (one level above src/)
# BASE_DIR = Path(__file__).resolve().parent.parent
# DB_PATH = BASE_DIR / "expenses.db"

# def fetch_frame(db_path=DB_PATH):
#     """Fetch transactions data from SQLite and prepare dataframe."""

#     # 🔒 Check if DB exists
#     if not db_path.exists():
#         print(f"⚠️ Database not found: {db_path}")
#         return pd.DataFrame()

#     con = sqlite3.connect(db_path)

#     query = """
#     SELECT 
#         t.tx_date,
#         t.description,
#         t.amount,
#         t.account,
#         c.name AS category
#     FROM transactions t
#     LEFT JOIN categories c ON c.id = t.category_id
#     """

#     try:
#         df = pd.read_sql_query(query, con, parse_dates=["tx_date"])
#     except Exception as e:
#         print("⚠️ SQL error:", e)
#         con.close()
#         return pd.DataFrame()

#     con.close()

#     # 🛑 If no data, return safely
#     if df.empty:
#         return df

#     # ✅ Create month column
#     df["month"] = df["tx_date"].dt.to_period("M").astype(str)

#     return df


# def kpis(df):
#     """Calculate KPIs for dashboard."""

#     # 🛑 Handle empty dataframe
#     if df.empty:
#         return {
#             "total_spend": 0,
#             "income": 0,
#             "savings": 0,
#             "top_categories": pd.Series(dtype=float)
#         }

#     kpi = {}

#     # 💸 Total spend (negative values)
#     kpi["total_spend"] = -df.loc[df["amount"] < 0, "amount"].sum()

#     # 💰 Income
#     kpi["income"] = df.loc[df["amount"] > 0, "amount"].sum()

#     # 🏦 Savings
#     kpi["savings"] = kpi["income"] - kpi["total_spend"]

#     # 📊 Top spending categories
#     kpi["top_categories"] = (
#         -df[df["amount"] < 0]
#         .groupby("category")["amount"]
#         .sum()
#         .sort_values(ascending=False)
#         .head(5)
#     )

#     return kpi

import sqlite3
import pandas as pd
from pathlib import Path

# ✅ Locate database (one level above src/)
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "expenses.db"


def fetch_frame(db_path=DB_PATH):
    """Fetch transactions data from SQLite and prepare dataframe."""

    if not db_path.exists():
        print(f"⚠️ Database not found: {db_path}")
        return pd.DataFrame()

    con = sqlite3.connect(db_path)

    query = """
    SELECT 
        t.tx_date,
        t.description,
        t.amount,
        t.account,
        COALESCE(c.name, 'Uncategorized') AS category
    FROM transactions t
    LEFT JOIN categories c ON c.id = t.category_id
    """

    df = pd.read_sql_query(query, con, parse_dates=["tx_date"])
    con.close()

    if df.empty:
        return df

    # Ensure category column has no nulls
    df["category"] = df["category"].fillna("Uncategorized")

    # Create month column
    df["month"] = df["tx_date"].dt.to_period("M").astype(str)

    return df


def kpis(df):
    """Calculate KPIs for dashboard."""

    if df.empty:
        return {
            "total_spend": 0,
            "income": 0,
            "savings": 0,
            "top_categories": pd.Series(dtype=float)
        }

    kpi = {}

    # Total spend
    kpi["total_spend"] = -df.loc[df["amount"] < 0, "amount"].sum()

    # Income
    kpi["income"] = df.loc[df["amount"] > 0, "amount"].sum()

    # Savings
    kpi["savings"] = kpi["income"] - kpi["total_spend"]

    # 🔥 THIS FIX SHOWS ALL CATEGORIES
    kpi["top_categories"] = (
        -df[df["amount"] < 0]
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return kpi