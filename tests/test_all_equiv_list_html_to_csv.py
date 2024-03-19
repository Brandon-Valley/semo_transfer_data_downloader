from pathlib import Path
from pprint import pprint

from semo_transfer_data_downloader.utils import file_io_utils
from tests.cmn import TEST_INPUTS_DIR_PATH
from tests.cmn import TEST_OUTPUTS_DIR_PATH
import pytest
from semo_transfer_data_downloader._all_equiv_list_html_to_csv import all_equiv_list_html_to_csv

TEST_INPUT_HTML_DIR_PATH = TEST_INPUTS_DIR_PATH / "test_equiv_list_html_to_csv"
TEST_OUTPUT_CSV_DIR_PATH = TEST_OUTPUTS_DIR_PATH / "test_equiv_list_html_to_csv"


# @pytest.mark.skip()
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
        "semo_course_1_hours": "ELECTIVE",
        "semo_course_1_name": "",
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
        "inst_course_name": "APPLIED ACCOUNTING",
        "inst_course_num": "1101",
        "institution_name": "FRONTIER COMMUNITY COLLEGE",
        "note": "",
        "semo_course_1_dept": "DNT",
        "semo_course_1_dept_num": "DNTCOURSE",
        "semo_course_1_hours": "TRANSFER",
        "semo_course_1_name": "DOES NOT",
        "semo_course_1_num": "COURSE",
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
        "begin": "08/01/2005",
        "end": "",
        "inst_course_dept": "BMK",
        "inst_course_hours": "3",
        "inst_course_name": "INTRODUCTION TO SALES",
        "inst_course_num": "2102",
        "institution_name": "FRONTIER COMMUNITY COLLEGE",
        "note": "",
        "semo_course_1_dept": "MK",
        "semo_course_1_dept_num": "MK198",
        "semo_course_1_hours": "ELECTIVE",
        "semo_course_1_name": "",
        "semo_course_1_num": "198",
        "semo_course_2_dept": "",
        "semo_course_2_dept_num": "",
        "semo_course_2_hours": "",
        "semo_course_2_name": "",
        "semo_course_2_num": "",
    }
    # exit("here end of test")
