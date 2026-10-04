"""
analysis/profit_analysis.py
Computes true item-level profitability and financial returns.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
from utils.csv_handler import CSVHandler

class ProfitAnalyzer:
    def __init__(self, data_dir="data"):
        if not os.path.isabs(data_dir):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            data_dir = os.path.join(base_dir, data_dir)
        self.data_dir = data_dir
        self.sales_handler = CSVHandler(os.path.join(data_dir, "sales.csv"), id_column=None)
        self.products_handler = CSVHandler(os.path.join(data_dir, "products.csv"), id_column="product_id")
        self.waste_handler = CSVHandler(os.path.join(data_dir, "waste.csv"), id_column=None)

    def calculate_item_profitability(self) -> pd.DataFrame:
        """
        Calculates net profit per menu item:
        Net Profit = Gross Revenue - (Ingredient Production Cost + Waste Cost)
        """
        sales_df = self.sales_handler.load()
        products_df = self.products_handler.load()
        waste_df = self.waste_handler.load()

        # 1. Aggregate Sales Revenue and Total Units Sold per Product
        sales_summary = sales_df.groupby("product_id").agg(
            total_units_sold=("quantity_sold", "sum"),
            total_revenue=("selling_price", lambda x: (x * sales_df.loc[x.index, "quantity_sold"]).sum())
        ).reset_index()

        # 2. Merge with Product Master for unit costs
        profit_df = sales_summary.merge(products_df[["product_id", "product_name", "category", "unit_cost"]], on="product_id", how="inner")
        
        # Total Production Ingredient Cost = Units Sold * Baseline Unit Cost
        profit_df["total_ingredient_cost"] = profit_df["total_units_sold"] * profit_df["unit_cost"]

        # 3. Filter and aggregate Prepared Food Waste Cost per product
        prepared_waste = waste_df[waste_df["waste_type"] == "Prepared Food"]
        waste_summary = prepared_waste.groupby("item_id")["waste_cost"].sum().reset_index().rename(columns={"item_id": "product_id", "waste_cost": "total_waste_cost"})

        # Merge waste costs (fill missing with 0)
        profit_df = profit_df.merge(waste_summary, on="product_id", how="left").fillna({"total_waste_cost": 0.0})

        # 4. Calculate Net Profit and Profit Margin Percentage
        profit_df["net_profit"] = profit_df["total_revenue"] - (profit_df["total_ingredient_cost"] + profit_df["total_waste_cost"])
        
        profit_df["profit_margin_pct"] = np.where(
            profit_df["total_revenue"] > 0,
            (profit_df["net_profit"] / profit_df["total_revenue"]) * 100,
            0.0
        )

        profit_df = profit_df.sort_values(by="net_profit", ascending=False).reset_index(drop=True)
        return profit_df

if __name__ == "__main__":
    analyzer = ProfitAnalyzer()
    df_profit = analyzer.calculate_item_profitability()
    print("--- Item Profitability Summary (Top 5) ---")
    print(df_profit[["product_name", "total_revenue", "net_profit", "profit_margin_pct"]].head())