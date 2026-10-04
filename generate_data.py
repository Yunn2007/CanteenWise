"""
generate_data.py
Synthetic Data Generator for CanteenWise.
Generates 7 interconnected CSV files modeling an Indian college canteen's
inventory, food waste, recipes, sales, and purchasing operations.
"""

import os
import random
import datetime
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np


# ---------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------
RANDOM_SEED = 42
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
START_DATE = datetime.date(2026, 1, 1)
NUM_DAYS = 180  # 6 months (approx 26 weeks)


def set_seed(seed: int = RANDOM_SEED) -> None:
    """Sets deterministic random seeds for reproducible data generation."""
    random.seed(seed)
    np.random.seed(seed)


# ---------------------------------------------------------
# 1. Products Definition (20–25 rows)
# ---------------------------------------------------------
def create_products() -> pd.DataFrame:
    """
    Creates products dataset (22 products).
    Columns: product_id, product_name, category, selling_price, unit_cost
    """
    products_data = [
        # Beverages
        {"product_id": "P001", "product_name": "Masala Chai", "category": "Beverages", "selling_price": 15.0, "unit_cost": 5.50},
        {"product_id": "P002", "product_name": "Filter Coffee", "category": "Beverages", "selling_price": 20.0, "unit_cost": 7.20},
        {"product_id": "P003", "product_name": "Sweet Lassi", "category": "Beverages", "selling_price": 35.0, "unit_cost": 14.50},
        {"product_id": "P004", "product_name": "Fresh Lime Soda", "category": "Beverages", "selling_price": 25.0, "unit_cost": 7.80},
        # Snacks & Quick Bites
        {"product_id": "P005", "product_name": "Samosa", "category": "Snacks", "selling_price": 15.0, "unit_cost": 6.20},
        {"product_id": "P006", "product_name": "Vada Pav", "category": "Snacks", "selling_price": 20.0, "unit_cost": 8.10},
        {"product_id": "P007", "product_name": "Poha", "category": "Breakfast", "selling_price": 25.0, "unit_cost": 9.20},
        {"product_id": "P008", "product_name": "Masala Dosa", "category": "Breakfast", "selling_price": 50.0, "unit_cost": 17.50},
        {"product_id": "P009", "product_name": "Idli Sambar", "category": "Breakfast", "selling_price": 40.0, "unit_cost": 13.80},
        {"product_id": "P010", "product_name": "Chole Bhature", "category": "Breakfast", "selling_price": 60.0, "unit_cost": 21.50},
        {"product_id": "P011", "product_name": "Bread Pakora", "category": "Snacks", "selling_price": 20.0, "unit_cost": 7.50},
        # Meals
        {"product_id": "P012", "product_name": "Veg Thali", "category": "Meals", "selling_price": 80.0, "unit_cost": 31.00},
        {"product_id": "P013", "product_name": "Rajma Chawal", "category": "Meals", "selling_price": 60.0, "unit_cost": 20.50},
        {"product_id": "P014", "product_name": "Dal Khichdi", "category": "Meals", "selling_price": 50.0, "unit_cost": 16.00},
        {"product_id": "P015", "product_name": "Paneer Butter Masala", "category": "Meals", "selling_price": 90.0, "unit_cost": 35.00},
        {"product_id": "P016", "product_name": "Paneer Pulao", "category": "Meals", "selling_price": 75.0, "unit_cost": 27.50},
        {"product_id": "P017", "product_name": "Veg Biryani", "category": "Meals", "selling_price": 70.0, "unit_cost": 25.00},
        {"product_id": "P018", "product_name": "Veg Fried Rice", "category": "Meals", "selling_price": 60.0, "unit_cost": 21.00},
        # Fast Food
        {"product_id": "P019", "product_name": "Aloo Tikki Burger", "category": "Fast Food", "selling_price": 45.0, "unit_cost": 16.00},
        {"product_id": "P020", "product_name": "Veg Cheese Burger", "category": "Fast Food", "selling_price": 60.0, "unit_cost": 23.50},
        {"product_id": "P021", "product_name": "Paneer Roll", "category": "Fast Food", "selling_price": 65.0, "unit_cost": 24.00},
        {"product_id": "P022", "product_name": "Veg Cutlet", "category": "Snacks", "selling_price": 25.0, "unit_cost": 9.00},
    ]
    df = pd.DataFrame(products_data)
    return df


