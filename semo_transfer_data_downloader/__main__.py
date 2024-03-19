import csv
from pathlib import Path

from semo_transfer_data_downloader._easy_csv_db import EasyCsvDb
from semo_transfer_data_downloader._all_inst_list_html_to_csv import all_inst_list_html_to_csv
from semo_transfer_data_downloader._all_equiv_list_html_to_csv import all_equiv_list_html_to_csv
from semo_transfer_data_downloader.utils import file_sys_utils
from semo_transfer_data_downloader.utils.file_io_utils import write_csv_from_concatenated_csvs
from .scrape_html.scrape_html import scrape_html


_SCRIPT_PARENT_DIR_PATH = Path(__file__).parent
REPO_ROOT_DIR_PATH = _SCRIPT_PARENT_DIR_PATH.parent
WORK_DIR_PATH = REPO_ROOT_DIR_PATH / "work"
OUT_DIR_PATH = REPO_ROOT_DIR_PATH / "outputs"
WORK_HTML_DOWNLOADS_DIR_PATH = WORK_DIR_PATH / "html_downloads"
WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "institution_list_html"
WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "equivalency_list_html"
WORK_INST_LIST_CSVS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "institution_list_csv"
WORK_EQUIV_LIST_CSVS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "equivalency_list_csv"
WORK_CONCATENATED_EQUIV_LIST_CSVS_DIR_PATH = (
    WORK_HTML_DOWNLOADS_DIR_PATH / "concatenated_equivalency_list_csv"
)  # TMPneed?
WORK_BIG_BOYS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "big_boys"
WORK_CONCATENATED_EQUIV_LIST_CSV_PATH = WORK_BIG_BOYS_DIR_PATH / "concatenated_equivalency_list.csv"
WORK_CONCATENATED_INST_LIST_CSV_PATH = WORK_BIG_BOYS_DIR_PATH / "concatenated_institution_list.csv"
OUT_FULL_TRANSFERS_CSV_PATH = OUT_DIR_PATH / "semo_transfer_course_equivalencies.csv"
OUT_FULL_TRANSFERS_CSV_PATH_2 = OUT_DIR_PATH / "semo_transfer_course_equivalencies_OUTER.csv"  # TMP

# def _concat_all_equiv_list_csvs_by_inst(out_dir_path: Path):

#     equiv_list_csv_paths_by_inst_num_str = {}

#     for equiv_list_csv_path in file_sys_utils.get_abs_path_generator_to_child_files_no_recurs(
#         WORK_EQUIV_LIST_CSVS_DIR_PATH
#     ):
#         equiv_list_csv_inst_num_str = equiv_list_csv_path.stem.split("inst_list_page_")[1].split("__inst_")[0]

#         if equiv_list_csv_inst_num_str not in equiv_list_csv_paths_by_inst_num_str:
#             equiv_list_csv_paths_by_inst_num_str[equiv_list_csv_inst_num_str] = []
#         equiv_list_csv_paths_by_inst_num_str[equiv_list_csv_inst_num_str].append(equiv_list_csv_path)

#     for inst_list_csv_path in file_sys_utils.get_abs_path_generator_to_child_files_no_recurs(
#         WORK_INST_LIST_CSVS_DIR_PATH
#     ):
#         inst_list_inst_num_str = inst_list_csv_path.stem.split("inst_list_page_")[-1].split(".html")[0]

#         print(f"inst_num_str: {inst_list_inst_num_str=}")

#         out_csv_path = out_dir_path / f"inst_list_page_{inst_list_inst_num_str}__equiv_list.csv"
#         print(f"Concatenating all {inst_list_inst_num_str} equivalency list csvs into {out_csv_path}...")
#         write_csv_from_concatenated_csvs(equiv_list_csv_paths_by_inst_num_str[inst_list_inst_num_str], out_csv_path)


# def _concat_all_equiv_list_csvs(in_dir_path, out_csv_path: Path):
#     equiv_list_csv_paths = file_sys_utils.get_abs_paths_to_child_files_no_recurs(in_dir_path)
#     print(f"Concatenating all equivalency list csvs into {out_csv_path}...")
#     write_csv_from_concatenated_csvs(equiv_list_csv_paths, out_csv_path)


def _concat_csvs_in_dir(in_dir_path, out_csv_path: Path):
    csv_paths = file_sys_utils.get_abs_paths_to_child_files_no_recurs(in_dir_path)
    print(f"Concatenating all equivalency list csvs into {out_csv_path}...")
    write_csv_from_concatenated_csvs(csv_paths, out_csv_path)


