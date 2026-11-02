"""
gui.py
------
The Tkinter desktop window. It only handles buttons and display;
calculations come from analysis.py and charts come from charts.py.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import analysis
import charts
import data_loader

# Path of the sample CSV that ships with the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FILE = os.path.join(BASE_DIR, "data", "sample_fitness_data.csv")


class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.df = None
        self.stat_vars = {}

        root.title("Fitness Performance Analytics System")
        root.geometry("1050x680")
        root.minsize(900, 600)

        self.build_header()
        self.build_statistics()
        self.build_tabs()

        # Load the sample data so the app is not empty at start
        self.load_file(SAMPLE_FILE)

    # ---------------- Layout ----------------
    def build_header(self):
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill="x")

        ttk.Label(header, text="Fitness Performance Analytics System",
                  font=("Segoe UI", 16, "bold")).pack(side="left")

        ttk.Button(header, text="Load Sample Data",
                   command=lambda: self.load_file(SAMPLE_FILE)).pack(side="right", padx=5)
        ttk.Button(header, text="Upload CSV",
                   command=self.upload_csv).pack(side="right", padx=5)

        self.file_label = ttk.Label(header, text="", foreground="gray")
        self.file_label.pack(side="right", padx=15)

    def build_statistics(self):
        box = ttk.LabelFrame(self.root, text="Summary Statistics", padding=10)
        box.pack(fill="x", padx=10, pady=5)

        names = ["Total Workouts", "Total Distance", "Average Distance",
                 "Average Duration", "Total Calories", "Average Calories",
                 "Avg Running Pace"]

        for index, name in enumerate(names):
            row, col = divmod(index, 4)
            cell = ttk.Frame(box, padding=5)
            cell.grid(row=row, column=col, padx=15, pady=3, sticky="w")

            ttk.Label(cell, text=name, foreground="gray").pack(anchor="w")
            var = tk.StringVar(value="-")
            ttk.Label(cell, textvariable=var,
                      font=("Segoe UI", 13, "bold")).pack(anchor="w")
            self.stat_vars[name] = var

    def build_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: data table
        self.table_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.table_tab, text="  Data Table  ")
        self.build_table()

        # Tabs 2-4: charts (each tab is an empty frame filled later)
        self.bar_tab = ttk.Frame(self.notebook)
        self.line_tab = ttk.Frame(self.notebook)
        self.pie_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.bar_tab, text="  Bar Chart  ")
        self.notebook.add(self.line_tab, text="  Progress Line Chart  ")
        self.notebook.add(self.pie_tab, text="  Activity Pie Chart  ")

    def build_table(self):
        columns = ("Date", "Activity", "Distance (km)", "Duration (min)",
                   "Calories", "Pace (min/km)")
        self.table = ttk.Treeview(self.table_tab, columns=columns,
                                  show="headings")
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=130, anchor="center")

        scrollbar = ttk.Scrollbar(self.table_tab, orient="vertical",
                                  command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ---------------- Actions ----------------
    def upload_csv(self):
        path = filedialog.askopenfilename(
            title="Select a fitness CSV file",
            filetypes=[("CSV files", "*.csv")])
        if path:
            self.load_file(path)

    def load_file(self, path):
        try:
            df = data_loader.load_data(path)
        except Exception as error:
            messagebox.showerror("Could not load file", str(error))
            return

        self.df = df
        self.file_label.config(text="File: " + os.path.basename(path))
        self.update_statistics()
        self.update_table()
        self.update_charts()

    # ---------------- Updating the screen ----------------
    def update_statistics(self):
        summary = analysis.get_summary(self.df)
        for name, value in summary.items():
            self.stat_vars[name].set(value)

    def update_table(self):
        self.table.delete(*self.table.get_children())
        data = analysis.add_pace(self.df)
        for _, row in data.iterrows():
            self.table.insert("", "end", values=(
                row["Date"].strftime("%Y-%m-%d"),
                row["Activity"],
                f"{row['Distance']:.1f}",
                f"{row['Duration']:.0f}",
                f"{row['Calories']:.0f}",
                analysis.format_pace(row["Pace"]),
            ))

    def update_charts(self):
        self.show_figure(self.bar_tab, charts.create_bar_chart(self.df))
        self.show_figure(self.line_tab, charts.create_line_chart(self.df))
        self.show_figure(self.pie_tab, charts.create_pie_chart(self.df))

    def show_figure(self, parent, figure):
        """Remove the old chart (if any) and draw the new one in 'parent'."""
        for widget in parent.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
