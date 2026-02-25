import pandas as pd, sqlite3
def export_month(month, path="exports/report.xlsx", db="db/expenses.db"):
    con = sqlite3.connect(db)
    tx = pd.read_sql_query("""SELECT tx_date,description,amount,account,c.name AS category
                              FROM transactions t LEFT JOIN categories c ON c.id=t.category_id
                              WHERE strftime('%Y-%m', tx_date)=? ORDER BY tx_date""", con, params=[month])
    piv = (-tx[tx.amount<0].pivot_table(index="category", values="amount", aggfunc="sum").sort_values("amount", ascending=False))
    with pd.ExcelWriter(path, engine="xlsxwriter") as w:
        tx.to_excel(w, sheet_name="Transactions", index=False)
        piv.to_excel(w, sheet_name="Category Summary")
    con.close(); return path
