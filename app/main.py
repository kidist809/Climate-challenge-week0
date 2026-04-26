import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import (
    COUNTRIES, CLIMATE_VARS, VAR_LABELS,
    load_clean_data, filter_years, monthly_avg, yearly_avg, summary_table
)

st.set_page_config(page_title="African Climate Dashboard", layout="wide")

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.title("🌍 Filters")

selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=COUNTRIES,
    default=COUNTRIES
)

year_range = st.sidebar.slider(
    "Year Range",
    min_value=2015,
    max_value=2026,
    value=(2015, 2026)
)

selected_var = st.sidebar.selectbox(
    "Climate Variable",
    options=CLIMATE_VARS,
    format_func=lambda x: VAR_LABELS[x]
)

# ── Load Data ─────────────────────────────────────────────────────────────────
if not selected_countries:
    st.warning("Please select at least one country.")
    st.stop()

df_all = load_clean_data(selected_countries)

if df_all.empty:
    st.error("No cleaned data found. Please run the EDA notebooks first to generate the cleaned CSVs in the data/ folder.")
    st.stop()

df = filter_years(df_all, year_range)

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("🌦️ African Climate Trend Analysis (2015–2026)")
st.markdown("NASA POWER MERRA-2 Daily Climate Data — Ethiopia, Kenya, Sudan, Tanzania, Nigeria")

# ── Row 1: KPI Cards ──────────────────────────────────────────────────────────
st.subheader("📊 Summary Statistics")
summary = summary_table(df, selected_var)
cols = st.columns(len(selected_countries))
for i, country in enumerate(selected_countries):
    if country in summary.index:
        cols[i].metric(
            label=country,
            value=f"{summary.loc[country, 'Mean']:.1f}",
            delta=f"Std: {summary.loc[country, 'Std']:.1f}"
        )

# ── Row 2: Temperature Trend Line Chart ───────────────────────────────────────
st.subheader(f"📈 Monthly {VAR_LABELS[selected_var]} Trend")

monthly = monthly_avg(df, selected_var)

fig, ax = plt.subplots(figsize=(14, 5))
for country in selected_countries:
    cdf = monthly[monthly["Country"] == country]
    ax.plot(cdf["Date"], cdf[selected_var], label=country, linewidth=1.5)
ax.set_xlabel("Date")
ax.set_ylabel(VAR_LABELS[selected_var])
ax.legend(fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig)
plt.close()

# ── Row 3: Yearly Average Bar Chart ───────────────────────────────────────────
st.subheader(f"📅 Yearly Average {VAR_LABELS[selected_var]}")

yearly = yearly_avg(df, selected_var)

fig2, ax2 = plt.subplots(figsize=(14, 5))
for country in selected_countries:
    cdf = yearly[yearly["Country"] == country]
    ax2.plot(cdf["Year"], cdf[selected_var], marker="o", label=country, linewidth=1.5)
ax2.set_xlabel("Year")
ax2.set_ylabel(VAR_LABELS[selected_var])
ax2.legend(fontsize=9)
ax2.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig2)
plt.close()

# ── Row 4: Precipitation Boxplot ──────────────────────────────────────────────
st.subheader("🌧️ Precipitation Distribution by Country")

fig3, ax3 = plt.subplots(figsize=(10, 5))
data_to_plot = [df[df["Country"] == c]["PRECTOTCORR"].dropna().values for c in selected_countries]
ax3.boxplot(data_to_plot, labels=selected_countries, patch_artist=True,
            boxprops=dict(facecolor="steelblue", alpha=0.6))
ax3.set_xlabel("Country")
ax3.set_ylabel("PRECTOTCORR (mm/day)")
ax3.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig3)
plt.close()

# ── Row 5: Summary Table ──────────────────────────────────────────────────────
st.subheader(f"📋 {VAR_LABELS[selected_var]} — Summary Table")
st.dataframe(summary.style.format("{:.2f}"), use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("Data source: [NASA POWER MERRA-2](https://power.larc.nasa.gov/) | Built for COP32 Climate Analysis")
