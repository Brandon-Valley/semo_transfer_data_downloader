from pathlib import Path

from semo_transfer_data_downloader._all_inst_list_html_to_csv import all_inst_list_html_to_csv
from .scrape_html.scrape_html import scrape_html


_SCRIPT_PARENT_DIR_PATH = Path(__file__).parent
REPO_ROOT_DIR_PATH = _SCRIPT_PARENT_DIR_PATH.parent
WORK_DIR_PATH = REPO_ROOT_DIR_PATH / "work"
WORK_HTML_DOWNLOADS_DIR_PATH = WORK_DIR_PATH / "html_downloads"
WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "institution_list_html"
WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "equivalency_list_html"
WORK_INST_LIST_CSVS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "institution_list_csv"
WORK_EQUIV_LIST_CSVS_DIR_PATH = WORK_HTML_DOWNLOADS_DIR_PATH / "equivalency_list_csv"


# print("Step #1 - Scraping HTML...")
# scrape_html(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH)

print("Step #2 - Converting Institution List HTMLs to CSVs...")
all_inst_list_html_to_csv(WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH, WORK_INST_LIST_CSVS_DIR_PATH)
