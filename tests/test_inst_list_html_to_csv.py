from pathlib import Path
from semo_transfer_data_downloader.html_to_csv._inst_list_html_to_csv import inst_list_html_to_csv
from tests.cmn import TEST_INPUTS_DIR_PATH


def test_inst_list_html_to_csv():
    inst_list_html_to_csv(
        in_html_path=Path("C:/p/semo_transfer_data_downloader/tests/inputs/inst_list_page_41.html"),
        csv_path=TEST_INPUTS_DIR_PATH / "inst_list_page_41.html.csv",
    )
