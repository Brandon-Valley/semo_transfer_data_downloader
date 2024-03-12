from pathlib import Path
from pprint import pprint
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from web_scrape_tools import DOT_DOT_DOT_INST_PAGE_NUMS, download_current_page_source, read_soup_from_html_file, wait_until_inst_page_loaded

from bs4 import BeautifulSoup
import re

HTML_PATH = Path("C:/Users/Brandon/Downloads/tmp.html")
HTML_1_PAGE_PATH = Path("C:/p/semo_transfer_data_downloader/page_downloads/institution_page_downloads/equiv_w_1_page_ex.htm")

soup = read_soup_from_html_file(HTML_PATH)

# Find all 'tr' elements with class 'pagination-tes'
pagination_table_row_html = soup.find('tr', class_='pagination-tes')
soup = BeautifulSoup(pagination_table_row_html)
pagination_table_row_html = soup.find('tr', class_='pagination-tes')

print("pagination_rows:")
pprint(pagination_table_row_html)

print("###################################################################")

soup = read_soup_from_html_file(HTML_1_PAGE_PATH)

# Find all 'tr' elements with class 'pagination-tes'
pagination_table_row_html = soup.find_all('tr', class_='pagination-tes')

print("pagination_rows:")
pprint(pagination_table_row_html)