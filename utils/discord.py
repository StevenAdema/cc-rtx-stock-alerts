from discord import Webhook, RequestsWebhookAdapter
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import yaml


def get_yaml():
    with open('./config/config.yaml', 'r') as stream:
    # with open('../config/config.yaml', 'r') as stream: # if running here
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    globals().update(conf)


def generate_description(d):
    body = ''
    for i in range(0, len(d)):
        card_name = d[list(d)[i]]['card name']
        # card_name = card_name.split("Ti", 1)[0]
        # card_name = card_name.split("0 ", 1)[0]
        price = d[list(d)[i]]['price']
        location = d[list(d)[i]]['store location']
        stock = d[list(d)[i]]['stock']
        url = d[list(d)[i]]['url']
        body += '''\
            {c}.
            price: {p}
            store: {s}
            stock: {t}
            {u}\n\n\
            '''.format(c=card_name, p=price, s=location, t=stock, u=url)
    
    return body


def send_discord_message(dic):
    get_yaml()
    captain_hook = WEBHOOK
    webhook = DiscordWebhook(url=captain_hook)
    title = 'RTX Card(s) in Stock!'
    body = generate_description(dic)
    embed = DiscordEmbed(title=title, description=body, color='03b2f8')
    webhook.add_embed(embed)
    response = webhook.execute()


