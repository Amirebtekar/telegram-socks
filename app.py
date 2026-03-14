import re
import base64
import time
import requests
import subprocess
from telethon.sync import TelegramClient

api_id = 123456
api_hash = "API_HASH"

channels = [
    "NetAccount",
]

limit_messages = 120

pattern = r"https://t\.me/socks\?server=([^&\s]+)&port=([^&\s]+)(?:&user=([^&\s]+)&pass=([^&\s]+))?"

def clean(value):
    return re.sub(r"[^\w\.\-:]", "", value)

def convert(server, port, user=None, password=None):

    server = clean(server)
    port = clean(port)

    if user and password:
        auth = f"{user}:{password}"
        b64 = base64.b64encode(auth.encode()).decode()
        return f"socks://{b64}@{server}:{port}#sock5"
    else:
        return f"socks://{server}:{port}#sock5"

def get_country(ip):

    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()

        if data["status"] == "success":
            return data["countryCode"]

    except:
        pass

    return "UN"


with TelegramClient("session", api_id, api_hash) as client:

    telegram_links = set()
    socks_links = set()

    country_map = {}

    for channel in channels:

        print("Scanning:", channel)

        for msg in client.iter_messages(channel, limit=limit_messages):

            if not msg.text:
                continue

            matches = re.findall(pattern, msg.text)

            for server, port, user, password in matches:

                server = clean(server)
                port = clean(port)

                tg_link = f"https://t.me/socks?server={server}&port={port}"

                if user and password:
                    tg_link += f"&user={user}&pass={password}"

                telegram_links.add(tg_link)

                socks = convert(server, port, user, password)

                socks_links.add(socks)

                country = get_country(server)

                if country not in country_map:
                    country_map[country] = set()

                country_map[country].add(socks)

        time.sleep(1)


# فایل های اصلی
with open("telegram_socks.txt","w",encoding="utf-8") as f:
    for i in telegram_links:
        f.write(i+"\n")

with open("socks5.txt","w",encoding="utf-8") as f:
    for i in socks_links:
        f.write(i+"\n")


# فایل جدا برای هر کشور
for country, socks_list in country_map.items():

    filename = f"{country}.txt"

    with open(filename,"w",encoding="utf-8") as f:

        for s in socks_list:
            f.write(s+"\n")


def update_github():

    subprocess.run(["git","add","."],check=True)
    subprocess.run(["git","commit","-m","auto update socks"],check=False)
    subprocess.run(["git","pull","--rebase","origin","main"],check=False)
    subprocess.run(["git","push"],check=True)

update_github()

print("Done ✅")