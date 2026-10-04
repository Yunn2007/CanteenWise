import tkinter as tk
from tkinter import ttk, messagebox
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from analysis.profit_analysis import ProfitAnalyzer
from analysis.reports import ReportGenerator

class ProfitFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller

        # Load Analytical Data
        self.load_data()

        # Header Bar
        self.build_header()

        # KPI Summary Cards
        self.cards_frame = tk.Frame(self, bg="#f4f6f9")
        self.cards_frame.pack(fill="x", pady=(0, 15))

        # Main Layout: Left = Profit Bar Chart, Right = Treeview Table
        content_panes = tk.Frame(self, bg="#f4f6f9")
        content_panes.pack(fill="both", expand=True)

        # Chart Container
        self.chart_container = tk.Frame(content_panes, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        self.chart_container.pack(side="left", fill="both", expand=False, padx=(0, 12))
        self.chart_container.configure(width=440)
        self.chart_container.pack_propagate(False)

        # Table Container
        table_container = tk.Frame(content_panes, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        table_container.pack(side="right", fill="both", expand=True)

        table_header = tk.Frame(table_container, bg="white", padx=12, pady=10)
        table_header.pack(fill="x")
        ttk.Label(table_header, text="Item-Level Profit & Margin Breakdown", font=("Segoe UI", 12, "bold"), background="white").pack(side="left")

        # Setup Table
        columns = ("name", "category", "units", "revenue", "cost", "waste", "profit", "margin")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)

        headers = [
            ("name", "Product Name", 150),
            ("category", "Category", 95),
            ("units", "Units", 70),
            ("revenue", "Revenue", 85),
            ("cost", "Ingr. Cost", 85),
            ("waste", "Waste Cost", 85),
            ("profit", "Net Profit (₹)", 95),
            ("margin", "Margin %", 80)
        ]
        for col_id, col_name, width in headers:
            self.tree.heading(col_id, text=col_name)
            self.tree.column(col_id, width=width, anchor="center" if col_id in ["units", "margin"] else "w")

        self.tree.tag_configure('high', background='#f0fdf4', foreground='#166534')
        self.tree.tag_configure('medium', background='#f8fafc', foreground='#1e293b')
        self.tree.tag_configure('low', background='#fef2f2', foreground='#991b1b')

        tree_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        tree_scroll.pack(side="right", fill="y", pady=(0, 10), padx=(0, 10))

        # Initial Render
        self.render_view()

    def load_data(self):
        try:
            analyzer = ProfitAnalyzer()
            self.profit_df = analyzer.calculate_item_profitability()
        except Exception as e:
            self.profit_df = pd.DataFrame()

    def build_header(self):
        header_bar = tk.Frame(self, bg="#f4f6f9")
        header_bar.pack(fill="x", pady=(0, 15))

        ttk.Label(header_bar, text="Profitability & Returns Analysis", style="Header.TLabel").pack(side="left", anchor="w")

        actions = tk.Frame(header_bar, bg="#f4f6f9")
        actions.pack(side="right")

        export_btn = tk.Button(actions, text="📄 Export Executive PDF", bg="#2563eb", fg="black", 
                               font=("Segoe UI", 9, "bold"), padx=12, pady=4, relief="groove",
                               command=self.export_pdf)
        export_btn.pack(side="left")

    def export_pdf(self):
        try:
            report_gen = ReportGenerator()
            output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "CanteenWise_Executive_Report.pdf"))
            pdf_file = report_gen.export_monthly_summary_pdf(output_path)
            messagebox.showinfo("Export Successful", f"Monthly Executive Financial Report successfully exported to:\n\n{pdf_file}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not generate PDF: {e}")

    def render_view(self):
        # 1. Render Cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if not self.profit_df.empty:
            total_net_profit = self.profit_df["net_profit"].sum()
            total_revenue = self.profit_df["total_revenue"].sum()
            overall_margin = (total_net_profit / total_revenue * 100) if total_revenue > 0 else 0.0
            top_earner = self.profit_df.iloc[0]["product_name"]
            highest_margin_row = self.profit_df.sort_values("profit_margin_pct", ascending=False).iloc[0]
            top_margin_item = f"{highest_margin_row['product_name']} ({highest_margin_row['profit_margin_pct']:.1f}%)"
        else:
            total_net_profit, total_revenue, overall_margin, top_earner, top_margin_item = 0, 0, 0, "N/A", "N/A"

        kpis = [
            ("Total Net Operating Profit", f"₹{total_net_profit:,.0f}", "#16a34a"),
            ("Net Profit Margin", f"{overall_margin:.1f}%", "#2563eb"),
            ("Top Net Profit Generator", str(top_earner), "#7c3aed"),
            ("Highest Margin Item", str(top_margin_item), "#d97706")
        ]

        for title, val, col in kpis:
            c = tk.Frame(self.cards_frame, bg="white", padx=16, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
            c.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(c, text=title, font=("Segoe UI", 9, "bold"), bg="white", fg="#64748b").pack(anchor="w")
            tk.Label(c, text=val, font=("Segoe UI", 15, "bold"), bg="white", fg=col).pack(anchor="w", pady=(3, 0))

        # 2. Render Chart
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        ttk.Label(self.chart_container, text="Top Net Profit Contributors (₹)", font=("Segoe UI", 11, "bold"), background="white").pack(anchor="w", padx=12, pady=(10, 5))

        if not self.profit_df.empty:
            top_items = self.profit_df.head(7).iloc[::-1]
            fig = Figure(figsize=(4.4, 3.8), dpi=100)
            ax = fig.add_subplot(111)

            colors_bar = ["#10b981" if p > 0 else "#ef4444" for p in top_items["net_profit"]]
            ax.barh(top_items["product_name"], top_items["net_profit"], color=colors_bar, height=0.6)
            ax.set_xlabel("Net Profit (Rs.)", fontsize=9, fontweight="bold")
            ax.tick_params(axis="y", labelsize=8)
            ax.tick_params(axis="x", labelsize=8)
            ax.grid(axis="x", linestyle="--", alpha=0.5)

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
        else:
            tk.Label(self.chart_container, text="No profit data available", bg="white").pack(pady=40)

        # 3. Populate Table
        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, row in self.profit_df.iterrows():
            margin = row["profit_margin_pct"]
            tag = "high" if margin >= 50 else ("low" if margin < 20 or row["net_profit"] < 0 else "medium")

            self.tree.insert("", "end", values=(
                row["product_name"],
                row["category"],
                f"{int(row['total_units_sold']):,}",
                f"₹{row['total_revenue']:,.0f}",
                f"₹{row['total_ingredient_cost']:,.0f}",
                f"₹{row['total_waste_cost']:,.0f}",
                f"₹{row['net_profit']:,.0f}",
                f"{margin:.1f}%"
            ), tags=(tag,))