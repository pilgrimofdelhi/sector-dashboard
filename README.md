# 📊 Sector Indices Dashboard

An interactive and visually rich dashboard built with **Streamlit** and **Plotly** to analyze, compare, and monitor the performance of various sector indices over time.

---

## 🔧 Features

- **Interactive Time Series Charts**
  - Select sectors and date ranges dynamically
  - Apply optional **normalization** and **moving averages**
  - Choose from multiple **chart themes** (Dark, White, Seaborn, etc.)

- **Sector Group Filters**
  - Predefined groupings (e.g., Banking, Tech, Healthcare) for easy selection
  - Multiselect support to compare any combination of sectors

- **Statistical Summary**
  - Calculates key metrics: **Start/End values**, **CAGR**, **Average**, **Volatility**
  - Highlights **Top Movers** by CAGR

- **Correlation Analysis**
  - Displays a correlation heatmap to analyze inter-sector relationships

- **Export Capability**
  - Download filtered dataset as a CSV for further analysis

- **Custom Styling Options**
  - Toggle bold color palettes and chart themes

---

## 📁 Data Format

The dashboard expects a CSV file named `sector_indices.csv` with the following structure:

| DATE       | Private Banks | PSU Banks | NBFCs | IT Services | ... |
|------------|----------------|-----------|-------|-------------|-----|
| 2024-01-01 | 1120.5         | 980.4     | 1230.3| 1340.2      | ... |
| 2024-01-02 | 1130.0         | 985.0     | 1245.8| 1355.0      | ... |

- `DATE` must be a valid date column
- Each sector column should contain numeric index values

---

## ▶️ Getting Started

1. **Install dependencies**

```bash
pip install -r requirements.txt
