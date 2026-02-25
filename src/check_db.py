# import sqlite3

# con = sqlite3.connect("expenses.db")

# print("Transactions:")
# print(con.execute("SELECT id, description, category_id FROM transactions LIMIT 5").fetchall())

# print("\nCategories:")
# print(con.execute("SELECT * FROM categories").fetchall())

# con.close()

# import sqlite3

# con = sqlite3.connect("expenses.db")

# print("\nTables in DB:")
# print(con.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())

# con.close()

import sqlite3

con = sqlite3.connect("expenses.db")

print("\nTransactions:")
rows = con.execute("SELECT id, description, amount, category_id FROM transactions").fetchall()
for r in rows:
    print(r)

con.close()