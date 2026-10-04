import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from analysis.insight_engine import InsightEngine

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller
        
        # Header
        header_frame = tk.Frame(self, bg="#f4f6f9")
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="Executive Dashboard & Overview", style="Header.TLabel").pack(side="left", anchor="w")

        # Load Real Data
        self.load_data()
        
        # --- KPI Cards ---
        self.render_kpis()

        # --- Charts & Alerts Area ---
        bottom_frame = tk.Frame(self, bg="#f4f6f9")
        bottom_frame.pack(fill="both", expand=True)

        # Matplotlib/Seaborn Chart
        chart_frame = tk.Frame(bottom_frame, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))
        ttk.Label(chart_frame, text="Recent 14-Day Revenue vs Waste Trend", font=("Segoe UI", 12, "bold"), background="white").pack(anchor="w", padx=12, pady=(10, 5))
        self.plot_trend_chart(chart_frame)

        # Alert Box
        alert_container = tk.Frame(bottom_frame, bg="white", width=340, highlightbackground="#e2e8f0", highlightthickness=1)
        alert_container.pack(side="right", fill="y")
        alert_container.pack_propagate(False)
        
        ttk.Label(alert_container, text="Actionable Intelligence Alerts", font=("Segoe UI", 12, "bold"), background="white").pack(anchor="w", padx=12, pady=(10, 5))
        
        self.render_alerts(alert_container)

    def load_data(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        sales_path = os.path.join(base_dir, "sales.csv")
        waste_path = os.path.join(base_dir, "waste.csv")
        purchases_path = os.path.join(base_dir, "purchases.csv")
        
        self.sales_df = pd.read_csv(sales_path) if os.path.exists(sales_path) else pd.DataFrame()
        self.waste_df = pd.read_csv(waste_path) if os.path.exists(waste_path) else pd.DataFrame()
        self.purchases_df = pd.read_csv(purchases_path) if os.path.exists(purchases_path) else pd.DataFrame()

    def render_kpis(self):
        kpi_frame = tk.Frame(self, bg="#f4f6f9")
        kpi_frame.pack(fill="x", pady=(0, 15))

        if not self.sales_df.empty:
            revenue = (self.sales_df["quantity_sold"] * self.sales_df["selling_price"]).sum()
            items_sold = self.sales_df["quantity_sold"].sum()
        else:
            revenue, items_sold = 0, 0

        waste_cost = self.waste_df["waste_cost"].sum() if not self.waste_df.empty else 0.0
        purchases_cost = self.purchases_df["total_cost"].sum() if not self.purchases_df.empty else 0.0
        waste_rate = (waste_cost / revenue * 100) if revenue > 0 else 0.0

        kpis = [
            ("Gross Sales Revenue", f"₹{revenue:,.0f}", "#16a34a", "sales.csv • Total earnings"),
            ("Procurement Spend", f"₹{purchases_cost:,.0f}", "#2563eb", "purchases.csv • Raw purchases"),
            ("Recorded Waste Loss", f"₹{waste_cost:,.0f}", "#dc2626", "waste.csv • Spoilage & scraps"),
            ("Waste / Sales Ratio", f"{waste_rate:.1f}%", "#d97706", "Efficiency metric"),
            ("Units Served", f"{items_sold:,}", "#7c3aed", "sales.csv • Total items")
        ]

        for title, value, color, subtitle in kpis:
            card = tk.Frame(kpi_frame, bg="white", padx=14, pady=10, relief="flat", highlightbackground="#e2e8f0", highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=(0, 8))
            tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w")
            tk.Label(card, text=value, font=("Segoe UI", 15, "bold"), bg="white", fg=color).pack(anchor="w", pady=(3, 1))
            tk.Label(card, text=subtitle, font=("Segoe UI", 8), bg="white", fg="#94a3b8").pack(anchor="w")

    def plot_trend_chart(self, parent):
        if self.sales_df.empty or self.waste_df.empty:
            tk.Label(parent, text="Insufficient data to render chart", bg="white").pack(pady=40)
            return

        # Prepare daily aggregates
        s_df = self.sales_df.copy()
        w_df = self.waste_df.copy()
        s_df["revenue"] = s_df["quantity_sold"] * s_df["selling_price"]

        daily_rev = s_df.groupby("date")["revenue"].sum().reset_index()
        daily_w = w_df.groupby("date")["waste_cost"].sum().reset_index()

        merged = pd.merge(daily_rev, daily_w, on="date", how="outer").fillna(0).sort_values("date")
        recent = merged.tail(14).copy()
        recent["short_date"] = pd.to_datetime(recent["date"]).dt.strftime("%d %b")

        fig = Figure(figsize=(6.5, 3.8), dpi=100)
        ax1 = fig.add_subplot(111)
        ax2 = ax1.twinx()

        sns.set_style("whitegrid")
        ax1.grid(color="#edf2f7", linestyle="--", linewidth=0.7)
        ax2.grid(False)

        # Bar chart for revenue
        bars = ax1.bar(recent["short_date"], recent["revenue"], color="#3b82f6", alpha=0.75, width=0.55, label="Revenue")
        # Line chart for waste
        line = ax2.plot(recent["short_date"], recent["waste_cost"], color="#ef4444", marker="o", linewidth=2.2, markersize=5, label="Waste Cost")

        ax1.set_ylabel("Revenue (Rs.)", color="#1e3a8a", fontsize=9, fontweight="bold")
        ax2.set_ylabel("Waste Cost (Rs.)", color="#991b1b", fontsize=9, fontweight="bold")
        ax1.tick_params(axis="x", rotation=40, labelsize=8)
        ax1.tick_params(axis="y", labelsize=8)
        ax2.tick_params(axis="y", labelsize=8)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(0, 8))

    def render_alerts(self, parent):
        try:
            engine = InsightEngine()
            alerts = engine.generate_insights()
        except Exception as e:
            alerts = [{"priority": "Info", "category": "System", "item": "Notice", "message": f"Alert engine ready. {e}", "action": "None"}]

        canvas = tk.Canvas(parent, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=320)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scrollbar.pack(side="right", fill="y")

        if not alerts:
            tk.Label(scrollable_frame, text="✅ All operations optimal. No alerts.", bg="white", font=("Segoe UI", 10), fg="#10b981").pack(anchor="w", padx=6, pady=10)
            return

        priority_colors = {
            "Critical": ("#fee2e2", "#b91c1c", "🔴"),
            "High": ("#ffedd5", "#c2410c", "🟠"),
            "Medium": ("#fef9c3", "#a16207", "🟡"),
            "Info": ("#e0f2fe", "#0369a1", "🔵")
        }

        for alert in alerts:
            bg_badge, fg_badge, icon = priority_colors.get(alert.get("priority", "Info"), ("#f1f5f9", "#334155", "ℹ️"))
            
            card = tk.Frame(scrollable_frame, bg="white", pady=6, padx=6, highlightbackground="#e2e8f0", highlightthickness=1)
            card.pack(fill="x", pady=4, padx=4)

            # Badge
            badge_frame = tk.Frame(card, bg=bg_badge, padx=6, pady=2)
            badge_frame.pack(anchor="w")
            tk.Label(badge_frame, text=f"{icon} {alert.get('priority', 'Info')} - {alert.get('category', '')}", 
                     bg=bg_badge, fg=fg_badge, font=("Segoe UI", 8, "bold")).pack()

            # Message
            tk.Label(card, text=alert.get("message", ""), font=("Segoe UI", 8), bg="white", fg="#1e293b",
                     wraplength=290, justify="left").pack(anchor="w", pady=(3, 2))
            
            # Recommendation
            tk.Label(card, text=f"Action: {alert.get('action', '')}", font=("Segoe UI", 8, "italic"), bg="white", fg="#64748b",
                     wraplength=290, justify="left").pack(anchor="w")