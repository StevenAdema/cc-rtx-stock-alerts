import datetime
import pandas as pd
import utils.cc_scraper as cc
import os
import sys
from colorama import init, Fore, Back, Style
import time
import utils.discord as dis
import requests
import re
import logging
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler("log.txt"),
                        logging.StreamHandler()]
                    )
logging.getLogger().setLevel(logging.INFO)

def get_stock_dic():
    cc.get_yaml()
    driver = cc.get_driver()
    stock_dic = cc.scrape_canada_computers(driver)

    driver.quit()
    return stock_dic

logging.info('CC RTX Tracking Bot Started')
nexttime = time.time()
current_stock = get_stock_dic()

if current_stock:
    logging.info('CARD FOUND!')
    logging.info(cc.generate_text_body(current_stock))
    dis.send_discord_message(current_stock)
else:
    logging.info('No cards in stock.')

while True:
    new_stock = get_stock_dic()
    if current_stock != new_stock:
        logging.info('CARD FOUND!')
        logging.info(cc.generate_text_body(current_stock))
        dis.send_discord_message(new_stock)
    else:
        logging.info('No cards in stock. Trying again in 120 seconds')
    nexttime += 120
    sleeptime = nexttime - time.time()
    if sleeptime > 0:
        time.sleep(sleeptime)
