"""
Kavita to Discord bot
---------------------
by DLBPointon

A simple bot to send a notification to discord
of todays updated series.

Takes json list from Kavita, formats and posts to Discord.
    
"""

from discord_webhook import DiscordWebhook, DiscordEmbed
import json
import os
import requests
import http.client

def args():
    #kavita_api_key
    #base_url
    #kavita_port
    #Discord hook
    pass

def get_recommended_kavita_data(KAVITA_BASE: str, KAVITA_PORT: int, HEADERS):
    KAVITA_EXTENTION = "/api/Recommended/quick-reads"

    conn = http.client.HTTPConnection(KAVITA_BASE, KAVITA_PORT)
    payload = ''
    conn.request("GET", KAVITA_EXTENTION, payload, HEADERS)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_recently_updated_kavita_data(KAVITA_BASE: str, KAVITA_PORT: int, HEADERS):
    EXTENTION = "api/Opds/{KAVITA_API_KEY}/recently-added?pageNumber=1"

    data = requests.get(f'http://{KAVITA_BASE}:{KAVITA_PORT}/{EXTENTION}')
    return data.content

def format_kavita_data(data):
    for i in data:
        print(i['name'])

def send_to_discord():
    pass

def main():
    KAVITA_BASE = "192.168.1.222"
    KAVITA_PORT = 5000
    HEADERS = {"Authorization": "Bearer {KAVITA_JWT}"}
    DISCORD_WEBHOOK = ""

    data = get_recommended_kavita_data(KAVITA_BASE, KAVITA_PORT, HEADERS)
    data2 = get_recently_updated_kavita_data(KAVITA_BASE, KAVITA_PORT, HEADERS)
    #format_kavita_data(data)
    print(data2)
    
if __name__ == '__main__':
    main()