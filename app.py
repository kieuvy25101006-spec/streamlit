import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# CONFIG

st.set_page_config(
    page_title="Business Dashboard",
    layout="wide"
)

st.title("📊 Business Dashboard")


# LOAD DATA


file = "viz_data.xlsx"

trend = pd.read_excel(file, sheet_name="Trend")
comparative = pd.read_excel(file, sheet_name="Comparative")
visual = pd.read_excel(file, sheet_name="VisualEncoding")


# KPI


total_revenue = trend["Revenue"].sum()
total_cost = trend["Cost"].sum()
total_profit = (trend["Revenue"] - trend["Cost"]).sum()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Revenue",
    f"{total_revenue:,.0f}"
)

col2.metric(
    "Cost",
    f"{total_cost:,.0f}"
)

col3.metric(
    "Profit",
    f"{total_profit:,.0f}"
)


# TREND ANALYSIS


st.header("Trend Analysis")

profit = trend["Revenue"] - trend["Cost"]

col1, col2 = st.columns(2)

with col1:

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=trend["Month"],
            y=trend["Revenue"],
            mode="lines+markers",
            name="Revenue"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend["Month"],
            y=trend["Cost"],
            mode="lines+markers",
            name="Cost"
        )
    )

    fig.update_layout(
        title="Revenue vs Cost"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig2 = px.area(
        x=trend["Month"],
        y=profit,
        title="Profit Trend"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# COMPARATIVE ANALYSIS


st.header("Comparative Analysis")

comparative["Total Sales"] = comparative[
    ["Q1", "Q2", "Q3", "Q4"]
].sum(axis=1)

col1, col2 = st.columns(2)

with col1:

    fig3 = px.bar(
        comparative,
        x="Region",
        y="Total Sales",
        title="Sales by Region"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col2:

    quarter_sales = [
        comparative["Q1"].sum(),
        comparative["Q2"].sum(),
        comparative["Q3"].sum(),
        comparative["Q4"].sum()
    ]

    pie_df = pd.DataFrame({
        "Quarter": ["Q1", "Q2", "Q3", "Q4"],
        "Sales": quarter_sales
    })

    fig4 = px.pie(
        pie_df,
        names="Quarter",
        values="Sales",
        title="Quarter Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )


# VISUAL ENCODING

st.header("Visual Encoding")

fig5 = px.scatter(
    visual,
    x="MarketingSpend",
    y="UnitsSold",
    size="Price",
    color="Rating",
    symbol="Category",
    hover_name="Category",
    title="Marketing Spend vs Units Sold"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


# RAW DATA


with st.expander("View Raw Data"):

    st.subheader("Trend")
    st.dataframe(trend)

    st.subheader("Comparative")
    st.dataframe(comparative)

    st.subheader("Visual Encoding")
    st.dataframe(visual)