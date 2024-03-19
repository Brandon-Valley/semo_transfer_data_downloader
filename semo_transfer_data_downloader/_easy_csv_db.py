from pathlib import Path
from sys import displayhook
import pandas as pd
from pandas import DataFrame
import sqlite3
import json
from pathlib import Path
from typing import Dict, Optional
from tabulate import tabulate


class EasyCsvDb:
    def __init__(self):
        self.csv_path_by_table_name: Dict[str, Path] = {}

        # Connect to SQLite Database (In-memory)
        self.sqlite_connection = sqlite3.connect(":memory:")

    def query(self, query: str) -> DataFrame:
        return pd.read_sql_query(query, self.sqlite_connection)

    def display_tables(self, max_table_rows_to_display: int = 4) -> list:
        print("")
        print("#####################################################################################################")
        print("#####################################################################################################")
        print(f"EasyCsvDb Table Display ({max_table_rows_to_display=}):")
        print("")
        result = self.query("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = result["name"].tolist()
        for table_name in table_names:

            # Get csv_path_str
            csv_path_str = "This table was not created from a CSV file."
            if table_name in self.csv_path_by_table_name:
                csv_path_str = self.csv_path_by_table_name[table_name].as_posix()

            print(f"Table: {table_name}")
            print(f"  - From: {csv_path_str}")
            print("")

            # Get DataFrame to display
            df = self.query(f"SELECT * FROM {table_name} LIMIT {max_table_rows_to_display};")

            # Display DataFrame
            # print(df.to_string(index=False))#TMP
            # Print the DataFrame as a nice text-based table
            print(tabulate(df, headers="keys", tablefmt="psql", maxcolwidths=None, showindex=False))
            print("")
        print("\n#####################################################################################################")
        print("\n#####################################################################################################")

    def create_table_from_csv(
        self, csv_path: Path, table_name: Optional[str] = None, index: bool = False, low_memory=False
    ) -> None:
        """
        # Parameters:
        ---
        index : bool, default True
            Write DataFrame index as a column. Uses index_label as the column name in the table.

        low_memory : bool, default True
            Setting low_memory=False causes pandas to read more of the file to decide what the data types should be.
            This can use more memory, but it can also prevent incorrect data type guesses. If your file is very large
            and you're running out of memory, you might need to consider other options, such as reading the file in
            chunks or specifying the data types of the columns manually.
        """
        if not table_name:
            table_name = csv_path.stem

        # Read CSV files into pandas DataFrames
        data_frame: DataFrame = pd.read_csv(csv_path, low_memory=low_memory)
        # print(data_frame.head())
        # exit(data_frame.head())

        # Store DataFrames in the database
        data_frame.to_sql(table_name, self.sqlite_connection, index=index)

        self.csv_path_by_table_name[table_name] = csv_path

    def to_json(self) -> dict:
        return self.csv_path_by_table_name

    def __repr__(self) -> str:
        return json.dumps(self.to_json())

    def __exit__(self) -> str:
        # Save Changes and Close Connection
        self.sqlite_connection.commit()
        self.sqlite_connection.close()

    # DOC / remove?
    # def write_ordered_tables(
    #     self, dest_ordered_joe_test_case_table_csv_path: Path, dest_ordered_bob_test_file_table_csv_path: Path
    # ):
    #     dest_ordered_joe_test_case_table_csv_path.parent.mkdir(parents=True, exist_ok=True)
    #     dest_ordered_bob_test_file_table_csv_path.parent.mkdir(parents=True, exist_ok=True)

    #     result_df = self._get_query_result_data_frame(
    #         f"""
    #         SELECT * FROM joe_test_case_table
    #         Order By {",".join(cmn.joe_TEST_CASE_TABLE_HEADER_ORDER)}
    #         """
    #     )
    #     print(f"Writing {dest_ordered_joe_test_case_table_csv_path=}...")
    #     result_df.to_csv(dest_ordered_joe_test_case_table_csv_path, index=False)

    # def get_num_test_cases(self):
    #     result_df = self._get_query_result_data_frame("SELECT COUNT(*) AS row_count FROM joe_test_case_table")
    #     # row_count = result_df['row_count'].tolist()[0]
    #     return result_df.at[0, "row_count"]

    # def get_num_unique_requirements(self):
    #     result_df = self._get_query_result_data_frame(
    #         "SELECT COUNT(DISTINCT requirement_id) AS n FROM joe_test_case_table"
    #     )
    #     return result_df.at[0, "n"]

    # def get_num_test_cases_by_test_env(self):
    #     result_df = self._get_query_result_data_frame(
    #         """
    #         SELECT test_environment, COUNT(*) AS test_environment_count
    #         FROM joe_test_case_table
    #         GROUP BY test_environment;
    #     """
    #     )
    #     d = {}
    #     for _index, row in result_df.iterrows():
    #         d[row["test_environment"]] = row["test_environment_count"]
    #     return d

    # def get_num_test_cases(self):
    #     result_df = self._get_query_result_data_frame("SELECT COUNT(*) AS row_count FROM joe_test_case_table")
    #     return result_df.at[0, "row_count"]


# class TestProcedure:
#     def __init__(self, id: str):
#         self.id = id
#         self.executed_in_bob = False

#         self.has_strange_id = False
#         if not self.id.startswith("MK30_TP_"):
#             self.has_strange_id = True

#     def to_json(self) -> dict:
#         return self.__dict__

#     def __repr__(self) -> str:
#         return json.dumps(self.to_json())

# class TestCase:
#     def __init__(self, id: str, test_procedure_id: Optional[str] = None):
#         self.id = id
#         self.test_procedures: List[TestProcedure] = []

#         if test_procedure_id:
#             self.add_test_procedure(test_procedure_id)

#     def add_test_procedure(self, test_procedure_id: str):
#         if test_procedure_id not in self.test_procedures:
#             self.test_procedures.append(TestProcedure(test_procedure_id))

#     def get_all_unique_test_procedure_ids(self):
#         tp_id_set = set()
#         for test_procedure in self.test_procedures:
#             tp_id_set.add(test_procedure.id)
#         return list(tp_id_set)

#     def mark_test_procedure_id_as_executed_in_bob_if_needed(self, test_procedure_id: str) -> None:
#         for tp in self.test_procedures:
#             if tp.id == test_procedure_id:
#                 tp.executed_in_bob = True

#     def is_fully_traced_with_execution(self):
#         '''Contains at least one TestProcedure and all contained TestProcedures are marked as executed in bob'''
#         if len(self.test_procedures) == 0:
#             return False
#         for tp in self.test_procedures:
#             if not tp.executed_in_bob:
#                 return False
#         return True

#     def to_json(self) -> dict:
#         return self.__dict__

#     def __repr__(self) -> str:
#         return json.dumps(self.to_json())


# class Requirement:
#     def __init__(self, id, test_case_id: Optional[str] = None, test_procedure_id: Optional[str] = None):
#         self.id = id
#         self.test_cases: List[TestCase] = []

#         self.add(test_case_id, test_procedure_id)


#     def add(self, test_case_id: str, test_procedure_id: Optional[str] = None):
#         for test_case in self.test_cases:
#             if test_case.id == test_case_id:
#                 if test_procedure_id:
#                     test_case.add_test_procedure(test_procedure_id)
#                 return
#         self.test_cases.append(TestCase(test_case_id, test_procedure_id))


#     def is_traceable(self):
#         '''Has at least one test case & each test case traces to at least one test procedure'''
#         if len(self.test_cases) == 0:
#             return False

#         for test_case in self.test_cases:
#             if len(test_case.test_procedures) == 0:
#                 return False

#         return True

#     def is_fully_traced_with_execution(self) -> bool:
#         '''Has at least one test case & each test case traces to at least one test procedure, each of which has been marked as executed in bob'''
#         if not self.is_traceable():
#             return False

#         for test_case in self.test_cases:
#             if not test_case.is_fully_traced_with_execution():
#                 return False

#         return True


#     def get_all_unique_test_procedure_ids(self):
#         tp_id_set = set()
#         for test_case in self.test_cases:
#             for tp_id in test_case.get_all_unique_test_procedure_ids():
#                 print(f"{tp_id=}")
#                 tp_id_set.add(tp_id)
#         return list(tp_id_set)

#     def mark_test_procedure_id_as_executed_in_bob_if_needed(self, test_procedure_id: str) -> None:
#         for test_case in self.test_cases:
#             test_case.mark_test_procedure_id_as_executed_in_bob_if_needed(test_procedure_id)

#     def to_json(self) -> dict:
#         return self.__dict__

#     def __repr__(self) -> str:
#         return json.dumps(self.to_json())
