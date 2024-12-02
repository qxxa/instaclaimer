import asyncio
import sys
from availability_check import run_availability_check
from autoclaimer import run_autoclaimer
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("""
██╗███╗   ██╗███████╗████████╗ █████╗     ██╗  ██╗██╗   ██╗███╗   ██╗████████╗
██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝
██║██╔██╗ ██║███████╗   ██║   ███████║    ███████║██║   ██║██╔██╗ ██║   ██║   
██║██║╚██╗██║╚════██║   ██║   ██╔══██║    ██╔══██║██║   ██║██║╚██╗██║   ██║   
██║██║ ╚████║███████║   ██║   ██║  ██║    ██║  ██║╚██████╔╝██║ ╚████║   ██║   
╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝
""")
    option = int(input("Choose an option: \n 1. Username Availability Checker \n 2. Autoclaimer \n \n >"))

    if option == 1:
        await run_availability_check()
    elif option == 2:
        await run_autoclaimer()
    else:
        print('Invalid Option')


asyncio.run(main())
