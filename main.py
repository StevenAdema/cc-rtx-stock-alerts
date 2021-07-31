import datetime
import pandas as pd
import utils.cc_scraper as cc
import os
import sys
from colorama import init, Fore, Back, Style
import time
from discord import Webhook, RequestsWebhookAdapter
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import re
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_colwidth', 50)
pd.set_option('display.width', 400)


def get_stock_dic():
    conf = cc.get_yaml()
    driver = cc.get_driver()
    stock_dic = cc.scrape_canada_computers(driver)

    driver.quit()
    return stock_dic

# def send_discord_message():

def send_discord_message(dic):
    captain_hook = ""
    webhook = DiscordWebhook(url=captain_hook)
    title = 'RTX Card(s) in Stock!'
    body = generate_description(dic)
    embed = DiscordEmbed(title=title, description=body, color='03b2f8')
    webhook.add_embed(embed)
    response = webhook.execute()

def generate_description(d):
    card_name = d[list(d)[0]]['card name']
    # card_name = card_name.split("Ti", 1)[0]
    # card_name = card_name.split("0 ", 1)[0]
    price = d[list(d)[0]]['price']
    location = d[list(d)[0]]['store location']
    stock = d[list(d)[0]]['stock']
    url = d[list(d)[0]]['url']
    body = '''\
        {c}.
        price: {p}.
        store: {s}.
        stock: {t}.
        url: {u}.\
        '''.format(c=card_name, p=price, s=location, t=stock, u=url)
    
    return body

current_stock = {
     "PNY GeForce RTX 3070 8GB XLR8 Gaming REVEL EPIC-X RGB Triple F":{
        "url":"https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=193053&sid=f1jbh3voqgfbbt2aql6tbuopj2",
        "card name":"PNY GeForce RTX 3070 8GB XLR8 Gaming REVEL EPIC-X RGB Triple F",
        "price":"$1,399.00",
        "store location":"Orleans",
        "stock":'2'
     },
     "ZOTAC GAMING GeForce RTX 3060 Ti Twin Edge OC LHR 8GB GDDR6 1695 MHz 3 DP+HDMI ZT-A30610H-10MLHR":{
        "url":"https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=196048&sid=f1jbh3voqgfbbt2aql6tbuopj2",
        "card name":"ZOTAC GAMING GeForce RTX 3060 Ti Twin Edge OC LHR 8GB GDDR6 1695 MHz 3 DP+HDMI ZT-A30610H-10MLHR",
        "price":"$849.00",
        "store location":"Kanata",
        "stock":1
     }
  }

nexttime = time.time()
# current_stock = get_stock_dic()

if current_stock:
    send_discord_message(current_stock)
    exit()

while True:
    new_stock = get_stock_dic()
    if next(iter(current_stock)) != next(iter(new_stock)) and len(current_stock) != len(new_stock):
        print(len(current_stock))
        print(len(new_stock))
        send_discord_message(new_stock)
    exit()
    nexttime += 60
    sleeptime = nexttime - time.time()
    if sleeptime > 0:
        time.sleep(sleeptime)
