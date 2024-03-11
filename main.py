from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Setup WebDriver (you need to download a driver for this, e.g., chromedriver)
driver = webdriver.Chrome()

# The URL of the page you're interacting with
url = "https://tes.collegesource.com/publicview/TES_publicview01.aspx?rid=1f7d5d36-c901-4196-8575-28ee59bf7f4a&aid=aa590d78-6e6a-4ea3-97c6-9f6102c1c4c0"
driver.get(url)

# Find the link by its id and click it
link = driver.find_element(By.ID, "gdvInstWithEQ_btnCreditFromInstName_0")
link.click()

# sleep(30)

# Wait until equiv. info loads
wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_element_located((By.ID, 'btnAddToMyEQList')))

# Now the driver page source should have the new info loaded, you can save it or parse it as needed
html_content = driver.page_source

# Save the page source to a file
with open(Path('page_downloads') / 'page_content.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

# Always remember to close the driver
driver.quit()
