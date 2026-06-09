import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# -- Page config ------------------
st.set_page_config(
    page_title="Superstore Sales Intelligence",
    page_icon="📊",
    layout="wide"
)

# -- Custom CSS for professional look ---------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.2rem;
        letter-spacing: 0.2px;
    }
    .sub-header {
        font-size: 1rem;
        color: #4a627a;
        margin-bottom: 1rem;
        line-height: 1.4;
    }
    hr { margin-top: 1rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📊 Superstore Sales Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Explore sales, profit, and product insights by region, category, and time.</div>', unsafe_allow_html=True)
st.markdown("---")

# -- Load data --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Sample_-_Superstore.csv", encoding="latin1")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"], errors="coerce")
    df["Month"]      = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"]       = df["Order Date"].dt.year
    return df

df = load_data()

# -- Sidebar filters -------------------------------------------------
st.sidebar.header("🔎 Explore your dashboard")
st.sidebar.markdown("Pick filters to focus on a specific part of the business.")

def sorted_unique(col):
    return sorted(df[col].dropna().astype(str).unique().tolist())

regions    = ["All"] + sorted_unique("Region") if "Region" in df.columns else ["All"]
categories = ["All"] + sorted_unique("Category") if "Category" in df.columns else ["All"]
segments   = ["All"] + sorted_unique("Segment") if "Segment" in df.columns else ["All"]

sel_region   = st.sidebar.selectbox("📍 Region", regions)
sel_category = st.sidebar.selectbox("📂 Category", categories)
sel_segment  = st.sidebar.selectbox("👥 Customer Segment", segments)

years = sorted(df["Year"].dropna().unique().tolist()) if "Year" in df.columns else []
sel_years = st.sidebar.multiselect("📅 Year(s)", years, default=years)

st.sidebar.markdown("---")
st.sidebar.markdown("**📌 Dataset:** Superstore sales records")
st.sidebar.markdown("**✨ Dashboard by:** Devang Yadav")
st.sidebar.markdown("[GitHub Repository](https://github.com/Dushdeva)")

# -- Apply filters ----------------------------------------------------
fdf = df.copy()

if sel_region != "All" and "Region" in fdf.columns:
    fdf = fdf[fdf["Region"] == sel_region]
if sel_category != "All" and "Category" in fdf.columns:
    fdf = fdf[fdf["Category"] == sel_category]
if sel_segment != "All" and "Segment" in fdf.columns:
    fdf = fdf[fdf["Segment"] == sel_segment]
if sel_years:
    fdf = fdf[fdf["Year"].isin(sel_years)]

if fdf.empty:
    st.warning("No results found for your selected filters. Try adjusting them and explore again.")
    st.stop()

# -- KPI cards (professional metrics) --------------------------------
total_sales   = fdf["Sales"].sum() if "Sales" in fdf.columns else 0
total_profit  = fdf["Profit"].sum() if "Profit" in fdf.columns else 0
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

total_orders = fdf["Order ID"].nunique() if "Order ID" in fdf.columns else 0
total_customers = fdf["Customer ID"].nunique() if "Customer ID" in fdf.columns else 0
avg_order_value = total_sales / total_orders if total_orders else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("💰 Total Sales", f"${total_sales:,.0f}")
c2.metric("📈 Total Profit", f"${total_profit:,.0f}")
c3.metric("📌 Profit Margin", f"{profit_margin:.1f}%")
c4.metric("🧾 Orders", f"{total_orders:,}")
c5.metric("👥 Customers", f"{total_customers:,}")
c6.metric("💵 Avg Order Value", f"${avg_order_value:,.0f}")

st.markdown("---")

# -- Helper function for cleaner plots -------------------------------
def style_axis(ax, title=None, xlabel=None, ylabel=None):
    if title:
        ax.set_title(title, fontsize=12, fontweight='semibold', color='#1E3A5F')
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# -- Row 1: Monthly trend + Regional sales & profit ----------------------
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📅 How sales and profit changed over time")
    monthly = fdf.groupby("Month")[["Sales", "Profit"]].sum().reset_index().sort_values("Month")

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.fill_between(range(len(monthly)), monthly["Sales"], alpha=0.2, color="#2C7DA0")
    ax.plot(range(len(monthly)), monthly["Sales"], color="#2C7DA0", linewidth=2.5,
            marker='o', markersize=4, label="Sales")

    ax2 = ax.twinx()
    ax2.plot(range(len(monthly)), monthly["Profit"], color="#E76F51", linewidth=2, linestyle='--',
             marker='s', markersize=4, label="Profit")

    ax.set_xticks(range(len(monthly)))
    ax.set_xticklabels(monthly["Month"], rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("Sales ($)", color="#2C7DA0")
    ax2.set_ylabel("Profit ($)", color="#E76F51")

    style_axis(ax, xlabel="Month", ylabel="Sales ($)")
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)

    fig.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("🌎 Which regions performed best")
    region_stats = fdf.groupby("Region")[["Sales", "Profit"]].sum().reset_index().sort_values("Sales", ascending=False)

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    x = np.arange(len(region_stats))
    width = 0.35

    bars_sales = ax2.bar(x - width/2, region_stats["Sales"], width, label="Sales", color="#2C7DA0")
    bars_profit = ax2.bar(x + width/2, region_stats["Profit"], width, label="Profit", color="#E76F51")

    ax2.set_xticks(x)
    ax2.set_xticklabels(region_stats["Region"])
    style_axis(ax2, xlabel="Region", ylabel="Amount ($)")
    ax2.legend(fontsize=9)

    for bar in bars_sales:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                 f"${bar.get_height():,.0f}", ha='center', va='bottom', fontsize=7)
    for bar in bars_profit:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                 f"${bar.get_height():,.0f}", ha='center', va='bottom', fontsize=7)

    fig2.tight_layout()
    st.pyplot(fig2)

