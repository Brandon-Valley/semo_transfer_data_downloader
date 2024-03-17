import csv
from pathlib import Path
from semo_transfer_data_downloader.utils.html_io_utils import read_soup_from_html_file


def inst_list_html_to_csv(in_html_path: Path, out_csv_path: Path) -> None:
    """
    Convert the html file to csv file
    :param html_file: html file
    :param csv_file: csv file
    :return: None
    """
    soup = read_soup_from_html_file(in_html_path)

    # # write soup to tmp txt file
    # with open(Path("C:/p/semo_transfer_data_downloader/semo_transfer_data_downloader/html_to_csv/tmp.txt"), "w") as f:
    #     f.write(soup.prettify())

    # Find the table containing the desired data
    # This example assumes you're interested in a table with a specific ID or class. Adjust as necessary.
    table = soup.find("table", id="gdvInstWithEQ")

    # Prepare to collect the rows of data
    rows = []

    # Assuming each institution's info is within <tr> tags directly under the table
    for tr in table.find_all("tr")[2:]:  # Skip header rows if necessary
        cols = tr.find_all("td")
        if len(cols) > 1:  # Ensure there are enough columns
            # Extract text from each column. Adjust indices as necessary.
            institution_name = cols[0].text.strip()
            city = cols[1].text.strip()
            state = cols[2].text.strip()

            # Append the collected data to the rows list (if legit)
            if not institution_name.startswith("..."):
                rows.append([institution_name, city, state])

    out_csv_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the data to a CSV file
    with open(out_csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Optional: write header
        writer.writerow(["Institution Name", "City", "State"])
        # Write the data rows
        writer.writerows(rows)

    print(f"Data successfully written to {out_csv_path}")
