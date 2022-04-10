from calendar import c
from operator import ge
import sys
from traceback import format_list
import Helper
import os
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest
import telethon
import time
import asyncio
import random
from colorama import Fore, Style
api_hash = "95db77689e2aae95cfbdcb92de1a36e1"
app_id = 10245235

class Pervonah_prepare:
    def __init__(self, id):
        self.id = id
        self.__prepare()

    def __prepare(self):
        self.main_path = f"Sessions/pervonah_data_{self.id}"
        data = os.listdir(self.main_path)
        self.sessions = [i for i in data if i.endswith(".session")]
        with open(f"{self.main_path}/config.txt", "r") as file:
            data = file.read().split("\n")

        self.links_path = data[0]
        self.comments_path = data[1]
        self.count = int(data[2])

        with open(f"{self.main_path}/{self.links_path}", "r") as file:
            self.links = file.read().split("\n")
        
        with open(f"{self.main_path}/{self.comments_path}", "r") as file:
            self.comments = file.read().split("\n")

        print(f"{Fore.YELLOW}<======== {Fore.GREEN} Config {Fore.YELLOW}=========>{Style.RESET_ALL}")
        print(f"Links: {self.links}")
        print(f"Comments: {self.comments}")
        print(f"Count: {self.count}")
        print(f"Sessions: {self.sessions}")
        print(f"Api Hash: {api_hash}")
        print(f"App Id: {app_id}")
        print(f"{Fore.YELLOW}<==========================>{Style.RESET_ALL}")
        return (self.links, self.comments, self.count, self.sessions)
        

root = Pervonah_prepare(sys.argv[1])
links = root.links
comments = root.comments
countq = root.count
sessions = root.sessions

cout_links = {}

for link in links:
    cout_links[link] = 0



async def join_to_channels():
    """ Join to channels """
    for session in sessions:
        client = telethon.TelegramClient(session, app_id, api_hash)
        await client.start()
        await client.connect()
        
        for link in links:
             await client(JoinChannelRequest(link))
             await asyncio.sleep(1)
             counts = await client(GetHistoryRequest(link, 1, None, 0,0,0,0,0))
             cout_links[link] = counts.count
             print(f"{link} - {cout_links[link]}")
        await client.disconnect()


async def get_post_counts():
    client = telethon.TelegramClient(sessions[0], app_id, api_hash )
    await client.start()
    await client.connect()
    for link in links:
        counts = await client(GetHistoryRequest(link, 1, None, 0,0,0,0,0))
        cout_links[link] = counts.count
        Helper.logger(f"{link} - {cout_links[link]}")
    await client.disconnect()
        

async def _get_new_post(link):
    client = telethon.TelegramClient(sessions[0], app_id, api_hash )
    await client.start()
    await client.connect()
    counts = await client(GetHistoryRequest(link, 1, None, 0,0,0,0,0))
    await client.disconnect()
    return counts.count


async def _get_post(link):
    client = telethon.TelegramClient(sessions[0], app_id, api_hash )
    await client.start()
    await client.connect()
    posts = await client(GetHistoryRequest(peer=link,
                                        limit=1,
                                        offset_date=None,
                                        offset_id=0,
                                        max_id=0,
                                        min_id=0,
                                        add_offset=0,
                                        hash=0))
    await client.disconnect()
    return posts.messages[0]

async def _send_message(post, link):
    for session in sessions:
        client = telethon.TelegramClient(session, app_id, api_hash)
        await client.start()
        await client.connect()
        await client.send_message(entity = link, message = comments[random.randint(0,len(comments)-1)] , comment_to = post)
        Helper.logger(f"Sended message to {link}", "DEBUG")
        await client.disconnect()


async def main():
    await join_to_channels()
    Helper.logger(f"Joined to all channels", "DEBUG")
    await get_post_counts()
    Helper.logger(f"Got post counts", "DEBUG")
    while True:
        for link in links:
            counts = await _get_new_post(link)
            if cout_links[link] < counts:
                Helper.logger(f"New POST from {link}")
                post = await _get_post(link)
                await _send_message(post, link)
                cout_links[link] = counts




loop = asyncio.get_event_loop()
loop.run_until_complete(main())