def _write_csv_from_simple_sql_full_join_on_single_field(csv_path_1: Path, csv_path_2: Path, out_csv_path: Path):
    # Read the first CSV file and store its contents
    with open(csv_path_1, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        headers_1 = next(reader)
        data_1 = {rows[0]: rows[1:] for rows in reader}

    # Read the second CSV file and store its contents
    with open(csv_path_2, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        headers_2 = next(reader)
        data_2 = {rows[0]: rows[1:] for rows in reader}

    # Prepare the header for the output file, assuming the join field is the first field
    join_field = headers_1[0]
    assert join_field == headers_2[0], "The join fields do not match."
    out_headers = [join_field] + headers_1[1:] + headers_2[1:]

    # Perform the join
    joined_data = []
    for key in data_1:
        if key in data_2:
            joined_data.append([key] + data_1[key] + data_2[key])

    # Write the joined data to the output CSV file
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    with open(out_csv_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(out_headers)
        writer.writerows(joined_data)


def _write_csv_from_simple_sql_outer_join(csv_path_1: Path, csv_path_2: Path, out_csv_path: Path):
    # Read the first CSV file and store its contents
    with open(csv_path_1, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        headers_1 = next(reader)
        data_1 = {rows[0]: rows[1:] for rows in reader}

    # Read the second CSV file and store its contents
    with open(csv_path_2, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        headers_2 = next(reader)
        data_2 = {rows[0]: rows[1:] for rows in reader}

    # Prepare the header for the output file, assuming the join field is the first field
    join_field = headers_1[0]
    assert join_field == headers_2[0], "The join fields do not match."
    out_headers = [join_field] + headers_1[1:] + headers_2[1:]

    # Perform the outer join
    joined_data = []
    all_keys = set(data_1.keys()) | set(data_2.keys())  # Union of keys from both data sets

    for key in all_keys:
        row_data_1 = data_1.get(key, [""] * (len(headers_1) - 1))  # Fill missing data with empty strings
        row_data_2 = data_2.get(key, [""] * (len(headers_2) - 1))
        joined_data.append([key] + row_data_1 + row_data_2)

    # Write the joined data to the output CSV file
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    with open(out_csv_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(out_headers)
        writer.writerows(joined_data)


# print("Step #1 - Scraping HTML...")
# scrape_html(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH)

# print("Step #2 - Converting Institution List HTMLs to CSVs...")
# all_inst_list_html_to_csv(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_INST_LIST_CSVS_DIR_PATH)

# print("Step #3 - Converting Equivalency List HTMLs to CSVs...")
# all_equiv_list_html_to_csv(WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_EQUIV_LIST_CSVS_DIR_PATH)

# print("Step #4 - Concatenating all equivalency list csvs by inst...")
# _concat_csvs_in_dir(WORK_EQUIV_LIST_CSVS_DIR_PATH, WORK_CONCATENATED_EQUIV_LIST_CSV_PATH)

# print("Step #5 - Concatenating all inst list csvs...")
# _concat_csvs_in_dir(WORK_INST_LIST_CSVS_DIR_PATH, WORK_CONCATENATED_INST_LIST_CSV_PATH)

# print("Step #6 - Joining institutions and equivalencies...")
# _write_csv_from_simple_sql_full_join_on_single_field(
#     WORK_CONCATENATED_INST_LIST_CSV_PATH, WORK_CONCATENATED_EQUIV_LIST_CSV_PATH, OUT_FULL_TRANSFERS_CSV_PATH
# )

# print("Step #6 - Joining institutions and equivalencies...")
# _write_csv_from_simple_sql_outer_join(
#     WORK_CONCATENATED_INST_LIST_CSV_PATH, WORK_CONCATENATED_EQUIV_LIST_CSV_PATH, OUT_FULL_TRANSFERS_CSV_PATH_2
# )

print("Step #6 - Joining institutions and equivalencies...")
# Full inner and outer join of the equiv_table and inst_table by using the institution_name
# field - the values of the inst_table should come after that of the equiv_table
db = EasyCsvDb()
db.create_table_from_csv(WORK_CONCATENATED_INST_LIST_CSV_PATH, "inst_table")
db.create_table_from_csv(WORK_CONCATENATED_EQUIV_LIST_CSV_PATH, "equiv_table")
df = db.query(
    """
    SELECT * FROM inst_table
    JOIN equiv_table
    ON inst_table.institution_name = equiv_table.institution_name
"""
)
print(f"Writing {OUT_FULL_TRANSFERS_CSV_PATH=}...")
df.to_csv(OUT_FULL_TRANSFERS_CSV_PATH, index=False)

db.display_tables()
