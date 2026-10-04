import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SalesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller

        # Load Data
        self.load_data()

        # Top Header & Filters
        self.build_header()

        # Summary KPI Cards
        self.cards_frame = tk.Frame(self, bg="#f4f6f9")
        self.cards_frame.pack(fill="x", pady=(0, 15))

        # Main Content Layout: Left = Chart, Right = Transactions Treeview
        content_panes = tk.Frame(self, bg="#f4f6f9")
        content_panes.pack(fill="both", expand=True)

        # Chart Container
        self.chart_container = tk.Frame(content_panes, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        self.chart_container.pack(side="left", fill="both", expand=False, padx=(0, 12))
        self.chart_container.configure(width=420)
        self.chart_container.pack_propagate(False)

        # Treeview Container
        table_container = tk.Frame(content_panes, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        table_container.pack(side="right", fill="both", expand=True)

        table_header = tk.Frame(table_container, bg="white", padx=12, pady=10)
        table_header.pack(fill="x")
        ttk.Label(table_header, text="Sales Transactions Log", font=("Segoe UI", 12, "bold"), background="white").pack(side="left")
        self.record_count_label = tk.Label(table_header, text="", font=("Segoe UI", 9), bg="white", fg="#64748b")
        self.record_count_label.pack(side="right")

        # Setup Table
        columns = ("date", "meal_period", "product_name", "category", "quantity_sold", "selling_price", "total")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)
        
        headers = [
            ("date", "Date", 90),
            ("meal_period", "Meal Period", 95),
            ("product_name", "Product", 140),
            ("category", "Category", 95),
            ("quantity_sold", "Qty Sold", 70),
            ("selling_price", "Unit Price", 80),
            ("total", "Total (₹)", 90)
        ]
        for col_id, col_name, width in headers:
            self.tree.heading(col_id, text=col_name)
            self.tree.column(col_id, width=width, anchor="center" if col_id in ["date", "meal_period", "quantity_sold"] else "w")

        tree_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        tree_scroll.pack(side="right", fill="y", pady=(0, 10), padx=(0, 10))

        # Initial Render
        self.update_view()

    def load_data(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        sales_path = os.path.join(base_dir, "sales.csv")
        products_path = os.path.join(base_dir, "products.csv")

        if os.path.exists(sales_path) and os.path.exists(products_path):
            sales_df = pd.read_csv(sales_path)
            products_df = pd.read_csv(products_path)
            self.df = sales_df.merge(products_df[["product_id", "product_name", "category"]], on="product_id", how="left")
            self.df["total_amount"] = self.df["quantity_sold"] * self.df["selling_price"]
        else:
            self.df = pd.DataFrame()

    def build_header(self):
        header_bar = tk.Frame(self, bg="#f4f6f9")
        header_bar.pack(fill="x", pady=(0, 15))

        ttk.Label(header_bar, text="Sales & Order Analytics", style="Header.TLabel").pack(side="left", anchor="w")

        # Filters frame
        filter_frame = tk.Frame(header_bar, bg="#f4f6f9")
        filter_frame.pack(side="right")

        tk.Label(filter_frame, text="Category:", bg="#f4f6f9", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(10, 4))
        categories = ["All Categories"]
        if not self.df.empty and "category" in self.df.columns:
            categories.extend(sorted(self.df["category"].dropna().unique().tolist()))
        self.cat_var = tk.StringVar(value="All Categories")
        cat_combo = ttk.Combobox(filter_frame, textvariable=self.cat_var, values=categories, state="readonly", width=14)
        cat_combo.pack(side="left", padx=(0, 10))
        cat_combo.bind("<<ComboboxSelected>>", lambda e: self.update_view())

        tk.Label(filter_frame, text="Meal Period:", bg="#f4f6f9", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(10, 4))
        periods = ["All Periods", "Morning", "Lunch", "Evening", "Dinner"]
        self.period_var = tk.StringVar(value="All Periods")
        period_combo = ttk.Combobox(filter_frame, textvariable=self.period_var, values=periods, state="readonly", width=12)
        period_combo.pack(side="left")
        period_combo.bind("<<ComboboxSelected>>", lambda e: self.update_view())

    def update_view(self):
        # 1. Filter dataset
        filtered = self.df.copy()
        if not filtered.empty:
            cat_val = self.cat_var.get()
            if cat_val != "All Categories":
                filtered = filtered[filtered["category"] == cat_val]

            period_val = self.period_var.get()
            if period_val != "All Periods":
                filtered = filtered[filtered["meal_period"] == period_val]

        # 2. Render Cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if not filtered.empty:
            tot_rev = filtered["total_amount"].sum()
            tot_units = filtered["quantity_sold"].sum()
            avg_price = filtered["total_amount"].sum() / filtered["quantity_sold"].sum() if tot_units > 0 else 0
            top_item = filtered.groupby("product_name")["total_amount"].sum().idxmax()
        else:
            tot_rev, tot_units, avg_price, top_item = 0, 0, 0, "N/A"

        kpis = [
            ("Filtered Revenue", f"₹{tot_rev:,.0f}", "#27ae60"),
            ("Units Sold", f"{tot_units:,}", "#2980b9"),
            ("Avg Item Revenue", f"₹{avg_price:.1f}", "#8e44ad"),
            ("Top Selling Product", str(top_item), "#d35400")
        ]
        for title, val, col in kpis:
            c = tk.Frame(self.cards_frame, bg="white", padx=16, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
            c.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(c, text=title, font=("Segoe UI", 9, "bold"), bg="white", fg="#64748b").pack(anchor="w")
            tk.Label(c, text=val, font=("Segoe UI", 15, "bold"), bg="white", fg=col).pack(anchor="w", pady=(3, 0))

        # 3. Render Chart
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        ttk.Label(self.chart_container, text="Sales by Category (Gross ₹)", font=("Segoe UI", 11, "bold"), background="white").pack(anchor="w", padx=12, pady=(10, 5))

        if not filtered.empty:
            cat_summary = filtered.groupby("category")["total_amount"].sum().reset_index()
            fig = Figure(figsize=(4.2, 3.8), dpi=100)
            ax = fig.add_subplot(111)
            
            colors_list = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899"]
            wedges, texts, autotexts = ax.pie(
                cat_summary["total_amount"], 
                labels=cat_summary["category"], 
                autopct="%1.1f%%",
                startangle=140,
                colors=colors_list[:len(cat_summary)],
                textprops={'fontsize': 8}
            )
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_weight('bold')

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
        else:
            tk.Label(self.chart_container, text="No sales data for selection", bg="white").pack(pady=40)

        # 4. Render Table (limit to last 200 rows for high responsiveness)
        for item in self.tree.get_children():
            self.tree.delete(item)

        sample = filtered.tail(200).iloc[::-1]
        self.record_count_label.config(text=f"Showing latest {len(sample)} of {len(filtered):,} records")

        for _, row in sample.iterrows():
            self.tree.insert("", "end", values=(
                row["date"],
                row["meal_period"],
                row["product_name"],
                row["category"],
                f"{row['quantity_sold']}",
                f"₹{row['selling_price']:.1f}",
                f"₹{row['total_amount']:,.1f}"
            ))