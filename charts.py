"""
charts.py
---------
Each function builds one chart and returns a matplotlib Figure.
The Tkinter window (gui.py) then shows the Figure inside the app.
"""

import seaborn as sns
from matplotlib.figure import Figure

import analysis

sns.set_theme(style="whitegrid")


def create_bar_chart(df):
    """Bar chart: distance of each workout."""
    fig = Figure(figsize=(8, 4.5), dpi=100)
    ax = fig.add_subplot(111)

    labels = df["Date"].dt.strftime("%d %b")
    sns.barplot(x=labels, y=df["Distance"], color="#4C72B0", ax=ax)

    ax.set_title("Workout Distances")
    ax.set_xlabel("Date")
    ax.set_ylabel("Distance (km)")
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    return fig


def create_line_chart(df):
    """Line chart: running pace over time (lower pace = faster = progress).

    If the file has no running workouts, it shows calories burned instead.
    """
    fig = Figure(figsize=(8, 4.5), dpi=100)
    ax = fig.add_subplot(111)

    runs = analysis.add_pace(df).dropna(subset=["Pace"])

    if not runs.empty:
        sns.lineplot(x=runs["Date"], y=runs["Pace"], marker="o",
                     color="#4C72B0", ax=ax)
        ax.set_title("Running Pace Over Time (lower is faster)")
        ax.set_ylabel("Pace (min/km)")
    else:
        sns.lineplot(x=df["Date"], y=df["Calories"], marker="o",
                     color="#DD8452", ax=ax)
        ax.set_title("Calories Burned Over Time")
        ax.set_ylabel("Calories (kcal)")

    ax.set_xlabel("Date")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def create_pie_chart(df):
    """Pie chart: how many workouts of each activity type."""
    fig = Figure(figsize=(6, 4.5), dpi=100)
    ax = fig.add_subplot(111)

    counts = df["Activity"].value_counts()
    colors = sns.color_palette("pastel", len(counts))
    ax.pie(counts, labels=counts.index, autopct="%1.0f%%",
           startangle=90, colors=colors)
    ax.set_title("Workout Activity Types")
    ax.axis("equal")
    fig.tight_layout()
    return fig
