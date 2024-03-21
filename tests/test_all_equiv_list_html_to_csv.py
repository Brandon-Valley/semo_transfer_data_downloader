from pathlib import Path
from pprint import pprint

from semo_transfer_data_downloader.utils import file_io_utils
from tests.cmn import TEST_INPUTS_DIR_PATH
from tests.cmn import TEST_OUTPUTS_DIR_PATH
import pytest
from semo_transfer_data_downloader._all_equiv_list_html_to_csv import all_equiv_list_html_to_csv
from semo_transfer_data_downloader._all_equiv_list_html_to_csv import _parse_init_course_str
from semo_transfer_data_downloader._all_equiv_list_html_to_csv import _equiv_list_html_to_init_html_table_row_dicts

TEST_INPUT_HTML_DIR_PATH = TEST_INPUTS_DIR_PATH / "test_equiv_list_html_to_csv"
TEST_OUTPUT_CSV_DIR_PATH = TEST_OUTPUTS_DIR_PATH / "test_equiv_list_html_to_csv"


@pytest.fixture
def test_html_path():
    return (
        TEST_INPUT_HTML_DIR_PATH
        / "inst_list_page_2__inst_gdvInstWithEQ_btnCreditFromInstName_6__equiv_list_page_1.html"
    )


def test_equiv_list_html_to_init_html_table_row_dicts(test_html_path):
    # Ensure the test HTML file exists
    assert test_html_path.exists(), f"Test HTML file does not exist: {test_html_path}"

    # Call the function with the test HTML file
    result = _equiv_list_html_to_init_html_table_row_dicts(test_html_path)

    # Assert that the result is a non-empty list of dictionaries
    assert isinstance(result, list) and len(result) > 0, "The result should be a non-empty list of dictionaries."
    assert all(isinstance(item, dict) for item in result), "Each item in the result list should be a dictionary."
    print("result:")
    pprint(result, width=220)

    # exit(result)

    assert any(
        "CH 186 GENERAL CHEMISTRY II (3)CH 187 GENERAL CHEMISTRY II LABORATORY (1)" in row_dict.values()
        for row_dict in result
    ), "Expected row not found in result."

    # Further detailed assertions can be added here depending on the expected content of your HTML file
    # For example:
    # assert result[0]['SOUTHEAST MISSOURI STATE UNIVERSITY'] == 'Expected Value', "First row's value for 'SOUTHEAST MISSOURI STATE UNIVERSITY' does not match expected."


# course_dept, course_num, course_name, course_hours
@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "ACC 2221 COMPUTERIZED ACCOUNTING (4)",
            ("ACC", "2221", "COMPUTERIZED ACCOUNTING", "4"),
        ),  # Note: Modified input to fit expected parsing behavior.
        ("AR 198 ELECTIVE", ("AR", "198", "ELECTIVE", "")),
    ],
)
# @pytest.mark.skip()  # TMP
def test_parse_init_course_str(input_str, expected):
    assert _parse_init_course_str(input_str) == expected


