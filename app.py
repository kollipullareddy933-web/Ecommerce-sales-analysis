
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="E-commerce Analytics Pro",
    page_icon="🛍️",
    layout="wide"
)

# ---------------- CUSTOM STYLING ----------------
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background-color: #f3f6fb;
        border: 1px solid #e1e8f0;
        padding: 16px;
        border-radius: 12px;
    }
    h1, h2, h3 {
        color: #17365d;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
DATA_FILE = Path(__file__).parent / "data" / "ecommerce_sales.csv"

st.title("🛍️ E-commerce Sales Analytics")
st.caption(
    "Sales performance | Product insights | Customer analytics"
)

if not DATA_FILE.exists():
    st.error("Dataset not found. Run: python generate_data.py")
    st.stop()

df = pd.read_csv(DATA_FILE, parse_dates=["Order_Date"])

required_columns = [
    "Order_ID", "Order_Date", "Customer_ID", "City",
    "Product", "Category", "Quantity", "Unit_Price",
    "Discount", "Revenue"
]

if not all(col in df.columns for col in required_columns):
    st.error("Your dataset is missing one or more required columns.")
    st.stop()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.title("🔎 Dashboard Filters")

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

start_date = st.sidebar.date_input(
    "Start date", value=min_date,
    min_value=min_date, max_value=max_date
)
end_date = st.sidebar.date_input(
    "End date", value=max_date,
    min_value=min_date, max_value=max_date
)

all_categories = sorted(df["Category"].dropna().unique())
selected_categories = st.sidebar.multiselect(
    "Product categories",
    all_categories,
    default=all_categories
)

all_cities = sorted(df["City"].dropna().unique())
selected_cities = st.sidebar.multiselect(
    "Cities",
    all_cities,
    default=all_cities
)

if start_date > end_date:
    st.error("Start date must be on or before the end date.")
    st.stop()

# ---------------- FILTER DATA ----------------
filtered = df[
    df["Order_Date"].dt.date.between(start_date, end_date)
    & df["Category"].isin(selected_categories)
    & df["City"].isin(selected_cities)
].copy()

if filtered.empty:
    st.warning("No sales records match your filters.")
    st.stop()

# ---------------- KPI CALCULATIONS ----------------
total_revenue = filtered["Revenue"].sum()
total_orders = filtered["Order_ID"].nunique()
total_customers = filtered["Customer_ID"].nunique()
units_sold = filtered["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders if total_orders else 0
)

st.header("📊 Sales Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Unique Customers", f"{total_customers:,}")
c4.metric("Units Sold", f"{units_sold:,}")

c5, c6 = st.columns(2)
c5.metric("Average Order Value", f"₹{average_order_value:,.2f}")
c6.metric(
    "Revenue per Customer",
    f"₹{total_revenue / total_customers:,.2f}"
    if total_customers else "₹0.00"
)

st.caption(
    "A record represents an order line in this simulated dataset. "
    "Order counts use distinct Order_ID values."
)

# ---------------- MONTHLY SALES SUMMARY ----------------
st.header("📅 Monthly Sales Summary")

monthly = filtered.copy()
monthly["Month"] = monthly["Order_Date"].dt.to_period("M")

monthly_summary = (
    monthly.groupby("Month")
    .agg(
        Revenue=("Revenue", "sum"),
        Orders=("Order_ID", "nunique"),
        Units_Sold=("Quantity", "sum"),
        Customers=("Customer_ID", "nunique")
    )
    .sort_index()
)

monthly_summary["MoM Growth (%)"] = (
    monthly_summary["Revenue"].pct_change() * 100
)

monthly_summary.index = monthly_summary.index.astype(str)

left, right = st.columns([2, 1])

with left:
    st.subheader("Monthly Revenue Trend")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(
        monthly_summary.index,
        monthly_summary["Revenue"],
        marker="o",
        linewidth=2
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (₹)")
    ax.grid(axis="y", alpha=0.25)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.subheader("Revenue by Month")
    st.bar_chart(monthly_summary[["Revenue"]])

st.subheader("Monthly Performance Table")

monthly_display = monthly_summary.copy()
monthly_display["Revenue"] = monthly_display["Revenue"].map(
    lambda x: f"₹{x:,.2f}"
)
monthly_display["MoM Growth (%)"] = monthly_display[
    "MoM Growth (%)"
].map(
    lambda x: "N/A" if pd.isna(x) else f"{x:+.2f}%"
)

st.dataframe(monthly_display, use_container_width=True)

st.caption(
    "Month-over-month growth compares each month's revenue with "
    "the previous month in the filtered results."
)

# ---------------- TOP 5 PRODUCTS ----------------
st.header("🏆 Top 5 Best-Performing Products")

product_summary = (
    filtered.groupby("Product")
    .agg(
        Units_Sold=("Quantity", "sum"),
        Revenue=("Revenue", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .sort_values("Revenue", ascending=False)
)

top5 = product_summary.head(5).copy()

left, right = st.columns([1, 1.4])

with left:
    st.subheader("Top Products by Revenue")
    st.bar_chart(top5[["Revenue"]])

with right:
    st.subheader("Product Ranking")
    top5_display = top5.reset_index()
    top5_display.insert(
        0, "Rank", range(1, len(top5_display) + 1)
    )
    top5_display["Revenue"] = top5_display["Revenue"].map(
        lambda x: f"₹{x:,.2f}"
    )
    st.dataframe(top5_display, use_container_width=True, hide_index=True)

st.caption(
    "Products are ranked by total revenue, not by units sold."
)

# ---------------- CATEGORY AND CITY ANALYSIS ----------------
st.header("📦 Category and City Insights")

left, right = st.columns(2)

with left:
    st.subheader("Revenue by Category")
    category_summary = (
        filtered.groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(category_summary)

with right:
    st.subheader("Revenue by City")
    city_summary = (
        filtered.groupby("City")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(city_summary)

# ---------------- CUSTOMER ANALYSIS ----------------
st.header("👥 Customer Analysis")

customer_summary = (
    filtered.groupby("Customer_ID")
    .agg(
        Orders=("Order_ID", "nunique"),
        Revenue=("Revenue", "sum"),
        Units_Purchased=("Quantity", "sum"),
        Cities=("City", "nunique")
    )
    .sort_values("Revenue", ascending=False)
)

repeat_customers = int((customer_summary["Orders"] > 1).sum())
repeat_rate = (
    repeat_customers / len(customer_summary) * 100
    if len(customer_summary) else 0
)

a, b, c = st.columns(3)
a.metric("Customers in Filter", f"{len(customer_summary):,}")
b.metric("Repeat Customers", f"{repeat_customers:,}")
c.metric("Repeat Customer Rate", f"{repeat_rate:.1f}%")

left, right = st.columns(2)

with left:
    st.subheader("Top 10 Customers by Revenue")
    top_customers = customer_summary.head(10)
    st.bar_chart(top_customers[["Revenue"]])

with right:
    st.subheader("Customer Purchase Summary")
    customer_display = customer_summary.head(10).reset_index()
    customer_display["Revenue"] = customer_display["Revenue"].map(
        lambda x: f"₹{x:,.2f}"
    )
    st.dataframe(
        customer_display,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "Repeat customers are customers with more than one distinct "
    "Order_ID in the filtered data."
)

# ---------------- DETAILED SALES DATA ----------------
st.header("📋 Detailed Sales Records")

st.dataframe(
    filtered.sort_values("Order_Date", ascending=False),
    use_container_width=True,
    hide_index=True
)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Filtered Sales Data",
    data=csv_data,
    file_name="filtered_ecommerce_sales.csv",
    mime="text/csv"
)

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "E-commerce Sales Analytics | Built with Python, Pandas, "
    "Matplotlib and Streamlit | Simulated dataset for demonstration"
)
