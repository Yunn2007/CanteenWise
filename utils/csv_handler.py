"""
utils/csv_handler.py
Reusable, object-oriented CSV handling module for CanteenWise.
Built with pandas and native Python file handling.
"""

import os
from typing import Any, Dict, List, Optional
import pandas as pd


class CSVHandlerError(Exception):
    """Base exception class for CSVHandler errors."""
    pass


class MissingFileError(CSVHandlerError):
    """Raised when the specified CSV file cannot be found."""
    pass


class SchemaValidationError(CSVHandlerError):
    """Raised when a CSV or record does not match the expected schema/columns."""
    pass


class DuplicateIDError(CSVHandlerError):
    """Raised when attempting to add a record with an ID that already exists."""
    pass


class RecordNotFoundError(CSVHandlerError):
    """Raised when a record with the specified ID is not found."""
    pass


class CSVHandler:
    """
    Reusable CSV Handler for CanteenWise backend operations.
    
    Provides simple, robust CRUD operations, schema validation,
    and graceful error handling for CSV datasets.
    """

    def __init__(
        self,
        file_path: str,
        id_column: Optional[str] = None,
        required_columns: Optional[List[str]] = None,
    ):
        """
        Initializes the CSVHandler.

        :param file_path: Path to the target CSV file.
        :param id_column: Optional primary key / unique ID column name.
        :param required_columns: Optional list of column names that must exist in the CSV.
        """
        self.file_path = file_path
        self.id_column = id_column
        self.required_columns = required_columns
        self._df: Optional[pd.DataFrame] = None

    @property
    def file_exists(self) -> bool:
        """Check whether the target CSV file exists on disk."""
        return os.path.exists(self.file_path)

    def load(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Loads the CSV into a pandas DataFrame and caches it in memory.
        
        :param force_reload: If True, reloads from disk even if already cached.
        :return: Loaded pandas DataFrame.
        :raises MissingFileError: If the file does not exist.
        :raises SchemaValidationError: If required columns are missing.
        """
        if self._df is not None and not force_reload:
            return self._df.copy()

        if not self.file_exists:
            raise MissingFileError(f"CSV file not found at: '{self.file_path}'")

        try:
            df = pd.read_csv(self.file_path)
        except Exception as e:
            raise CSVHandlerError(f"Failed to read CSV '{self.file_path}': {str(e)}") from e

        if self.required_columns:
            self.validate_schema(df, self.required_columns)

        self._df = df
        return self._df.copy()

    def save(self, df: Optional[pd.DataFrame] = None) -> bool:
        """
        Saves a DataFrame to disk. If no DataFrame is passed, saves the cached DataFrame.

        :param df: Optional DataFrame to save. If None, saves self._df.
        :return: True if save succeeded.
        :raises CSVHandlerError: If there is no data to save or writing fails.
        """
        if df is not None:
            self._df = df.copy()

        if self._df is None:
            raise CSVHandlerError("No DataFrame loaded or provided to save.")

        try:
            # Ensure the directory exists
            parent_dir = os.path.dirname(self.file_path)
            if parent_dir and not os.path.exists(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            self._df.to_csv(self.file_path, index=False)
            return True
        except Exception as e:
            raise CSVHandlerError(f"Failed to write CSV '{self.file_path}': {str(e)}") from e

    def validate_schema(
        self,
        df: Optional[pd.DataFrame] = None,
        required_columns: Optional[List[str]] = None,
    ) -> bool:
        """
        Validates that a DataFrame contains all expected columns.

        :param df: DataFrame to validate. If None, uses loaded DataFrame.
        :param required_columns: List of required column names. If None, uses self.required_columns.
        :return: True if schema is valid.
        :raises SchemaValidationError: If any required column is missing.
        """
        target_df = df if df is not None else self.load()
        expected = required_columns if required_columns is not None else self.required_columns

        if not expected:
            return True

        missing_cols = [col for col in expected if col not in target_df.columns]
        if missing_cols:
            raise SchemaValidationError(
                f"Schema validation failed for '{self.file_path}'. "
                f"Missing required columns: {missing_cols}. "
                f"Found columns: {list(target_df.columns)}"
            )
        return True

    def read_records(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Reads records from the CSV as a list of Python dictionaries.
        Supports optional key-value equality filtering.

        :param filters: Optional dictionary of {column_name: expected_value}.
        :return: List of record dictionaries.
        """
        df = self.load()

        if filters:
            for col, val in filters.items():
                if col in df.columns:
                    df = df[df[col] == val]
                else:
                    raise SchemaValidationError(
                        f"Cannot filter by '{col}': column not found in '{self.file_path}'"
                    )

        return df.to_dict(orient="records")

    def id_exists(self, record_id: Any) -> bool:
        """
        Checks whether a record with the given ID exists.

        :param record_id: ID value to check.
        :return: True if ID exists, False otherwise.
        :raises CSVHandlerError: If id_column was not specified.
        """
        if not self.id_column:
            raise CSVHandlerError(
                f"Cannot check ID existence: 'id_column' not configured for '{self.file_path}'"
            )

        df = self.load()
        # Ensure type comparison works across string/numeric formats
        matches = df[df[self.id_column].astype(str) == str(record_id)]
        return len(matches) > 0

    def get_record_by_id(self, record_id: Any) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single record dictionary by its primary ID.

        :param record_id: ID value to look up.
        :return: Dictionary of the matching record, or None if not found.
        """
        if not self.id_column:
            raise CSVHandlerError(
                f"Cannot get record by ID: 'id_column' not configured for '{self.file_path}'"
            )

        df = self.load()
        matches = df[df[self.id_column].astype(str) == str(record_id)]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()

    def add_record(self, record: Dict[str, Any]) -> bool:
        """
        Appends a new record to the CSV file.
        Validates required schema and ensures unique ID if id_column is configured.

        :param record: Dictionary representing the new record.
        :return: True if added and saved successfully.
        :raises DuplicateIDError: If the ID already exists.
        :raises SchemaValidationError: If required columns are missing from the record.
        """
        df = self.load()

        # Validate schema for the record
        if self.required_columns:
            missing_keys = [col for col in self.required_columns if col not in record]
            if missing_keys:
                raise SchemaValidationError(
                    f"Cannot add record: missing required fields {missing_keys}"
                )

        # Check unique ID constraint
        if self.id_column:
            new_id = record.get(self.id_column)
            if new_id is None:
                raise SchemaValidationError(
                    f"Record must contain ID column '{self.id_column}'"
                )
            if self.id_exists(new_id):
                raise DuplicateIDError(
                    f"Record with {self.id_column}='{new_id}' already exists in '{self.file_path}'"
                )

        new_row_df = pd.DataFrame([record])
        updated_df = pd.concat([df, new_row_df], ignore_index=True)
        return self.save(updated_df)

    def update_record(self, record_id: Any, updated_fields: Dict[str, Any]) -> bool:
        """
        Updates fields of an existing record identified by its ID.

        :param record_id: ID of the record to update.
        :param updated_fields: Dictionary of field names and their new values.
        :return: True if updated and saved successfully.
        :raises RecordNotFoundError: If no record matches the ID.
        :raises SchemaValidationError: If updated_fields contain unknown columns.
        """
        if not self.id_column:
            raise CSVHandlerError(
                f"Cannot update record: 'id_column' not configured for '{self.file_path}'"
            )

        df = self.load()
        mask = df[self.id_column].astype(str) == str(record_id)
        if not mask.any():
            raise RecordNotFoundError(
                f"Record with {self.id_column}='{record_id}' not found in '{self.file_path}'"
            )

        # Check that updated fields are valid columns
        invalid_cols = [col for col in updated_fields if col not in df.columns]
        if invalid_cols:
            raise SchemaValidationError(
                f"Cannot update: unknown column(s) {invalid_cols} in '{self.file_path}'"
            )

        for col, val in updated_fields.items():
            df.loc[mask, col] = val

        return self.save(df)

    def delete_record(self, record_id: Any) -> bool:
        """
        Deletes a record matching the given ID.

        :param record_id: ID of the record to delete.
        :return: True if deleted and saved successfully.
        :raises RecordNotFoundError: If no record matches the ID.
        """
        if not self.id_column:
            raise CSVHandlerError(
                f"Cannot delete record: 'id_column' not configured for '{self.file_path}'"
            )

        df = self.load()
        mask = df[self.id_column].astype(str) == str(record_id)
        if not mask.any():
            raise RecordNotFoundError(
                f"Record with {self.id_column}='{record_id}' not found in '{self.file_path}'"
            )

        updated_df = df[~mask].reset_index(drop=True)
        return self.save(updated_df)

    def get_row_count(self) -> int:
        """Returns the total number of records currently loaded."""
        df = self.load()
        return len(df)

    def to_dataframe(self) -> pd.DataFrame:
        """Returns a copy of the underlying pandas DataFrame."""
        return self.load()

    def __repr__(self) -> str:
        return f"<CSVHandler file='{self.file_path}' id_column='{self.id_column}' records={self.get_row_count() if self.file_exists else 'not_loaded'}>"
