import requests
from datetime import datetime
import random
from proxy_checker import run_proxy_checker

valid_proxies = []

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Referer": "https://www.instagram.com/accounts/emailsignup/"
})

def check_username(username):
    if not valid_proxies:
        print("No proxies available.")
        return None

    proxy = random.choice(valid_proxies)
    proxy_config = {
        'http': proxy,
        'https': proxy
    }

    signup_url = "https://www.instagram.com/accounts/emailsignup/"
    response = session.get(signup_url, proxies=proxy_config)

    if response.status_code == 429:    
        print(f"Rate limited using proxy {proxy}. Status code: {response.status_code}")
        return None

    csrf_token = session.cookies.get("csrftoken")
    
    if not csrf_token:
        print(f"Failed to fetch CSRF token using proxy {proxy}.")
        return None

    session.headers.update({"X-CSRFToken": csrf_token})

    password = "randompassword213"
    time = str(int(datetime.now().timestamp()))
    enc_password = f"#PWD_INSTAGRAM_BROWSER:0:{time}:{password}"

    signup_data = {
        "emailOrPhone": "asklfdjkl2@gmail.com",
        "fullName": "abcd",
        "username": username,
        "enc_password": enc_password,
        "client_id": session.cookies.get("mid"),
        "seamless_login_enabled": "1",
        "opt_into_one_tap": "false",
    }

    signup_api_url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"
    response = session.post(signup_api_url, data=signup_data, cookies=session.cookies, proxies=proxy_config)

    if response.status_code != 200:
        print(f"Failed to check username {username} using proxy {proxy}. Status code: {response.status_code}")
        return None

    response_data = response.json()

    #check availability
    errors = response_data.get("errors", {})
    if "username" in errors:
        for error in errors["username"]:
            if error.get("code") == "username_is_taken":
                print(f"Username '{username}' is taken.")
                return False
    print(f"Username '{username}' is available.")
    return True

with open('usernames.txt', 'r') as file:
    target_list = [line.strip() for line in file]

async def run_availability_check():
    global valid_proxies
    print("[Username Availability Check]")
    print(f"{len(target_list)} usernames in usernames.txt file")
    use_proxy = input("Use proxy? [y/n]: ")

    # Proxy checker
    if use_proxy.lower() == 'y':
        valid_proxies = await run_proxy_checker()
    elif use_proxy.lower() == 'n':
        valid_proxies.append('')
    else:
        print("Choose either [y/n]")
        return

    # Start Autoclaimer
    start = input("Start? ")
    for username in target_list:
        check_username(username)
