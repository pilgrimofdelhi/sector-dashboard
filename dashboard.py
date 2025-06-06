import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# ---- Config ----
st.set_page_config(page_title="Sector Index Dashboard", layout="wide")
DATA_PATH = os.path.join("output", "sector_indices.csv")

# ---- Load Data ----
df = pd.read_csv(DATA_PATH, parse_dates=["DATE"])
df.sort_values("DATE", inplace=True)

# ---- Predefined Sector Groupings ----
sector_groups = {
    "Banking": ["Private Banks", "PSU Banks", "NBFCs"],
    "Tech": ["IT Services", "Midcap IT", "Fintech"],
    "Healthcare": ["Pharma", "Diagnostics", "Hospitals", "Animal Health"],
    "Industrials": ["Capital Goods", "Construction", "Railways", "Defence"],
    "Consumer": ["FMCG", "Consumer Durables", "Paints", "QSR"],
    "Energy": ["Renewable Energy", "Green Energy"],
    "Others": ["Real Estate", "Telecom", "Cement", "Logistics", "Insurance"]
}

all_grouped_sectors = sum(sector_groups.values(), [])
available_sectors = [col for col in df.columns if col != "DATE"]

# ---- Sidebar Controls ----
st.sidebar.header("🔍 Controls")

group_choice = st.sidebar.selectbox("Filter by Group", ["All"] + list(sector_groups.keys()))
if group_choice == "All":
    sector_pool = available_sectors
else:
    sector_pool = [s for s in sector_groups[group_choice] if s in available_sectors]

selected_sectors = st.sidebar.multiselect("Select Sectors", sector_pool, default=sector_pool[:5])

min_date = df["DATE"].min().to_pydatetime()
max_date = df["DATE"].max().to_pydatetime()
date_range = st.sidebar.slider("Date Range", min_value=min_date, max_value=max_date,
                               value=(min_date, max_date))

normalize_toggle = st.sidebar.checkbox("Normalize to 100", value=True)
ma_toggle = st.sidebar.checkbox("Apply Moving Average", value=True)
ma_window = st.sidebar.slider("MA Window (days)", 3, 60, 14)

# Themes and palettes
plotly_templates = {
    "Default": "plotly",
    "White": "plotly_white",
    "Dark": "plotly_dark",
    "GGPlot2": "ggplot2",
    "Seaborn": "seaborn"
}
theme_name = st.sidebar.selectbox("Chart Theme", list(plotly_templates.keys()), index=1)
theme = plotly_templates.get(theme_name, "plotly")
custom_color_scale = st.sidebar.checkbox("Use Custom Color Palette")
custom_palette = px.colors.qualitative.Bold if custom_color_scale else None

# ---- Filter Data ----
df_filtered = df[(df["DATE"] >= pd.to_datetime(date_range[0])) &
                 (df["DATE"] <= pd.to_datetime(date_range[1]))].copy()

# ---- Normalize to 100 ----
if normalize_toggle:
    for sec in selected_sectors:
        base = df_filtered[sec].iloc[0]
        if base > 0:
            df_filtered[sec] = df_filtered[sec] / base * 100

# ---- Main Chart ----
st.title("📊 Sector Indices Dashboard")
st.caption("Compare performance, volatility, and trends across sectors.")

plot_df = df_filtered[["DATE"] + selected_sectors].copy()

if ma_toggle:
    for sec in selected_sectors:
        plot_df[f"{sec} (MA)"] = plot_df[sec].rolling(window=ma_window).mean()

plot_columns = [col for col in plot_df.columns if col != "DATE"]

fig = px.line(plot_df, x="DATE", y=plot_columns,
              title="Sector Index Trends",
              template=theme,
              color_discrete_sequence=custom_palette)

st.plotly_chart(fig, use_container_width=True)

# ---- Sector Stats ----
st.subheader("📈 Sector Summary Statistics")
stat_rows = []
for sec in selected_sectors:
    series = df_filtered[sec]
    start, end = series.iloc[0], series.iloc[-1]
    avg = series.mean()
    days = (df_filtered["DATE"].iloc[-1] - df_filtered["DATE"].iloc[0]).days
    cagr = ((end / start) ** (365 / days) - 1) * 100 if start > 0 and days > 0 else np.nan
    daily_returns = series.pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252) * 100  # annualized
    stat_rows.append({
        "Sector": sec,
        "Start": f"{start:.2f}",
        "End": f"{end:.2f}",
        "Average": f"{avg:.2f}",
        "CAGR": cagr,
        "Volatility": volatility
    })

stat_df = pd.DataFrame(stat_rows)
stat_df_display = stat_df.copy()
stat_df_display["CAGR %"] = stat_df_display["CAGR"].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "N/A")
stat_df_display["Volatility %"] = stat_df_display["Volatility"].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "N/A")
st.dataframe(stat_df_display.drop(columns=["CAGR", "Volatility"]))

# ---- Top Movers ----
st.subheader("🚀 Top Movers")
top_cagr = stat_df.sort_values("CAGR", ascending=False)
st.write("Top Sectors by CAGR:", top_cagr[["Sector", "CAGR"]].head(5))

# ---- Correlation Heatmap ----
if len(selected_sectors) >= 2:
    st.subheader("🧠 Correlation Heatmap")
    corr_data = df_filtered[selected_sectors].corr()
    fig_corr = px.imshow(corr_data, text_auto=".2f", color_continuous_scale="RdBu_r",
                         title="Sector Correlation Matrix", aspect="auto")
    st.plotly_chart(fig_corr, use_container_width=True)

# ---- Download ----
download_df = df_filtered[["DATE"] + selected_sectors]
st.download_button("📥 Download Filtered Data", data=download_df.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_sector_data.csv", mime="text/csv")

# ---- Help / Tooltips ----
with st.expander("❓ Help / Info"):
    st.markdown("""
    - **Normalize to 100**: Re-bases all selected sectors to 100 at the start of the selected date range for comparison.
    - **Moving Average**: Smooths the time series using a rolling mean over selected window size.
    - **Chart Theme**: Changes the background and style of the plot.
    - **Custom Colors**: Uses bold color palette for better distinction.
    - **Top Movers**: Shows sectors with highest CAGR over the selected range.
    - **Correlation Heatmap**: Shows how sectors move together.
    - **Download Data**: Save filtered results as CSV.
    - **Sector Grouping**: Use predefined sector categories for simpler filtering and comparison.
    """)
