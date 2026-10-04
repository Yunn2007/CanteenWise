import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        
        ttk.Label(self, text="Today's Overview", style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        
        # --- KPI Cards ---
        kpi_frame = tk.Frame(self, bg="#f4f6f9")
        kpi_frame.pack(fill="x", pady=(0, 20))
        
        kpis = [("Revenue", "₹45,200", "#27ae60"), 
                ("Items Sold", "412", "#2980b9"), 
                ("Waste Cost", "₹3,100", "#e74c3c"), 
                ("Waste Rate %", "6.8%", "#f39c12")]
                
        for title, value, color in kpis:
            card = tk.Frame(kpi_frame, bg="white", padx=20, pady=15, relief="flat", highlightbackground="#ddd", highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(card, text=title, font=("Segoe UI", 10), bg="white", fg="#7f8c8d").pack(anchor="w")
            tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), bg="white", fg=color).pack(anchor="w", pady=(5,0))

        # --- Charts & Alerts Area ---
        bottom_frame = tk.Frame(self, bg="#f4f6f9")
        bottom_frame.pack(fill="both", expand=True)

        # Matplotlib/Seaborn Chart
        chart_frame = tk.Frame(bottom_frame, bg="white", highlightbackground="#ddd", highlightthickness=1)
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ttk.Label(chart_frame, text="Weekly Revenue vs Waste Trend", font=("Segoe UI", 12, "bold"), background="white").pack(anchor="w", padx=10, pady=10)
        self.plot_trend_chart(chart_frame)

        # Alert Box
        alert_frame = tk.Frame(bottom_frame, bg="white", width=300, highlightbackground="#ddd", highlightthickness=1)
        alert_frame.pack(side="right", fill="y")
        alert_frame.pack_propagate(False)
        ttk.Label(alert_frame, text="Real-Time Alerts", font=("Segoe UI", 12, "bold"), background="white").pack(anchor="w", padx=10, pady=10)
        
        alerts = ["🔴 Tomato stock critically low!", "🟡 Milk expiring in 1 day", "🟢 Chicken stock replenished"]
        for alert in alerts:
            tk.Label(alert_frame, text=alert, bg="white", font=("Segoe UI", 10), anchor="w").pack(fill="x", padx=10, pady=5)

    def plot_trend_chart(self, parent):
        # Mock Data
        data = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Revenue": [40000, 42000, 38000, 45000, 51000, 32000, 28000],
            "Waste": [3000, 3200, 4000, 3100, 2500, 5000, 4800]
        })

        fig = Figure(figsize=(6, 4), dpi=100)
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        sns.set_style("whitegrid")
        sns.barplot(data=data, x="Day", y="Revenue", ax=ax1, color="#3498db", alpha=0.7, label="Revenue")
        sns.lineplot(data=data, x="Day", y="Waste", ax=ax2, color="#e74c3c", marker="o", linewidth=2, label="Waste Cost")

        ax1.set_ylabel("Revenue (₹)")
        ax2.set_ylabel("Waste Cost (₹)")
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)