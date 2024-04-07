import csv
from pathlib import Path

from semo_transfer_data_downloader._easy_csv_db import EasyCsvDb
from semo_transfer_data_downloader._all_inst_list_html_to_csv import all_inst_list_html_to_csv
from semo_transfer_data_downloader._all_equiv_list_html_to_csv import all_equiv_list_html_to_csv
from semo_transfer_data_downloader.utils import file_sys_utils
from semo_transfer_data_downloader.utils.file_io_utils import (
    read_csv_as_row_dicts,
    write_csv_from_concatenated_csvs,
    write_csv_from_row_dicts,
)
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
OUT_TRANSFERS_FULL_CSV_PATH = OUT_DIR_PATH / "semo_transfer_course_equivalencies_full.csv"
OUT_TRANSFERS_NO_ELECTIVE_CSV_PATH = OUT_DIR_PATH / "semo_transfer_course_equivalencies_no_electives.csv"


def _concat_csvs_in_dir(in_dir_path, out_csv_path: Path):
    def _remove_duplicates_from_csv(csv_path):
        og_row_dicts = read_csv_as_row_dicts(csv_path)
        new_row_dicts_by_blank = {}
        for og_row_dict in og_row_dicts:
            if str(og_row_dict) in new_row_dicts_by_blank.keys():
                continue
            new_row_dicts_by_blank[str(og_row_dict)] = og_row_dict
        write_csv_from_row_dicts(list(new_row_dicts_by_blank.values()), csv_path)

    csv_paths = file_sys_utils.get_abs_paths_to_child_files_no_recurs(in_dir_path)

    # Print path to csv if csv contains `NATIONAL AMERICAN UNIVERSITY,EN,1150,COMPOSITION I,4.5,EN,100,EN100,ENGLISH COMPOSITION,3,,,,,,,08/01/2005`#TMP
    # for csv_path in csv_paths:
    # with open(csv_path, encoding="utf-8", newline="") as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #     for row in csv_reader:
    #         # print(f"{row=}")
    #         if row == [
    #             "NATIONAL AMERICAN UNIVERSITY",
    #             "AC",
    #             "1160",
    #             "PRINCIPLES OF ACCOUNTING II",
    #             "4.5",
    #             "AC",
    #             "222",
    #             "AC222",
    #             "PRINCIPLES OF ACCOUNTING II",
    #             "3",
    #             "",
    #             "",
    #             "",
    #             "",
    #             "",
    #             "",
    #             "08/01/2005",
    #             "",
    #         ]:
    #             print(f"FOUND LINE - {csv_path}")
    #             break

    print(f"Concatenating all equivalency list csvs into {out_csv_path}...")
    write_csv_from_concatenated_csvs(csv_paths, out_csv_path)

    # Remove duplicate lines from out_csv_path using standard python
    # This step shows flaw in method
    # did not account for multiple institutions with the same name but in different states
    # Example:
    #     inst_list_page_21__inst_gdvInstWithEQ_btnCreditFromInstName_13__equiv_list
    #     inst_list_page_21__inst_gdvInstWithEQ_btnCreditFromInstName_12__equiv_list
    #     'NATIONAL AMERICAN UNIVERSITY', 'AC', '1160'
    # Vast majority of cases this just creates "not untrue" duplicates, so being lazy and just removing dups here instead
    # or re-arch
    _remove_duplicates_from_csv(out_csv_path)


# print("Step #1 - Scraping HTML...")
# scrape_html(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH)

# print("Step #2 - Converting Institution List HTMLs to CSVs...")
# all_inst_list_html_to_csv(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_INST_LIST_CSVS_DIR_PATH)

# print("Step #3 - Converting Equivalency List HTMLs to CSVs...")
# all_equiv_list_html_to_csv(WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_EQUIV_LIST_CSVS_DIR_PATH)

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
print(f"Writing {OUT_TRANSFERS_FULL_CSV_PATH=}...")
df.to_csv(OUT_TRANSFERS_FULL_CSV_PATH, index=False)

print("Step #7 - Creating No-Elective version...")
full_row_dicts = read_csv_as_row_dicts(OUT_TRANSFERS_FULL_CSV_PATH)
no_elective_row_dicts = [row_dict for row_dict in full_row_dicts if "ELECTIVE" not in row_dict["semo_course_1_name"]]
print(f"Writing {OUT_TRANSFERS_NO_ELECTIVE_CSV_PATH=}...")
write_csv_from_row_dicts(no_elective_row_dicts, OUT_TRANSFERS_NO_ELECTIVE_CSV_PATH)
