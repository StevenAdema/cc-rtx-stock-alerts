from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from email.mime.text import MIMEText
from fake_useragent import UserAgent
import os.path
from os import path
import requests
from discord import Webhook, RequestsWebhookAdapter, Embed
import smtplib
import dotenv
import os
import sys
import winsound

# Set to True to turn on
discord_message_enabled = True
email_enabled = False
beep_enabled = True

# Variables
CC_URL = "https://www.canadacomputers.com/index.php?cPath=43_557_559&sf=:3_6,3_7,3_8&mfr=&pr="
vendor_name = "Canada Computers"
stores_to_check = [
    "Kanata",
    "Downtown Ottawa",
    "Ottawa Orleans",
    "Ottawa Merivale",
    "East Vancouver",
    "Richmond"
    ]
item = "RTX 3070"    
email_bodies = {
        "Newegg": "",
        "Best Buy": "",
        "Memory Express": "",
        "Canada Computers": "",
        "Amazon": "",
        "PC Canada": "",
    }
def initialize_webdriver():
    """Initializes a chrome webdriver for use in the scraping functions.
    Generates a random user agent and run in a headless browser.
    Compatible with both Windows and Linux once chromedriver paths are set.

    :return: the initialized webdriver, ready to accept URLs
    """
    WINDOWS_PATH = 'C:/bin/chromedriver.exe'

    # Operates as a random user agent in a headless browser
    chromeOptions = Options()
    ua = UserAgent()
    userAgent = ua.random
    chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    chromeOptions.add_argument(f'user-agent={userAgent}')
    chromeOptions.headless = True

    if (path.exists(WINDOWS_PATH)):
        driver = webdriver.Chrome(executable_path=WINDOWS_PATH, options=chromeOptions)
    else:
        print('chromedrive not found in path')
        
    # driver.get('chrome://settings/clearBrowserData')

    return driver


def scrape_canada_computers(driver, vendor_name):
    """Scrapes a single canadacomputers.com webpage with multiple listings for any in-stock items.

    :param vendor_name: the name of the webpage vendor
    :param driver: an initialized webdriver
    :return: email_body
    """

    # Check all listings on page for stock
    canada_computer_urls = []
    stock_dict = {}

    driver.get(CC_URL)
    driver.implicitly_wait(2)
    
    listings = driver.find_elements_by_class_name("stocklevel-pop")
    # listings = driver.find_elements_by_partial_link_text(item)
    # print(listings)

    for listing in listings:
        listing_info = listing.find_element_by_xpath("following-sibling::div[1]")
        try:
            driver.implicitly_wait(0.01) # Give the scraper 10 ms to look for the element below
            item_URL = ((listing_info.find_element_by_class_name("productImageSearch")).find_element_by_tag_name("a")).get_attribute("href")
            # pq-hdr-bolder contains stock information text if the item is in stock at all, otherwise does not appear on page
            stock_status_element = listing_info.find_elements_by_class_name('pq-hdr-bolder')
            if len(stock_status_element) != 0:
                canada_computer_urls.append(item_URL)
        except:  # When stock_status_element is not on the page for that listing, move on to the next listing
            pass

    # drop duplicates=
    # print(canada_computer_urls)
    # exit()
       
    # Iterates through individual pages for where stock may have been detected
    for URL in canada_computer_urls:
        driver.get(URL)
        driver.implicitly_wait(10)
        # Looks for items in stock online vs in store
        for elements in driver.find_elements_by_class_name('pi-prod-availability'):
            item_name = driver.title.rstrip("| Canada Computers & Electronics")
            stock_dict[item_name] = {}
            stock_dict[item_name]["url"] = URL
            # Checks and stores online stock status for item
            if "Online In Stock" in elements.text:
                print(f"Online stock found: \n{URL}")
                stock_dict[item_name]["online stock status"] = "In stock"
            else:
                stock_dict[item_name]["online stock status"] = "Out of stock"

            # Checks and stores local store stock status for item
            if len(stores_to_check) != 0:
                if "Available In Stores" in elements.text:
                    # Opens inventory view for all stores
                    other_stores = driver.find_element_by_css_selector(".stocklevel-pop")
                    driver.execute_script("arguments[0].setAttribute('class','stocklevel-pop d-block')", other_stores)

                    # Only changes if stock at desired store is detected
                    stock_dict[item_name]["in store status"] = "No store stock"

                    for store in stores_to_check:
                        # Finds store's name on webpage
                        store_element = driver.find_element_by_link_text(store)
                        # Finds stock value by xpath relative to store name
                        stock = store_element.find_element_by_xpath('./../../../div[2]/div/p/span').text

                        # Converts stock value into integer
                        if stock == "-":
                            stock = 0
                        else:
                            stock = int(stock[0:1])  # Truncates 5+ to 5
                        
                        if stock > 0:
                            print(f"In-store stock found at {store}: \n{URL}")
                            stock_dict[item_name]["in store status"] = "In store"
                            if "store location" in stock_dict[item_name]:
                                stock_dict[item_name]["store location"] += f", {store}"
                            else:
                                stock_dict[item_name]["store location"] = store 
                else:
                    stock_dict[item_name]["in store status"] = "No store stock"
            else:
                stock_dict[item_name]["in store status"] = "Not checked"
            
            stock_dict[item_name]["backorder status"] = "Not checked"
            
    email_body = generate_email_body(stock_dict, vendor_name)

    return email_body



