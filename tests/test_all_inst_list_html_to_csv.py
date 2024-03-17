from pathlib import Path
from pprint import pprint

from semo_transfer_data_downloader.utils import file_io_utils
from tests.cmn import TEST_INPUTS_DIR_PATH
from tests.cmn import TEST_OUTPUTS_DIR_PATH
from semo_transfer_data_downloader._all_inst_list_html_to_csv import _inst_list_html_to_csv
import pytest

INST_LIST_41_CSV_PATH = TEST_OUTPUTS_DIR_PATH / "inst_list_page_41.csv"
EXPECTED_OUTPUT = [
    {"city": "CINCINNATI", "institution_name": "XAVIER UNIVERSITY", "state": "OH"},
    {"city": "NEW ORLEANS", "institution_name": "XAVIER UNIVERSITY OF LOUISIANA", "state": "LA"},
    {"city": "YAKIMA", "institution_name": "YAKIMA VALLEY COLLEGE", "state": "WA"},
    {"city": "YORK", "institution_name": "YORK COLLEGE", "state": "NE"},
    {"city": "YOUNG HARRIS", "institution_name": "YOUNG HARRIS COLLEGE", "state": "GA"},
    {"city": "MARYSVILLE", "institution_name": "YUBA COLLEGE", "state": "CA"},
]


# @pytest.mark.skip()
def _test_inst_list_html_to_csv():
    _inst_list_html_to_csv(
        in_html_path=TEST_INPUTS_DIR_PATH / "inst_list_page_41.html",
        out_csv_path=INST_LIST_41_CSV_PATH,
    )

    row_dicts = file_io_utils.read_csv_as_row_dicts(INST_LIST_41_CSV_PATH)
    print("row_dicts:")
    pprint(row_dicts)

    assert row_dicts == EXPECTED_OUTPUT


def test_inst_list_html_to_csv():
    print("hi")
