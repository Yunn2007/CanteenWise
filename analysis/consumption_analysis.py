"""
analysis/consumption_analysis.py
Calculates Expected vs. Actual Consumption variance using Pandas and NumPy.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from utils.csv_handler import CSVHandler

class ConsumptionAnalyzer:
    def __init__(self, data_dir="data"):
        # Resolve data_dir relative to project root if relative path provided
        if not os.path.isabs(data_dir):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            data_dir = os.path.join(base_dir, data_dir)
        self.data_dir = data_dir
        self.sales_handler = CSVHandler(os.path.join(data_dir, "sales.csv"), id_column=None)
        self.recipes_handler = CSVHandler(os.path.join(data_dir, "recipes.csv"), id_column=None)
        self.inventory_handler = CSVHandler(os.path.join(data_dir, "inventory.csv"), id_column=None)
        self.ingredients_handler = CSVHandler(os.path.join(data_dir, "ingredients.csv"), id_column="ingredient_id")

    def calculate_consumption_variance(self) -> pd.DataFrame:
        """
        Merges sales, recipes, and inventory data to compute theoretical (expected)
        vs. actual raw material consumption and variance percentages.
        """
        sales_df = self.sales_handler.load()
        recipes_df = self.recipes_handler.load()
        inventory_df = self.inventory_handler.load()
        ingredients_df = self.ingredients_handler.load()

        # 1. Calculate Expected Usage: Sum(quantity_sold * quantity_per_unit) per ingredient across all dates
        sales_recipe_merged = sales_df.merge(recipes_df, on="product_id", how="inner")
        sales_recipe_merged["expected_usage"] = sales_recipe_merged["quantity_sold"] * sales_recipe_merged["quantity_per_unit"]
        
        expected_grouped = sales_recipe_merged.groupby("ingredient_id")["expected_usage"].sum().reset_index()

        # 2. Calculate Actual Usage: Sum of 'used' column from inventory ledger per ingredient
        actual_grouped = inventory_df.groupby("ingredient_id")["used"].sum().reset_index().rename(columns={"used": "actual_usage"})

        # 3. Merge Expected and Actual
        variance_df = pd.merge(expected_grouped, actual_grouped, on="ingredient_id", how="inner")
        
        # Merge with ingredient master for names and units
        variance_df = variance_df.merge(ingredients_df[["ingredient_id", "ingredient_name", "unit", "purchase_cost"]], on="ingredient_id", how="left")

        # 4. Compute Variance and Variance Percentage using NumPy
        variance_df["absolute_variance"] = variance_df["actual_usage"] - variance_df["expected_usage"]
        
        # Avoid division by zero using np.where
        variance_df["variance_percentage"] = np.where(
            variance_df["expected_usage"] > 0,
            (variance_df["absolute_variance"] / variance_df["expected_usage"]) * 100,
            0.0
        )
        
        # Calculate financial cost of variance
        variance_df["variance_cost"] = variance_df["absolute_variance"] * variance_df["purchase_cost"]

        # Sort by highest absolute variance percentage
        variance_df = variance_df.sort_values(by="variance_percentage", ascending=False).reset_index(drop=True)
        return variance_df

if __name__ == "__main__":
    analyzer = ConsumptionAnalyzer()
    df_var = analyzer.calculate_consumption_variance()
    print("--- Expected vs Actual Consumption Variance (Top 5) ---")
    print(df_var[["ingredient_name", "expected_usage", "actual_usage", "variance_percentage"]].head())
