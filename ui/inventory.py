import tkinter as tk
from tkinter import ttk
import os
import pandas as pd

class InventoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller

        # Current active tab: 'stock' or 'purchases'
        self.current_view = "stock"

        # Load Data
        self.load_data()

        # Header Bar & Filter Controls
        self.build_header()

        # KPI Summary Cards
        self.cards_frame = tk.Frame(self, bg="#f4f6f9")
        self.cards_frame.pack(fill="x", pady=(0, 12))

        # Main Table Container
        self.table_container = tk.Frame(self, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        self.table_container.pack(fill="both", expand=True)

        self.tree = None
        self.tree_scroll = None

        # Initial populate
        self.render_active_view()

    def load_data(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        inv_path = os.path.join(base_dir, "inventory.csv")
        ing_path = os.path.join(base_dir, "ingredients.csv")
        pur_path = os.path.join(base_dir, "purchases.csv")

        # 1. Load Inventory & Ingredients
        if os.path.exists(inv_path) and os.path.exists(ing_path):
            inv_df = pd.read_csv(inv_path)
            self.ing_df = pd.read_csv(ing_path)

            latest_inv = inv_df.sort_values("date").groupby("ingredient_id").last().reset_index()
            merged = latest_inv.merge(self.ing_df, on="ingredient_id", how="inner")
            merged["stock_value"] = merged["closing_stock"] * merged["purchase_cost"]
            self.stock_df = merged
        else:
            self.stock_df = pd.DataFrame()
            self.ing_df = pd.DataFrame()

        # 2. Load Purchases
        if os.path.exists(pur_path) and not self.ing_df.empty:
            pur_df = pd.read_csv(pur_path)
            self.purchases_df = pur_df.merge(
                self.ing_df[["ingredient_id", "ingredient_name", "unit"]], 
                on="ingredient_id", 
                how="left"
            )
        else:
            self.purchases_df = pd.DataFrame()

    def build_header(self):
        header_bar = tk.Frame(self, bg="#f4f6f9")
        header_bar.pack(fill="x", pady=(0, 12))

        ttk.Label(header_bar, text="Pantry Inventory & Procurement (data/inventory.csv & purchases.csv)", style="Header.TLabel").pack(side="left", anchor="w")

        controls = tk.Frame(header_bar, bg="#f4f6f9")
        controls.pack(side="right")

        # View Switcher Toggle
        self.stock_btn = tk.Button(controls, text="📦 Live Stock Ledger", bg="#2563eb", fg="black", font=("Segoe UI", 9, "bold"), padx=10, pady=4, relief="groove", command=lambda: self.switch_view("stock"))
        self.stock_btn.pack(side="left", padx=(0, 6))

        self.pur_btn = tk.Button(controls, text="🚚 Purchases Log", bg="#e2e8f0", fg="#0f172a", font=("Segoe UI", 9), padx=10, pady=4, relief="groove", command=lambda: self.switch_view("purchases"))
        self.pur_btn.pack(side="left", padx=(0, 14))

        # Search Box
        tk.Label(controls, text="Search:", bg="#f4f6f9", font=("Segoe UI", 9, "bold"), fg="#0f172a").pack(side="left", padx=(0, 4))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.render_active_view())
        search_entry = ttk.Entry(controls, textvariable=self.search_var, width=14)
        search_entry.pack(side="left", padx=(0, 10))

        # Refresh Button
        refresh_btn = ttk.Button(controls, text="↻ Refresh", command=self.refresh_data)
        refresh_btn.pack(side="left")

    def switch_view(self, view_name):
        self.current_view = view_name
        if view_name == "stock":
            self.stock_btn.configure(bg="#2563eb", fg="black", font=("Segoe UI", 9, "bold"))
            self.pur_btn.configure(bg="#e2e8f0", fg="#0f172a", font=("Segoe UI", 9))
        else:
            self.stock_btn.configure(bg="#e2e8f0", fg="#0f172a", font=("Segoe UI", 9))
            self.pur_btn.configure(bg="#2563eb", fg="black", font=("Segoe UI", 9, "bold"))
        self.render_active_view()

    def refresh_data(self):
        self.load_data()
        self.render_active_view()

    def render_active_view(self):
        # Clear existing table widgets
        for widget in self.table_container.winfo_children():
            widget.destroy()

        # Clear KPI cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if self.current_view == "stock":
            self.render_stock_view()
        else:
            self.render_purchases_view()

    def render_stock_view(self):
        if self.stock_df.empty:
            return

        filtered = self.stock_df.copy()
        search_text = self.search_var.get().strip().lower()
        if search_text:
            filtered = filtered[filtered["ingredient_name"].str.lower().str.contains(search_text)]

        # Tags & Status
        status_list, tags_list = [], []
        for _, row in filtered.iterrows():
            stock = row["closing_stock"]
            reorder = row["reorder_level"]
            if stock <= (reorder * 0.5):
                status_list.append("🔴 Critical Low")
                tags_list.append("critical")
            elif stock <= reorder:
                status_list.append("🟡 Low Stock")
                tags_list.append("low")
            else:
                status_list.append("🟢 Adequate")
                tags_list.append("ok")

        filtered["status_label"] = status_list
        filtered["status_tag"] = tags_list

        # KPIs
        total_items = len(self.stock_df)
        total_value = self.stock_df["stock_value"].sum()
        critical_count = sum(self.stock_df["closing_stock"] <= (self.stock_df["reorder_level"] * 0.5))
        low_count = sum((self.stock_df["closing_stock"] > (self.stock_df["reorder_level"] * 0.5)) & 
                        (self.stock_df["closing_stock"] <= self.stock_df["reorder_level"]))

        kpis = [
            ("Tracked Raw Ingredients", f"{total_items}", "#2c3e50"),
            ("Total Stock Valuation", f"₹{total_value:,.0f}", "#27ae60"),
            ("Low Stock Items", f"{low_count}", "#f39c12"),
            ("Critical Low Items", f"{critical_count}", "#e74c3c")
        ]
        for title, val, col in kpis:
            c = tk.Frame(self.cards_frame, bg="white", padx=16, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
            c.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(c, text=title, font=("Segoe UI", 9, "bold"), bg="white", fg="#64748b").pack(anchor="w")
            tk.Label(c, text=val, font=("Segoe UI", 15, "bold"), bg="white", fg=col).pack(anchor="w", pady=(3, 0))

        # Table
        columns = ("id", "name", "stock", "unit", "reorder", "cost", "value", "status")
        tree = ttk.Treeview(self.table_container, columns=columns, show="headings", height=16)

        headers = [
            ("id", "Item ID", 90),
            ("name", "Ingredient Name", 180),
            ("stock", "Current Stock", 110),
            ("unit", "Unit", 70),
            ("reorder", "Reorder Level", 110),
            ("cost", "Unit Cost", 95),
            ("value", "Stock Value (₹)", 120),
            ("status", "Status", 140)
        ]
        for col_id, col_name, width in headers:
            tree.heading(col_id, text=col_name)
            tree.column(col_id, width=width, anchor="center" if col_id in ["id", "unit", "stock", "reorder"] else "w")

        tree.tag_configure('ok', background='#f0fdf4', foreground='#166534')
        tree.tag_configure('low', background='#fffbeb', foreground='#92400e')
        tree.tag_configure('critical', background='#fef2f2', foreground='#991b1b')

        scroll = ttk.Scrollbar(self.table_container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scroll.pack(side="right", fill="y", pady=10, padx=(0, 10))

        for _, row in filtered.iterrows():
            tree.insert("", "end", values=(
                row["ingredient_id"],
                row["ingredient_name"],
                f"{row['closing_stock']:.2f}",
                row["unit"],
                f"{row['reorder_level']:.1f}",
                f"₹{row['purchase_cost']:.1f}",
                f"₹{row['stock_value']:,.1f}",
                row["status_label"]
            ), tags=(row["status_tag"],))

    def render_purchases_view(self):
        if self.purchases_df.empty:
            tk.Label(self.table_container, text="No purchases found in data/purchases.csv", bg="white").pack(pady=40)
            return

        filtered = self.purchases_df.copy()
        search_text = self.search_var.get().strip().lower()
        if search_text:
            filtered = filtered[
                filtered["ingredient_name"].astype(str).str.lower().str.contains(search_text) |
                filtered["supplier"].astype(str).str.lower().str.contains(search_text) |
                filtered["purchase_id"].astype(str).str.lower().str.contains(search_text)
            ]

        # KPIs
        total_spent = self.purchases_df["total_cost"].sum()
        total_orders = len(self.purchases_df)
        top_supplier = self.purchases_df.groupby("supplier")["total_cost"].sum().idxmax()
        top_supplier_spend = self.purchases_df.groupby("supplier")["total_cost"].sum().max()

        kpis = [
            ("Total Procurement Spend", f"₹{total_spent:,.0f}", "#2563eb"),
            ("Purchase Orders Logged", f"{total_orders:,}", "#2c3e50"),
            ("Primary Vendor", str(top_supplier), "#7c3aed"),
            ("Vendor Spend", f"₹{top_supplier_spend:,.0f}", "#059669")
        ]
        for title, val, col in kpis:
            c = tk.Frame(self.cards_frame, bg="white", padx=16, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
            c.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(c, text=title, font=("Segoe UI", 9, "bold"), bg="white", fg="#64748b").pack(anchor="w")
            tk.Label(c, text=val, font=("Segoe UI", 14, "bold"), bg="white", fg=col).pack(anchor="w", pady=(3, 0))

        # Table
        columns = ("pur_id", "date", "supplier", "ingredient", "quantity", "unit", "total_cost")
        tree = ttk.Treeview(self.table_container, columns=columns, show="headings", height=16)

        headers = [
            ("pur_id", "PO #", 90),
            ("date", "Date", 95),
            ("supplier", "Vendor / Supplier", 220),
            ("ingredient", "Raw Material", 160),
            ("quantity", "Quantity", 90),
            ("unit", "Unit", 70),
            ("total_cost", "Total Cost (₹)", 110)
        ]
        for col_id, col_name, width in headers:
            tree.heading(col_id, text=col_name)
            tree.column(col_id, width=width, anchor="center" if col_id in ["pur_id", "date", "unit", "quantity"] else "w")

        scroll = ttk.Scrollbar(self.table_container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scroll.pack(side="right", fill="y", pady=10, padx=(0, 10))

        # Display latest 250 rows
        for _, row in filtered.tail(250).iloc[::-1].iterrows():
            tree.insert("", "end", values=(
                row["purchase_id"],
                row["date"],
                row["supplier"],
                row["ingredient_name"],
                f"{row['quantity']:.2f}",
                row["unit"],
                f"₹{row['total_cost']:,.2f}"
            ))