import asyncio
import aiohttp
from lxml import html
valid_proxies = []

async def check_proxies(proxy):
    async with aiohttp.ClientSession() as session:
        try:
            proxy_url = proxy
            print(f"Testing HTTPS proxy: {proxy_url}")

            async with session.get("https://www.instagram.com/cristiano", proxy=proxy_url, timeout=5) as response:
                if response.status == 200:
                    content = await response.text()
                    tree = html.fromstring(content)
                    title = tree.xpath('//title/text()')[0]
                    if 'Login' not in title:
                        valid_proxies.append(proxy)
                        print(f"Valid HTTPS proxy found: {proxy}, Total Proxies: {len(valid_proxies)}")
                    else:
                        print(f"Proxy {proxy} failed (redirected to login).")
        except aiohttp.ClientProxyConnectionError:
            print(f"Proxy {proxy} failed (connection error).")
        except aiohttp.ClientSSLError as ssl_err:
            print(f"SSL verification failed for proxy {proxy}: {ssl_err}")
        except asyncio.TimeoutError:
            print(f"Proxy {proxy} failed (timeout).")
        except Exception as e:
            print(f"Proxy {proxy} failed (other error): {e}")

async def run_proxy_checker():
    print("Checking proxies.txt for usable proxies...")
    tasks = []
    with open("proxies.txt", "r") as f:
        proxies = f.read().splitlines()
    for proxy in proxies:
        tasks.append(check_proxies(proxy))
    await asyncio.gather(*tasks)
    print(f"Valid proxies: {len(valid_proxies)}")
    return valid_proxies
