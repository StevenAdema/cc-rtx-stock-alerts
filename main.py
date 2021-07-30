import datetime
import pandas as pd
import scraping.cc_scraper as cc
import os
import sys
from colorama import init, Fore, Back, Style
import pprint as pp
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)

init()
conf = cc.get_yaml()
driver = cc.get_driver()
# stock_dic = cc.scrape_canada_computers(driver)
stock_dic = {
   "PNY GeForce RTX 3070 8GB XLR8 Gaming REVEL EPIC-X RGB Triple F":{
      "url":"https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=193053&sid=f1jbh3voqgfbbt2aql6tbuopj2",
      "card name":"PNY GeForce RTX 3070 8GB XLR8 Gaming REVEL EPIC-X RGB Triple F",
      "price":"$1,399.00",
      "store location":"online only",
      "stock":0
   },
   "ZOTAC GAMING GeForce RTX 3060 Ti Twin Edge OC LHR 8GB GDDR6 1695 MHz 3 DP+HDMI ZT-A30610H-10MLHR":{
      "url":"https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=196048&sid=f1jbh3voqgfbbt2aql6tbuopj2",
      "card name":"ZOTAC GAMING GeForce RTX 3060 Ti Twin Edge OC LHR 8GB GDDR6 1695 MHz 3 DP+HDMI ZT-A30610H-10MLHR",
      "price":"$849.00",
      "store location":"online only, Kanata",
      "stock":1
   }
}

df = pd.DataFrame.from_dict(stock_dic)
pp.pprint(df)
exit()
# text_body = cc.generate_text_body(stock_dic)
print(Fore.GREEN + text_body)


