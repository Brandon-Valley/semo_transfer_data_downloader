from pathlib import Path
from pprint import pprint
from semo_transfer_data_downloader.html_to_csv._inst_list_html_to_csv import inst_list_html_to_csv
from semo_transfer_data_downloader.utils import file_io_utils
from tests.cmn import TEST_INPUTS_DIR_PATH
from tests.cmn import TEST_OUTPUTS_DIR_PATH

INST_LIST_41_CSV_PATH = TEST_OUTPUTS_DIR_PATH / "inst_list_page_41.csv"
EXPECTED_OUTPUT = [
    {"City": "CINCINNATI", "Institution Name": "XAVIER UNIVERSITY", "State": "OH"},
    {"City": "NEW ORLEANS", "Institution Name": "XAVIER UNIVERSITY OF LOUISIANA", "State": "LA"},
    {"City": "YAKIMA", "Institution Name": "YAKIMA VALLEY COLLEGE", "State": "WA"},
    {"City": "YORK", "Institution Name": "YORK COLLEGE", "State": "NE"},
    {"City": "YOUNG HARRIS", "Institution Name": "YOUNG HARRIS COLLEGE", "State": "GA"},
    {"City": "MARYSVILLE", "Institution Name": "YUBA COLLEGE", "State": "CA"},
]


def test_inst_list_html_to_csv():
    inst_list_html_to_csv(
        in_html_path=TEST_INPUTS_DIR_PATH / "inst_list_page_41.html",
        out_csv_path=INST_LIST_41_CSV_PATH,
    )

    row_dicts = file_io_utils.read_csv_as_row_dicts(INST_LIST_41_CSV_PATH)
    print("row_dicts:")
    pprint(row_dicts)

    assert row_dicts == EXPECTED_OUTPUT