# @pytest.mark.skip()  # TMP
def test_all_equiv_list_html_to_csv():
    all_equiv_list_html_to_csv(
        in_dir_path=TEST_INPUT_HTML_DIR_PATH,
        out_dir_path=TEST_OUTPUT_CSV_DIR_PATH,
    )
    row_dicts = file_io_utils.read_csv_as_row_dicts(
        TEST_OUTPUT_CSV_DIR_PATH / "inst_list_page_2__inst_gdvInstWithEQ_btnCreditFromInstName_6__equiv_list.csv"
    )
    print("row_dicts:")
    pprint(row_dicts[0])

    assert row_dicts[0] == {
        "begin": "01/01/2016",
        "end": "",
        "inst_course_dept": "ASB",
        "inst_course_hours": "3",
        "inst_course_name": "POVERTY AND GLOBAL HEALTH",
        "inst_course_num": "305",
        "institution_name": "ARIZONA STATE UNIVERSITY - COCHISE",
        "note": "",
        "semo_course_1_dept": "AN",
        "semo_course_1_dept_num": "AN398",
        "semo_course_1_hours": "",
        "semo_course_1_name": "ELECTIVE",
        "semo_course_1_num": "398",
        "semo_course_2_dept": "",
        "semo_course_2_dept_num": "",
        "semo_course_2_hours": "",
        "semo_course_2_name": "",
        "semo_course_2_num": "",
    }

    assert row_dicts[15] == {
        "begin": "08/01/2005",
        "end": "",
        "inst_course_dept": "CHM",
        "inst_course_hours": "4",
        "inst_course_name": "GENERAL CHEMISTRY II",
        "inst_course_num": "116",
        "institution_name": "ARIZONA STATE UNIVERSITY - COCHISE",
        "note": "",
        "semo_course_1_dept": "CH",
        "semo_course_1_dept_num": "CH186",
        "semo_course_1_hours": "3",
        "semo_course_1_name": "GENERAL CHEMISTRY II",
        "semo_course_1_num": "186",
        "semo_course_2_dept": "CH",
        "semo_course_2_dept_num": "CH187",
        "semo_course_2_hours": "1",
        "semo_course_2_name": "GENERAL CHEMISTRY II LABORATORY",
        "semo_course_2_num": "187",
    }

    row_dicts = file_io_utils.read_csv_as_row_dicts(
        TEST_OUTPUT_CSV_DIR_PATH / "inst_list_page_13__inst_gdvInstWithEQ_btnCreditFromInstName_8__equiv_list.csv"
    )
    print("row_dicts:")
    pprint(row_dicts[0])

    assert row_dicts[0] == {
        "begin": "",
        "end": "",
        "inst_course_dept": "ACC",
        "inst_course_hours": "4",
        "inst_course_name": "FUNDAMENTALS OF ACCOUNTING",
        "inst_course_num": "1102",
        "institution_name": "FRONTIER COMMUNITY COLLEGE",
        "note": "",
        "semo_course_1_dept": "AC",
        "semo_course_1_dept_num": "AC198",
        "semo_course_1_hours": "",
        "semo_course_1_name": "ELECTIVE",
        "semo_course_1_num": "198",
        "semo_course_2_dept": "",
        "semo_course_2_dept_num": "",
        "semo_course_2_hours": "",
        "semo_course_2_name": "",
        "semo_course_2_num": "",
    }

    row_dicts = file_io_utils.read_csv_as_row_dicts(
        TEST_OUTPUT_CSV_DIR_PATH / "inst_list_page_13__inst_gdvInstWithEQ_btnCreditFromInstName_8__equiv_list.csv"
    )
    print("row_dicts:")
    pprint(row_dicts[17])

    assert row_dicts[17] == {
        "begin": "08/01/2011",
        "end": "",
        "inst_course_dept": "BRD",
        "inst_course_hours": "3",
        "inst_course_name": "INTRODUCTION TO BROADCASTING",
        "inst_course_num": "1101",
        "institution_name": "FRONTIER COMMUNITY COLLEGE",
        "note": "",
        "semo_course_1_dept": "MC",
        "semo_course_1_dept_num": "MC198",
        "semo_course_1_hours": "",
        "semo_course_1_name": "ELECTIVE",
        "semo_course_1_num": "198",
        "semo_course_2_dept": "",
        "semo_course_2_dept_num": "",
        "semo_course_2_hours": "",
        "semo_course_2_name": "",
        "semo_course_2_num": "",
    }

    row_dicts = file_io_utils.read_csv_as_row_dicts(
        TEST_OUTPUT_CSV_DIR_PATH / "inst_list_page_27__inst_gdvInstWithEQ_btnCreditFromInstName_23__equiv_list.csv"
    )
    print("row_dicts:")
    pprint(row_dicts[16])

    assert row_dicts[16] == {
        "begin": "",
        "end": "",
        "inst_course_dept": "THRA",
        "inst_course_hours": "2",
        "inst_course_name": "CREATIVE AWARENESS",
        "inst_course_num": "257",
        "institution_name": "SAINT LOUIS UNIVERSITY-MAIN CAMPUS",
        "note": "",
        "semo_course_1_dept": "TH",
        "semo_course_1_dept_num": "TH198",
        "semo_course_1_hours": "",
        "semo_course_1_name": "ELECTIVE",
        "semo_course_1_num": "198",
        "semo_course_2_dept": "",
        "semo_course_2_dept_num": "",
        "semo_course_2_hours": "",
        "semo_course_2_name": "",
        "semo_course_2_num": "",
    }

    # exit("here end of test - add / fix rest")