# ---------------------------------------------------------
# 2. Ingredients Definition (30–40 rows)
# ---------------------------------------------------------
def create_ingredients() -> pd.DataFrame:
    """
    Creates ingredients dataset (32 ingredients).
    Columns: ingredient_id, ingredient_name, unit, purchase_cost, shelf_life_days, reorder_level
    """
    ingredients_data = [
        {"ingredient_id": "ING001", "ingredient_name": "Potatoes", "unit": "kg", "purchase_cost": 25.0, "shelf_life_days": 15, "reorder_level": 30.0},
        {"ingredient_id": "ING002", "ingredient_name": "Onions", "unit": "kg", "purchase_cost": 35.0, "shelf_life_days": 20, "reorder_level": 25.0},
        {"ingredient_id": "ING003", "ingredient_name": "Tomatoes", "unit": "kg", "purchase_cost": 30.0, "shelf_life_days": 6, "reorder_level": 20.0},
        {"ingredient_id": "ING004", "ingredient_name": "Green Chillies", "unit": "kg", "purchase_cost": 60.0, "shelf_life_days": 7, "reorder_level": 4.0},
        {"ingredient_id": "ING005", "ingredient_name": "Ginger Garlic Paste", "unit": "kg", "purchase_cost": 120.0, "shelf_life_days": 15, "reorder_level": 5.0},
        {"ingredient_id": "ING006", "ingredient_name": "Coriander Leaves", "unit": "kg", "purchase_cost": 50.0, "shelf_life_days": 4, "reorder_level": 3.0},
        {"ingredient_id": "ING007", "ingredient_name": "Capsicum", "unit": "kg", "purchase_cost": 70.0, "shelf_life_days": 6, "reorder_level": 5.0},
        {"ingredient_id": "ING008", "ingredient_name": "Cabbage", "unit": "kg", "purchase_cost": 30.0, "shelf_life_days": 8, "reorder_level": 6.0},
        {"ingredient_id": "ING009", "ingredient_name": "Carrots", "unit": "kg", "purchase_cost": 45.0, "shelf_life_days": 10, "reorder_level": 5.0},
        {"ingredient_id": "ING010", "ingredient_name": "Lemon", "unit": "kg", "purchase_cost": 80.0, "shelf_life_days": 10, "reorder_level": 3.0},
        {"ingredient_id": "ING011", "ingredient_name": "Fresh Milk", "unit": "L", "purchase_cost": 56.0, "shelf_life_days": 2, "reorder_level": 25.0},
        {"ingredient_id": "ING012", "ingredient_name": "Paneer", "unit": "kg", "purchase_cost": 320.0, "shelf_life_days": 3, "reorder_level": 8.0},
        {"ingredient_id": "ING013", "ingredient_name": "Curd / Yogurt", "unit": "kg", "purchase_cost": 60.0, "shelf_life_days": 4, "reorder_level": 10.0},
        {"ingredient_id": "ING014", "ingredient_name": "Butter", "unit": "kg", "purchase_cost": 480.0, "shelf_life_days": 30, "reorder_level": 5.0},
        {"ingredient_id": "ING015", "ingredient_name": "Cheese Slices", "unit": "pkt", "purchase_cost": 130.0, "shelf_life_days": 45, "reorder_level": 6.0},
        {"ingredient_id": "ING016", "ingredient_name": "White Rice", "unit": "kg", "purchase_cost": 45.0, "shelf_life_days": 180, "reorder_level": 40.0},
        {"ingredient_id": "ING017", "ingredient_name": "Basmati Rice", "unit": "kg", "purchase_cost": 85.0, "shelf_life_days": 180, "reorder_level": 25.0},
        {"ingredient_id": "ING018", "ingredient_name": "Wheat Flour (Atta)", "unit": "kg", "purchase_cost": 40.0, "shelf_life_days": 90, "reorder_level": 35.0},
        {"ingredient_id": "ING019", "ingredient_name": "Maida (Refined Flour)", "unit": "kg", "purchase_cost": 42.0, "shelf_life_days": 90, "reorder_level": 25.0},
        {"ingredient_id": "ING020", "ingredient_name": "Poha (Flattened Rice)", "unit": "kg", "purchase_cost": 50.0, "shelf_life_days": 90, "reorder_level": 15.0},
        {"ingredient_id": "ING021", "ingredient_name": "Toor Dal", "unit": "kg", "purchase_cost": 140.0, "shelf_life_days": 180, "reorder_level": 20.0},
        {"ingredient_id": "ING022", "ingredient_name": "Rajma (Kidney Beans)", "unit": "kg", "purchase_cost": 130.0, "shelf_life_days": 180, "reorder_level": 15.0},
        {"ingredient_id": "ING023", "ingredient_name": "Chole (Chickpeas)", "unit": "kg", "purchase_cost": 120.0, "shelf_life_days": 180, "reorder_level": 15.0},
        {"ingredient_id": "ING024", "ingredient_name": "Urad Dal", "unit": "kg", "purchase_cost": 135.0, "shelf_life_days": 180, "reorder_level": 12.0},
        {"ingredient_id": "ING025", "ingredient_name": "Cooking Refined Oil", "unit": "L", "purchase_cost": 130.0, "shelf_life_days": 180, "reorder_level": 30.0},
        {"ingredient_id": "ING026", "ingredient_name": "Tea Powder", "unit": "kg", "purchase_cost": 320.0, "shelf_life_days": 180, "reorder_level": 6.0},
        {"ingredient_id": "ING027", "ingredient_name": "Coffee Powder", "unit": "kg", "purchase_cost": 600.0, "shelf_life_days": 180, "reorder_level": 4.0},
        {"ingredient_id": "ING028", "ingredient_name": "Sugar", "unit": "kg", "purchase_cost": 42.0, "shelf_life_days": 365, "reorder_level": 25.0},
        {"ingredient_id": "ING029", "ingredient_name": "Spices & Masala", "unit": "kg", "purchase_cost": 280.0, "shelf_life_days": 180, "reorder_level": 8.0},
        {"ingredient_id": "ING030", "ingredient_name": "Burger Buns", "unit": "pkt", "purchase_cost": 35.0, "shelf_life_days": 4, "reorder_level": 12.0},
        {"ingredient_id": "ING031", "ingredient_name": "Pav Buns", "unit": "pkt", "purchase_cost": 30.0, "shelf_life_days": 3, "reorder_level": 18.0},
        {"ingredient_id": "ING032", "ingredient_name": "Bread Loaf", "unit": "pkt", "purchase_cost": 35.0, "shelf_life_days": 4, "reorder_level": 12.0},
    ]
    df = pd.DataFrame(ingredients_data)
    return df