st.markdown("---")

# -- Row 2: Category performance + Sub-category leaders ------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("📦 Category breakdown: sales vs profit")
    cat_data = fdf.groupby("Category")[["Sales", "Profit"]].sum().reset_index()

    fig3, ax3 = plt.subplots(figsize=(6, 4))
    x = np.arange(len(cat_data))
    width = 0.35

    ax3.bar(x - width/2, cat_data["Sales"], width, label="Sales", color="#2C7DA0")
    ax3.bar(x + width/2, cat_data["Profit"], width, label="Profit", color="#E76F51")

    ax3.set_xticks(x)
    ax3.set_xticklabels(cat_data["Category"])
    style_axis(ax3, xlabel="Category", ylabel="Amount ($)")
    ax3.legend(fontsize=9)
    fig3.tight_layout()
    st.pyplot(fig3)

with col4:
    st.subheader("🏆 Top sub-categories (by sales)")
    subcat_sales = (fdf.groupby("Sub-Category")["Sales"]
                     .sum().sort_values(ascending=False).head(10))

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    ax4.barh(subcat_sales.index[::-1], subcat_sales.values[::-1], color="#2C7DA0")
    style_axis(ax4, xlabel="Total Sales ($)", ylabel="Sub-category")

    for i, v in enumerate(subcat_sales.values[::-1]):
        ax4.text(v + 500, i, f"${v:,.0f}", va='center', fontsize=8)

    fig4.tight_layout()
    st.pyplot(fig4)

st.markdown("---")

# -- Row 3: Segment + Discount analysis -------------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("👥 Sales share across customer segments")
    seg_data = fdf.groupby("Segment")["Sales"].sum()

    colors_pie = ["#2C7DA0", "#E76F51", "#2A9D8F"]
    fig5, ax5 = plt.subplots(figsize=(5, 4))

    wedges, texts, autotexts = ax5.pie(
        seg_data.values,
        labels=seg_data.index,
        autopct="%1.1f%%",
        colors=colors_pie[:len(seg_data)],
        startangle=90,
        pctdistance=0.75,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )

    for at in autotexts:
        at.set_fontsize(10)
        at.set_color('white')
        at.set_fontweight('bold')

    ax5.set_title("Sales distribution by segment", fontsize=12, fontweight='semibold')
    fig5.tight_layout()
    st.pyplot(fig5)

