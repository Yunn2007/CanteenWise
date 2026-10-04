import tkinter as tk
from tkinter import ttk

class InventoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        
        ttk.Label(self, text="Inventory Management", style="Header.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Setup Treeview
        columns = ("Item", "Category", "Quantity", "Unit", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Define color tags for stock status
        self.tree.tag_configure('ok', background='#d4edda', foreground='#155724')
        self.tree.tag_configure('low', background='#fff3cd', foreground='#856404')
        self.tree.tag_configure('expiring', background='#f8d7da', foreground='#721c24')

        self.tree.pack(fill="both", expand=True)
        self.load_dummy_data()

    def load_dummy_data(self):
        data = [
            ("Rice", "Dry Goods", 150, "kg", "🟢 OK", "ok"),
            ("Tomatoes", "Vegetables", 5, "kg", "🟡 Low Stock", "low"),
            ("Paneer", "Dairy", 2, "kg", "🔴 Expiring", "expiring"),
            ("Chicken", "Meat", 45, "kg", "🟢 OK", "ok")
        ]
        for item in data:
            self.tree.insert("", "end", values=item[:5], tags=(item[5],))