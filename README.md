# Fitness Performance Analytics System

A simple college-level Python project that loads fitness data from a CSV file,
calculates statistics, draws charts, and shows everything in a Tkinter window.

## Features
- Load data from a CSV file (sample data included)
- Total distance, average distance, average workout duration, calories
- Running pace in minutes per kilometre
- Bar chart (workout distances), line chart (running pace over time), pie chart (activity types)
- Simple Tkinter interface with an **Upload CSV** button

## Folder Structure
```
Fitness_Performance_Analytics_System/
├── main.py              # starts the app
├── gui.py               # Tkinter window
├── data_loader.py       # reads and cleans the CSV (Pandas)
├── analysis.py          # calculations (NumPy / Pandas)
├── charts.py            # bar, line and pie charts (Matplotlib / Seaborn)
├── requirements.txt     # libraries to install
├── README.md
└── data/
    └── sample_fitness_data.csv
```

## CSV Format
Columns: `Date, Activity, Distance, Duration, Calories`
- Date: `YYYY-MM-DD`
- Distance in km, Duration in minutes, Calories in kcal

## Run (Windows + VS Code)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
