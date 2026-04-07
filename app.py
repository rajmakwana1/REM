import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="VIT Campus Energy Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("VIT Campus Energy Utility Dashboard")
st.markdown(
    "Interactive summary of campus energy consumption, savings potential, and reconciliation for key energy blocks."
)

# Load data
block_data = pd.read_csv("data/energy_consumption.csv")
initiative_data = pd.read_csv("data/energy_initiatives.csv")
recon_data = pd.read_csv("data/energy_reconciliation.csv")

# Sidebar controls
st.sidebar.header("Filters")
block_types = block_data["Block Type"].unique().tolist()
selected_types = st.sidebar.multiselect(
    "Select block types",
    block_types,
    default=block_types,
)

selected_blocks = st.sidebar.multiselect(
    "Select blocks",
    block_data["Block"].tolist(),
    default=block_data["Block"].tolist(),
)

filtered_blocks = block_data[
    (block_data["Block Type"].isin(selected_types))
    & (block_data["Block"].isin(selected_blocks))
]

if filtered_blocks.empty:
    st.warning("No blocks selected. Please choose at least one block from the sidebar.")
else:
    # KPI cards
    total_reported = 2592
    total_modeled = 2112
    total_gap = total_reported - total_modeled
    solar_savings = initiative_data.loc[initiative_data["Initiative"].str.contains("Rooftop Solar"), "Daily kWh Savings"].iloc[0]
    led_savings = initiative_data.loc[initiative_data["Initiative"].str.contains("LED"), "Daily kWh Savings"].iloc[0]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Reported Total (kWh/day)", f"{total_reported:,.0f}")
    kpi2.metric("Modeled Total (kWh/day)", f"{total_modeled:,.0f}")
    kpi3.metric("Reconciliation Gap (kWh/day)", f"{total_gap:,.0f}")
    kpi4.metric("Solar + LED Savings (kWh/day)", f"{solar_savings + led_savings:,.1f}")

    st.markdown("---")

    # Charts row 1
    col1, col2 = st.columns((2, 1))
    with col1:
        fig_blocks = px.bar(
            filtered_blocks,
            x="Block",
            y="Daily kWh",
            color="Block Type",
            title="Daily Energy Consumption by Block",
            text="Daily kWh",
            labels={"Daily kWh": "kWh/day"},
        )
        fig_blocks.update_traces(texttemplate="%{text:.0f}", textposition="outside")
        fig_blocks.update_layout(yaxis_title="Daily consumption (kWh)", xaxis_title="Block", uniformtext_minsize=8)
        st.plotly_chart(fig_blocks, width="stretch")

    with col2:
        fig_recon = go.Figure(
            go.Waterfall(
                name="Reconciliation",
                orientation="v",
                measure=recon_data["Measure"].tolist(),
                x=recon_data["Stage"].tolist(),
                y=recon_data["Amount"].tolist(),
                textposition="outside",
                text=[f"{v:+,.0f}" for v in recon_data["Amount"].tolist()],
                decreasing=dict(marker=dict(color="#d62728")),
                increasing=dict(marker=dict(color="#2ca02c")),
                totals=dict(marker=dict(color="#1f77b4")),
            )
        )
        fig_recon.update_layout(
            title="Reported vs Modeled Energy Reconciliation",
            yaxis_title="kWh/day",
        )
        st.plotly_chart(fig_recon, width="stretch")

    st.markdown("---")

    # Driver breakdown
    st.header("Driver Breakdown by Block")
    driver_cols = ["AC kWh", "Lighting kWh", "Equipment kWh", "Other kWh"]
    fig_stack = px.bar(
        filtered_blocks,
        x="Block",
        y=driver_cols,
        title="Load Drivers Across Blocks",
        labels={"value": "kWh/day", "variable": "Load Driver"},
    )
    fig_stack.update_layout(barmode="stack", xaxis_title="Block")
    st.plotly_chart(fig_stack, width="stretch")

    st.markdown("---")

    st.header("Energy Savings Initiatives")
    st.markdown(
        "The dataset includes two quantified measures (rooftop solar and LED replacement) and several further initiatives with zero estimates in the provided data."
    )
    st.dataframe(initiative_data.style.format({"Savings %": "{:.1f}%", "Daily kWh Savings": "{:.1f}"}))

    fig_initiatives = px.bar(
        initiative_data,
        x="Initiative",
        y="Daily kWh Savings",
        title="Potential Daily Savings by Initiative",
        labels={"Daily kWh Savings": "kWh/day"},
    )
    fig_initiatives.update_layout(xaxis_title=None, xaxis_tickangle=-45)
    st.plotly_chart(fig_initiatives, width="stretch")

    st.markdown("---")
    st.header("Report Notes")
    st.write(
        "- M Block uses the most energy at 752 kWh/day, roughly 2.3x a standard classroom block."
    )
    st.write("- Six classroom blocks have equal reported consumption at 328 kWh/day.")
    st.write("- Library is the low-end outlier with 200 kWh/day.")
    st.write(
        "- Solar and LED projects account for the only quantified estimate savings in the provided data."
    )
