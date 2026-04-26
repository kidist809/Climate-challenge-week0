# =========================
# STEP 1: IMPORT LIBRARIES
# =========================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# STEP 2: LOAD ALL CSV FILES
# =========================
df_eth = pd.read_csv("ethiopia (1).csv")
df_ken = pd.read_csv("kenya (1).csv")
df_sud = pd.read_csv("sudan.csv")
df_tan = pd.read_csv("tanzania.csv")
df_nga = pd.read_csv("nigeria.csv")

# =========================
# STEP 3: ADD COUNTRY COLUMN
# =========================
df_eth["Country"] = "Ethiopia"
df_ken["Country"] = "Kenya"
df_sud["Country"] = "Sudan"
df_tan["Country"] = "Tanzania"
df_nga["Country"] = "Nigeria"

# =========================
# STEP 4: COMBINE ALL DATA
# =========================
df = pd.concat([df_eth, df_ken, df_sud, df_tan, df_nga], ignore_index=True)

# =========================
# STEP 5: CLEAN MISSING VALUES
# =========================
df.replace(-999, np.nan, inplace=True)

# Optional check
print("\nMissing values per column:")
print(df.isna().sum())

# =========================
# STEP 6: CREATE DATE COLUMN
# =========================
df["Date"] = pd.to_datetime(
    df["YEAR"].astype(str),
    format="%Y"
) + pd.to_timedelta(df["DOY"] - 1, unit="D")

# Sort data properly
df = df.sort_values(["Country", "Date"])

# =========================
# FINAL CHECK
# =========================
print("\nFinal dataset preview:")
print(df.head())

print("\nDataset shape:")
print(df.shape)
# =========================
# STEP 7: DATA PROFILING
# =========================
print("\nSummary Statistics:")
print(df.describe())

print("\nDuplicate rows:", df.duplicated().sum())
df.drop_duplicates(inplace=True)

# =========================
# STEP 8: OUTLIER DETECTION (Z-SCORE)
# =========================
from scipy import stats

climate_cols = ["T2M", "T2M_MAX", "T2M_MIN", "T2M_RANGE", "PRECTOTCORR", "RH2M", "WS2M", "WS2M_MAX", "PS", "QV2M"]

z_scores = df[climate_cols].apply(lambda col: np.abs(stats.zscore(col.dropna())))
outlier_counts = (z_scores > 3).sum()
print("\nOutlier counts per column (Z-score > 3):")
print(outlier_counts)

# =========================
# STEP 9: COUNTRY COMPARISON — ALL COLUMNS
# =========================
fig, axes = plt.subplots(2, 5, figsize=(22, 8))
axes = axes.flatten()

for i, col in enumerate(climate_cols):
    country_avg = df.groupby("Country")[col].mean().sort_values()
    country_avg.plot(kind="bar", ax=axes[i])
    axes[i].set_title(f"Avg {col} by Country")
    axes[i].set_xlabel("Country")
    axes[i].set_ylabel(col)
    axes[i].tick_params(axis="x", rotation=45)

plt.suptitle("Average Climate Variables by Country (2015-2026)", fontsize=14)
plt.tight_layout()
plt.show()

# =========================
# STEP 10: YEARLY TREND — ALL COLUMNS
# =========================
fig, axes = plt.subplots(2, 5, figsize=(22, 8))
axes = axes.flatten()

for i, col in enumerate(climate_cols):
    for country in df["Country"].unique():
        country_data = df[df["Country"] == country]
        yearly_avg = country_data.groupby(country_data["Date"].dt.year)[col].mean()
        axes[i].plot(yearly_avg.index, yearly_avg.values, marker="o", label=country)
    axes[i].set_title(f"Yearly {col} Trend")
    axes[i].set_xlabel("Year")
    axes[i].set_ylabel(col)

axes[0].legend(fontsize=7)
plt.suptitle("Yearly Climate Trends by Country (2015-2026)", fontsize=14)
plt.tight_layout()
plt.show()