# ---------------------------------------------------------
# 3. Recipes Definition (100–150 rows)
# ---------------------------------------------------------
def create_recipes() -> pd.DataFrame:
    """
    Creates Bill of Materials linking products to ingredients (127 rows).
    Columns: product_id, ingredient_id, quantity_per_unit
    """
    recipes_data = [
        # P001: Masala Chai (4)
        {"product_id": "P001", "ingredient_id": "ING011", "quantity_per_unit": 0.100},  # Milk (L)
        {"product_id": "P001", "ingredient_id": "ING026", "quantity_per_unit": 0.008},  # Tea Powder (kg)
        {"product_id": "P001", "ingredient_id": "ING028", "quantity_per_unit": 0.012},  # Sugar (kg)
        {"product_id": "P001", "ingredient_id": "ING029", "quantity_per_unit": 0.003},  # Spices (kg)

        # P002: Filter Coffee (3)
        {"product_id": "P002", "ingredient_id": "ING011", "quantity_per_unit": 0.120},  # Milk (L)
        {"product_id": "P002", "ingredient_id": "ING027", "quantity_per_unit": 0.008},  # Coffee Powder (kg)
        {"product_id": "P002", "ingredient_id": "ING028", "quantity_per_unit": 0.012},  # Sugar (kg)

        # P003: Sweet Lassi (4)
        {"product_id": "P003", "ingredient_id": "ING013", "quantity_per_unit": 0.200},  # Curd (kg)
        {"product_id": "P003", "ingredient_id": "ING028", "quantity_per_unit": 0.025},  # Sugar (kg)
        {"product_id": "P003", "ingredient_id": "ING011", "quantity_per_unit": 0.050},  # Milk (L)
        {"product_id": "P003", "ingredient_id": "ING029", "quantity_per_unit": 0.002},  # Cardamom/Spices (kg)

        # P004: Fresh Lime Soda (3)
        {"product_id": "P004", "ingredient_id": "ING010", "quantity_per_unit": 0.050},  # Lemon (kg)
        {"product_id": "P004", "ingredient_id": "ING028", "quantity_per_unit": 0.020},  # Sugar (kg)
        {"product_id": "P004", "ingredient_id": "ING029", "quantity_per_unit": 0.003},  # Rock salt/Spices (kg)

        # P005: Samosa (6)
        {"product_id": "P005", "ingredient_id": "ING001", "quantity_per_unit": 0.070},  # Potatoes (kg)
        {"product_id": "P005", "ingredient_id": "ING019", "quantity_per_unit": 0.040},  # Maida (kg)
        {"product_id": "P005", "ingredient_id": "ING025", "quantity_per_unit": 0.020},  # Oil (L)
        {"product_id": "P005", "ingredient_id": "ING004", "quantity_per_unit": 0.005},  # Green Chillies (kg)
        {"product_id": "P005", "ingredient_id": "ING029", "quantity_per_unit": 0.004},  # Spices (kg)
        {"product_id": "P005", "ingredient_id": "ING006", "quantity_per_unit": 0.003},  # Coriander (kg)

        # P006: Vada Pav (6)
        {"product_id": "P006", "ingredient_id": "ING001", "quantity_per_unit": 0.060},  # Potatoes (kg)
        {"product_id": "P006", "ingredient_id": "ING031", "quantity_per_unit": 0.167},  # Pav Bun (pkt)
        {"product_id": "P006", "ingredient_id": "ING025", "quantity_per_unit": 0.015},  # Oil (L)
        {"product_id": "P006", "ingredient_id": "ING004", "quantity_per_unit": 0.004},  # Chillies (kg)
        {"product_id": "P006", "ingredient_id": "ING005", "quantity_per_unit": 0.003},  # Ginger Garlic (kg)
        {"product_id": "P006", "ingredient_id": "ING029", "quantity_per_unit": 0.004},  # Spices (kg)

        # P007: Poha (7)
        {"product_id": "P007", "ingredient_id": "ING020", "quantity_per_unit": 0.080},  # Poha (kg)
        {"product_id": "P007", "ingredient_id": "ING002", "quantity_per_unit": 0.030},  # Onions (kg)
        {"product_id": "P007", "ingredient_id": "ING001", "quantity_per_unit": 0.020},  # Potatoes (kg)
        {"product_id": "P007", "ingredient_id": "ING025", "quantity_per_unit": 0.010},  # Oil (L)
        {"product_id": "P007", "ingredient_id": "ING004", "quantity_per_unit": 0.003},  # Chillies (kg)
        {"product_id": "P007", "ingredient_id": "ING010", "quantity_per_unit": 0.010},  # Lemon (kg)
        {"product_id": "P007", "ingredient_id": "ING029", "quantity_per_unit": 0.002},  # Spices (kg)

        # P008: Masala Dosa (6)
        {"product_id": "P008", "ingredient_id": "ING016", "quantity_per_unit": 0.080},  # Rice (kg)
        {"product_id": "P008", "ingredient_id": "ING024", "quantity_per_unit": 0.025},  # Urad Dal (kg)
        {"product_id": "P008", "ingredient_id": "ING001", "quantity_per_unit": 0.060},  # Potatoes (kg)
        {"product_id": "P008", "ingredient_id": "ING002", "quantity_per_unit": 0.020},  # Onions (kg)
        {"product_id": "P008", "ingredient_id": "ING025", "quantity_per_unit": 0.015},  # Oil (L)
        {"product_id": "P008", "ingredient_id": "ING029", "quantity_per_unit": 0.004},  # Spices (kg)

        # P009: Idli Sambar (6)
        {"product_id": "P009", "ingredient_id": "ING016", "quantity_per_unit": 0.080},  # Rice (kg)
        {"product_id": "P009", "ingredient_id": "ING024", "quantity_per_unit": 0.025},  # Urad Dal (kg)
        {"product_id": "P009", "ingredient_id": "ING021", "quantity_per_unit": 0.030},  # Toor Dal (kg)
        {"product_id": "P009", "ingredient_id": "ING003", "quantity_per_unit": 0.020},  # Tomatoes (kg)
        {"product_id": "P009", "ingredient_id": "ING002", "quantity_per_unit": 0.020},  # Onions (kg)
        {"product_id": "P009", "ingredient_id": "ING029", "quantity_per_unit": 0.005},  # Sambar Masala (kg)

        # P010: Chole Bhature (7)
        {"product_id": "P010", "ingredient_id": "ING023", "quantity_per_unit": 0.080},  # Chole (kg)
        {"product_id": "P010", "ingredient_id": "ING019", "quantity_per_unit": 0.080},  # Maida (kg)
        {"product_id": "P010", "ingredient_id": "ING002", "quantity_per_unit": 0.040},  # Onions (kg)
        {"product_id": "P010", "ingredient_id": "ING003", "quantity_per_unit": 0.040},  # Tomatoes (kg)
        {"product_id": "P010", "ingredient_id": "ING025", "quantity_per_unit": 0.030},  # Oil (L)
        {"product_id": "P010", "ingredient_id": "ING005", "quantity_per_unit": 0.005},  # Ginger Garlic (kg)
        {"product_id": "P010", "ingredient_id": "ING029", "quantity_per_unit": 0.006},  # Spices (kg)

        # P011: Bread Pakora (5)
        {"product_id": "P011", "ingredient_id": "ING032", "quantity_per_unit": 0.125},  # Bread (pkt)
        {"product_id": "P011", "ingredient_id": "ING001", "quantity_per_unit": 0.050},  # Potatoes (kg)
        {"product_id": "P011", "ingredient_id": "ING025", "quantity_per_unit": 0.020},  # Oil (L)
        {"product_id": "P011", "ingredient_id": "ING029", "quantity_per_unit": 0.004},  # Spices (kg)
        {"product_id": "P011", "ingredient_id": "ING004", "quantity_per_unit": 0.003},  # Chillies (kg)

        # P012: Veg Thali (8)
        {"product_id": "P012", "ingredient_id": "ING016", "quantity_per_unit": 0.100},  # Rice (kg)
        {"product_id": "P012", "ingredient_id": "ING018", "quantity_per_unit": 0.060},  # Atta (kg)
        {"product_id": "P012", "ingredient_id": "ING021", "quantity_per_unit": 0.040},  # Toor Dal (kg)
        {"product_id": "P012", "ingredient_id": "ING001", "quantity_per_unit": 0.050},  # Potatoes (kg)
        {"product_id": "P012", "ingredient_id": "ING002", "quantity_per_unit": 0.030},  # Onions (kg)
        {"product_id": "P012", "ingredient_id": "ING003", "quantity_per_unit": 0.030},  # Tomatoes (kg)
        {"product_id": "P012", "ingredient_id": "ING025", "quantity_per_unit": 0.015},  # Oil (L)
        {"product_id": "P012", "ingredient_id": "ING013", "quantity_per_unit": 0.050},  # Curd (kg)

        # P013: Rajma Chawal (7)
        {"product_id": "P013", "ingredient_id": "ING022", "quantity_per_unit": 0.070},  # Rajma (kg)
        {"product_id": "P013", "ingredient_id": "ING016", "quantity_per_unit": 0.100},  # Rice (kg)
        {"product_id": "P013", "ingredient_id": "ING002", "quantity_per_unit": 0.040},  # Onions (kg)
        {"product_id": "P013", "ingredient_id": "ING003", "quantity_per_unit": 0.040},  # Tomatoes (kg)
        {"product_id": "P013", "ingredient_id": "ING025", "quantity_per_unit": 0.015},  # Oil (L)
        {"product_id": "P013", "ingredient_id": "ING005", "quantity_per_unit": 0.005},  # Ginger Garlic (kg)
        {"product_id": "P013", "ingredient_id": "ING029", "quantity_per_unit": 0.005},  # Spices (kg)

        # P014: Dal Khichdi (6)
        {"product_id": "P014", "ingredient_id": "ING016", "quantity_per_unit": 0.080},  # Rice (kg)
        {"product_id": "P014", "ingredient_id": "ING021", "quantity_per_unit": 0.040},  # Toor Dal (kg)
        {"product_id": "P014", "ingredient_id": "ING002", "quantity_per_unit": 0.020},  # Onions (kg)
        {"product_id": "P014", "ingredient_id": "ING003", "quantity_per_unit": 0.020},  # Tomatoes (kg)
        {"product_id": "P014", "ingredient_id": "ING014", "quantity_per_unit": 0.010},  # Butter (kg)
        {"product_id": "P014", "ingredient_id": "ING029", "quantity_per_unit": 0.004},  # Spices (kg)

        # P015: Paneer Butter Masala (7)
        {"product_id": "P015", "ingredient_id": "ING012", "quantity_per_unit": 0.120},  # Paneer (kg)
        {"product_id": "P015", "ingredient_id": "ING014", "quantity_per_unit": 0.025},  # Butter (kg)
        {"product_id": "P015", "ingredient_id": "ING003", "quantity_per_unit": 0.060},  # Tomatoes (kg)
        {"product_id": "P015", "ingredient_id": "ING002", "quantity_per_unit": 0.040},  # Onions (kg)
        {"product_id": "P015", "ingredient_id": "ING005", "quantity_per_unit": 0.006},  # Ginger Garlic (kg)
        {"product_id": "P015", "ingredient_id": "ING011", "quantity_per_unit": 0.030},  # Milk (L)
        {"product_id": "P015", "ingredient_id": "ING029", "quantity_per_unit": 0.006},  # Spices (kg)

        # P016: Paneer Pulao (7)
        {"product_id": "P016", "ingredient_id": "ING012", "quantity_per_unit": 0.080},  # Paneer (kg)
        {"product_id": "P016", "ingredient_id": "ING017", "quantity_per_unit": 0.100},  # Basmati Rice (kg)
        {"product_id": "P016", "ingredient_id": "ING002", "quantity_per_unit": 0.030},  # Onions (kg)
        {"product_id": "P016", "ingredient_id": "ING009", "quantity_per_unit": 0.020},  # Carrots (kg)
        {"product_id": "P016", "ingredient_id": "ING007", "quantity_per_unit": 0.020},  # Capsicum (kg)
        {"product_id": "P016", "ingredient_id": "ING014", "quantity_per_unit": 0.015},  # Butter (kg)
        {"product_id": "P016", "ingredient_id": "ING029", "quantity_per_unit": 0.005},  # Spices (kg)

        # P017: Veg Biryani (8)
        {"product_id": "P017", "ingredient_id": "ING017", "quantity_per_unit": 0.120},  # Basmati Rice (kg)
        {"product_id": "P017", "ingredient_id": "ING001", "quantity_per_unit": 0.040},  # Potatoes (kg)
        {"product_id": "P017", "ingredient_id": "ING009", "quantity_per_unit": 0.030},  # Carrots (kg)
        {"product_id": "P017", "ingredient_id": "ING002", "quantity_per_unit": 0.040},  # Onions (kg)
        {"product_id": "P017", "ingredient_id": "ING013", "quantity_per_unit": 0.030},  # Curd (kg)
        {"product_id": "P017", "ingredient_id": "ING025", "quantity_per_unit": 0.015},  # Oil (L)
        {"product_id": "P017", "ingredient_id": "ING029", "quantity_per_unit": 0.008},  # Biryani Masala (kg)
        {"product_id": "P017", "ingredient_id": "ING006", "quantity_per_unit": 0.005},  # Mint/Coriander (kg)

        # P018: Veg Fried Rice (7)
        {"product_id": "P018", "ingredient_id": "ING016", "quantity_per_unit": 0.100},  # Rice (kg)
        {"product_id": "P018", "ingredient_id": "ING007", "quantity_per_unit": 0.025},  # Capsicum (kg)
        {"product_id": "P018", "ingredient_id": "ING008", "quantity_per_unit": 0.025},  # Cabbage (kg)
        {"product_id": "P018", "ingredient_id": "ING009", "quantity_per_unit": 0.020},  # Carrots (kg)
        {"product_id": "P018", "ingredient_id": "ING002", "quantity_per_unit": 0.020},  # Onions (kg)
        {"product_id": "P018", "ingredient_id": "ING025", "quantity_per_unit": 0.015},  # Oil (L)
        {"product_id": "P018", "ingredient_id": "ING029", "quantity_per_unit": 0.004},  # Spices (kg)

        # P019: Aloo Tikki Burger (6)
        {"product_id": "P019", "ingredient_id": "ING030", "quantity_per_unit": 0.250},  # Buns (pkt)
        {"product_id": "P019", "ingredient_id": "ING001", "quantity_per_unit": 0.060},  # Potatoes (kg)
        {"product_id": "P019", "ingredient_id": "ING002", "quantity_per_unit": 0.020},  # Onions (kg)
        {"product_id": "P019", "ingredient_id": "ING003", "quantity_per_unit": 0.020},  # Tomatoes (kg)
        {"product_id": "P019", "ingredient_id": "ING025", "quantity_per_unit": 0.015},  # Oil (L)
        {"product_id": "P019", "ingredient_id": "ING029", "quantity_per_unit": 0.004},  # Spices (kg)

        # P020: Veg Cheese Burger (6)
        {"product_id": "P020", "ingredient_id": "ING030", "quantity_per_unit": 0.250},  # Buns (pkt)
        {"product_id": "P020", "ingredient_id": "ING001", "quantity_per_unit": 0.050},  # Potatoes (kg)
        {"product_id": "P020", "ingredient_id": "ING015", "quantity_per_unit": 1.000},  # Cheese Slice (pkt)
        {"product_id": "P020", "ingredient_id": "ING002", "quantity_per_unit": 0.015},  # Onions (kg)
        {"product_id": "P020", "ingredient_id": "ING003", "quantity_per_unit": 0.015},  # Tomatoes (kg)
        {"product_id": "P020", "ingredient_id": "ING025", "quantity_per_unit": 0.010},  # Oil (L)

        # P021: Paneer Roll (6)
        {"product_id": "P021", "ingredient_id": "ING018", "quantity_per_unit": 0.060},  # Atta (kg)
        {"product_id": "P021", "ingredient_id": "ING012", "quantity_per_unit": 0.060},  # Paneer (kg)
        {"product_id": "P021", "ingredient_id": "ING002", "quantity_per_unit": 0.025},  # Onions (kg)
        {"product_id": "P021", "ingredient_id": "ING007", "quantity_per_unit": 0.020},  # Capsicum (kg)
        {"product_id": "P021", "ingredient_id": "ING025", "quantity_per_unit": 0.015},  # Oil (L)
        {"product_id": "P021", "ingredient_id": "ING029", "quantity_per_unit": 0.005},  # Spices (kg)

        # P022: Veg Cutlet (6)
        {"product_id": "P022", "ingredient_id": "ING001", "quantity_per_unit": 0.050},  # Potatoes (kg)
        {"product_id": "P022", "ingredient_id": "ING009", "quantity_per_unit": 0.020},  # Carrots (kg)
        {"product_id": "P022", "ingredient_id": "ING008", "quantity_per_unit": 0.020},  # Cabbage (kg)
        {"product_id": "P022", "ingredient_id": "ING032", "quantity_per_unit": 0.080},  # Bread Crumbs (pkt)
        {"product_id": "P022", "ingredient_id": "ING025", "quantity_per_unit": 0.020},  # Oil (L)
        {"product_id": "P022", "ingredient_id": "ING029", "quantity_per_unit": 0.004},  # Spices (kg)
    ]
    df = pd.DataFrame(recipes_data)
    return df


