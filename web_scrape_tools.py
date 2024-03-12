from pathlib import Path
import random
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


DOT_DOT_DOT_INST_PAGE_NUMS = [11, 21, 31, 41]


def setup_driver():
    options = Options()
    # options.add_argument("--headless")  # Uncomment if you run in a headless environment
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    # Change user agent to avoid detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

    # Setup proxy if you have one - this is optional and can be commented out if not needed
    # proxy = Proxy()
    # proxy.proxy_type = ProxyType.MANUAL
    # proxy.http_proxy = "ip:port"
    # proxy.ssl_proxy = "ip:port"
    # capabilities = webdriver.DesiredCapabilities.CHROME
    # proxy.add_to_capabilities(capabilities)

    driver = webdriver.Chrome(options=options)  # , desired_capabilities=capabilities if using proxy
    return driver

def read_soup_from_html_file(html_path: Path) -> BeautifulSoup:
    with open(html_path, 'r', encoding='utf-8') as f:
        contents = f.read()
    return BeautifulSoup(contents, 'html.parser')

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