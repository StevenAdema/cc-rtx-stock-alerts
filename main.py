import datetime
import scraping.cc_scraper as cc
import os
import sys
from colorama import init, Fore, Back, Style

init()
conf = cc.get_yaml()
driver = cc.get_driver()
stock_dic = cc.scrape_canada_computers(driver)
text_body = cc.generate_text_body(stock_dic)
print(Fore.GREEN + text_body)


