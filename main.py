import datetime
import pandas as pd
import scraping.cc_scraper as cc
import os
import sys
from colorama import init, Fore, Back, Style
import time
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.width', 400)


def get_stock():
	conf = cc.get_yaml()
	driver = cc.get_driver()
	# stock_dic = cc.scrape_canada_computers(driver)
	stock_dic = {
	   "PNY GeForce RTX 3070 8GB XLR8 Gaming REVEL EPIC-X RGB Triple F":{
	      "url":"https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=193053&sid=f1jbh3voqgfbbt2aql6tbuopj2",
	      "card name":"PNY GeForce RTX 3070 8GB XLR8 Gaming REVEL EPIC-X RGB Triple F",
	      "price":"$1,399.00",
	      "store location":"online only",
	      "stock":'n/a'
	   },
	   "ZOTAC GAMING GeForce RTX 3060 Ti Twin Edge OC LHR 8GB GDDR6 1695 MHz 3 DP+HDMI ZT-A30610H-10MLHR":{
	      "url":"https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=196048&sid=f1jbh3voqgfbbt2aql6tbuopj2",
	      "card name":"ZOTAC GAMING GeForce RTX 3060 Ti Twin Edge OC LHR 8GB GDDR6 1695 MHz 3 DP+HDMI ZT-A30610H-10MLHR",
	      "price":"$849.00",
	      "store location":"Kanata",
	      "stock":1
	   }
	}
	df = pd.DataFrame(stock_dic.values())
	print(df)

nexttime = time.time()
while True:
    get_stock()
    nexttime += 15
    sleeptime = nexttime - time.time()
    if sleeptime > 0:
        time.sleep(sleeptime)
