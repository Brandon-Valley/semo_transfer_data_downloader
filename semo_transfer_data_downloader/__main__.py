from pathlib import Path

from semo_transfer_data_downloader._all_inst_list_html_to_csv import all_inst_list_html_to_csv
from semo_transfer_data_downloader._all_equiv_list_html_to_csv import all_equiv_list_html_to_csv
from semo_transfer_data_downloader.utils import file_sys_utils
from semo_transfer_data_downloader.utils.file_io_utils import write_csv_from_concatenated_csvs
from .scrape_html.scrape_html import scrape_html


_SCRIPT_PARENT_DIR_PATH = Path(__file__).parent
REPO_ROOT_DIR_PATH = _SCRIPT_PARENT_DIR_PATH.parent
WORK_DIR_PATH = REPO_ROOT_DIR_PATH / "work"
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
WORK_CONCATENATED_INST_LIST_CSV_PATH = WORK_BIG_BOYS_DIR_PATH / "concatenated_equivalency_list.csv"


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


# print("Step #1 - Scraping HTML...")
# scrape_html(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH)

# print("Step #2 - Converting Institution List HTMLs to CSVs...")
# all_inst_list_html_to_csv(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_INST_LIST_CSVS_DIR_PATH)

# print("Step #3 - Converting Equivalency List HTMLs to CSVs...")
# all_equiv_list_html_to_csv(WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_EQUIV_LIST_CSVS_DIR_PATH)

# print("Step #4 - Concatenating all equivalency list csvs by inst...")
# _concat_csvs_in_dir(WORK_EQUIV_LIST_CSVS_DIR_PATH, WORK_CONCATENATED_EQUIV_LIST_CSV_PATH)

print("Step #5 - Concatenating all inst list csvs...")
_concat_csvs_in_dir(WORK_INST_LIST_CSVS_DIR_PATH, WORK_CONCATENATED_INST_LIST_CSV_PATH)
