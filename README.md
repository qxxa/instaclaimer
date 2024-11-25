# InstaHunt - Instagram Username Autoclaimer

Instagram Autoclaimer / Swapper / Turbo <br>
A Python script that claims a username by repeatedly checking until it becomes available.

![Example](https://github.com/user-attachments/assets/2792cd37-c423-40f9-863d-62bdee3959c7)

## Features
- Supports asynchronous checks (similar to multi-threading but faster)
- Proxy support with a built-in proxy checker
- Repeatedly checks a target username and claims when available <br> (In the future, checker for a list of target usernames will be added)

## Usage
1. Download the [ZIP File](https://github.com/qxxa/instaclaimer/archive/refs/heads/main.zip) and extract the ZIP
2. Use the command `pip install -r requirements.txt` to install the dependencies.
3. If you are using proxies, add them to the `proxies_list.txt` in the `ip:port` format.
4. run `main.py` 

## Note
- If your account has 2FA, you will need to disable it to use the script <br> (support for login of accounts with 2FA will be added in the future).
- You'll need to use high-quality HTTPS proxies. Otherwise, run the script without proxy. Free proxies won't work.
- The recommended number of threads is around 2-5 without proxies. With proxies, you can set a higher number of threads.
- This script does not have the 14 day bypass which is needed to swap usernames.

## Disclaimer

This project is intended **for educational purposes only**. The developer is not responsible for any consequences resulting from its use.
