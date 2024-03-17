from pathlib import Path
from semo_transfer_data_downloader.utils.html_io_utils import read_soup_from_html_file


def inst_list_html_to_csv(in_html_path: Path, csv_path: Path) -> None:
    """
    Convert the html file to csv file
    :param html_file: html file
    :param csv_file: csv file
    :return: None
    """
    soup = read_soup_from_html_file(in_html_path)

    # write soup to tmp txt file
    with open(Path("C:/p/semo_transfer_data_downloader/semo_transfer_data_downloader/html_to_csv/tmp.txt"), "w") as f:
        f.write(soup.prettify())

    # table = soup.find_all("table")[0]

    # rows = table.find_all("tr")

    # with open(in_html_path, "w") as f:
    #     for row in rows:
    #         cols = row.find_all("td")
    #         cols = [ele.text.strip() for ele in cols]
    #         f.write(",".join(cols) + "\n")
    # return None
