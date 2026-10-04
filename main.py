import tkinter as tk
from tkinter import ttk
import sys
import os

from ui.dashboard import DashboardFrame
from ui.sales import SalesFrame
from ui.inventory import InventoryFrame
from ui.waste import WasteFrame
from ui.products import ProductsFrame
from ui.profit import ProfitFrame

class CanteenWiseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CanteenWise - Food Waste & Profit Analytics")
        self.geometry("1300x840")
        self.configure(bg="#f4f6f9")
        self.minsize(1080, 720)

        # Elevate window on startup
        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes, '-topmost', False)
        self.focus_force()

        self.nav_buttons = {}
        self.current_frame_class = None

        self.setup_styles()
        self.build_sidebar()
        self.build_main_content()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), background="#f4f6f9", foreground="#0f172a")
        style.configure("Card.TFrame", background="white", relief="raised", borderwidth=1)
        
        # Configure Treeview styling
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#f8fafc", foreground="#0f172a")
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
        style.map("Treeview", background=[("selected", "#2563eb")], foreground=[("selected", "white")])

    def build_sidebar(self):
        # Crisp white sidebar for maximum contrast with bold black text
        self.sidebar = tk.Frame(self, bg="#ffffff", width=255, highlightbackground="#cbd5e1", highlightthickness=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # App Brand Header
        brand_frame = tk.Frame(self.sidebar, bg="#ffffff", pady=22, padx=16)
        brand_frame.pack(fill="x")

        # 100% Bold Black Brand Title & Subtitle
        tk.Label(brand_frame, text="🍽️ CanteenWise", font=("Segoe UI", 18, "bold"), 
                 bg="#ffffff", fg="#000000", anchor="w").pack(fill="x")
        tk.Label(brand_frame, text="Waste & Profit Intelligence", font=("Segoe UI", 9, "bold"), 
                 bg="#ffffff", fg="#0f172a", anchor="w").pack(fill="x", pady=(3, 0))

        # Divider
        tk.Frame(self.sidebar, bg="#e2e8f0", height=1).pack(fill="x", padx=14, pady=(0, 15))

        # Navigation Buttons
        nav_items = [
            ("📊  Dashboard", DashboardFrame),
            ("🛒  Sales & Orders", SalesFrame),
            ("📦  Inventory & Purchases", InventoryFrame),
            ("🗑️  Waste Tracking", WasteFrame),
            ("📋  Products & Recipes", ProductsFrame),
            ("💰  Profit & Analytics", ProfitFrame)
        ]

        for label_text, frame_class in nav_items:
            btn = tk.Button(
                self.sidebar,
                text=f" {label_text}",
                font=("Segoe UI", 11, "bold"),
                bg="#ffffff",
                fg="#000000",
                activebackground="#e2e8f0",
                activeforeground="#000000",
                relief="flat",
                anchor="w",
                padx=16,
                pady=11,
                cursor="hand2",
                highlightthickness=1,
                highlightbackground="#f1f5f9",
                command=lambda fc=frame_class: self.show_frame(fc)
            )
            btn.pack(fill="x", pady=3, padx=12)
            self.nav_buttons[frame_class] = btn

        # Bottom System Info with High-Contrast Black Text
        footer = tk.Frame(self.sidebar, bg="#ffffff", pady=15, padx=16)
        footer.pack(side="bottom", fill="x")
        tk.Frame(footer, bg="#e2e8f0", height=1).pack(fill="x", pady=(0, 10))
        tk.Label(footer, text="● All 7 CSV Backend Datasets Connected", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#16a34a").pack(anchor="w")
        tk.Label(footer, text="CanteenWise Enterprise v1.0", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#000000").pack(anchor="w", pady=(2, 0))

    def build_main_content(self):
        self.content_container = tk.Frame(self, bg="#f4f6f9")
        self.content_container.pack(side="right", fill="both", expand=True)

    def show_frame(self, frame_class):
        self.current_frame_class = frame_class

        # Update Sidebar Active State (high-contrast active state with dark black text)
        for fc, btn in self.nav_buttons.items():
            if fc == frame_class:
                btn.configure(bg="#e2e8f0", fg="#000000", font=("Segoe UI", 11, "bold"), 
                              highlightbackground="#94a3b8", relief="solid", bd=1)
            else:
                btn.configure(bg="#ffffff", fg="#000000", font=("Segoe UI", 11), 
                              highlightbackground="#f1f5f9", relief="flat", bd=0)

        # Destroy current frame widgets
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Initialize and pack the requested frame
        try:
            frame = frame_class(self.content_container, self)
            frame.pack(fill="both", expand=True, padx=20, pady=20)
        except Exception as e:
            err_frame = tk.Frame(self.content_container, bg="#fee2e2", padx=20, pady=20)
            err_frame.pack(fill="both", expand=True, padx=20, pady=20)
            tk.Label(err_frame, text=f"⚠️ Error loading module: {e}", font=("Segoe UI", 12, "bold"), fg="#b91c1c", bg="#fee2e2").pack(anchor="w")

if __name__ == "__main__":
    print("=" * 60)
    print("  🍽️  CanteenWise Desktop Application")
    print("  Food Waste & Profit Analytics System")
    print("=" * 60)
    print("[INFO] Initializing CanteenWise GUI...")
    app = CanteenWiseApp()
    app.show_frame(DashboardFrame)
    print("[INFO] Application running. Displaying window on screen...")
    print("[INFO] (Close the window or press Ctrl+C to stop)")
    print("=" * 60)
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\n[INFO] Application closed by user.")