from pathlib import Path
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def download_current_page_source(driver, dest_path: Path):
    print(f"Downloading current page source to {dest_path=}...")

    # Now the driver page source should have the new info loaded, you can save it or parse it as needed
    html_content = driver.page_source

    # Save the page source to a file
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(html_content)



def wait_until_inst_page_loaded(driver, page_num):
    # Wait until the clicked page number is highlighted
    WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, f"//span[text()='{page_num}']"))
    )
    # sleep(random.randint(1, 5))