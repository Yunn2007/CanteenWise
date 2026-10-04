import tkinter as tk
from tkinter import ttk, messagebox
import os
import pandas as pd
from utils.csv_handler import CSVHandler

class ProductsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        self.controller = controller

        # Init Paths & Handlers
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        self.products_csv_path = os.path.join(base_dir, "products.csv")
        self.recipes_csv_path = os.path.join(base_dir, "recipes.csv")
        self.ingredients_csv_path = os.path.join(base_dir, "ingredients.csv")

        self.csv_handler = CSVHandler(self.products_csv_path, id_column="product_id")
        self.selected_product_id = None

        # Build UI
        self.build_header()
        self.build_form()

        # Split container: Left = Products Table, Right = Recipe & Ingredients breakdown
        panes = tk.Frame(self, bg="#f4f6f9")
        panes.pack(fill="both", expand=True)

        self.build_products_table(panes)
        self.build_recipe_pane(panes)

        # Load Products
        self.load_and_display()

    def build_header(self):
        header_bar = tk.Frame(self, bg="#f4f6f9")
        header_bar.pack(fill="x", pady=(0, 12))

        ttk.Label(header_bar, text="Menu Products & Recipe Formulations", style="Header.TLabel").pack(side="left", anchor="w")

        filter_frame = tk.Frame(header_bar, bg="#f4f6f9")
        filter_frame.pack(side="right")

        tk.Label(filter_frame, text="Filter Category:", bg="#f4f6f9", font=("Segoe UI", 9, "bold"), fg="#0f172a").pack(side="left", padx=(0, 5))
        self.cat_filter_var = tk.StringVar(value="All Categories")
        self.cat_filter_combo = ttk.Combobox(filter_frame, textvariable=self.cat_filter_var, state="readonly", width=14)
        self.cat_filter_combo.pack(side="left", padx=(0, 10))
        self.cat_filter_combo.bind("<<ComboboxSelected>>", lambda e: self.load_and_display())

    def build_form(self):
        form_card = tk.Frame(self, bg="white", highlightbackground="#e2e8f0", highlightthickness=1, pady=10, padx=14)
        form_card.pack(fill="x", pady=(0, 12))

        tk.Label(form_card, text="Product Editor (data/products.csv)", font=("Segoe UI", 10, "bold"), bg="white", fg="#0f172a").grid(row=0, column=0, columnspan=8, sticky="w", pady=(0, 8))

        # Fields
        tk.Label(form_card, text="Item Name:", bg="white", font=("Segoe UI", 9, "bold"), fg="#0f172a").grid(row=1, column=0, padx=5, pady=4, sticky="e")
        self.name_entry = ttk.Entry(form_card, width=18)
        self.name_entry.grid(row=1, column=1, padx=5, pady=4, sticky="w")

        tk.Label(form_card, text="Category:", bg="white", font=("Segoe UI", 9, "bold"), fg="#0f172a").grid(row=1, column=2, padx=5, pady=4, sticky="e")
        self.category_combo = ttk.Combobox(form_card, values=["Beverages", "Snacks", "Breakfast", "Meals"], state="readonly", width=13)
        self.category_combo.grid(row=1, column=3, padx=5, pady=4, sticky="w")
        self.category_combo.set("Meals")

        tk.Label(form_card, text="Selling Price (₹):", bg="white", font=("Segoe UI", 9, "bold"), fg="#0f172a").grid(row=1, column=4, padx=5, pady=4, sticky="e")
        self.price_entry = ttk.Entry(form_card, width=10)
        self.price_entry.grid(row=1, column=5, padx=5, pady=4, sticky="w")

        tk.Label(form_card, text="Unit Cost (₹):", bg="white", font=("Segoe UI", 9, "bold"), fg="#0f172a").grid(row=1, column=6, padx=5, pady=4, sticky="e")
        self.cost_entry = ttk.Entry(form_card, width=10)
        self.cost_entry.grid(row=1, column=7, padx=5, pady=4, sticky="w")

        # Action Buttons
        btn_frame = tk.Frame(form_card, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=8, pady=(8, 0), sticky="w")

        self.add_btn = tk.Button(btn_frame, text="✚ Add Item", bg="#10b981", fg="black", font=("Segoe UI", 9, "bold"), padx=10, pady=3, relief="groove", command=self.add_product)
        self.add_btn.pack(side="left", padx=(0, 6))

        self.update_btn = tk.Button(btn_frame, text="✎ Update Selected", bg="#f59e0b", fg="black", font=("Segoe UI", 9, "bold"), padx=10, pady=3, relief="groove", command=self.update_product)
        self.update_btn.pack(side="left", padx=(0, 6))

        self.delete_btn = tk.Button(btn_frame, text="✕ Delete Selected", bg="#ef4444", fg="black", font=("Segoe UI", 9, "bold"), padx=10, pady=3, relief="groove", command=self.delete_product)
        self.delete_btn.pack(side="left", padx=(0, 6))

        self.clear_btn = tk.Button(btn_frame, text="↺ Clear Selection", bg="#e2e8f0", fg="#0f172a", font=("Segoe UI", 9), padx=10, pady=3, relief="groove", command=self.clear_form)
        self.clear_btn.pack(side="left")

        self.status_label = tk.Label(form_card, text="Select any item from the table to view its underlying ingredients from recipes.csv.", bg="white", fg="#475569", font=("Segoe UI", 8, "italic"))
        self.status_label.grid(row=3, column=0, columnspan=8, sticky="w", pady=(4, 0))

    def build_products_table(self, parent):
        table_container = tk.Frame(parent, bg="white", highlightbackground="#e2e8f0", highlightthickness=1)
        table_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        lbl_frame = tk.Frame(table_container, bg="white", padx=10, pady=8)
        lbl_frame.pack(fill="x")
        tk.Label(lbl_frame, text="Product Master Catalog", font=("Segoe UI", 11, "bold"), bg="white", fg="#0f172a").pack(side="left")

        columns = ("product_id", "product_name", "category", "selling_price", "unit_cost", "margin_pct")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", height=12)

        headers = [
            ("product_id", "ID", 60),
            ("product_name", "Product Name", 150),
            ("category", "Category", 100),
            ("selling_price", "Selling (₹)", 80),
            ("unit_cost", "Cost (₹)", 75),
            ("margin_pct", "Margin %", 75)
        ]
        for col_id, col_name, width in headers:
            self.tree.heading(col_id, text=col_name)
            self.tree.column(col_id, width=width, anchor="center" if col_id in ["product_id", "margin_pct"] else "w")

        tree_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 8))
        tree_scroll.pack(side="right", fill="y", pady=(0, 8), padx=(0, 8))

        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

    def build_recipe_pane(self, parent):
        # Displays recipes.csv connected with ingredients.csv
        recipe_card = tk.Frame(parent, bg="white", width=420, highlightbackground="#e2e8f0", highlightthickness=1)
        recipe_card.pack(side="right", fill="both", expand=False)
        recipe_card.pack_propagate(False)

        top_bar = tk.Frame(recipe_card, bg="white", padx=10, pady=8)
        top_bar.pack(fill="x")
        self.recipe_title_label = tk.Label(top_bar, text="Recipe Bill of Materials (data/recipes.csv)", font=("Segoe UI", 11, "bold"), bg="white", fg="#0f172a")
        self.recipe_title_label.pack(side="left")

        self.recipe_summary_label = tk.Label(recipe_card, text="Click a product to load its ingredient recipe.", font=("Segoe UI", 9), bg="white", fg="#64748b", padx=10)
        self.recipe_summary_label.pack(anchor="w", pady=(0, 6))

        columns = ("ingredient", "qty", "unit", "cost")
        self.recipe_tree = ttk.Treeview(recipe_card, columns=columns, show="headings", height=10)
        
        r_headers = [
            ("ingredient", "Raw Ingredient", 150),
            ("qty", "Qty/Unit", 80),
            ("unit", "Unit", 60),
            ("cost", "Cost (₹)", 80)
        ]
        for c_id, c_name, w in r_headers:
            self.recipe_tree.heading(c_id, text=c_name)
            self.recipe_tree.column(c_id, width=w, anchor="center" if c_id in ["qty", "unit"] else "w")

        r_scroll = ttk.Scrollbar(recipe_card, orient="vertical", command=self.recipe_tree.yview)
        self.recipe_tree.configure(yscrollcommand=r_scroll.set)
        self.recipe_tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 8))
        r_scroll.pack(side="right", fill="y", pady=(0, 8), padx=(0, 8))

    def load_recipe(self, product_id, product_name):
        # Clear current recipe items
        for item in self.recipe_tree.get_children():
            self.recipe_tree.delete(item)

        if not os.path.exists(self.recipes_csv_path) or not os.path.exists(self.ingredients_csv_path):
            self.recipe_summary_label.config(text="Recipe or ingredients CSV file missing.")
            return

        try:
            recipes_df = pd.read_csv(self.recipes_csv_path)
            ingredients_df = pd.read_csv(self.ingredients_csv_path)

            filtered = recipes_df[recipes_df["product_id"] == product_id].merge(ingredients_df, on="ingredient_id", how="left")
            if filtered.empty:
                self.recipe_title_label.config(text=f"Recipe: {product_name} ({product_id})")
                self.recipe_summary_label.config(text="No recipe mapped in data/recipes.csv.")
                return

            filtered["ingredient_cost"] = filtered["quantity_per_unit"] * filtered["purchase_cost"]
            total_calc_cost = filtered["ingredient_cost"].sum()

            self.recipe_title_label.config(text=f"Recipe: {product_name} ({product_id})")
            self.recipe_summary_label.config(text=f"{len(filtered)} Ingredients • Total Raw Cost: ₹{total_calc_cost:.2f}")

            for _, row in filtered.iterrows():
                self.recipe_tree.insert("", "end", values=(
                    row["ingredient_name"],
                    f"{row['quantity_per_unit']:.3f}",
                    row["unit"],
                    f"₹{row['ingredient_cost']:.2f}"
                ))
        except Exception as e:
            self.recipe_summary_label.config(text=f"Error reading recipe: {e}")

    def load_and_display(self):
        try:
            df = self.csv_handler.load()
            if df.empty:
                return

            cats = ["All Categories"] + sorted(df["category"].dropna().unique().tolist())
            self.cat_filter_combo["values"] = cats

            selected_cat = self.cat_filter_var.get()
            if selected_cat != "All Categories":
                df = df[df["category"] == selected_cat]

            for item in self.tree.get_children():
                self.tree.delete(item)

            for _, row in df.iterrows():
                sp = float(row.get("selling_price", 0))
                uc = float(row.get("unit_cost", 0))
                margin = ((sp - uc) / sp * 100) if sp > 0 else 0.0

                self.tree.insert("", "end", values=(
                    row["product_id"],
                    row["product_name"],
                    row["category"],
                    f"₹{sp:.2f}",
                    f"₹{uc:.2f}",
                    f"{margin:.1f}%"
                ))

            # Select first product by default if available
            children = self.tree.get_children()
            if children:
                self.tree.selection_set(children[0])
                self.on_item_select(None)
        except Exception as e:
            self.status_label.config(text=f"Error loading products: {e}", fg="#ef4444")

    def on_item_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if not values:
            return

        self.selected_product_id = values[0]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.category_combo.set(values[2])

        sp_clean = values[3].replace("₹", "").strip()
        uc_clean = values[4].replace("₹", "").strip()

        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, sp_clean)

        self.cost_entry.delete(0, tk.END)
        self.cost_entry.insert(0, uc_clean)

        self.status_label.config(text=f"Editing '{values[1]}' ({self.selected_product_id}). Recipe formulation loaded.", fg="#2563eb")

        # Load linked recipe
        self.load_recipe(self.selected_product_id, values[1])

    def clear_form(self):
        self.selected_product_id = None
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        self.category_combo.set("Meals")
        self.tree.selection_remove(self.tree.selection())
        self.status_label.config(text="Form cleared. Enter values to add a new product.", fg="#64748b")
        for item in self.recipe_tree.get_children():
            self.recipe_tree.delete(item)
        self.recipe_title_label.config(text="Recipe Bill of Materials")
        self.recipe_summary_label.config(text="Select a product to view recipe formulation.")

    def generate_next_id(self) -> str:
        df = self.csv_handler.load()
        existing_ids = df["product_id"].astype(str).tolist()
        num = 1
        while True:
            candidate = f"P{num:03d}"
            if candidate not in existing_ids:
                return candidate
            num += 1

    def add_product(self):
        name = self.name_entry.get().strip()
        category = self.category_combo.get().strip()
        price_str = self.price_entry.get().strip()
        cost_str = self.cost_entry.get().strip()

        if not name or not price_str or not cost_str:
            messagebox.showwarning("Validation Error", "Please fill in all fields (Name, Price, Unit Cost).")
            return

        try:
            price = float(price_str)
            cost = float(cost_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Price and Unit Cost must be valid numbers.")
            return

        new_id = self.generate_next_id()
        record = {
            "product_id": new_id,
            "product_name": name,
            "category": category,
            "selling_price": price,
            "unit_cost": cost
        }

        try:
            self.csv_handler.add_record(record)
            self.clear_form()
            self.load_and_display()
            self.status_label.config(text=f"✅ Added '{name}' as {new_id} successfully.", fg="#16a34a")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")

    def update_product(self):
        if not self.selected_product_id:
            messagebox.showinfo("Select Product", "Please select a product from the table first to update it.")
            return

        name = self.name_entry.get().strip()
        category = self.category_combo.get().strip()
        price_str = self.price_entry.get().strip()
        cost_str = self.cost_entry.get().strip()

        if not name or not price_str or not cost_str:
            messagebox.showwarning("Validation Error", "Please fill in all fields.")
            return

        try:
            price = float(price_str)
            cost = float(cost_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Price and Unit Cost must be valid numbers.")
            return

        record = {
            "product_id": self.selected_product_id,
            "product_name": name,
            "category": category,
            "selling_price": price,
            "unit_cost": cost
        }

        try:
            self.csv_handler.update_record(self.selected_product_id, record)
            self.clear_form()
            self.load_and_display()
            self.status_label.config(text=f"✅ Updated product {self.selected_product_id} successfully.", fg="#16a34a")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {e}")

    def delete_product(self):
        if not self.selected_product_id:
            messagebox.showinfo("Select Product", "Please select a product from the table first to delete it.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete product '{self.selected_product_id}'?")
        if not confirm:
            return

        try:
            self.csv_handler.delete_record(self.selected_product_id)
            self.clear_form()
            self.load_and_display()
            self.status_label.config(text=f"✅ Deleted product {self.selected_product_id} successfully.", fg="#dc2626")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {e}")