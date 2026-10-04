import tkinter as tk
from tkinter import ttk
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
        self.geometry("1280x800")
        self.configure(bg="#f4f6f9")
        self.minsize(1024, 768)

        self.setup_styles()
        self.build_sidebar()
        self.build_main_content()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Sidebar.TButton", font=("Segoe UI", 12), padding=10, 
                        background="#2c3e50", foreground="white", borderwidth=0)
        style.map("Sidebar.TButton", background=[("active", "#34495e")])
        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), background="#f4f6f9")
        style.configure("Card.TFrame", background="white", relief="raised", borderwidth=1)
        
    def build_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#2c3e50", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # App Logo / Title
        tk.Label(self.sidebar, text="CanteenWise", font=("Segoe UI", 18, "bold"), 
                 bg="#2c3e50", fg="#ecf0f1", pady=20).pack()

        # Navigation Buttons
        nav_items = [
            ("Dashboard", DashboardFrame),
            ("Sales", SalesFrame),
            ("Inventory", InventoryFrame),
            ("Waste", WasteFrame),
            ("Products & Recipes", ProductsFrame),
            ("Profit & Analytics", ProfitFrame)
        ]

        self.frames = {}
        for btn_text, frame_class in nav_items:
            btn = ttk.Button(self.sidebar, text=btn_text, style="Sidebar.TButton",
                             command=lambda fc=frame_class: self.show_frame(fc))
            btn.pack(fill="x", pady=2, padx=10)

    def build_main_content(self):
        self.content_container = tk.Frame(self, bg="#f4f6f9")
        self.content_container.pack(side="right", fill="both", expand=True)

    def show_frame(self, frame_class):
        # Destroy current frame if it exists
        for widget in self.content_container.winfo_children():
            widget.destroy()
            
        # Initialize and pack the requested frame
        frame = frame_class(self.content_container, self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

if __name__ == "__main__":
    app = CanteenWiseApp()
    # Load Dashboard by default
    app.show_frame(DashboardFrame)
    app.mainloop()