# ---------------------------------------------------------
# 4. Sales Generation (5,000–10,000 rows)
# ---------------------------------------------------------
def generate_sales(products_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates 6 months of realistic sales transactions across meal periods.
    Columns: date, product_id, quantity_sold, selling_price, meal_period, working_day
    """
    prices_map = dict(zip(products_df["product_id"], products_df["selling_price"]))

    # Products typical to each meal period
    period_offerings = {
        "Morning": [
            ("P001", (25, 60)),  # Masala Chai
            ("P002", (15, 40)),  # Filter Coffee
            ("P007", (15, 35)),  # Poha
            ("P008", (12, 30)),  # Masala Dosa
            ("P009", (15, 35)),  # Idli Sambar
            ("P010", (10, 25)),  # Chole Bhature
            ("P011", (12, 30)),  # Bread Pakora
            ("P005", (15, 35)),  # Samosa
            ("P006", (12, 30)),  # Vada Pav
            ("P004", (8, 20)),   # Fresh Lime Soda
        ],
        "Lunch": [
            ("P012", (20, 50)),  # Veg Thali
            ("P013", (18, 45)),  # Rajma Chawal
            ("P014", (15, 35)),  # Dal Khichdi
            ("P015", (12, 30)),  # Paneer Butter Masala
            ("P016", (14, 32)),  # Paneer Pulao
            ("P017", (16, 38)),  # Veg Biryani
            ("P018", (15, 35)),  # Veg Fried Rice
            ("P001", (20, 45)),  # Chai after lunch
            ("P002", (10, 25)),  # Coffee
            ("P003", (12, 30)),  # Sweet Lassi
            ("P004", (15, 35)),  # Lime Soda
            ("P005", (10, 25)),  # Samosa
            ("P019", (10, 22)),  # Burger
            ("P021", (12, 28)),  # Paneer Roll
        ],
        "Evening": [
            ("P001", (30, 70)),  # Masala Chai (peak evening rush)
            ("P002", (15, 40)),  # Filter Coffee
            ("P003", (10, 25)),  # Sweet Lassi
            ("P004", (12, 30)),  # Lime Soda
            ("P005", (25, 60)),  # Samosa
            ("P006", (20, 50)),  # Vada Pav
            ("P011", (15, 40)),  # Bread Pakora
            ("P019", (15, 35)),  # Aloo Tikki Burger
            ("P020", (12, 30)),  # Veg Cheese Burger
            ("P021", (15, 38)),  # Paneer Roll
            ("P022", (12, 32)),  # Veg Cutlet
            ("P007", (8, 20)),   # Poha
            ("P018", (10, 24)),  # Fried Rice
            ("P017", (8, 20)),   # Biryani
            ("P014", (6, 18)),   # Khichdi
        ]
    }

    sales_records = []

    for day_idx in range(NUM_DAYS):
        current_date = START_DATE + datetime.timedelta(days=day_idx)
        # Weekdays: Mon-Fri (0-4) are working days; Sat-Sun (5-6) are non-working
        is_working_day = current_date.weekday() < 5
        date_str = current_date.strftime("%Y-%m-%d")

        # Demand factor: 1.0 on weekdays, 0.25 to 0.40 on weekends
        demand_factor = random.uniform(0.9, 1.15) if is_working_day else random.uniform(0.25, 0.40)

        for period, items in period_offerings.items():
            for pid, (min_qty, max_qty) in items:
                # Slight probability of occasional item sold out or not prepared that slot
                if random.random() < 0.03:
                    continue

                scaled_min = max(1, int(min_qty * demand_factor))
                scaled_max = max(scaled_min + 1, int(max_qty * demand_factor))
                quantity_sold = random.randint(scaled_min, scaled_max)

                sales_records.append({
                    "date": date_str,
                    "product_id": pid,
                    "quantity_sold": int(quantity_sold),
                    "selling_price": float(prices_map[pid]),
                    "meal_period": period,
                    "working_day": is_working_day
                })

    df = pd.DataFrame(sales_records)
    return df


# ---------------------------------------------------------
# 5. Purchases & Inventory Generation
# ---------------------------------------------------------
def generate_purchases_and_inventory(
    ingredients_df: pd.DataFrame,
    recipes_df: pd.DataFrame,
    sales_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Simulates daily canteen inventory consumption and generates matching purchases.
    Ensures closing_stock = opening_stock + purchased - used for every row.
    
    Inventory columns (strictly 6): date, ingredient_id, opening_stock, purchased, used, closing_stock
    Purchases columns: purchase_id, date, ingredient_id, quantity, total_cost, supplier
    """
    suppliers_by_type = {
        "Dairy": "Annapurna Dairy & Milk Supplies",
        "Produce": "Kisan Sabzi Mandi Co-op",
        "Grains": "Balaji Provisions & Grain Traders",
        "Bakery": "Modern Bakery & Buns Supplies",
        "Beverage": "Metro Wholesale Mart",
        "Oils": "Swastik Oil Mills & Spices",
    }

    def get_supplier(ing_id: str, ing_name: str) -> str:
        if "Milk" in ing_name or "Paneer" in ing_name or "Curd" in ing_name or "Butter" in ing_name or "Cheese" in ing_name:
            return suppliers_by_type["Dairy"]
        elif "Bun" in ing_name or "Bread" in ing_name:
            return suppliers_by_type["Bakery"]
        elif any(veg in ing_name for veg in ["Potatoes", "Onions", "Tomatoes", "Chillies", "Garlic", "Coriander", "Capsicum", "Cabbage", "Carrots", "Lemon"]):
            return suppliers_by_type["Produce"]
        elif "Rice" in ing_name or "Dal" in ing_name or "Rajma" in ing_name or "Chole" in ing_name or "Flour" in ing_name or "Poha" in ing_name:
            return suppliers_by_type["Grains"]
        elif "Tea" in ing_name or "Coffee" in ing_name or "Sugar" in ing_name:
            return suppliers_by_type["Beverage"]
        else:
            return suppliers_by_type["Oils"]

    # Pre-aggregate daily usage of each ingredient from sales * recipe
    # Merge sales with recipes to calculate consumption
    merged = sales_df.merge(recipes_df, on="product_id")
    merged["ingredient_used"] = merged["quantity_sold"] * merged["quantity_per_unit"]
    daily_usage = merged.groupby(["date", "ingredient_id"])["ingredient_used"].sum().unstack(fill_value=0.0)

    all_dates = sorted(sales_df["date"].unique())
    ing_ids = ingredients_df["ingredient_id"].tolist()
    reorder_map = dict(zip(ingredients_df["ingredient_id"], ingredients_df["reorder_level"]))
    cost_map = dict(zip(ingredients_df["ingredient_id"], ingredients_df["purchase_cost"]))
    name_map = dict(zip(ingredients_df["ingredient_id"], ingredients_df["ingredient_name"]))
    shelf_life_map = dict(zip(ingredients_df["ingredient_id"], ingredients_df["shelf_life_days"]))

    # Initial stock: 3x reorder level
    current_stock = {iid: round(reorder_map[iid] * 3.0, 2) for iid in ing_ids}

    inventory_records = []
    purchase_records = []
    purchase_counter = 1

    for date_str in all_dates:
        for iid in ing_ids:
            opening = current_stock[iid]
            used_today = round(float(daily_usage.loc[date_str, iid]) if (date_str in daily_usage.index and iid in daily_usage.columns) else 0.0, 2)
            
            # Decide if purchase is needed
            reorder_lvl = reorder_map[iid]
            shelf_life = shelf_life_map[iid]

            # Fast perishables restock frequently; dry staples order larger batches
            projected_closing = opening - used_today
            needs_restock = projected_closing < (reorder_lvl * 1.2)

            purchased_today = 0.0
            if needs_restock:
                # Order enough to replenish stock up to 3-4x reorder level
                if shelf_life <= 4:
                    # Fresh milk, paneer, buns: frequent small batches
                    batch_qty = round(reorder_lvl * random.uniform(1.8, 2.5), 1)
                elif shelf_life <= 15:
                    # Veggies: medium batches
                    batch_qty = round(reorder_lvl * random.uniform(2.0, 3.0), 1)
                else:
                    # Grains, oil, spices: larger batch
                    batch_qty = round(reorder_lvl * random.uniform(2.5, 4.0), 1)

                purchased_today = batch_qty
                unit_cost = cost_map[iid]
                total_cost = round(purchased_today * unit_cost, 2)
                supplier = get_supplier(iid, name_map[iid])

                purchase_id = f"PUR{purchase_counter:04d}"
                purchase_counter += 1

                purchase_records.append({
                    "purchase_id": purchase_id,
                    "date": date_str,
                    "ingredient_id": iid,
                    "quantity": purchased_today,
                    "total_cost": total_cost,
                    "supplier": supplier
                })

            # Calculate closing stock strictly using formula:
            closing = round(opening + purchased_today - used_today, 2)
            # Update running stock for next day
            current_stock[iid] = max(0.0, closing)

            inventory_records.append({
                "date": date_str,
                "ingredient_id": iid,
                "opening_stock": opening,
                "purchased": purchased_today,
                "used": used_today,
                "closing_stock": closing
            })

    inventory_df = pd.DataFrame(inventory_records)
    purchases_df = pd.DataFrame(purchase_records)
    return purchases_df, inventory_df


# ---------------------------------------------------------
# 6. Waste Generation (1,000–2,000 rows)
# ---------------------------------------------------------
def generate_waste(
    products_df: pd.DataFrame,
    ingredients_df: pd.DataFrame,
    sales_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Generates realistic food waste tracking data.
    Columns: date, waste_type, item_id, quantity, unit, reason, waste_cost
    waste_type: 'Raw Material' or 'Prepared Food'
    reason: 'Spoilage', 'Expiry', 'Unsold', 'Leftover'
    """
    all_dates = sorted(sales_df["date"].unique())
    waste_records = []

    ing_unit_map = dict(zip(ingredients_df["ingredient_id"], ingredients_df["unit"]))
    ing_cost_map = dict(zip(ingredients_df["ingredient_id"], ingredients_df["purchase_cost"]))
    ing_shelf_map = dict(zip(ingredients_df["ingredient_id"], ingredients_df["shelf_life_days"]))
    
    prod_cost_map = dict(zip(products_df["product_id"], products_df["unit_cost"]))
    
    # High-risk perishable ingredients
    perishable_ings = [
        "ING003",  # Tomatoes
        "ING004",  # Green Chillies
        "ING006",  # Coriander Leaves
        "ING007",  # Capsicum
        "ING010",  # Lemon
        "ING011",  # Fresh Milk
        "ING012",  # Paneer
        "ING013",  # Curd
        "ING030",  # Burger Buns
        "ING031",  # Pav Buns
        "ING032",  # Bread Loaf
    ]
    # Other ingredients that occasionally have minor waste
    other_ings = ["ING001", "ING002", "ING008", "ING009", "ING014"]

    # Products with daily leftover/unsold risks
    snack_products = ["P005", "P006", "P007", "P011", "P019", "P020", "P021", "P022"]
    meal_products = ["P012", "P013", "P014", "P015", "P016", "P017", "P018"]

    for date_str in all_dates:
        # Generate 6 to 10 waste events per day (average ~7.8 per day -> ~1,400 rows total)
        num_raw_waste = random.randint(3, 5)
        num_prepared_waste = random.randint(3, 5)

        # 1. Raw Material Waste (Spoilage or Expiry)
        chosen_ings = random.sample(perishable_ings, k=min(num_raw_waste, len(perishable_ings)))
        for iid in chosen_ings:
            reason = "Expiry" if ing_shelf_map[iid] <= 3 and random.random() < 0.4 else "Spoilage"
            unit = ing_unit_map[iid]

            if unit in ["kg", "L"]:
                qty = round(random.uniform(0.3, 1.8), 2)
            else:  # pkt
                qty = float(random.randint(1, 3))

            cost = round(qty * ing_cost_map[iid], 2)

            waste_records.append({
                "date": date_str,
                "waste_type": "Raw Material",
                "item_id": iid,
                "quantity": qty,
                "unit": unit,
                "reason": reason,
                "waste_cost": cost
            })

        # 2. Prepared Food Waste (Unsold or Leftover)
        chosen_prods = random.sample(snack_products, k=2) + random.sample(meal_products, k=num_prepared_waste - 2)
        for pid in chosen_prods:
            reason = random.choice(["Unsold", "Leftover"])
            qty = float(random.randint(2, 8))
            unit = "pcs" if pid in snack_products else "portions"
            cost = round(qty * prod_cost_map[pid], 2)

            waste_records.append({
                "date": date_str,
                "waste_type": "Prepared Food",
                "item_id": pid,
                "quantity": qty,
                "unit": unit,
                "reason": reason,
                "waste_cost": cost
            })

    df = pd.DataFrame(waste_records)
    return df


# ---------------------------------------------------------
# 7. Dataset Validation
# ---------------------------------------------------------
def validate_datasets(datasets: Dict[str, pd.DataFrame]) -> None:
    """
    Validates row ranges, column specifications, and foreign-key relationships.
    Raises AssertionError if any validation fails.
    """
    print("\n" + "=" * 65)
    print("RUNNING INTEGRITY & RELATIONSHIP VALIDATIONS")
    print("=" * 65)

    specs = {
        "products.csv": (20, 25, ["product_id", "product_name", "category", "selling_price", "unit_cost"]),
        "ingredients.csv": (30, 40, ["ingredient_id", "ingredient_name", "unit", "purchase_cost", "shelf_life_days", "reorder_level"]),
        "recipes.csv": (100, 150, ["product_id", "ingredient_id", "quantity_per_unit"]),
        "sales.csv": (5000, 10000, ["date", "product_id", "quantity_sold", "selling_price", "meal_period", "working_day"]),
        "inventory.csv": (3000, 6000, ["date", "ingredient_id", "opening_stock", "purchased", "used", "closing_stock"]),
        "waste.csv": (1000, 2000, ["date", "waste_type", "item_id", "quantity", "unit", "reason", "waste_cost"]),
        "purchases.csv": (500, 1000, ["purchase_id", "date", "ingredient_id", "quantity", "total_cost", "supplier"]),
    }

    # 1. Row range and column checks
    for fname, (min_rows, max_rows, expected_cols) in specs.items():
        df = datasets[fname]
        row_count = len(df)
        assert min_rows <= row_count <= max_rows, (
            f"Row count validation failed for {fname}: {row_count} rows not in range [{min_rows}, {max_rows}]"
        )
        assert list(df.columns) == expected_cols, (
            f"Columns mismatch in {fname}.\nExpected: {expected_cols}\nFound: {list(df.columns)}"
        )
        print(f"  [PASS] {fname:16s} : {row_count:6,d} rows (Range [{min_rows}, {max_rows}]) - Schema OK")

    # 2. Foreign Key & Domain Checks
    prod_ids = set(datasets["products.csv"]["product_id"])
    ing_ids = set(datasets["ingredients.csv"]["ingredient_id"])

    # Unique Primary Keys
    assert len(prod_ids) == len(datasets["products.csv"]), "Duplicate product_id detected!"
    assert len(ing_ids) == len(datasets["ingredients.csv"]), "Duplicate ingredient_id detected!"
    assert len(set(datasets["purchases.csv"]["purchase_id"])) == len(datasets["purchases.csv"]), "Duplicate purchase_id detected!"

    # Recipes foreign keys
    assert set(datasets["recipes.csv"]["product_id"]).issubset(prod_ids), "Invalid product_id in recipes.csv!"
    assert set(datasets["recipes.csv"]["ingredient_id"]).issubset(ing_ids), "Invalid ingredient_id in recipes.csv!"

    # Sales foreign keys
    assert set(datasets["sales.csv"]["product_id"]).issubset(prod_ids), "Invalid product_id in sales.csv!"

    # Inventory foreign keys & math formula
    assert set(datasets["inventory.csv"]["ingredient_id"]).issubset(ing_ids), "Invalid ingredient_id in inventory.csv!"
    inv_df = datasets["inventory.csv"]
    math_diff = np.abs((inv_df["opening_stock"] + inv_df["purchased"] - inv_df["used"]) - inv_df["closing_stock"])
    assert (math_diff < 0.05).all(), "inventory.csv formula mismatch: closing_stock != opening_stock + purchased - used!"

    # Purchases foreign keys
    assert set(datasets["purchases.csv"]["ingredient_id"]).issubset(ing_ids), "Invalid ingredient_id in purchases.csv!"

    # Waste validation
    waste_df = datasets["waste.csv"]
    valid_waste_types = {"Raw Material", "Prepared Food"}
    valid_reasons = {"Spoilage", "Expiry", "Unsold", "Leftover"}
    assert set(waste_df["waste_type"]).issubset(valid_waste_types), "Invalid waste_type found in waste.csv!"
    assert set(waste_df["reason"]).issubset(valid_reasons), "Invalid reason found in waste.csv!"

    raw_items = set(waste_df[waste_df["waste_type"] == "Raw Material"]["item_id"])
    prepared_items = set(waste_df[waste_df["waste_type"] == "Prepared Food"]["item_id"])
    assert raw_items.issubset(ing_ids), "Raw material waste item_id must exist in ingredients.csv!"
    assert prepared_items.issubset(prod_ids), "Prepared food waste item_id must exist in products.csv!"

    print("  [PASS] All Foreign Key relationships verified successfully.")
    print("  [PASS] All Primary Key uniqueness checks passed.")
    print("  [PASS] inventory.csv mathematical identity (closing = opening + purchased - used) verified.")
    print("  [PASS] waste.csv item_id & categorical values strictly validated.")
    print("=" * 65 + "\n")


# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------
def main() -> None:
    """Generates all 7 datasets, saves to data/, and validates."""
    print("Starting CanteenWise Synthetic Data Generation...")
    set_seed(RANDOM_SEED)

    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Target data directory: {DATA_DIR}")

    # Generate each dataset
    products_df = create_products()
    ingredients_df = create_ingredients()
    recipes_df = create_recipes()
    sales_df = generate_sales(products_df)
    purchases_df, inventory_df = generate_purchases_and_inventory(ingredients_df, recipes_df, sales_df)
    waste_df = generate_waste(products_df, ingredients_df, sales_df)

    datasets = {
        "products.csv": products_df,
        "ingredients.csv": ingredients_df,
        "recipes.csv": recipes_df,
        "sales.csv": sales_df,
        "inventory.csv": inventory_df,
        "waste.csv": waste_df,
        "purchases.csv": purchases_df,
    }

    # Save to CSV files
    for filename, df in datasets.items():
        file_path = os.path.join(DATA_DIR, filename)
        df.to_csv(file_path, index=False)

    # Validate all requirements
    validate_datasets(datasets)

    # Print summary table
    print("=" * 65)
    print("CANTEENWISE DATA GENERATION SUMMARY")
    print("=" * 65)
    print(f"{'Filename':<18} | {'Rows':<8} | {'Columns':<8} | {'Status':<10}")
    print("-" * 65)
    for filename, df in datasets.items():
        print(f"{filename:<18} | {len(df):<8,d} | {len(df.columns):<8} | {'CREATED':<10}")
    print("=" * 65)
    print("Data generation completed successfully!\n")


if __name__ == "__main__":
    main()
