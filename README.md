# 📊 Superstore Sales Intelligence Dashboard

> **Business Analytics · Streamlit · Python · Interactive Data Visualization**

[![Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-Streamlit-FF4B4B?logo=streamlit)](https://superstoresalesdashboardforyou.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Project Overview

An interactive business intelligence dashboard built with Streamlit to analyze 4 years of retail sales data from a US superstore. The dashboard covers sales performance, profit trends, regional breakdowns, category analysis, and product-level insights — all updating instantly with sidebar filters.

**Core objective:** Surface actionable business insights from raw transactional data — identifying which regions, categories, and products drive revenue and which ones drain profit.

---

## 🚀 Live Demo

**[→ Open Dashboard](https://superstoresalesdashboardforyou.streamlit.app/)**

Use the sidebar filters to explore by Region, Category, Customer Segment, and Year. Every chart updates instantly.

---

## 📊 Dashboard Sections

| Section | What it shows |
|---------|--------------|
| **KPI Cards** | Total sales, profit, margin %, orders, customers, avg order value |
| **Monthly Trend** | Sales vs profit over time — dual-axis line chart |
| **Regional Performance** | Sales & profit by region — grouped bar chart |
| **Category Breakdown** | Sales vs profit across Furniture, Office Supplies, Technology |
| **Top Sub-Categories** | Top 10 sub-categories by total sales |
| **Segment Analysis** | Revenue share across Consumer, Corporate, Home Office |
| **Discount Impact** | Scatter plot with trend line — does discounting hurt profit? |
| **Product Spotlight** | Top 10 sellers + bottom 10 by profit |
| **Profit Margin by Region** | Which region is most efficient |
| **Raw Data Table** | Filtered data explorer |

---

## 💡 Key Business Insights

- **West region** leads in total sales; **Central** has the lowest profit margin
- **Technology** category drives the highest profit despite lower sales volume than Furniture
- **Higher discounts strongly correlate with negative profit** — trend line shows clear downward slope
- **Consumer segment** accounts for the majority of revenue (~50%)
- Several high-selling products appear in the bottom-profit list — indicating over-discounting

---

## 🏗️ How It Works

```
Sample_-_Superstore.csv
        │
        ▼
  load_data() — cached with @st.cache_data
  (parse dates, create Month/Year columns)
        │
        ▼
  Sidebar filters applied
  (Region, Category, Segment, Year)
        │
        ▼
  All charts re-render on filtered dataframe
  (matplotlib figures embedded via st.pyplot)
        │
        ▼
  Live dashboard at streamlit.app
```

---

## 📁 Repository Structure

```
Superstore_sales_dashboard/
│
├── main.py                     # Streamlit dashboard — all charts and logic
├── Sample_-_Superstore.csv     # Dataset (9,994 orders, 21 columns)
├── requirements.txt            # Python dependencies
├── .gitignore
└── LICENSE
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/Dushdeva/Superstore_sales_dashboard.git
cd Superstore_sales_dashboard
pip install -r requirements.txt
streamlit run main.py
```

Opens at **http://localhost:8501**

---

## 📦 Dataset

| Property | Value |
|----------|-------|
| Source | [Kaggle — Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) |
| Records | 9,994 orders |
| Columns | 21 (Order ID, Date, Region, Category, Sales, Profit, Discount...) |
| Period | 2014 – 2017 |
| Geography | United States |

---

## 🔮 Identified Improvements

- [ ] **Sales forecasting** — add ARIMA or Prophet model to predict next quarter revenue
- [ ] **Customer segmentation** — K-Means clustering on RFM (Recency, Frequency, Monetary) features
- [ ] **State-level map** — choropleth map showing sales density by US state
- [ ] **Export button** — download filtered data as CSV directly from dashboard

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Dashboard framework | Streamlit |
| Data manipulation | Pandas, NumPy |
| Visualization | Matplotlib |
| Deployment | Streamlit Cloud (free) |
| Dataset | Kaggle Superstore |

---

*Built by [Devang Yadav](https://github.com/Dushdeva)*
