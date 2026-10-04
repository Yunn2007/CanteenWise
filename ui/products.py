import tkinter as tk
from tkinter import ttk

class ProductsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        
        ttk.Label(self, text="Products & Recipes (CRUD)", style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        
        form_frame = tk.Frame(self, bg="white", highlightbackground="#ddd", highlightthickness=1, pady=10, padx=10)
        form_frame.pack(fill="x", pady=(0, 20))
        
        # Form Inputs
        tk.Label(form_frame, text="Item Name:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Price (₹):", bg="white").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(form_frame).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Category:", bg="white").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        ttk.Combobox(form_frame, values=["Main Course", "Snacks", "Beverages"]).grid(row=0, column=5, padx=5, pady=5)

        # Action Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=1, column=0, columnspan=6, pady=10)
        tk.Button(btn_frame, text="Add Item", bg="#27ae60", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", bg="#f39c12", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", bg="#e74c3c", fg="white", width=12).pack(side="left", padx=5)

        # Data Table
        columns = ("ID", "Item Name", "Category", "Price", "Ingredients Count")
        tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        for col in columns: tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        
        # Mock Data
        tree.insert("", "end", values=("001", "Veg Thali", "Main Course", "80.00", "12"))
        tree.insert("", "end", values=("002", "Samosa", "Snacks", "15.00", "5"))