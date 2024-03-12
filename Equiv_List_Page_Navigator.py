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

from web_scrape_tools import DOT_DOT_DOT_INST_PAGE_NUMS, download_current_page_source, read_soup_from_html_file, setup_driver, wait_until_inst_page_loaded

from bs4 import BeautifulSoup
import re


# def _is_equiv_list_page_number_highlighted(html_file_path, page_num):
#     """no link if highlighted, can start any page highlighted"""
#     soup = read_soup_from_html_file(html_file_path)
#     highlighted_page_num = soup.find('span', text=str(page_num))
#     return highlighted_page_num is not None

# def _click_non_highlighted_equiv_list_page_num_and_wait_for_load(driver, equiv_list_page_num):

#     print(f"Attempting to Click non-highlighted {equiv_list_page_num=}...")

#     try:
#         link = driver.find_element(By.LINK_TEXT, str(equiv_list_page_num))
#     except Exception as e:
#         print(str(e))

#         if equiv_list_page_num == 1:
#             while True:
#                 print("HOPE THIS DOESN'T CAUSE AN INFINITE LOOP")

#                 # Find the first link with visible text "..." and click it
#                 link = driver.find_element(By.XPATH, "//a[text()='...']")
#                 link.click()

#                 sleep(40) # Dont know start / what num to wait for
#                 try:
#                     link = driver.find_element(By.LINK_TEXT, str(equiv_list_page_num))
#                     print("Found #1!")
#                     break # Found #1 !!
#                 except Exception as e:
#                     print(f"Here we go again...{str(e)}")
#         else:
#             try:
#                 link = driver.find_element(By.XPATH, f"//a[@href=\"javascript:__doPostBack('gdvCourseEQ','Page${equiv_list_page_num}')\"]")
#             except Exception as e2:
#                 if equiv_list_page_num == 1:
#                     # # Find the first link with visible text "..." and click it
#                     # link = driver.find_element(By.XPATH, "//a[text()='...']")
#                     # FIXME??

#                     raise Exception(f"Could not find non-highlighted {equiv_list_page_num=}") from e2

#     link.click()

#     # Wait until new paginated equiv list page has loaded
#     wait = WebDriverWait(driver, 50)
#     wait.until(EC.text_to_be_present_in_element((By.XPATH, "//td/span"), str(equiv_list_page_num)))
#     sleep(random.randint(1, 3)) # Mimic human delay after click

# def _get_to_first_equiv_list_page_downloaded_and_highlighted(driver, equiv_page_1_dest_path, inst_id):
#     """Get to starting position"""
#     _click_inst_link(driver, inst_id)

#     _wait_until_equiv_page_loaded(driver)
#     sleep(random.randint(1, 3))

#     # Download what is most likely to be the first equiv list page
#     download_current_page_source(driver, equiv_page_1_dest_path)

#     # Confirm this is actually page #1, if not, click page #1 and download
#     if not _is_equiv_list_page_number_highlighted(equiv_page_1_dest_path, 1) and _get_num_equiv_list_pages_from_first_equiv_list_html_path(equiv_page_1_dest_path) > 1:
#         print("Page #1 is not highlighted, replacing it & getting tto known starting position...")
#         _click_non_highlighted_equiv_list_page_num_and_wait_for_load(driver, 1)
#         download_current_page_source(driver, equiv_page_1_dest_path)
    
#     print("Now we know equiv list page #1 is highlighted (if more than 1 page) AND downloaded!")


# def _get_cur_equiv_list_page_position_info(html_file_path):
#     # Parse the HTML with BeautifulSoup
#     soup = read_soup_from_html_file(html_file_path)

#     # Find the highlighted page number
#     highlighted_page_num = int(soup.find('span').text)

#     # Find all visible page numbers
#     visible_page_nums = [int(a.text) for a in soup.find_all('a') if a.text.isdigit()]

#     # Include the highlighted page number in the list of visible page numbers
#     if highlighted_page_num not in visible_page_nums:
#         visible_page_nums.append(highlighted_page_num)

#     return highlighted_page_num, visible_page_nums




