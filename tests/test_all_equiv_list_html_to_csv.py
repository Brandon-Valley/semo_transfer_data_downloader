from pathlib import Path
from pprint import pprint

from semo_transfer_data_downloader.utils import file_io_utils
from tests.cmn import TEST_INPUTS_DIR_PATH
from tests.cmn import TEST_OUTPUTS_DIR_PATH
import pytest
from semo_transfer_data_downloader._all_equiv_list_html_to_csv import all_equiv_list_html_to_csv

TEST_INPUT_HTML_DIR_PATH = TEST_INPUTS_DIR_PATH / "test_equiv_list_html_to_csv"
TEST_OUTPUT_CSV_DIR_PATH = TEST_OUTPUTS_DIR_PATH / "test_equiv_list_html_to_csv"

# EQUIV_LIST_HTML_PATHS = [
#     TEST_INPUTS_DIR_PATH
#     / "test_equiv_list_html_to_csv"
#     / "inst_list_page_2__inst_gdvInstWithEQ_btnCreditFromInstName_6__equiv_list_page_1.html",
#     TEST_INPUTS_DIR_PATH
#     / "test_equiv_list_html_to_csv"
#     / "inst_list_page_2__inst_gdvInstWithEQ_btnCreditFromInstName_6__equiv_list_page_2.html",
# ]
# EXPECTED_OUTPUT = [
#     {"city": "CINCINNATI", "institution_name": "XAVIER UNIVERSITY", "state": "OH"},
#     {"city": "NEW ORLEANS", "institution_name": "XAVIER UNIVERSITY OF LOUISIANA", "state": "LA"},
#     {"city": "YAKIMA", "institution_name": "YAKIMA VALLEY COLLEGE", "state": "WA"},
#     {"city": "YORK", "institution_name": "YORK COLLEGE", "state": "NE"},
#     {"city": "YOUNG HARRIS", "institution_name": "YOUNG HARRIS COLLEGE", "state": "GA"},
#     {"city": "MARYSVILLE", "institution_name": "YUBA COLLEGE", "state": "CA"},
# ]


# @pytest.mark.skip()
def test_all_equiv_list_html_to_csv():
    all_equiv_list_html_to_csv(
        in_dir_path=TEST_INPUT_HTML_DIR_PATH,
        out_dir_path=TEST_OUTPUT_CSV_DIR_PATH,
    )

    exit(TEST_OUTPUT_CSV_DIR_PATH)

    # row_dicts = file_io_utils.read_csv_as_row_dicts(INST_LIST_41_CSV_PATH)
    # print("row_dicts:")
    # pprint(row_dicts)

    # assert row_dicts == EXPECTED_OUTPUT


# def test_inst_list_html_to_csv():
#     print("hi")
