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
WORK_BIG_BOYS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "big_boys"
WORK_CONCATENATED_EQUIV_LIST_CSV_PATH = WORK_BIG_BOYS_DIR_PATH / "concatenated_equivalency_list.csv"
WORK_CONCATENATED_INST_LIST_CSV_PATH = WORK_BIG_BOYS_DIR_PATH / "concatenated_institution_list.csv"
OUT_FULL_TRANSFERS_CSV_PATH = OUT_DIR_PATH / "semo_transfer_course_equivalencies.csv"


def _concat_csvs_in_dir(in_dir_path, out_csv_path: Path):
    csv_paths = file_sys_utils.get_abs_paths_to_child_files_no_recurs(in_dir_path)
    print(f"Concatenating all equivalency list csvs into {out_csv_path}...")
    write_csv_from_concatenated_csvs(csv_paths, out_csv_path)


print("Step #1 - Scraping HTML...")
scrape_html(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH)

print("Step #2 - Converting Institution List HTMLs to CSVs...")
all_inst_list_html_to_csv(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_INST_LIST_CSVS_DIR_PATH)

print("Step #3 - Converting Equivalency List HTMLs to CSVs...")
all_equiv_list_html_to_csv(WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_EQUIV_LIST_CSVS_DIR_PATH)

print("Step #4 - Concatenating all equivalency list csvs by inst...")
_concat_csvs_in_dir(WORK_EQUIV_LIST_CSVS_DIR_PATH, WORK_CONCATENATED_EQUIV_LIST_CSV_PATH)

print("Step #5 - Concatenating all inst list csvs...")
_concat_csvs_in_dir(WORK_INST_LIST_CSVS_DIR_PATH, WORK_CONCATENATED_INST_LIST_CSV_PATH)

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

# db.display_tables()
