
# 🤖 canada-computers-rtx-stock-alerts

A selenium-python app to notify you as soon as RTX cards come in stock.

## What it Does

Get notified as soon as there is stock at your local Canada Computers store.
Configure via the config.yaml file to set the following:
- RTX Cards of interest (e.g. 3060 & 3070 Ti)
- Local store locations (the stores closest to you for pickup)
- Refresh interval (recommended at least 60s to avoid bot filter)
- Discord alert (on/off)

![YMCA auto-booking selenium bot](/utils/botty.PNG)

## How it Works

Using Selenium WebDriver, the Python code will navigate through the Canada Copmuters online-store looking
for any graphics cards that are in stock.  It filters this list based on the parameters provided in the
config.yaml file to find cards and locations relevant to you.  Notifications are recorded in the console
via loggging or can be sent to a discord server for notification by connecting a webhook.

## Installation
1. ``` git clone https://github.com/StevenAdema/cc-rtx-stock-alerts ```
2. ``` pip install -r requirements.txt ```
3. update config.yaml variables as desired
4. ``` python main.py```

