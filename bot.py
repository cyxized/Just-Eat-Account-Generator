import requests
import names
import random
from colorama import Fore, Style
import threading
import time

def worker():
    while True:
        try:
            main()
        except Exception as e:
            print(f'{Fore.RED}[!] Worker encountered an error: {e}{Style.RESET_ALL}')
        time.sleep(1)

def main():
    s = requests.Session()

    proxy = 'http://findurownproxy.com:8080'
    s.proxies = {
        'http': proxy,
        'https': proxy  
    }

    first_name = names.get_first_name().lower()
    random_number = random.randint(1, 1000000)

    email = f'{first_name}{random_number}@domain.com'

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en;q=0.6',
        'content-type': 'application/json;v=2',
        'origin': 'https://www.just-eat.co.uk',
        'priority': 'u=1, i',
        'referer': 'https://www.just-eat.co.uk/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'x-jet-application': 'OneWeb',
    }

    json_data = {
        'registrationSource': 'native',
        'fullName': f'{first_name}',
        'password': 'Password123!',
        'emailAddress': f'{email}',
    }

    try:
        response = s.post('https://uk.api.just-eat.io/consumers/uk', headers=headers, json=json_data, timeout=2)

        if response.json().get('token'):
            print(f'{Fore.GREEN}[+] {email}{Style.RESET_ALL}')

            with open('accs.txt', 'a') as f:
                f.write(f'{email}:Password123!\n')

            return True
        else:
            print(f'{Fore.RED}[-] FAIL REG {email}{Style.RESET_ALL}')
            return None

    except Exception as e:
        print(f'{Fore.RED}[-] {response.status_code} {email}{Style.RESET_ALL}')
        return None

if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()

    while True:
        time.sleep(10)
