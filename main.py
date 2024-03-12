from pathlib import Path
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from download_all_equiv_child_pages_of_inst_page import download_all_equiv_child_pages_of_inst_page
from web_scrape_tools import download_current_page_source, wait_until_inst_page_loaded

MAX_INST_PAGES = 41
STARTING_INST_PAGE_NUM = 1
MAX_INST_PER_INST_PAGE = 50 # TMP need?

DOT_DOT_DOT_INST_PAGE_NUMS = [11,21,31,41]

SCRIPT_PARENT_DIR_PATH = Path(__file__).parent
INST_PAGE_DOWNLOADS_DIR_PATH = SCRIPT_PARENT_DIR_PATH / "page_downloads" / "inst_pages"

def _click_inst_page_num(driver, page_num):
    print(f"Clicking {page_num=}...")

    if page_num in DOT_DOT_DOT_INST_PAGE_NUMS:
        # Find the link with text "..."
        link = driver.find_element(By.XPATH, f"//a[@href=\"javascript:__doPostBack('gdvInstWithEQ','Page${page_num}')\"]")
    else:
        # Find the link with text "page_num" and click it
        link = driver.find_element(By.LINK_TEXT, str(page_num))
    link.click()


# Setup WebDriver (you need to download a driver for this, e.g., chromedriver)
driver = webdriver.Chrome()


# The URL of the page you're interacting with
url = "https://tes.collegesource.com/publicview/TES_publicview01.aspx?rid=1f7d5d36-c901-4196-8575-28ee59bf7f4a&aid=aa590d78-6e6a-4ea3-97c6-9f6102c1c4c0"
driver.get(url)

# Start on right page when testing
if STARTING_INST_PAGE_NUM != 1:
    assert STARTING_INST_PAGE_NUM < 12, f"Invalid {STARTING_INST_PAGE_NUM=} / not yet supported"
    _click_inst_page_num(driver, STARTING_INST_PAGE_NUM)
    wait_until_inst_page_loaded(driver, STARTING_INST_PAGE_NUM)
    sleep(random.randint(1, 5))

for inst_page_num in range(STARTING_INST_PAGE_NUM, MAX_INST_PAGES + 1):
    print(f"{inst_page_num=}")

    if inst_page_num > STARTING_INST_PAGE_NUM:
        _click_inst_page_num(driver, inst_page_num)

    wait_until_inst_page_loaded(driver, inst_page_num)
    sleep(random.randint(1, 5))

    # Download inst page
    inst_page_dest_path = INST_PAGE_DOWNLOADS_DIR_PATH / f"inst_page_{inst_page_num}.html"
    download_current_page_source(driver, inst_page_dest_path)

    # Download all equiv child pages of inst page
    download_all_equiv_child_pages_of_inst_page(driver, inst_page_dest_path, inst_page_num)
    
# Always remember to close the driver
driver.quit()
