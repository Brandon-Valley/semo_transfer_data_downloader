from pathlib import Path
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType

from download_all_equiv_child_pages_of_inst_page import download_all_equiv_list_pages_of_all_insts_on_current_inst_list_page
from web_scrape_tools import DOT_DOT_DOT_INST_PAGE_NUMS, download_current_page_source, setup_driver, wait_until_inst_page_loaded

MAX_INST_PAGES = 41
STARTING_INST_PAGE_NUM = 1


SCRIPT_PARENT_DIR_PATH = Path(__file__).parent
INST_LIST_PAGE_DOWNLOADS_DIR_PATH = SCRIPT_PARENT_DIR_PATH / "page_downloads" / "TMP_institution_list_pages" #TMP put back after nav test
EQUIV_LIST_PAGE_DOWNLOADS_DIR_PATH = SCRIPT_PARENT_DIR_PATH / "page_downloads" / "TMP_equivalency_list_pages" #TMP put back after nav test

def _click_inst_page_num(driver, page_num):
    print(f"Clicking {page_num=}...")

    if page_num in DOT_DOT_DOT_INST_PAGE_NUMS:
        link = driver.find_element(By.XPATH, f"//a[@href=\"javascript:__doPostBack('gdvInstWithEQ','Page${page_num}')\"]")
    else:
        link = driver.find_element(By.LINK_TEXT, str(page_num))
    link.click()
    _random_sleep(1, 3)  # Mimic human delay after click

def _random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))


driver = setup_driver()
url = "https://tes.collegesource.com/publicview/TES_publicview01.aspx?rid=1f7d5d36-c901-4196-8575-28ee59bf7f4a&aid=aa590d78-6e6a-4ea3-97c6-9f6102c1c4c0"
driver.get(url)

if STARTING_INST_PAGE_NUM != 1:
    assert STARTING_INST_PAGE_NUM < 12, f"Invalid {STARTING_INST_PAGE_NUM=} / not yet supported"
    _click_inst_page_num(driver, STARTING_INST_PAGE_NUM)
    wait_until_inst_page_loaded(driver, STARTING_INST_PAGE_NUM)
    _random_sleep(1, 5)

for inst_page_num in range(STARTING_INST_PAGE_NUM, MAX_INST_PAGES + 1):
    print(f"{inst_page_num=}")
    if inst_page_num > STARTING_INST_PAGE_NUM:
        _click_inst_page_num(driver, inst_page_num)
    wait_until_inst_page_loaded(driver, inst_page_num)
    _random_sleep(2, 5)  # Random sleep to mimic human behavior

    inst_page_dest_path = INST_LIST_PAGE_DOWNLOADS_DIR_PATH / f"inst_list_page_{inst_page_num}.html"
    download_current_page_source(driver, inst_page_dest_path)

    download_all_equiv_list_pages_of_all_insts_on_current_inst_list_page(driver, inst_page_dest_path, inst_page_num, EQUIV_LIST_PAGE_DOWNLOADS_DIR_PATH)

    # Extra wait just in case
    # _random_sleep(20, 50)

# FIXME equiv page can have multiple pages!!!!!!!!!!!!!! - ARIZONA STATE UNIVERSITY - MESA CITY CENTER

driver.quit()
