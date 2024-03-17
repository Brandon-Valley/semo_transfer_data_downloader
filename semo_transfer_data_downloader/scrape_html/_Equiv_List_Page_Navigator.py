from pathlib import Path
from pprint import pprint
import random
import shutil
from time import sleep
from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from ._web_scrape_tools import PAGE_DOWNLOADS_DIR_PATH, ProbablyGotDetectedAsBotException, download_current_page_source, human_click, human_click_delay, read_soup_from_html_file, setup_driver, wait_until_inst_page_loaded

from bs4 import BeautifulSoup
import re

WORKING_NAV_HTML_PATH = PAGE_DOWNLOADS_DIR_PATH / "Equiv_List_Page_Navigator_Working.html"


class Equiv_List_Page_Navigator():
    def __init__(self, driver, working_html_path: Path = WORKING_NAV_HTML_PATH):
        # Starts not downloaded
        self.driver = driver
        self.cur_page_html_path = working_html_path
        self.total_pages = None
        
        self.update_pagination_info()
        

    def print_pagination_vars(self):
        print("Equiv_List_Page_Navigator Pagination Vars:")
        print(f"..{self.total_pages=}")
        print(f"..{self.pagination=}")
        print(f"..{self.current_page_num=}")
        print(f"..{self.visible_page_nums=}")
        print(f"..{self.previous_paging_xpath=}")
        print(f"..{self.next_paging_xpath=}")


    
    def get_current_html_path(self):
        return self.cur_page_html_path
    
    def copy_current_html_to_dest(self, dest_path: Path):
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(self.cur_page_html_path, dest_path)
    

    def navigate_to_page_num_and_wait_until_loaded_if_needed(self, driver, page_num):
        def _click_non_current_visible_page_num_wait_until_loaded_update_pagination_info(page_num):
            print(f"Attempting to Click {page_num=} which SHOULD be visible AND non-highlighted...")
            assert self.pagination, f"{self.pagination=} is False"
            assert page_num in self.visible_page_nums, f"{page_num=} not in {self.visible_page_nums=}"
            assert page_num != self.current_page_num, f"{page_num=} is already the current page"
            
            try:
                link = self.driver.find_element(By.LINK_TEXT, str(page_num))
                human_click(driver, link)

                # Wait until new paginated equiv list page has loaded
                wait = WebDriverWait(self.driver, 50)
                wait.until(EC.text_to_be_present_in_element((By.XPATH, "//td/span"), str(page_num)))
            except selenium.common.exceptions.TimeoutException:
                raise ProbablyGotDetectedAsBotException("Got timeout exception on back to paginated equiv list page load, this probably means you actually got a 403 b/c bot detected")

            human_click_delay()
            self.update_pagination_info()

        def _click_3_dot_wait_until_loaded_update_pagination_info(mode: str):
            def _wait_until_new_3_dot_page_loaded():
                print("DOING IMPERFECT WAIT TO LOAD NEXT 3 DOT PAGE, IF PAGE LOADS TOO SLOW THIS WILL BREAK THINGS!")
                sleep(50) # Not sure how to tell when next page loaded # FIXME could speed up!
            
            if mode == "next":
                print(f"Attempting to navigate to NEXT 3 dots {self.next_paging_xpath=}...")
                xpath = self.next_paging_xpath
            elif mode == "previous" or mode == "prev":
                print(f"Attempting to navigate to PREVIOUS 3 dots {self.next_paging_xpath=}...")
                xpath = self.previous_paging_xpath
            else:
                raise ValueError(f"Invalid {mode=}")
            
            assert xpath, f"{xpath=} is None - {mode=}"

            link = self.driver.find_element(By.XPATH, xpath)
            human_click(driver, link)
            _wait_until_new_3_dot_page_loaded()
            self.update_pagination_info()


        self.update_pagination_info() # FIXME needed?

        if self.current_page_num == page_num:
            print(f"Already on {page_num=}")
            return
        
        assert self.pagination, f"{self.pagination=} is False - should not be possible"

        while True:
            print('hopefully not infinite loop')
            if page_num in self.visible_page_nums:
                if self.current_page_num == page_num:
                    print(f"Not sure how this is possible, but already on {page_num=}")
                    return
                _click_non_current_visible_page_num_wait_until_loaded_update_pagination_info(page_num)
                return
                
            if page_num < self.current_page_num:
                print(f"{page_num=} is not visible, and less than {self.current_page_num=} so clicking previous 3 dots...")
                _click_3_dot_wait_until_loaded_update_pagination_info("previous")
            elif page_num > self.current_page_num:
                print(f"{page_num=} is not visible, and greater than {self.current_page_num=} so clicking next 3 dots...")
                _click_3_dot_wait_until_loaded_update_pagination_info("next")
            else:
                raise ValueError(f"Invalid {page_num=} and {self.current_page_num=} - was checked above so shouldn't be possible")


    def update_pagination_info(self):
        def _get_total_pages(self):
            assert self.cur_page_html_path.is_file(), f"{self.cur_page_html_path=} is not a file"
            soup = read_soup_from_html_file(self.cur_page_html_path)

            # Find the 'span' element with id 'lblCourseEQPaginationInfo'
            span = soup.find('span', id='lblCourseEQPaginationInfo')

            if not span:
                return 1
            # Extract the total number of pages from the span's text
            return int(span.text.split('OF')[-1])
        

        print(f"Updating pagination info...")

        # For testing
        if self.driver:
            download_current_page_source(self.driver, self.cur_page_html_path)

        if not self.total_pages:
            self.total_pages = _get_total_pages(self)

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
                self.current_page_num = int(td.find('span').text)
            except AttributeError:
                pass

            a = td.find('a')
            # print(f"{a=}")
            xpath = None
            if a:
                href = a['href']
                xpath = f"//a[@href=\"{href}\"]"
            # print(f"{href=}")
                
                # f"//a[@href=\"javascript:__doPostBack('gdvCourseEQ','Page${equiv_list_page_num}')\"]"

            if td.text == "...":
                if td_num == 1:
                    self.previous_paging_xpath = xpath
                else:
                    self.next_paging_xpath = xpath
                continue
            
            self.visible_page_nums.append(int(td.text))
        
        print("Updated pagination info.")
        self.print_pagination_vars()



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
        nav.print_pagination_vars()

    _test_html_str_path("C:/Users/Brandon/Downloads/tmp.html")
    _test_html_str_path("C:/p/semo_transfer_data_downloader/page_downloads/institution_page_downloads/equiv_w_1_page_ex.htm")
    _test_html_str_path("C:/p/semo_transfer_data_downloader/page_downloads/institution_page_downloads/equiv_11_pages_ex.html")
    _test_html_str_path("C:/Users/Brandon/Downloads/tttTES Public View_ SOUTHEAST MISSOURI STATE UNIVERSITY.html")

    print("End of Main") 