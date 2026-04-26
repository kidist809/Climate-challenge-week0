import pandas as pd
import numpy as np
import os

COUNTRIES = ["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"]

FILE_MAP = {
    "Ethiopia": "ethiopia (1).csv",
    "Kenya": "kenya (1).csv",
    "Sudan": "sudan.csv",
    "Tanzania": "tanzania.csv",
    "Nigeria": "nigeria.csv",
}

CLEAN_FILE_MAP = {
    "Ethiopia": "ethiopia_clean.csv",
    "Kenya": "kenya_clean.csv",
    "Sudan": "sudan_clean.csv",
    "Tanzania": "tanzania_clean.csv",
    "Nigeria": "nigeria_clean.csv",
}

CLIMATE_VARS = ["T2M", "T2M_MAX", "T2M_MIN", "T2M_RANGE", "PRECTOTCORR", "RH2M", "WS2M", "WS2M_MAX", "PS", "QV2M"]

VAR_LABELS = {
    "T2M": "Mean Temperature (°C)",
    "T2M_MAX": "Max Temperature (°C)",
    "T2M_MIN": "Min Temperature (°C)",
    "T2M_RANGE": "Temperature Range (°C)",
    "PRECTOTCORR": "Precipitation (mm/day)",
    "RH2M": "Relative Humidity (%)",
    "WS2M": "Wind Speed (m/s)",
    "WS2M_MAX": "Max Wind Speed (m/s)",
    "PS": "Surface Pressure (kPa)",
    "QV2M": "Specific Humidity (g/kg)",
}


def get_data_dir():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "data")


def load_clean_data(countries):
    data_dir = get_data_dir()
    dfs = []
    for country in countries:
        path = os.path.join(data_dir, CLEAN_FILE_MAP[country])
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=["Date"])
            dfs.append(df)
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    return df


def filter_years(df, year_range):
    return df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]


def monthly_avg(df, variable):
    return (
        df.groupby(["Country", "Year", "Month"])[variable]
        .mean()
        .reset_index()
        .assign(Date=lambda x: pd.to_datetime(x[["Year", "Month"]].assign(day=1)))
        .sort_values("Date")
    )


def yearly_avg(df, variable):
    return df.groupby(["Country", "Year"])[variable].mean().reset_index()


def summary_table(df, variable):
    return df.groupby("Country")[variable].agg(
        Mean="mean", Median="median", Std="std"
    ).round(2)
