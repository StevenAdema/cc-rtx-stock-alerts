"""
Class of functions to create a headless webdriver to scrape Canada Computers
site for in stock RTX graphics cards.  Can be used to create a dictionary of 
in stock items as well as print a simple formatted summary.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import os.path
from os import path
import requests
import os
import sys
import yaml


def get_driver():
    """Create a chrome webdriver.
    Generate a random user agent for use in headless browser.

    :return: webdriver
    """
    chromeOptions = Options()
    ua = UserAgent()
    ua = ua.random
    chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    chromeOptions.add_argument(f'user-agent={ua}')
    chromeOptions.headless = True

    if (path.exists(WINDOWS_PATH)):
        driver = webdriver.Chrome(executable_path=WINDOWS_PATH, options=chromeOptions)
    else:
        print('chromedriver does not exist in ', WINDOWS_PATH)

    driver.get('chrome://settings/clearBrowserData')

    return driver


def scrape_canada_computers(driver):
    """Scrapes a single canadacomputers.com webpage with multiple listings for any in-stock items.

    :param driver: intialized webdriver
    :return: text_body
    """

    # Check all listings on page for stock
    canada_computer_urls = []
    stock_dic = {}
    cc_url = CARD_TYPE_DIC.get(CARD_TYPE)

    driver.get(cc_url)
    driver.implicitly_wait(1)
    
    listings = driver.find_elements_by_class_name("stocklevel-pop")

    for listing in listings:
        listing_info = listing.find_element_by_xpath("following-sibling::div[1]")
        try:
            driver.implicitly_wait(0.01)
            item_URL = ((listing_info.find_element_by_class_name("productImageSearch")).find_element_by_tag_name("a")).get_attribute("href")
            stock_status_element = listing_info.find_elements_by_class_name('pq-hdr-bolder')
            if len(stock_status_element) != 0:
                canada_computer_urls.append(item_URL)
        except:  # Proceed when no stock is found
            pass
       
    # Loop through potential urls with cards in stock
    for URL in canada_computer_urls:
        driver.get(URL)
        driver.implicitly_wait(3)
        # Looks for items in stock online vs in store
        for elements in driver.find_elements_by_class_name('pi-prod-availability'):
            rtx_card = driver.title.rstrip("| Canada Computers & Electronics")
            stock_dic[rtx_card] = {}
            stock_dic[rtx_card]["url"] = URL
            stock_dic[rtx_card]['card name'] = rtx_card
            driver.implicitly_wait(.1)
            this = driver.find_elements_by_class_name("h2-big")
            stock_dic[rtx_card]["price"] = driver.find_elements_by_class_name("h2-big")[0].text

            # Check local store stock
            if len(stores_to_check) != 0:
                if "Available In Stores" in elements.text:
                    # Opens inventory view for all stores
                    other_stores = driver.find_element_by_css_selector(".stocklevel-pop")
                    driver.execute_script("arguments[0].setAttribute('class','stocklevel-pop d-block')", other_stores)

                    stock_dic[rtx_card]["store location"] = "online only"
                    stock_dic[rtx_card]["stock"] = 'n/a'

                    for store in stores_to_check:
                        store_element = driver.find_element_by_link_text(store)
                        stock = store_element.find_element_by_xpath('./../../../div[2]/div/p/span').text
                        if stock == "-":
                            stock = 0
                        else:
                            stock = int(stock[0:1])  # Truncates where x+ --> x
                        if stock > 0:
                            stock_dic[rtx_card]["stock"] = stock
                            if "store location" in stock_dic[rtx_card]:
                                stock_dic[rtx_card]["store location"] = store

    return stock_dic



def generate_text_body(stock_dic):
    """Produce summary of cards in stock

    :param stock_dic: a stock summary dictionary created by scraper
    """
    stock_summary = []
    for item, details in stock_dic.items():
        if details["stock"] != -1:
            # stock_summary.append(f"{item} is in stock IN STORE at Canada Computers for {details['price']}\n"
            stock_summary.append(f"{item}\n"
                                 f"{details['store location']}\n"
                                 f"{details['price']}\n"
                                 f"{details['stock']} in stock\n"
                                 f"{details['url']}\n\n"
                                 )                      

    text_body = ""
    for hits in stock_summary:
        text_body += hits

    return text_body


def get_yaml():
    with open("./config/config.yaml", 'r') as stream:
    # with open("../config/config.yaml", 'r') as stream: # if running here
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    globals().update(conf)

    return conf