def generate_email_body(stock_dict, vendor_name):
    """Generates an email body based on passed stock dictionary and vendor

    :param stock_dict: a stock summary dictionary created in the scraping function
    :param vendor_name: the name of the vendor that was scraped
    """
    # Creates a summary list of items in stock, differentiating online vs in store
    stock_summary = []
    for item, details in stock_dict.items():
        print(details)
        if details["online stock status"] == "In stock":
            # stock_summary.append(f"{item} is in stock ONLINE at {vendor_name} for {details['price']}\n"
            stock_summary.append(f"{item} is in stock ONLINE at {vendor_name}\n"
                                 f"{details['url']}\n\n")
        if details["in store status"] == "In store":
            # stock_summary.append(f"{item} is in stock IN STORE at {vendor_name} for {details['price']}\n"
            stock_summary.append(f"{item} is in stock IN STORE at {vendor_name}\n"
                                 f"{details['store location'].upper()}\n"
                                 f"{details['url']}\n\n")                      

    # Generates an email message from the summary list
    email_body = ""
    for hits in stock_summary:
        email_body += hits

    return email_body


def maybe_send_email(item, email_body, email_bodies, vendor_name):
    """Sends an email if the email body is not blank and is not the same as the previous email body
    Prevents spamming emails. Optionally sends a discord message too.

    :param item: the name of the item being checked for
    :param email_body: a string containing in-stock items
    :param email_bodies: the email body from the previous email sent, "" if no previous body
    :param vendor_name: the vendor name
    :return: none
    """
    # Only sends if the email body does not start the same as the last email sent
    if email_body != "" and email_body[:20] not in email_bodies[vendor_name]:
        print("Stock detected. Sending selected message types.")
        
        # Comes up with the subject line based on availability type
        if "online" in email_body.lower() and "in store" in email_body.lower():
            subject = f"{item} in Stock ONLINE and IN STORE at {vendor_name}"
        elif "online" in email_body.lower():
            subject = f"{item} in Stock ONLINE at {vendor_name}"
        elif "in store" in email_body.lower():
            subject = f"{item} in Stock IN STORE at {vendor_name}"
        elif "backorder" in email_body.lower():
            subject = f"{item} available for BACKORDER at {vendor_name}"

        # Sends different notification types
        if beep_enabled:
            make_beep_noise()
        if discord_message_enabled:
            try:
                send_discord_message(subject, email_body)
            except:
                print("Error with sending discord message.")
        if send_email:
            send_email(subject, email_body) 

    elif email_body != "":
        print("Previous email items still in stock.")
    else:
        print("No stock found")


def send_email(subject, email_body):
    """Sends an email containing the in-stock item details and link to the desired recipients

    :param subject: a string containing the in-stock status type and which website
    :param email_body: a string containing in-stock model details and website link
    :return: none
    """
    # Load sensitive login data from local .env file
    dotenv.load_dotenv()
    GMAIL_LOGIN = os.getenv('EMAIL')
    GMAIL_PASSWORD = os.getenv('PASSWORD')
    RECIPIENTS = []
    if os.getenv("RECIPIENT1") is not None:
        RECIPIENTS.append(os.getenv("RECIPIENT1"))
    if os.getenv("RECIPIENT2") is not None:
        RECIPIENTS.append(os.getenv("RECIPIENT2"))
    
    to_addr = RECIPIENTS
    from_addr = GMAIL_LOGIN
    
    msg = MIMEText(email_body)
    msg['Subject'] = subject

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(GMAIL_LOGIN, GMAIL_PASSWORD)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.close()


def title_line(vendor_name):
    """Prints the vendor name surrounded by "---" for readability in terminal"""
    vendor_name = vendor_name + " "
    while len(vendor_name) < 30:
        vendor_name += "-"
    print(vendor_name)


def send_discord_message(subject, email_body):
    """Sends an embedded message to your specific discord channel
    
    :param subject: the subject line of an email message
    :param email_body: the email body of an email message
    """
    dotenv.load_dotenv()
    webhook_url = os.getenv('DISCORD_WEBHOOK')
    webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
    embed = Embed(title=subject, description=email_body)
    webhook.send(embed=embed, tts=True)


def make_beep_noise():
    """Makes an audible beep sound. Supports Windows and Linux."""
    if beep_enabled:
        if sys.platform == "win32":
            duration = 1000
            freq = 1000
            winsound.Beep(freq, duration)
        elif sys.platform == "linux":
            # Documentation here: https://docs.python.org/3/library/sys.html#sys.platform 
            beep(sound=1)
        else:
            print("Platform not supported for make_beep_noise().")

driver = initialize_webdriver()
email_body = scrape_canada_computers(driver, vendor_name)
print(email_body)
maybe_send_email(item, email_body, email_bodies, vendor_name)
