from bs4 import BeautifulSoup
from pathlib import Path


def read_soup_from_html_file(html_path: Path) -> BeautifulSoup:
    with open(html_path, "r", encoding="utf-8") as f:
        contents = f.read()
    return BeautifulSoup(contents, "html.parser")
