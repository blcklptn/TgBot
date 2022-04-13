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
async def filterSessions(sessions):
    print('filtering sessions')

    working_sessions = []
    for sessionq in sessions:
        logged = False
        try:
            client = telethon.TelegramClient(f"{sessionq}", app_id, api_hash)
            #client = telethon.TelegramClient(f"Sessions/new_session.session", config.app_id, config.api_hash)
            await client.connect()
            logged = await client.get_me()
        except Exception as e:
            print(str(e))
            continue
        if (logged):
            print('IS LOGGED')
        else:
            print('NOT LOGGED')
            continue
        working_sessions.append(sessionq)
        await client.disconnect()
    return working_sessions

class Pervonah_prepare:
    def __init__(self, id):
        self.id = id
        self.__prepare()

    def __prepare(self):
        self.main_path = f"Sessions/pervonah_data_{self.id}"
        data = os.listdir(self.main_path)
        self.sessions = [f"{self.main_path}/" + i for i in data if i.endswith(".session")]
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
        print(f"ID: {self.id}")
        print(f"{Fore.YELLOW}<==========================>{Style.RESET_ALL}")
        return (self.links, self.comments, self.count, self.sessions)
        
id = sys.argv[1]
true_count =  int(sys.argv[2])
root = Pervonah_prepare(id)
links = root.links
comments = root.comments
countq = root.count
sessions = root.sessions
cout_links = {}

for link in links:
    cout_links[link] = 0



async def join_to_channels(sessions):
    """ Join to channels """
    for session in sessions:
        client = telethon.TelegramClient(session, app_id, api_hash)
        await client.start()
        await client.connect()
        
        for link in links:
            try:
                await client(JoinChannelRequest(link))
                await asyncio.sleep(1)
                counts = await client(GetHistoryRequest(link, 1, None, 0,0,0,0,0))
                cout_links[link] = counts.count
                print(f"{link} - {cout_links[link]}")
            except Exception as e:
                print(str(e))
                continue
        await client.disconnect()


async def get_post_counts(sessions):
    client = telethon.TelegramClient(sessions[0], app_id, api_hash )
    await client.start()
    await client.connect()
    for link in links:
        counts = await client(GetHistoryRequest(link, 1, None, 0,0,0,0,0))
        cout_links[link] = counts.count
        Helper.logger(f"{link} - {cout_links[link]}")
    await client.disconnect()
        

async def _get_new_post(link, sessions):
    client = telethon.TelegramClient(sessions[0], app_id, api_hash )
    await client.start()
    await client.connect()
    counts = await client(GetHistoryRequest(link, 1, None, 0,0,0,0,0))
    await client.disconnect()
    return counts.count


async def _get_post(link, sessions):
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

async def _send_message(post, link, sessions):
    for session in sessions:
        client = telethon.TelegramClient(session, app_id, api_hash)
        await client.start()
        await client.connect()
        try:
            await client.send_message(entity = link, message = comments[random.randint(0,len(comments)-1)] , comment_to = post)
        except Exception as e:
            print(str(e))
            continue
        Helper.logger(f"Sended message to {link}", "DEBUG")
        await client.disconnect()


async def main(sessions):
    sessions = await filterSessions(sessions)
    await join_to_channels(sessions)
    Helper.logger(f"Joined to all channels", "DEBUG")
    await get_post_counts(sessions)
    Helper.logger(f"Got post counts", "DEBUG")
    c2 = 0
    while True:
        for link in links:
            counts = await _get_new_post(link, sessions)
            if cout_links[link] < counts:
                Helper.logger(f"New POST from {link}")
                post = await _get_post(link, sessions)
                print('sending')
                await _send_message(post, link, sessions)
                cout_links[link] = counts
                c2 = c2 + 1
        print(c2)
        print(true_count)
        if c2 >= true_count:
            break




loop = asyncio.get_event_loop()
loop.run_until_complete(main(sessions))

