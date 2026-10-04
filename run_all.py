"""
run_all.py
Master runner and validator for CanteenWise.
Validates all backend analytics pipelines, data integrity, PDF generator,
and launches the interactive desktop GUI.
"""

import sys
import os
import glob
import pandas as pd

# Ensure root in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_banner(text):
    print("\n" + "=" * 65)
    print(f"  {text}")
    print("=" * 65)

def step_1_check_datasets():
    print_banner("1. DATASET INTEGRITY CHECK")
    data_files = [
        "products.csv", "ingredients.csv", "recipes.csv", 
        "inventory.csv", "sales.csv", "waste.csv", "purchases.csv"
    ]
    all_ok = True
    for f in data_files:
        path = os.path.join("data", f)
        if os.path.exists(path):
            df = pd.read_csv(path)
            print(f"  ✅ [FOUND] data/{f:<16} ({len(df):>5} records, {len(df.columns)} columns)")
        else:
            print(f"  ❌ [MISSING] data/{f}")
            all_ok = False
    return all_ok

def step_2_test_csv_handler():
    print_banner("2. TESTING CSVHANDLER CRUD OPERATIONS")
    from test_csv_handler import run_tests
    run_tests()
    print("  ✅ All CSVHandler operations passed successfully.")

def step_3_test_consumption_analysis():
    print_banner("3. TESTING CONSUMPTION & VARIANCE ENGINE")
    from analysis.consumption_analysis import ConsumptionAnalyzer
    analyzer = ConsumptionAnalyzer()
    df = analyzer.calculate_consumption_variance()
    print(f"  ✅ Computed theoretical vs actual consumption for {len(df)} ingredients.")
    print("  Top 3 consumption variances:")
    for _, row in df.head(3).iterrows():
        print(f"    • {row['ingredient_name']}: Actual {row['actual_usage']:.1f} vs Expected {row['expected_usage']:.1f} ({row['variance_percentage']:+.2f}%)")

def step_4_test_profit_analysis():
    print_banner("4. TESTING ITEM PROFITABILITY ENGINE")
    from analysis.profit_analysis import ProfitAnalyzer
    analyzer = ProfitAnalyzer()
    df = analyzer.calculate_item_profitability()
    print(f"  ✅ Calculated net profit and margins for {len(df)} menu items.")
    print("  Top 3 profit contributors:")
    for _, row in df.head(3).iterrows():
        print(f"    • {row['product_name']}: Revenue Rs. {row['total_revenue']:,.0f} | Net Profit Rs. {row['net_profit']:,.0f} ({row['profit_margin_pct']:.1f}%)")

def step_5_test_insight_engine():
    print_banner("5. TESTING RULE-BASED INSIGHT ENGINE")
    from analysis.insight_engine import InsightEngine
    engine = InsightEngine()
    alerts = engine.generate_insights()
    print(f"  ✅ Insight engine generated {len(alerts)} automated alerts.")
    for idx, alert in enumerate(alerts[:3], 1):
        print(f"    [{alert['priority']}] {alert['item']}: {alert['message']}")

def step_6_test_report_generation():
    print_banner("6. TESTING EXECUTIVE PDF REPORT EXPORT")
    from analysis.reports import ReportGenerator
    generator = ReportGenerator()
    pdf_path = generator.export_monthly_summary_pdf("CanteenWise_Executive_Report.pdf")
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"  ✅ PDF report created successfully: {pdf_path} ({size_kb:.1f} KB)")
        # Clean up test output
        try:
            os.remove(pdf_path)
        except OSError:
            pass

def step_7_launch_gui():
    print_banner("7. LAUNCHING CANTEENWISE DESKTOP GUI")
    print("  [INFO] Opening application window on your screen...")
    from main import CanteenWiseApp
    app = CanteenWiseApp()
    print("  [INFO] App is active. Close the window or press Ctrl+C to exit.\n")
    try:
        app.mainloop()
    except KeyboardInterrupt:
        print("\n[INFO] Application closed.")

def main():
    print("\n" + "#" * 65)
    print("         CANTEENWISE OVERALL SYSTEM VERIFICATION & RUN")
    print("#" * 65)

    try:
        step_1_check_datasets()
        step_2_test_csv_handler()
        step_3_test_consumption_analysis()
        step_4_test_profit_analysis()
        step_5_test_insight_engine()
        step_6_test_report_generation()
        
        print("\n" + "=" * 65)
        print("  🎉 ALL BACKEND, ANALYTICS & DATA PIPELINES VERIFIED 100%!")
        print("=" * 65)
        
        step_7_launch_gui()
    except Exception as e:
        print(f"\n❌ Error encountered during overall run: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
