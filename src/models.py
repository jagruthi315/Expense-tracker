import sqlite3
def init_db(path="db/expenses.db"):
    con = sqlite3.connect(path); cur = con.cursor()
    cur.executescript("""
    PRAGMA foreign_keys=ON;
    CREATE TABLE IF NOT EXISTS categories(
      id INTEGER PRIMARY KEY, name TEXT UNIQUE, parent TEXT
    );
    CREATE TABLE IF NOT EXISTS transactions(
      id INTEGER PRIMARY KEY,
      tx_date TEXT,           -- ISO date
      description TEXT,
      amount REAL,            -- negative=expense, positive=income
      currency TEXT DEFAULT 'INR',
      account TEXT,           -- e.g., 'HDFC', 'Cash'
      category_id INTEGER,    -- FK to categories
      raw_source TEXT,
      tags TEXT,
      UNIQUE(tx_date, description, amount, account),
      FOREIGN KEY(category_id) REFERENCES categories(id)
    );
    CREATE TABLE IF NOT EXISTS budgets(
      id INTEGER PRIMARY KEY,
      month TEXT,             -- '2025-11'
      category_name TEXT,
      limit_amount REAL
    );
    """)
    con.commit(); con.close()
