import tkinter as tk
from tkinter import ttk

class ProfitFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f6f9")
        ttk.Label(self, text="Profit & Analytics", style="Header.TLabel").pack(anchor="w")