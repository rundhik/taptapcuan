## https://github.com/rundhik/taptapcuan
## taptapcuan/helpers.py

import requests, time, urllib.parse, json, random
from datetime import datetime
from colorama import Fore, Style
from requests.exceptions import (
    Timeout, ConnectionError, JSONDecodeError,
    InvalidJSONError, InvalidHeader, MissingSchema
)

# Constanta
start_time = datetime.now()
merah = Fore.LIGHTRED_EX
kuning = Fore.LIGHTYELLOW_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.LIGHTBLUE_EX
hitam = Fore.LIGHTBLACK_EX
putih = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL


def config(file_path):
        '''Function to read JSON file and convert to dictionary'''
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

def log(msg):
    '''Print log message'''
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"{hitam}[{now}] {reset}{msg}")

def welcome_message(botname: str, interval: int):
    '''Welcome banner'''
    print(f"{hijau}========================= {botname} BOT =========================")
    print(f"{biru}=================== Autoclaim setiap {interval} menit ==================")
    print(f"""
    {merah}██████╗░██╗░░░██╗███╗░░██╗██████╗░██╗░░██╗██╗██╗░░██╗
    {merah}██╔══██╗██║░░░██║████╗░██║██╔══██╗██║░░██║██║██║░██╔╝
    {merah}██████╔╝██║░░░██║██╔██╗██║██║░░██║███████║██║█████═╝░
    {putih}██╔══██╗██║░░░██║██║╚████║██║░░██║██╔══██║██║██╔═██╗░
    {putih}██║░░██║╚██████╔╝██║░╚███║██████╔╝██║░░██║██║██║░╚██╗
    {putih}╚═╝░░╚═╝░╚═════╝░╚═╝░░╚══╝╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝
    """)
    print(f"{merah}Bebas untuk dimodifikasi ;) ")
    print(f"{kuning}Chat me: https://t.me/AyasMbois")
    print(f"{hijau}========================= {botname} BOT =========================")


def countdown(t):
    '''Animasi countdown'''
    s = ["|", "/", "-", "\\"]
    si = 0
    b = ['             ', 'by: AyasMbois']
    bi = 0
    while t:
        hours, remainder = divmod(t, 3600)
        mins, secs = divmod(remainder, 60)
        timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        for _ in range(10):  # Update spinner 10 times per second
            current_time = datetime.now()
            uptime = current_time - start_time
            formatted_uptime = format_timedelta(uptime)
            print(f'\r=== {b[bi]} === {s[si]} Uptime: {formatted_uptime} {s[si]} Next claim: {timer} {s[si]}', end='')
            time.sleep(0.1)
            si = (si + 1) % len(s)
        bi = (bi + 1) % len(b)
        t -= 1
    print('\r' + ' ' * 100, end='\r')  # Clear the line


def censor_word(word):
    if len(word) <= 2:
        return word
    return word[0] + '*' * (len(word) - 2) + word[-1]

def censor_text(text):
    words = text.split()
    censored_words = [censor_word(word) for word in words]
    return ' '.join(censored_words)

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}'
