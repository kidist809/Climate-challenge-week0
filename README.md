# Climate Challenge Week 0

African Climate Trend Analysis using NASA POWER MERRA-2 data for Ethiopia, Kenya, Sudan, Tanzania, and Nigeria (2015–2026).

## Reproduce the Environment

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/climate-challenge-week0.git
cd climate-challenge-week0
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add data files
Place the country CSV files inside a `data/` folder (excluded from Git via `.gitignore`):
```
data/
├── ethiopia (1).csv
├── kenya (1).csv
├── sudan.csv
├── tanzania.csv
└── nigeria.csv
```

### 5. Run the script
```bash
python scripts/main.py
```

## Project Structure
```
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

## Data Source
NASA POWER MERRA-2 — https://power.larc.nasa.gov/data-access-viewer/
