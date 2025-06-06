import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---- Config ----
st.set_page_config(page_title="Sector Index Dashboard", layout="wide")
DATA_PATH = os.path.join("output", "sector_indices.csv")

# ---- Load Data Safely ----
try:
    df = pd.read_csv(DATA_PATH, parse_dates=["DATE"])
    df.sort_values("DATE", inplace=True)
except FileNotFoundError:
    st.error(f"❌ File not found: {DATA_PATH}")
    st.stop()
except Exception as e:
    st.error(f"❌ Failed to read file: {e}")
    st.stop()

# ---- Identify Columns ----
index_columns = [col for col in df.columns if col != "DATE"]

# ---- Header ----
st.title("📊 Sector Indices Dashboard")
min_date = df["DATE"].min().date()
max_date = df["DATE"].max().date()
st.markdown(f"**Date Range:** {min_date} to {max_date}")

# ---- Main Combined Chart ----
fig_all = px.line(df, x="DATE", y=index_columns,
                  title="All Sector Indices (Pre-normalized)")

fig_all.update_layout(
    xaxis=dict(
        rangeslider=dict(visible=True),
        fixedrange=True,
        type="date"
    ),
    hovermode="x unified"
)
fig_all.update_traces(mode="lines+markers", hoverinfo="all", hovertemplate=None)
st.plotly_chart(fig_all, use_container_width=True, key="main_chart")

# ---- Individual Sector Charts: 13 Rows × 3 Columns ----
st.markdown("### 📈 Individual Sector Trends")

max_charts = 39
selected_sectors = index_columns[:max_charts]

cols_per_row = 3
rows = 13

for i in range(0, len(selected_sectors), cols_per_row):
    cols = st.columns(cols_per_row)
    for j in range(cols_per_row):
        idx = i + j
        if idx < len(selected_sectors):
            sec = selected_sectors[idx]
            with cols[j]:
                fig = px.line(df, x="DATE", y=sec, title=sec)
                fig.update_layout(
                    xaxis=dict(
                        rangeslider=dict(visible=True),
                        fixedrange=True,
                        type="date"
                    ),
                    hovermode="x unified"
                )
                fig.update_traces(mode="lines+markers", hoverinfo="all", hovertemplate=None)
                st.plotly_chart(fig, use_container_width=True, key=f"chart_{sec}")
