"""
analysis/insight_engine.py
Rule-Based Insight and Recommendation Engine for CanteenWise.
Scans analytical dataframes using conditional logic to generate automated alerts.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from analysis.consumption_analysis import ConsumptionAnalyzer
from analysis.profit_analysis import ProfitAnalyzer

class InsightEngine:
    def __init__(self, data_dir="data"):
        if not os.path.isabs(data_dir):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            data_dir = os.path.join(base_dir, data_dir)
        self.data_dir = data_dir
        self.consumption_analyzer = ConsumptionAnalyzer(data_dir)
        self.profit_analyzer = ProfitAnalyzer(data_dir)

    def generate_insights(self) -> list:
        """
        Runs rule-based checks on consumption variance and item profitability
        to compile a list of actionable business alerts and recommendations.
        """
        insights = []
        
        # 1. Fetch analytical datasets
        variance_df = self.consumption_analyzer.calculate_consumption_variance()
        profit_df = self.profit_analyzer.calculate_item_profitability()

        # 2. Rule: Excessive Consumption Variance Check (> 15% overuse)
        high_variance_items = variance_df[variance_df["variance_percentage"] > 15.0]
        for _, row in high_variance_items.iterrows():
            insights.append({
                "category": "Inventory Waste / Variance",
                "priority": "High",
                "item": row["ingredient_name"],
                "message": f"High usage variance detected for {row['ingredient_name']}. Actual usage exceeds expected recipe calculation by {row['variance_percentage']:.1f}% (Cost impact: Rs. {row['variance_cost']:.2f}).",
                "action": "Check for unrecorded kitchen spillage, over-portioning, or missing inventory logs."
            })

        # 3. Rule: Low or Negative Profit Margin Check (< 10% margin or negative net profit)
        low_profit_items = profit_df[profit_df["profit_margin_pct"] < 10.0]
        for _, row in low_profit_items.iterrows():
            priority = "Critical" if row["net_profit"] < 0 else "Medium"
            insights.append({
                "category": "Profit Optimization",
                "priority": priority,
                "item": row["product_name"],
                "message": f"'{row['product_name']}' has a low/negative profit margin of {row['profit_margin_pct']:.1f}% (Net Profit: Rs. {row['net_profit']:.2f}).",
                "action": "Review ingredient production costs, reduce prepared food waste, or adjust the selling price."
            })

        # 4. Rule: Top Revenue Driver Identification
        if not profit_df.empty:
            top_earner = profit_df.iloc[0]
            insights.append({
                "category": "Top Performer",
                "priority": "Info",
                "item": top_earner["product_name"],
                "message": f"'{top_earner['product_name']}' is your top-performing item, generating Rs. {top_earner['total_revenue']:.2f} in gross revenue.",
                "action": "Ensure stock levels for its underlying ingredients are always prioritized."
            })

        return insights

if __name__ == "__main__":
    engine = InsightEngine()
    alerts = engine.generate_insights()
    print(f"--- Rule-Based Insight Engine Generated {len(alerts)} Active Alerts ---")
    for idx, alert in enumerate(alerts[:3], 1):
        print(f"\n{idx}. [{alert['priority']}] {alert['category']} - {alert['item']}")
        print(f"   Alert: {alert['message']}")
        print(f"   Recommendation: {alert['action']}")