
import streamlit as st
import pandas as pd
from analyse import fetch_frame, kpis
from budget import check_budget
from ingest import read_bank_csv, upsert_transactions

st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
st.title("💸 Personal Expense Tracker")

# =========================
# 📂 Upload & Ingest CSV
# =========================
uploaded_file = st.file_uploader("Upload CSV")

if uploaded_file:
    df_upload = read_bank_csv(
        uploaded_file,
        account="Manual",
        date_col="Date",
        desc_col="Description",
        amt_col="Amount"
    )
    rows = upsert_transactions(df_upload)
    st.success(f"Ingested {rows} rows")

# =========================
# 📊 Load Data Safely
# =========================
def safe_fetch():
    try:
        df = fetch_frame()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = safe_fetch()

# =========================
# 🛑 Stop if no data
# =========================
if df.empty:
    st.warning("No data found. Please upload a CSV to begin.")
    st.stop()

# =========================
# 🧹 Clean & Normalize Columns
# =========================
df["category"] = df["category"].fillna("Uncategorized")

# Ensure month column exists & is string
if "month" not in df.columns:
    df["month"] = pd.to_datetime(df["tx_date"]).dt.to_period("M").astype(str)

# =========================
# 📅 Filters
# =========================
months = sorted(df["month"].dropna().unique())
selected_month = st.selectbox("Month", months[::-1])

accounts = sorted(df["account"].dropna().unique())
selected_accounts = st.multiselect(
    "Accounts",
    accounts,
    default=accounts
)

# Filtered dataframe
filtered_df = df[
    (df["month"] == selected_month) &
    (df["account"].isin(selected_accounts))
]

# =========================
# 📈 KPIs
# =========================
k = kpis(filtered_df)

c1, c2, c3 = st.columns(3)
c1.metric("Total Spend", f"₹{k['total_spend']:.0f}")
c2.metric("Income", f"₹{k['income']:.0f}")
c3.metric("Savings", f"₹{k['savings']:.0f}")

# =========================
# 📊 Charts
# =========================

# Spending by category
st.subheader("Spending by Category")

cat_spend = (
    filtered_df[filtered_df.amount < 0]
    .groupby("category")["amount"]
    .sum()
    .abs()
    .sort_values(ascending=False)
)

if not cat_spend.empty:
    st.bar_chart(cat_spend)
else:
    st.info("No spending data for selected filters.")

    # 🥧 Pie Chart for Category Distribution
st.subheader("Category Distribution")

if not cat_spend.empty:
    pie_df = cat_spend.reset_index()
    pie_df.columns = ["Category", "Amount"]

    st.pyplot(
        pie_df.set_index("Category").plot.pie(
            y="Amount",
            autopct="%1.0f%%",
            legend=False,
            ylabel="",
            figsize=(1.3,1.3),
            textprops={"fontsize": 5}  # 🔽 smaller text
        ).figure
    )
else:
    st.info("No category data available for pie chart.")

# Monthly trend
st.subheader("Monthly Spending Trend")

monthly_spend = (
    df[df.amount < 0]
    .groupby("month")["amount"]
    .sum()
    .abs()
)

if not monthly_spend.empty:
    st.line_chart(monthly_spend)
else:
    st.info("No monthly spending data available.")

# =========================
# 💰 Budget Check
# =========================
st.subheader("Budget Check")

try:
    budget_df = check_budget(selected_month)

    if budget_df is not None and not budget_df.empty:
        st.dataframe(budget_df)
    else:
        st.info("No budget data found for this month.")

except Exception as e:
    st.warning(f"Budget check unavailable: {e}")

