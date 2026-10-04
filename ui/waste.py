import tkinter as tk
from tkinter import ttk
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class WasteFrame(tk.Frame):
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

        # Main Content Layout: Left = Chart, Right = Treeview
        content_panes = tk.Frame(self, bg="#f4f6f9")
        content_panes.pack(fill="both", expand=True)

        # Chart Container
        self.chart_container = tk.Frame(content_panes, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        self.chart_container.pack(side="left", fill="both", expand=False, padx=(0, 12))
        self.chart_container.configure(width=420)
        self.chart_container.pack_propagate(False)

        # Table Container
        table_container = tk.Frame(content_panes, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        table_container.pack(side="right", fill="both", expand=True)

        table_header = tk.Frame(table_container, bg="white", padx=12, pady=10)
        table_header.pack(fill="x")
        ttk.Label(table_header, text="Food & Raw Material Waste Log", font=("Segoe UI", 12, "bold"), background="white").pack(side="left")
        self.record_count_label = tk.Label(table_header, text="", font=("Segoe UI", 9), bg="white", fg="#64748b")
        self.record_count_label.pack(side="right")

        # Setup Table
        columns = ("date", "waste_type", "item_name", "quantity", "unit", "reason", "cost")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=15)

        headers = [
            ("date", "Date", 90),
            ("waste_type", "Waste Type", 110),
            ("item_name", "Item Name", 140),
            ("quantity", "Quantity", 75),
            ("unit", "Unit", 65),
            ("reason", "Reason", 95),
            ("cost", "Loss Cost (₹)", 95)
        ]
        for col_id, col_name, width in headers:
            self.tree.heading(col_id, text=col_name)
            self.tree.column(col_id, width=width, anchor="center" if col_id in ["date", "quantity", "unit"] else "w")

        tree_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(0, 10))
        tree_scroll.pack(side="right", fill="y", pady=(0, 10), padx=(0, 10))

        # Initial Render
        self.update_view()

    def load_data(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        waste_path = os.path.join(base_dir, "waste.csv")
        products_path = os.path.join(base_dir, "products.csv")
        ingredients_path = os.path.join(base_dir, "ingredients.csv")

        if os.path.exists(waste_path):
            self.df = pd.read_csv(waste_path)
            
            # Map item names
            p_map = {}
            if os.path.exists(products_path):
                p_df = pd.read_csv(products_path)
                p_map = dict(zip(p_df["product_id"], p_df["product_name"]))
            
            ing_map = {}
            if os.path.exists(ingredients_path):
                ing_df = pd.read_csv(ingredients_path)
                ing_map = dict(zip(ing_df["ingredient_id"], ing_df["ingredient_name"]))

            self.df["item_name"] = self.df["item_id"].apply(lambda x: p_map.get(x, ing_map.get(x, x)))
        else:
            self.df = pd.DataFrame()

    def build_header(self):
        header_bar = tk.Frame(self, bg="#f4f6f9")
        header_bar.pack(fill="x", pady=(0, 15))

        ttk.Label(header_bar, text="Food Waste & Loss Tracking", style="Header.TLabel").pack(side="left", anchor="w")

        filter_frame = tk.Frame(header_bar, bg="#f4f6f9")
        filter_frame.pack(side="right")

        tk.Label(filter_frame, text="Type:", bg="#f4f6f9", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(10, 4))
        types = ["All Types"]
        if not self.df.empty and "waste_type" in self.df.columns:
            types.extend(sorted(self.df["waste_type"].dropna().unique().tolist()))
        self.type_var = tk.StringVar(value="All Types")
        type_combo = ttk.Combobox(filter_frame, textvariable=self.type_var, values=types, state="readonly", width=14)
        type_combo.pack(side="left", padx=(0, 10))
        type_combo.bind("<<ComboboxSelected>>", lambda e: self.update_view())

        tk.Label(filter_frame, text="Reason:", bg="#f4f6f9", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(10, 4))
        reasons = ["All Reasons"]
        if not self.df.empty and "reason" in self.df.columns:
            reasons.extend(sorted(self.df["reason"].dropna().unique().tolist()))
        self.reason_var = tk.StringVar(value="All Reasons")
        reason_combo = ttk.Combobox(filter_frame, textvariable=self.reason_var, values=reasons, state="readonly", width=12)
        reason_combo.pack(side="left")
        reason_combo.bind("<<ComboboxSelected>>", lambda e: self.update_view())

    def update_view(self):
        filtered = self.df.copy()
        if not filtered.empty:
            type_val = self.type_var.get()
            if type_val != "All Types":
                filtered = filtered[filtered["waste_type"] == type_val]

            reason_val = self.reason_var.get()
            if reason_val != "All Reasons":
                filtered = filtered[filtered["reason"] == reason_val]

        # 2. Render Cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        if not filtered.empty:
            tot_cost = filtered["waste_cost"].sum()
            prep_cost = filtered[filtered["waste_type"] == "Prepared Food"]["waste_cost"].sum()
            raw_cost = filtered[filtered["waste_type"] == "Raw Material"]["waste_cost"].sum()
            incidents = len(filtered)
        else:
            tot_cost, prep_cost, raw_cost, incidents = 0, 0, 0, 0

        kpis = [
            ("Total Waste Cost", f"₹{tot_cost:,.0f}", "#e74c3c"),
            ("Prepared Food Loss", f"₹{prep_cost:,.0f}", "#d35400"),
            ("Raw Material Spoilage", f"₹{raw_cost:,.0f}", "#8e44ad"),
            ("Waste Incidents Logged", f"{incidents:,}", "#2c3e50")
        ]
        for title, val, col in kpis:
            c = tk.Frame(self.cards_frame, bg="white", padx=16, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
            c.pack(side="left", fill="both", expand=True, padx=(0, 10))
            tk.Label(c, text=title, font=("Segoe UI", 9, "bold"), bg="white", fg="#64748b").pack(anchor="w")
            tk.Label(c, text=val, font=("Segoe UI", 15, "bold"), bg="white", fg=col).pack(anchor="w", pady=(3, 0))

        # 3. Render Chart
        for widget in self.chart_container.winfo_children():
            widget.destroy()

        ttk.Label(self.chart_container, text="Waste Cost by Reason (₹)", font=("Segoe UI", 11, "bold"), background="white").pack(anchor="w", padx=12, pady=(10, 5))

        if not filtered.empty:
            reason_summary = filtered.groupby("reason")["waste_cost"].sum().reset_index().sort_values("waste_cost", ascending=False)
            fig = Figure(figsize=(4.2, 3.8), dpi=100)
            ax = fig.add_subplot(111)

            colors_bar = ["#ef4444", "#f97316", "#eab308", "#8b5cf6"]
            ax.bar(reason_summary["reason"], reason_summary["waste_cost"], color=colors_bar[:len(reason_summary)], width=0.55)
            ax.set_ylabel("Waste Cost (Rs.)", fontsize=9, fontweight="bold")
            ax.tick_params(axis="x", labelsize=8)
            ax.tick_params(axis="y", labelsize=8)
            ax.grid(axis="y", linestyle="--", alpha=0.5)

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=6, pady=6)
        else:
            tk.Label(self.chart_container, text="No waste records found", bg="white").pack(pady=40)

        # 4. Render Table (limit to last 200 rows for smooth performance)
        for item in self.tree.get_children():
            self.tree.delete(item)

        sample = filtered.tail(200).iloc[::-1]
        self.record_count_label.config(text=f"Showing latest {len(sample)} of {len(filtered):,} records")

        for _, row in sample.iterrows():
            self.tree.insert("", "end", values=(
                row["date"],
                row["waste_type"],
                row["item_name"],
                f"{row['quantity']:.2f}",
                row["unit"],
                row["reason"],
                f"₹{row['waste_cost']:,.2f}"
            ))