with col6:
    st.subheader("📉 Does discounting affect profit?")
    sample = fdf.sample(min(800, len(fdf)), random_state=42)

    fig6, ax6 = plt.subplots(figsize=(6, 4))
    sc = ax6.scatter(
        sample["Discount"], sample["Profit"],
        alpha=0.6, c=sample["Profit"], cmap="RdYlGn",
        edgecolors='black', linewidth=0.3, s=35
    )

    plt.colorbar(sc, ax=ax6, label="Profit ($)")
    ax6.axhline(y=0, color='red', linestyle='--', alpha=0.6, linewidth=1)

    z = np.polyfit(sample["Discount"], sample["Profit"], 1)
    p = np.poly1d(z)
    x_sorted = np.sort(sample["Discount"])
    ax6.plot(x_sorted, p(x_sorted), "b--", linewidth=1.5,
             label=f"Trend (slope = {z[0]:.0f})")

    style_axis(ax6, xlabel="Discount (%)", ylabel="Profit ($)")
    ax6.legend(fontsize=8)
    fig6.tight_layout()
    st.pyplot(fig6)

st.markdown("---")

# -- Row 4: Product spotlight -------------------------------------------
st.subheader("🏅 Product spotlight: best sellers & biggest disappointments")
col7, col8 = st.columns(2)

with col7:
    st.markdown("#### 💰 Best products by sales")
    top_products = (fdf.groupby("Product Name")["Sales"].sum()
                     .sort_values(ascending=False).head(10).reset_index())
    top_products.columns = ["Product", "Sales"]
    top_products["Sales"] = top_products["Sales"].apply(lambda x: f"${x:,.0f}")
    top_products.index = range(1, 11)
    st.dataframe(top_products, use_container_width=True, height=350)

with col8:
    st.markdown("#### ⚠️ Products with the lowest profit")
    bottom_profit = (fdf.groupby("Product Name")["Profit"].sum()
                      .sort_values().head(10).reset_index())
    bottom_profit.columns = ["Product", "Profit"]
    bottom_profit["Profit"] = bottom_profit["Profit"].apply(lambda x: f"${x:,.0f}")
    bottom_profit.index = range(1, 11)
    st.dataframe(bottom_profit, use_container_width=True, height=350)

st.markdown("---")

# -- Profit margin by region ---------------------------------------
st.subheader("📊 Profit margin by region (quick insight)")
region_margin = (fdf.groupby("Region")
                   .apply(lambda x: (x["Profit"].sum() / x["Sales"].sum()) * 100
                          if x["Sales"].sum() != 0 else 0)
                   .reset_index(name="Margin (%)")
                   .sort_values("Margin (%)", ascending=False))

fig7, ax7 = plt.subplots(figsize=(7, 3.5))
bars = ax7.bar(region_margin["Region"], region_margin["Margin (%)"], color="#2A9D8F")
ax7.axhline(y=0, color='red', linestyle='--', alpha=0.5)

style_axis(ax7, xlabel="Region", ylabel="Profit margin (%)")
for bar in bars:
    height = bar.get_height()
    ax7.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f"{height:.1f}%", ha='center', va='bottom', fontsize=9)

fig7.tight_layout()
st.pyplot(fig7)

st.markdown("---")

# -- Raw data expander ---------------------------------------------
with st.expander("🔍 See the filtered data table"):
    st.dataframe(
        fdf[["Order Date", "Customer Name", "Segment", "Region",
             "Category", "Sub-Category", "Product Name",
             "Sales", "Quantity", "Discount", "Profit"]]
        .reset_index(drop=True),
        use_container_width=True
    )

# -- Footer --------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#6c757d; font-size:12px;'>"
    "Built with Streamlit • Superstore dataset (Kaggle) • "
    "All charts update instantly when you apply filters."
    "</div>",
    unsafe_allow_html=True
)
