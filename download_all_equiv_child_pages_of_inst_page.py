from pathlib import Path
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
    link.click()

def _click_inst_list_link(driver):
    print(f"Clicking INSTITUTION LIST...")
    link = driver.find_element(By.LINK_TEXT, "INSTITUTION LIST")
    link.click()

def _wait_until_equiv_page_loaded(driver):
    # Wait until the "EQUIVALENCY LIST" has loaded
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//li[text()='EQUIVALENCY LIST']"))
    )


def _get_equiv_page_dest_path(inst_page_num, inst_id, equiv_page_num, equiv_list_dl_dir_path: Path):
    return equiv_list_dl_dir_path / f"inst_list_page_{inst_page_num}__inst_{inst_id}__equiv_list_page_{equiv_page_num}.html"


def _download_all_equiv_list_pages_of_inst(driver, inst_id, inst_page_num, equiv_list_dl_dir_path: Path):
    """Start and end on inst list page"""

    def _is_equiv_list_page_number_highlighted(html_file_path, page_num):
        """no link if highlighted, can start any page highlighted"""
        soup = read_soup_from_html_file(html_file_path)
        highlighted_page_num = soup.find('span', text=str(page_num))
        return highlighted_page_num is not None
    
    def _click_non_highlighted_equiv_list_page_num_and_wait_for_load(driver, equiv_list_page_num):

        print(f"Attempting to Click non-highlighted {equiv_list_page_num=}...")

        try:
            link = driver.find_element(By.LINK_TEXT, str(equiv_list_page_num))
        except Exception as e:
            print(str(e))

            if equiv_list_page_num == 1:
                while True:
                    print("HOPE THIS DOESN'T CAUSE AN INFINITE LOOP")

                    # Find the first link with visible text "..." and click it
                    link = driver.find_element(By.XPATH, "//a[text()='...']")
                    link.click()

                    sleep(40) # Dont know start / what num to wait for
                    try:
                        link = driver.find_element(By.LINK_TEXT, str(equiv_list_page_num))
                        print("Found #1!")
                        break # Found #1 !!
                    except Exception as e:
                        print(f"Here we go again...{str(e)}")

            else:
                try:
                    link = driver.find_element(By.XPATH, f"//a[@href=\"javascript:__doPostBack('gdvCourseEQ','Page${equiv_list_page_num}')\"]")
                except Exception as e2:
                    if equiv_list_page_num == 1:
                        # # Find the first link with visible text "..." and click it
                        # link = driver.find_element(By.XPATH, "//a[text()='...']")
                        # FIXME??

                        raise Exception(f"Could not find non-highlighted {equiv_list_page_num=}") from e2

        link.click()

        # Wait until new paginated equiv list page has loaded
        wait = WebDriverWait(driver, 50)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//td/span"), str(equiv_list_page_num)))
        sleep(random.randint(1, 3)) # Mimic human delay after click

    def _get_to_first_equiv_list_page_downloaded_and_highlighted(driver, equiv_page_1_dest_path, inst_id):
        """Get to starting position"""
        _click_inst_link(driver, inst_id)

        _wait_until_equiv_page_loaded(driver)
        sleep(random.randint(1, 3))

        # Download what is most likely to be the first equiv list page
        download_current_page_source(driver, equiv_page_1_dest_path)

        # Confirm this is actually page #1, if not, click page #1 and download
        if not _is_equiv_list_page_number_highlighted(equiv_page_1_dest_path, 1) and _get_num_equiv_list_pages_from_first_equiv_list_html_path(equiv_page_1_dest_path) > 1:
            print("Page #1 is not highlighted, replacing it & getting tto known starting position...")
            _click_non_highlighted_equiv_list_page_num_and_wait_for_load(driver, 1)
            download_current_page_source(driver, equiv_page_1_dest_path)
        
        print("Now we know equiv list page #1 is highlighted (if more than 1 page) AND downloaded!")



    print(f"Downloading all equiv list pages of {inst_id=}...")

    # Get to starting position
    equiv_page_1_dest_path = _get_equiv_page_dest_path(inst_page_num, inst_id, 1, equiv_list_dl_dir_path)
    _get_to_first_equiv_list_page_downloaded_and_highlighted(driver, equiv_page_1_dest_path, inst_id)

    # Handle other equiv list pages if they exist
    print("Checking if there are more equiv list pages that need to be downloaded...")
    num_equiv_list_pages = _get_num_equiv_list_pages_from_first_equiv_list_html_path(equiv_page_1_dest_path)
    print(f"{num_equiv_list_pages=}")

    for cur_equiv_page_num in range(2, num_equiv_list_pages + 1):
        cur_equiv_page_dest_path = _get_equiv_page_dest_path(inst_page_num, inst_id, cur_equiv_page_num, equiv_list_dl_dir_path)

        print(f"Getting {cur_equiv_page_dest_path=}...")
        # Starts with PREVIOUS page # highlighted, ends with CURRENT page # highlighted
        _click_non_highlighted_equiv_list_page_num_and_wait_for_load(driver, cur_equiv_page_num)
        download_current_page_source(driver, cur_equiv_page_dest_path)

    # Back to inst page
    _click_inst_list_link(driver)
    wait_until_inst_page_loaded(driver, inst_page_num)
    sleep(random.randint(1, 3))

    

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



def download_all_equiv_list_pages_of_all_insts_on_current_inst_list_page(driver, inst_page_dest_path, inst_page_num, equiv_list_dl_dir_path: Path):
    """Returns ['gdvInstWithEQ_btnCreditFromInstName_0', 'gdvInstWithEQ_btnCreditFromInstName_1', 'gdvInstWithEQ_btnCreditFromInstName_2', ...]"""
    inst_ids = _get_inst_ids_from_html(inst_page_dest_path)

    for inst_id in inst_ids:
        if _all_equiv_pages_of_inst_already_downloaded(inst_page_num, inst_id, equiv_list_dl_dir_path):
            print(f"Skipping all equiv pages of {inst_id=} because they already exist...")
            continue

        _download_all_equiv_list_pages_of_inst(driver, inst_id, inst_page_num, equiv_list_dl_dir_path)

        # # loop through all paginated equiv pages
        # cur_equiv_page_num = 1
        # while True:
        #     cur_equiv_page_dest_path = _get_equiv_page_dest_path(inst_page_dest_path, inst_page_num, inst_id, cur_equiv_page_num)

        #     # Check for skips
        #     if cur_equiv_page_dest_path.exists():
        #         # Check if can skip all paginated equiv pages for this institution
        #         if cur_equiv_page_num == 1:
        #             _get_num_equiv_list_pages_from_first_equiv_list_html_path


        #         print(f"Skipping {cur_equiv_page_dest_path=} because it already exists...")
        #         continue

        #     print(f"{inst_id=}")
            
        #     _click_inst_link(driver, inst_id)

        #     _wait_until_equiv_page_loaded(driver)
        #     sleep(random.randint(1, 3))

        #     download_current_page_source(driver, cur_equiv_page_dest_path)

        #     # Back to inst page
        #     _click_inst_list_link(driver)
        #     wait_until_inst_page_loaded(driver, inst_page_num)
        #     sleep(random.randint(1, 3))

        #     # if inst_id == "gdvInstWithEQ_btnCreditFromInstName_3":# TMP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #     #     break


