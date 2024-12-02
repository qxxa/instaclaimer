from instagrapi import Client
import aiohttp
from lxml import html
import random
import json
import asyncio
from proxy_checker import run_proxy_checker

data = []
target = []
cl = Client()
valid_proxies = []

turbo_username = ''
turbo_password = ''

num_attempts = 20
check_attempt = 0
fails = 0

async def checker(session, proxy=None):
    global check_attempt, fails
    url = f"https://www.instagram.com/{target[0]}"

    while True:
        try:
            async with session.get(url, proxy=proxy) as response:
                if response.status == 200:
                    content = await response.text()
                    tree = html.fromstring(content)
                    title = tree.xpath('//title/text()')[0]

                    if "@" + target[0] in title:  # Username is taken
                        print(f"Username taken - Attempt: {check_attempt}")
                        check_attempt += 1
                    elif title == "Instagram":  # Username is available
                        print("Username available")
                        await turbo_basic()  # Attempt to claim the username
                        return
                    elif "Login" in title:
                        print(f"Fail [{fails}]")
                        fails += 1
                    else:
                        print("ERROR: " + title)
                else:
                    print("Request failed")
        except aiohttp.ClientError as e:
            print(f"Error: {e}")
        except Exception as e:
            print("Unexpected Error:", e)
            break

async def run_checker():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_threads):
            proxy = random.choice(valid_proxies) if valid_proxies else None
            tasks.append(checker(session, proxy))
        await asyncio.gather(*tasks)

async def turbo_login():
    global data
    try:
        await asyncio.to_thread(cl.login, turbo_username, turbo_password)
        await asyncio.to_thread(cl.dump_settings, "turbo.json")
        print("Logged in and session saved.")

        account_info = await asyncio.to_thread(cl.account_info)
        current_user = account_info.dict().get('username')
        print("Current account username:", current_user)

        with open("turbo.json") as json_file:
            data.append(json.load(json_file))
    except Exception as e:
        print("LOGIN ERROR:", e)

async def restore_session():
    cl.set_settings(data[0])
    await asyncio.to_thread(cl.login, turbo_username, turbo_password)

async def turbo_basic():
    attempt = 0
    while attempt < num_attempts:
        # await restore_session()
        try:
            await asyncio.to_thread(cl.account_edit, username=target[0])
            print("Attempting to claim")
            account_info = await asyncio.to_thread(cl.account_info)
            check_user = account_info.dict().get("username")

            # Check if the username was successfully claimed
            if check_user == target[0]:
                print(f"Username {target[0]} claimed!")
                return
            else:
                attempt += 1
                print(f"Claim attempt {attempt}")
        except Exception as e:
            print("Error:", e)

async def run_autoclaimer():
    global turbo_username, turbo_password, num_threads
    print("[Instagram Autoclaimer]")

    # Login to account and set target
    turbo_username = input("Enter account username: ")
    turbo_password = input("Enter account password: ")
    await turbo_login()
    swapuser = input("Enter target username: ")
    target.append(swapuser)
    num_threads = int(input("Enter the number of threads: "))
    use_proxy = input("Use proxy? [y/n]: ")

    # Proxy checker
    if use_proxy.lower() == 'y':
        await run_proxy_checker()
    elif use_proxy.lower() == 'n':
        valid_proxies.append('')
    else:
        print("Choose either [y/n]")
        return

    # Start Autoclaimer
    start = input("Start? ")
    await run_checker()
  
