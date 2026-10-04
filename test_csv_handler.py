"""
test_csv_handler.py
Demonstration and unit test for utils/csv_handler.py.
Verifies all CRUD operations, schema validations, error handling, and file safety.
"""

import os
import shutil
import tempfile
import pandas as pd
from utils.csv_handler import (
    CSVHandler,
    MissingFileError,
    SchemaValidationError,
    DuplicateIDError,
    RecordNotFoundError,
)


def run_tests():
    print("=" * 65)
    print("TESTING CSVHANDLER WITH REALISTIC CANTEENWISE OPERATIONS")
    print("=" * 65)

    # 1. Load actual generated products.csv
    products_file = os.path.join("data", "products.csv")
    handler = CSVHandler(
        file_path=products_file,
        id_column="product_id",
        required_columns=["product_id", "product_name", "category", "selling_price", "unit_cost"]
    )

    df = handler.load()
    print(f"1. [PASS] Loaded '{products_file}' successfully: {len(df)} records found.")

    # 2. Test schema validation on valid and invalid schemas
    handler.validate_schema()
    print("2. [PASS] Schema validation on valid DataFrame succeeded.")

    try:
        handler.validate_schema(required_columns=["non_existent_col"])
        assert False, "Should have raised SchemaValidationError"
    except SchemaValidationError as e:
        print(f"3. [PASS] Gracefully caught expected schema error: {e}")

    # 3. Test read_records and filtering
    beverages = handler.read_records(filters={"category": "Beverages"})
    print(f"4. [PASS] Filtered records by category='Beverages': {len(beverages)} items found.")
    for item in beverages[:2]:
        print(f"     -> {item['product_id']}: {item['product_name']} (Rs. {item['selling_price']})")

    # 4. Test ID lookup and existence check
    assert handler.id_exists("P001") is True
    assert handler.id_exists("P999") is False
    p1 = handler.get_record_by_id("P001")
    print(f"5. [PASS] ID check and lookup for 'P001': Found {p1['product_name']}.")

    # 5. Test CRUD operations on an isolated temporary copy
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_csv = os.path.join(tmpdir, "test_products.csv")
        shutil.copyfile(products_file, temp_csv)

        test_handler = CSVHandler(
            file_path=temp_csv,
            id_column="product_id",
            required_columns=["product_id", "product_name", "category", "selling_price", "unit_cost"]
        )

        initial_count = test_handler.get_row_count()

        # A: Add record
        new_item = {
            "product_id": "P099",
            "product_name": "Cold Coffee with Ice Cream",
            "category": "Beverages",
            "selling_price": 50.0,
            "unit_cost": 22.0
        }
        test_handler.add_record(new_item)
        assert test_handler.get_row_count() == initial_count + 1
        assert test_handler.id_exists("P099") is True
        print(f"6. [PASS] Add Record: Successfully inserted 'P099' ({new_item['product_name']}).")

        # B: Duplicate ID check
        try:
            test_handler.add_record(new_item)
            assert False, "Should have raised DuplicateIDError"
        except DuplicateIDError as e:
            print(f"7. [PASS] Duplicate ID Prevention: Caught expected error: {e}")

        # C: Update record
        test_handler.update_record("P099", {"selling_price": 55.0, "unit_cost": 24.0})
        updated_item = test_handler.get_record_by_id("P099")
        assert updated_item["selling_price"] == 55.0
        print(f"8. [PASS] Update Record: 'P099' selling_price updated to {updated_item['selling_price']}.")

        # D: Delete record
        test_handler.delete_record("P099")
        assert test_handler.id_exists("P099") is False
        assert test_handler.get_row_count() == initial_count
        print("9. [PASS] Delete Record: 'P099' successfully deleted, row count restored.")

        # E: Update nonexistent record check
        try:
            test_handler.update_record("P999", {"selling_price": 100.0})
            assert False, "Should have raised RecordNotFoundError"
        except RecordNotFoundError as e:
            print(f"10. [PASS] Nonexistent Record Check: Caught expected error: {e}")

    # 6. Test missing file error handling
    missing_handler = CSVHandler(file_path="non_existent_dir/missing.csv")
    try:
        missing_handler.load()
        assert False, "Should have raised MissingFileError"
    except MissingFileError as e:
        print(f"11. [PASS] Missing File Handling: Caught expected error: {e}")

    print("=" * 65)
    print("ALL CSVHANDLER TESTS PASSED SUCCESSFULLY!")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    run_tests()
