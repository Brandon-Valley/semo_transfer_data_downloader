import csv
from pathlib import Path
import pprint
from typing import Dict, List
from semo_transfer_data_downloader.utils import file_sys_utils
from semo_transfer_data_downloader.utils import file_io_utils
from semo_transfer_data_downloader.utils.file_io_utils import delete_last_n_lines_from_txt
from semo_transfer_data_downloader.utils.html_io_utils import read_soup_from_html_file
import csv
from pathlib import Path
from typing import List, Dict


class _InitHtmlTableRow:
    def __init__(self, init_html_table_row_dict: Dict[str, str]):
        self.inst_name = list(init_html_table_row_dict.keys())[0]
        self.init_inst_course = init_html_table_row_dict[self.inst_name]
        self.init_semo_course = init_html_table_row_dict["SOUTHEAST MISSOURI STATE UNIVERSITY"]
        self.init_note = init_html_table_row_dict["Note?"]
        self.init_begin = init_html_table_row_dict["Begin"]
        self.init_end = init_html_table_row_dict["End"]

        self._parse_init_inst_course()
        print("hi")

    def _parse_init_inst_course(self) -> None:
        """
        Example #1:
            Start:
                self.init_inst_course = ASB 305 POVERTY AND GLOBAL HEALTH (3)
            End:
                self.inst_dept = ASB
                self.inst_course_num = 305
                self.inst_course_name = POVERTY AND GLOBAL HEALTH
                self.inst_course_hours = 3
        Example #2:
            Start:
                self.init_inst_course = "COM 312 COMMUNICATION, CONFLICT, AND NEGOTIATION (3)"
            End:
                self.inst_dept = COM
                self.inst_course_num = 312
                self.inst_course_name = COMMUNICATION, CONFLICT, AND NEGOTIATION
                self.inst_course_hours = 3
        """
        self.inst_dept = self.init_inst_course.split(" ")[0]
        self.inst_course_num = self.init_inst_course.split(" ")[1]
        self.inst_course_name = " ".join(self.init_inst_course.split(" ")[2:-1])
        self.inst_course_hours = self.init_inst_course.split(" ")[-1].strip("()")


class _FinalRowDictFactory:
    def __init__(self, init_html_table_row_dicts: List[Dict[str, str]]):
        for init_html_table_row_dict in init_html_table_row_dicts:
            _InitHtmlTableRow(init_html_table_row_dict)

    #     self._parse_init_html_table_row_dicts(init_html_table_row_dicts)

    # def _parse_init_html_table_row_dicts(self, init_html_table_row_dicts: List[Dict[str, str]]) -> None:
    #     self.inst_name = init_html_table_row_dicts[0].keys()[0]


def _get_out_csv_path(html_path: Path, out_dir_path: Path) -> Path:
    """
    Example:
    Input: inst_list_page_2__inst_gdvInstWithEQ_btnCreditFromInstName_6__equiv_list_page_1.html
    Output: inst_list_page_2__inst_gdvInstWithEQ_btnCreditFromInstName_6__equiv_list.csv
    """
    html_file_name = html_path.name
    prefix = html_file_name.split("__equiv_list_page")[0]
    csv_file_name = f"{prefix}__equiv_list.csv"
    return out_dir_path / csv_file_name


def _equiv_list_html_to_init_html_table_row_dicts(in_html_path: Path) -> List[Dict[str, str]]:
    soup = read_soup_from_html_file(in_html_path)
    rows = []

    # Assuming data is in table rows after header in a table with class 'table'
    table = soup.find("table", class_="table")
    if not table:
        raise ValueError(f"No table with class 'table' found in {in_html_path}")

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    for row_num, row in enumerate(table.find_all("tr")[1:]):  # Skip header row
        cols = row.find_all(["td", "th"])
        if len(cols) != len(headers):
            continue  # Skip rows that don't have enough columns
        row_data = {}
        for i, col_and_header in enumerate(zip(cols, headers)):
            col, header = col_and_header
            row_data[header] = col.get_text(strip=True)
        rows.append(row_data)
    return rows[1:]


def all_equiv_list_html_to_csv(in_dir_path: Path, out_dir_path: Path) -> None:
    """
    Convert all html files in in_dir_path to csv files in out_dir_path
    :param in_dir_path: input directory containing html files
    :param out_dir_path: output directory to contain csv files
    :return: None
    """

    for html_path in file_sys_utils.get_abs_path_generator_to_child_files_no_recurs(in_dir_path):
        out_csv_path = _get_out_csv_path(html_path, out_dir_path)
        init_html_table_row_dicts = _equiv_list_html_to_init_html_table_row_dicts(in_html_path=html_path)

        final_row_dict_factory = _FinalRowDictFactory(init_html_table_row_dicts)

        file_io_utils.write_csv_from_row_dicts(init_html_table_row_dicts, out_csv_path, ordered_headers=None)
        exit(out_csv_path)
