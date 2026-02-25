import pandas as pd
import sqlite3
from pathlib import Path

# ✅ DB Path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "expenses.db"


def check_budget(month, db_path=DB_PATH):
    """
    Returns spending summary by category for a given month.
    """

    con = sqlite3.connect(db_path)

    query = """
        SELECT 
            c.name AS category,
            ABS(SUM(t.amount)) AS spent
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.amount < 0
          AND strftime('%Y-%m', t.tx_date) = ?
        GROUP BY c.name
        ORDER BY spent DESC
    """

    df = pd.read_sql_query(query, con, params=[month])
    con.close()

    if df.empty:
        return pd.DataFrame(columns=["category", "spent"])

    return df