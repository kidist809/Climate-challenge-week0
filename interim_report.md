# B9W0: African Climate Trend Analysis — Interim Report

**Name:** Kidist  
**GitHub Repository:** https://github.com/kidist809/Climate-challenge-week0  
**Submission Date:** April 26, 2026  

---

## Task 1: Git & Environment Setup — Summary

### Repository Initialization
A GitHub repository named `climate-challenge-week0` was created and cloned locally. The project follows the required folder structure:

```
climate-challenge-week0/
├── .github/workflows/ci.yml
├── .gitignore
├── requirements.txt
├── README.md
├── scripts/
│   └── main.py
├── notebooks/
├── tests/
└── src/
```

### Branching & Commits
A branch named `setup-task` was created from `main`. The following commits were made following Conventional Commits conventions:

1. `init: add .gitignore` — excludes `data/`, `*.csv`, `__pycache__/`, and virtual environment folders
2. `chore: add requirements.txt and README` — documents all dependencies and environment setup instructions
3. `ci: add GitHub Actions workflow and project structure` — sets up CI and folder scaffolding

The branch was merged into `main` via a Pull Request on GitHub.

### CI/CD
A GitHub Actions workflow (`.github/workflows/ci.yml`) was configured to run `pip install -r requirements.txt` on every push to `main` and `setup-task`, ensuring the environment is reproducible.

### Dependencies (`requirements.txt`)
```
pandas
numpy
matplotlib
scipy
seaborn
jupyter
```

### Environment Reproduction
To reproduce the environment locally:
```bash
git clone https://github.com/kidist809/Climate-challenge-week0.git
cd climate-challenge-week0
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

---

## Task 2: Data Profiling, Cleaning & EDA — Approach Outline

### Dataset
- **Source:** NASA POWER MERRA-2 satellite-derived reanalysis data
- **Countries:** Ethiopia, Kenya, Sudan, Tanzania, Nigeria
- **Period:** January 1, 2015 – March 31, 2026
- **Frequency:** Daily observations (~4,100 rows per country)
- **Representative locations:** Capital city coordinates for each country

### Approach

#### 1. Data Loading & Date Parsing
Each country's CSV is loaded separately into its own notebook (`ethiopia_eda.ipynb`, etc.). A `Country` column is added, and the `YEAR` and `DOY` columns are combined into a proper `Date` column using `pd.to_datetime(df['YEAR'] * 1000 + df['DOY'], format='%Y%j')`. A `Month` column is extracted for seasonal analysis.

#### 2. Missing Value Handling
All occurrences of `-999` (NASA POWER's sentinel value for missing data) are replaced with `NaN` before any statistics are computed. Missing value percentages are reported per column, and any column exceeding 5% nulls is flagged and documented.

#### 3. Duplicate Detection
`df.duplicated().sum()` is run on each dataset. Any duplicate rows found are dropped and the count is documented in a markdown cell.

#### 4. Summary Statistics
`df.describe()` is run on all numeric columns. Results are interpreted in a markdown cell covering temperature ranges, precipitation variability, humidity levels, and pressure patterns specific to each country's climate.

#### 5. Outlier Detection
Z-scores are computed for `T2M`, `T2M_MAX`, `T2M_MIN`, `PRECTOTCORR`, `RH2M`, `WS2M`, and `WS2M_MAX`. Rows where `|Z| > 3` are flagged and counted. **Decision: outliers are retained** because they represent genuine extreme weather events (heat spikes, heavy rainfall) that are critical for the vulnerability analysis in Task 3.

#### 6. Cleaning
Missing values in climate columns are forward-filled using `df.ffill()`. Rows where more than 30% of values remain missing are dropped. Each cleaned dataset is exported to `data/<country>_clean.csv` (excluded from GitHub via `.gitignore`).

#### 7. Planned Visualizations
- Monthly average T2M line chart (warmest/coolest months annotated)
- Monthly total PRECTOTCORR bar chart (peak rainy season annotated)
- Correlation heatmap across all numeric columns
- Scatter plots: T2M vs RH2M; T2M_RANGE vs WS2M
- PRECTOTCORR histogram (log scale)
- Bubble chart: T2M vs RH2M, bubble size = PRECTOTCORR

### Current Status
All 5 country EDA notebooks have been created, executed, and pushed to the `eda-ethiopia` branch on GitHub. Cleaned CSVs have been generated locally for all 5 countries and are ready for Task 3 cross-country comparison.

---

*Report prepared for the 10 Academy B9W0 African Climate Trend Analysis Challenge.*
