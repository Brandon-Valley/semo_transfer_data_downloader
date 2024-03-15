# from pathlib import Path
# from pprint import pprint
# import random
# from time import sleep
# from selenium import webdriver
# from selenium.webdriver.common.by import By

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from bs4 import BeautifulSoup
# from Equiv_List_Page_Navigator import Equiv_List_Page_Navigator

# from web_scrape_tools import DOT_DOT_DOT_INST_PAGE_NUMS, download_current_page_source, read_soup_from_html_file, wait_until_inst_page_loaded

# from bs4 import BeautifulSoup
# import re

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
#     human_click_delay() # Mimic human delay after click

# def _get_to_first_equiv_list_page_downloaded_and_highlighted(driver, equiv_page_1_dest_path, inst_id):
#     """Get to starting position"""
#     _click_inst_link(driver, inst_id)

#     _wait_until_equiv_page_loaded(driver)
#     human_click_delay()

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




# # def get_page_numbers_and_paging_xpaths(html_file_path):
# #     # Open and read the HTML file
# #     with open(html_file_path, 'r') as file:
# #         html = file.read()

# #     # Parse the HTML with BeautifulSoup
# #     soup = BeautifulSoup(html, 'html.parser')

# #     # Find the highlighted page number
# #     highlighted_page_num = int(soup.find('span').text)

# #     # Find all visible page numbers
# #     visible_page_nums = [int(a.text) for a in soup.find_all('a') if a.text.isdigit()]

# #     # Include the highlighted page number in the list of visible page numbers
# #     if highlighted_page_num not in visible_page_nums:
# #         visible_page_nums.append(highlighted_page_num)

# #     # Find the previous and next paging xpaths
# #     a_elements = soup.find_all('a')
# #     print("a_elements:")
# #     pprint(a_elements)
    
# #     previous_paging_xpath = None
# #     next_paging_xpath = None
# #     for i, a in enumerate(a_elements):
# #         if a.text == '...':
# #             if i < len(a_elements) - 1 and a_elements[i + 1].text.isdigit():
# #                 previous_paging_xpath = f"//a[@href=\"{a['href']}\"]"
# #             if i > 0 and a_elements[i - 1].text.isdigit():
# #                 next_paging_xpath = f"//a[@href=\"{a['href']}\"]"

# #     return highlighted_page_num, visible_page_nums, previous_paging_xpath, next_paging_xpath

# # # Use the function
# # highlighted_page_num, visible_page_nums, previous_paging_xpath, next_paging_xpath = get_page_numbers_and_paging_xpaths('path_to_your_html_file')
# # print('Highlighted page number:', highlighted_page_num)
# # print('Visible page numbers:', visible_page_nums)
# # print('Previous paging xpath:', previous_paging_xpath)
# # print('Next paging xpath:', next_paging_xpath)


# def get_to_first_equiv_list_page_downloaded_and_highlighted_from_any_inst_equiv_list_page(driver: webdriver.Chrome, equiv_page_1_dest_path: Path):
#     nav = Equiv_List_Page_Navigator(driver, equiv_page_1_dest_path)
#     print(f"{nav.highlighted_page_num=}")
#     exit(f"{nav.highlighted_page_num=}")