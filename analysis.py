"""
analysis.py
-----------
All calculations are here. Each function does one small job.
"""

import numpy as np


def total_distance(df):
    """Total distance covered (km)."""
    return float(np.sum(df["Distance"]))


def average_distance(df):
    """Average distance per workout (km)."""
    return float(np.mean(df["Distance"]))


def average_duration(df):
    """Average workout duration (minutes)."""
    return float(np.mean(df["Duration"]))


def total_calories(df):
    """Total calories burned."""
    return float(np.sum(df["Calories"]))


def average_calories(df):
    """Average calories burned per workout."""
    return float(np.mean(df["Calories"]))


def add_pace(df):
    """Add a 'Pace' column (minutes per km) for running workouts.

    Pace = Duration / Distance
    Non-running rows (or rows with 0 distance) get NaN.
    """
    result = df.copy()
    is_running = result["Activity"].str.lower() == "running"
    has_distance = result["Distance"] > 0

    # Replace 0 distance with NaN so we never divide by zero
    safe_distance = result["Distance"].replace(0, np.nan)
    pace = result["Duration"] / safe_distance

    result["Pace"] = np.where(is_running & has_distance, pace, np.nan)
    return result


def average_running_pace(df):
    """Average running pace in min/km, or None if there are no runs."""
    paced = add_pace(df)["Pace"].dropna()
    if paced.empty:
        return None
    return float(np.mean(paced))


def format_pace(pace):
    """Turn 7.5 into '7:30 min/km'."""
    if pace is None or np.isnan(pace):
        return "-"
    minutes = int(pace)
    seconds = int(round((pace - minutes) * 60))
    if seconds == 60:
        minutes += 1
        seconds = 0
    return f"{minutes}:{seconds:02d} min/km"


def get_summary(df):
    """Return all statistics together in one dictionary."""
    return {
        "Total Workouts": len(df),
        "Total Distance": f"{total_distance(df):.1f} km",
        "Average Distance": f"{average_distance(df):.2f} km",
        "Average Duration": f"{average_duration(df):.1f} min",
        "Total Calories": f"{total_calories(df):.0f} kcal",
        "Average Calories": f"{average_calories(df):.0f} kcal",
        "Avg Running Pace": format_pace(average_running_pace(df)),
    }
