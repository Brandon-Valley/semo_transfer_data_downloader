from pathlib import Path
import random
from time import sleep
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from ._Equiv_List_Page_Navigator import Equiv_List_Page_Navigator
from ._web_scrape_tools import DOT_DOT_DOT_INST_PAGE_NUMS, ProbablyGotDetectedAsBotException, download_current_page_source, human_click, human_click_delay, read_soup_from_html_file, wait_until_inst_page_loaded

import re

def _get_num_equiv_list_pages_from_first_equiv_list_html_path(file_path):
    """Assumes there will never be 1 inst with more than 10 equiv pages. If there are, this function will need to be updated."""
    soup = read_soup_from_html_file(file_path)
    element = soup.find(id='lblCourseEQPaginationInfo')
    
    if element is not None:
        # Extract the number of pages from the text
        match = re.search(r'PAGE \d+ OF (\d+)', element.text)
        if match is not None:
            return int(match.group(1))
    
    # If the element is not found or the text does not match the expected format, return 1
    return 1

def _get_inst_ids_from_html(file_path):
    soup = read_soup_from_html_file(file_path)
    ids = [element.get('id') for element in soup.find_all(id=True) if element.get('id').startswith('gdvInstWithEQ_btnCreditFromInstName_')]
    return ids


def _click_inst_link(driver, inst_id):
    # Added after fail on gdvInstWithEQ_btnCreditFromInstName_24
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.ID, inst_id))
    )

    print(f"Clicking {inst_id=}...")
    link = driver.find_element(By.ID, inst_id)
    human_click(driver, link)

def _click_inst_list_link(driver):
    print(f"Clicking INSTITUTION LIST...")
    link = driver.find_element(By.LINK_TEXT, "INSTITUTION LIST")
    human_click(driver, link)

def _wait_until_equiv_page_loaded(driver):
    # Wait until the "EQUIVALENCY LIST" has loaded
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//li[text()='EQUIVALENCY LIST']"))
    )


def _get_equiv_page_dest_path(inst_page_num, inst_id, equiv_page_num, equiv_list_dl_dir_path: Path):
    return equiv_list_dl_dir_path / f"inst_list_page_{inst_page_num}__inst_{inst_id}__equiv_list_page_{equiv_page_num}.html"


def _all_equiv_pages_of_inst_already_downloaded(inst_page_num, inst_id, equiv_list_dl_dir_path):
    print(f"Checking if all equiv list pages have already been downloaded for {inst_id=}...")
    equiv_page_1_dest_path = _get_equiv_page_dest_path(inst_page_num, inst_id, 1, equiv_list_dl_dir_path)
    if not equiv_page_1_dest_path.is_file():
        return False
    
    num_paginated_equiv_pages = _get_num_equiv_list_pages_from_first_equiv_list_html_path(equiv_page_1_dest_path)

    for i in range(2, num_paginated_equiv_pages + 1):
        if not _get_equiv_page_dest_path(inst_page_num, inst_id, i, equiv_list_dl_dir_path).is_file():
            return False
    
    return True


def _download_all_equiv_list_pages_of_inst_starting_from_inst_list_page(driver, inst_id, inst_page_num, equiv_list_dl_dir_path: Path):
    """Ends on last equiv list page of given inst"""
    print(f"Downloading all equiv list pages of {inst_id=} - (assuming that this is starting on the institution list page)...")

    # Click the institution link, this could put you on ANY equiv list page for the institution
    _click_inst_link(driver, inst_id)
    _wait_until_equiv_page_loaded(driver)
    human_click_delay()

    # Get to known starting position (this also downloads the first equiv list page)
    nav = Equiv_List_Page_Navigator(driver)

    # Download all other equiv list pages for the given institution
    for cur_page_num in range(1, nav.total_pages + 1):
        nav.navigate_to_page_num_and_wait_until_loaded_if_needed(driver, page_num=cur_page_num)
        cur_page_dest_path = _get_equiv_page_dest_path(inst_page_num, inst_id, cur_page_num, equiv_list_dl_dir_path)
        nav.copy_current_html_to_dest(cur_page_dest_path)


def download_all_equiv_list_pages_of_all_insts_on_current_inst_list_page(driver, inst_page_dest_path, inst_page_num, equiv_list_dl_dir_path: Path):
    """Returns ['gdvInstWithEQ_btnCreditFromInstName_0', 'gdvInstWithEQ_btnCreditFromInstName_1', 'gdvInstWithEQ_btnCreditFromInstName_2', ...]"""
    inst_ids = _get_inst_ids_from_html(inst_page_dest_path)

    for inst_id in inst_ids:
        if _all_equiv_pages_of_inst_already_downloaded(inst_page_num, inst_id, equiv_list_dl_dir_path):
            print(f"Skipping all equiv pages of {inst_id=} because they already exist...")
            continue

        _download_all_equiv_list_pages_of_inst_starting_from_inst_list_page(driver, inst_id, inst_page_num, equiv_list_dl_dir_path)

        # Back to inst page
        print(f"Finished downloading all equiv list pages for {inst_id=}, going back to institution list page...")


        try:
            _click_inst_list_link(driver)
            wait_until_inst_page_loaded(driver, inst_page_num)
        except selenium.common.exceptions.TimeoutException:
            raise ProbablyGotDetectedAsBotException("Got timeout exception on back to inst list click, this probably means you actually got a 403 b/c bot detected")
        human_click_delay()
