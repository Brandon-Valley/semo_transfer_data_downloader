from pathlib import Path
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType

from semo_transfer_data_downloader import cfg
from semo_transfer_data_downloader.scrape_html._web_scrape_tools import DOT_DOT_DOT_INST_PAGE_NUMS, human_click, human_click_delay, setup_driver, wait_until_inst_page_loaded, download_current_page_source
from semo_transfer_data_downloader.scrape_html._download_all_equiv_child_pages_of_inst_page import download_all_equiv_list_pages_of_all_insts_on_current_inst_list_page

MAX_INST_PAGES = 41
STARTING_INST_PAGE_NUM = 1


SCRIPT_PARENT_DIR_PATH = Path(__file__).parent

def _click_inst_page_num(driver, page_num):
    print(f"Clicking {page_num=}...")

    if page_num in DOT_DOT_DOT_INST_PAGE_NUMS:
        link = driver.find_element(By.XPATH, f"//a[@href=\"javascript:__doPostBack('gdvInstWithEQ','Page${page_num}')\"]")
    else:
        link = driver.find_element(By.LINK_TEXT, str(page_num))
    human_click(driver, link)

def _goto_clickable_inst_list_page_num(driver, clickable_inst_list_page_num):
    print(f"Clicking and loading what SHOULD BE clickable page num: {clickable_inst_list_page_num}...")
    _click_inst_page_num(driver, clickable_inst_list_page_num)
    wait_until_inst_page_loaded(driver, clickable_inst_list_page_num)
    human_click_delay()

def scrape_html():
    """Scrape all institution list pages and all equivalency list pages of all institutions on each institution list page."""

    driver = setup_driver()
    url = "https://tes.collegesource.com/publicview/TES_publicview01.aspx?rid=1f7d5d36-c901-4196-8575-28ee59bf7f4a&aid=aa590d78-6e6a-4ea3-97c6-9f6102c1c4c0"
    driver.get(url)

    if STARTING_INST_PAGE_NUM != 1:
        # Get to right inst list page from first
        for dot_dot_dot_page_num in DOT_DOT_DOT_INST_PAGE_NUMS:
            if STARTING_INST_PAGE_NUM > dot_dot_dot_page_num:
                _goto_clickable_inst_list_page_num(driver, dot_dot_dot_page_num)

        # Click the needed STARTING_INST_PAGE_NUM once you are on the right page
        _goto_clickable_inst_list_page_num(driver, STARTING_INST_PAGE_NUM)


    for inst_page_num in range(STARTING_INST_PAGE_NUM, MAX_INST_PAGES + 1):
        print(f"{inst_page_num=}")
        if inst_page_num > STARTING_INST_PAGE_NUM:
            _click_inst_page_num(driver, inst_page_num)
        wait_until_inst_page_loaded(driver, inst_page_num)
        human_click_delay()

        inst_page_dest_path = cfg.WORK_INST_LIST_HTML_DOWNLOADS_DIR_PATH / f"inst_list_page_{inst_page_num}.html"
        download_current_page_source(driver, inst_page_dest_path)

        download_all_equiv_list_pages_of_all_insts_on_current_inst_list_page(driver, inst_page_dest_path, inst_page_num, cfg.WORK_EQUIV_LIST_HTML_DOWNLOADS_DIR_PATH)

    driver.quit()