def _get_page_numbers_and_paging_xpaths(html_file_path):
    # Open and read the HTML file
    with open(html_file_path, 'r') as file:
        html = file.read()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find the highlighted page number
    highlighted_page_num = int(soup.find('span').text)

    # Find all visible page numbers
    visible_page_nums = [int(a.text) for a in soup.find_all('a') if a.text.isdigit()]

    # Include the highlighted page number in the list of visible page numbers
    if highlighted_page_num not in visible_page_nums:
        visible_page_nums.append(highlighted_page_num)

    # Find the previous and next paging xpaths
    a_elements = soup.find_all('a')
    print("a_elements:")
    pprint(a_elements)
    
    previous_paging_xpath = None
    next_paging_xpath = None
    for i, a in enumerate(a_elements):
        if a.text == '...':
            if i < len(a_elements) - 1 and a_elements[i + 1].text.isdigit():
                previous_paging_xpath = f"//a[@href=\"{a['href']}\"]"
            if i > 0 and a_elements[i - 1].text.isdigit():
                next_paging_xpath = f"//a[@href=\"{a['href']}\"]"

    return highlighted_page_num, visible_page_nums, previous_paging_xpath, next_paging_xpath




class Equiv_List_Page_Navigator():
    def __init__(self, driver, cur_page_html_path: Path):
        # Starts not downloaded
        self.driver = driver
        self.cur_page_html_path = cur_page_html_path
        
        self.update_pagination_info()


    def update_pagination_info(self):
        # download_current_page_source(self.driver, self.cur_page_html_path)#TMP

        # Pagination info
        self.pagination = False
        self.current_page_num = 1 # current page == highlighted page if pagination
        self.visible_page_nums = []
        self.previous_paging_xpath = None
        self.next_paging_xpath = None

        soup = read_soup_from_html_file(self.cur_page_html_path)
        pagination_table_row_html = soup.find('tr', class_='pagination-tes')
        # print("pagination_table_row_html:")
        # pprint(pagination_table_row_html)

        if not pagination_table_row_html:
            return
        
        self.pagination = True

        # print(type(pagination_table_row_html))
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # tbody = pagination_table_row_html.find('tbody')
        for td_num, td in enumerate(pagination_table_row_html.find_all('td')):
            if td_num == 0:
                continue
            # print("vvvvvvvvvvvvvvvvvvv td" + str(td_num))
            # print(f"{td=}")

            try:
                # print(f"{td['span']=}")
                self.current_page_num = td['span']
            except KeyError:
                pass

            # if 'span' in td.keys():
            #     self.current_page_num = int(td.text)

            # href = td.find('a')['href']
            a = td.find('a')
            # print(f"{a=}")
            href = None
            if a:
                href = a['href']
            # print(f"{href=}")

            if td.text == "...":
                if td_num == 1:
                    self.previous_paging_xpath = href
                else:
                    self.next_paging_xpath = href
                continue
            
            self.visible_page_nums.append(int(td.text))



        # self.highlighted_page_num, self.visible_page_nums, self.previous_paging_xpath, self.next_paging_xpath = _get_page_numbers_and_paging_xpaths(self.cur_page_html_path)

if __name__ == "__main__":
    import os.path as path
    print("Running " , path.abspath(__file__) , '...')


    HTML_PATH = Path("C:/Users/Brandon/Downloads/tmp.html")
    HTML_1_PAGE_PATH = Path("C:/p/semo_transfer_data_downloader/page_downloads/institution_page_downloads/equiv_w_1_page_ex.htm")
    # driver = setup_driver()

    def _test_html_str_path(html_str_path):
        print(f"Testing {html_str_path}...")
        nav = Equiv_List_Page_Navigator(None, Path(html_str_path))
        print("############# RESULTS #############")
        print(f"{nav.pagination=}")
        print(f"{nav.current_page_num=}")
        print(f"{nav.visible_page_nums=}")
        print(f"{nav.previous_paging_xpath=}")
        print(f"{nav.next_paging_xpath=}")

    _test_html_str_path("C:/Users/Brandon/Downloads/tmp.html")
    _test_html_str_path("C:/p/semo_transfer_data_downloader/page_downloads/institution_page_downloads/equiv_w_1_page_ex.htm")
    _test_html_str_path("C:/p/semo_transfer_data_downloader/page_downloads/institution_page_downloads/equiv_11_pages_ex.html")

    print("End of Main") 