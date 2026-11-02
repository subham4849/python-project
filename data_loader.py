"""
data_loader.py
--------------
Loads the fitness CSV file and cleans it using Pandas.
"""

import pandas as pd

# Columns that every fitness CSV must contain
REQUIRED_COLUMNS = ["Date", "Activity", "Distance", "Duration", "Calories"]


def load_data(file_path):
    """Read a CSV file and return a clean DataFrame.

    Raises ValueError with a friendly message if the file is not valid.
    """
    df = pd.read_csv(file_path)

    # Remove accidental spaces in column names, e.g. " Date" -> "Date"
    df.columns = df.columns.str.strip()

    # Check that all required columns are present
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError("The CSV file is missing these columns: " + ", ".join(missing))

    # Keep only the columns we need
    df = df[REQUIRED_COLUMNS].copy()

    # Convert data types (bad values become NaN / NaT)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Activity"] = df["Activity"].astype(str).str.strip().str.title()
    for column in ["Distance", "Duration", "Calories"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Drop rows with missing or invalid values
    df = df.dropna()

    if df.empty:
        raise ValueError("The CSV file has no valid rows.")

    # Sort by date so the line chart goes from oldest to newest
    df = df.sort_values("Date").reset_index(drop=True)
    return df
