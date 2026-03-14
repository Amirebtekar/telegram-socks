import re
import base64
import time
from telethon.sync import TelegramClient

api_id = 123456
api_hash = "API_HASH"

channels = [
    "Farah_Proxy",
    "NPROXY",
    "Pruuxi",
    "saministamm",
    "configraygan",
]

limit_messages = 80

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


with TelegramClient("session", api_id, api_hash) as client:

    telegram_links = set()
    socks_links = set()

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

                socks_links.add(convert(server, port, user, password))

        time.sleep(1)

    with open("telegram_socks.txt", "w", encoding="utf-8") as f:
        for i in telegram_links:
            f.write(i + "\n")

    with open("socks5.txt", "w", encoding="utf-8") as f:
        for i in socks_links:
            f.write(i + "\n")

print("Done ✅")
print("Telegram socks:", len(telegram_links))
print("Converted socks:", len(socks_links))