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

from web_scrape_tools import download_current_page_source, wait_until_inst_page_loaded

def _get_inst_ids_from_html(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    ids = [element.get('id') for element in soup.find_all(id=True) if element.get('id').startswith('gdvInstWithEQ_btnCreditFromInstName_')]
    return ids


def _click_inst_link(driver, inst_id):
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


def download_all_equiv_child_pages_of_inst_page(driver, inst_page_dest_path, inst_page_num):
    """Returns ['gdvInstWithEQ_btnCreditFromInstName_0', 'gdvInstWithEQ_btnCreditFromInstName_1', 'gdvInstWithEQ_btnCreditFromInstName_2', ...]"""
    inst_ids = _get_inst_ids_from_html(inst_page_dest_path)

    for inst_id in inst_ids:
        print(f"{inst_id=}")

        _click_inst_link(driver, inst_id)

        _wait_until_equiv_page_loaded(driver)
        sleep(random.randint(1, 5))

        equiv_page_dest_path = inst_page_dest_path.parent / "equiv_pages" / f"inst_page_{inst_page_num}__{inst_id}.html"
        download_current_page_source(driver, equiv_page_dest_path)

        # Back to inst page
        _click_inst_list_link(driver)
        wait_until_inst_page_loaded(driver, inst_page_num)
        sleep(random.randint(1, 5))

        # if inst_id == "gdvInstWithEQ_btnCreditFromInstName_3":# TMP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #     break


