"""
Kavita to Discord bot
---------------------
by DLBPointon

A simple bot to send a notification to discord
of todays updated series.

Takes json list from Kavita, formats and posts to Discord.
    
"""

from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os
import requests
import http.client
import xml.etree.ElementTree as ET

def dotloader():
    load_dotenv()
    kav_base = os.getenv('KAVITA_BASE')
    kav_port = int(os.getenv('KAVITA_PORT'))
    kav_api = os.getenv('KAVITA_API')
    kav_jwt = os.getenv('KAVITA_JWT')
    disc_hook = os.getenv('DISCORD_WEBHOOK')
    return kav_base, kav_port, kav_api, kav_jwt, disc_hook


def get_recommended_kavita_data(kav_base: str, kav_port: int, kav_headers):
    EXTENTION = "/api/Recommended/quick-reads"

    conn = http.client.HTTPConnection(kav_base, kav_port)
    payload = ''
    conn.request("GET", EXTENTION, payload, kav_headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def get_recently_updated_kavita_data(kav_base: str, kav_port: int, kav_api: str, kav_headers):
    EXTENTION = f"api/Opds/{kav_api}/recently-added?pageNumber=1"
    data = requests.get(f'http://{kav_base}:{kav_port}/{EXTENTION}')
    return str_to_xml(data.content)

def str_to_xml(data: str):
    return ET.fromstring(data)

def get_titles(data: str):
    title_list = ""
    for x in data.iter('{http://www.w3.org/2005/Atom}entry'):
        for i in x.findall('{http://www.w3.org/2005/Atom}title'):
            title_list += f"{i.text.split(' (')[0]} \n"
    return title_list

def send_to_discord(data, disc_hook):
    content_pack = f'{data}'
    print(data)
    webhook = DiscordWebhook(url=disc_hook)
    embed = DiscordEmbed(title='Todays Added Comics', description=content_pack)
    
    embed.set_timestamp()
    embed.set_footer(text='I am currently a manually run bot')
    webhook.add_embed(embed)
    webhook.execute()

def main():
    kav_base, kav_port, kav_api, kav_jwt, disc_hook = dotloader()
    print(kav_base, kav_port, kav_api, kav_jwt, disc_hook)
    kav_headers = {"Authorization": f"Bearer {kav_jwt}"}

    data = get_recommended_kavita_data(kav_base, kav_port, kav_headers)
    data2 = get_recently_updated_kavita_data(kav_base, kav_port, kav_api, kav_headers)
    list = get_titles(data2)
    send_to_discord(list, disc_hook)
    
if __name__ == '__main__':
    main()