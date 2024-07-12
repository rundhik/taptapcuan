## https://github.com/rundhik/taptapcuan
## taptapcuan/pocketfi/pocketfi.py

import sys
import os

# Add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import *
from requests.exceptions import (
    Timeout, ConnectionError, JSONDecodeError,
    InvalidJSONError, InvalidHeader, MissingSchema
)

# Configuration
json_file = 'pocketfi.json'
cfg = config(json_file)
game = 'PocketFi'
claim_interval = int(cfg['interval'])

class Header():
    '''Header http client'''
    def __init__(self):
        self.header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en,en-US;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://pocketfi.app',
        'Referer': 'https://pocketfi.app/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'X-Requested-With': 'org.telegram.messenger',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

class Client(Header):
    def __init__(self, config: dict):
        super().__init__()
        self.tgWebAppData    = config['tgWebAppData']
        self.userAgent          = config['User-Agent']
        self.user_id            = self._get_userinfo()['user']['id']
        self.username           = self._get_userinfo()['user']['username']

    def _set_headers(self, extra_headers=None):
        # Sesuaikan host
        self.header['Host'] = 'bot.pocketfi.org'
        self.header['telegramRawData'] = self.tgWebAppData
        self.header['User-Agent'] = self.userAgent
        if extra_headers:
            self.header.update(extra_headers)

    def _make_request(self, method, url, extra_headers=None, data=None, success_message=None):
        self._set_headers(extra_headers)
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.header)
            elif method == 'POST':
                response = requests.post(url, headers=self.header, data=data)

            if response.status_code == 200 :
                if success_message != None:
                    log(f'{hijau}[SUKSES ] {success_message}')
                return response.json()
            elif response.status_code == 201:
                log(f'{hijau}[SUKSES ] {success_message}')
                return response.json()
            else:
                log(f'{merah}[ERROR:{response.status_code}] Terjadi Kesalahan!')
                return response.json()
        except (Timeout, ConnectionError, JSONDecodeError, InvalidHeader, InvalidJSONError, MissingSchema) as e:
            log(f'{merah}[ERROR  ] Terjadi Kesalahan!')
            log(f'{merah}{e.args[0]}')

    def _get_userinfo(self):
        query = {k: json.loads(urllib.parse.unquote(v[0])) if k == 'user' else v[0] for k, v in urllib.parse.parse_qs(self.tgWebAppData).items()}
        return query

    def get_user_mining(self):
        url = 'https://bot.pocketfi.org/mining/getUserMining'
        sm = 'Mendapatkan informasi akun'
        return self._make_request('GET', url, success_message=sm)

    def claim_mining(self):
        url = 'https://rubot.pocketfi.org/mining/claimMining'
        eh = {
            'Content-Length': '0'
        }
        sm = 'Claim token'
        return self._make_request('POST', url, extra_headers=eh, success_message=sm)

    def task_executing(self):
        url = 'https://bot.pocketfi.org/mining/taskExecuting'
        sm = 'Memeriksa tugas harian'
        return self._make_request('GET', url, success_message=sm)

    def daily_boost(self):
        url = 'https://bot.pocketfi.org/boost/activateDailyBoost'
        eh = {
            'Content-Length': '0'
        }
        sm = 'Daily login berhasil'
        return self._make_request('POST', url, extra_headers=eh, success_message=sm)

def main():
    welcome_message(game, claim_interval)
    try:
        accounts = cfg['accounts']
        line = putih + "=" * 64
        if len(accounts) <= 0:
            log(f'{merah}[ERROR  ]: Data akun tidak ditemukan')
            log(f'{kuning}[WARNING]: Tambahkan data akun pada file {json_file}')
            sys.exit()
        else:
            log(f'{kuning}[INFO   ] Memeriksa akun ....')
            time.sleep(2)
            log(f'{biru}[INFO   ] Akun ditemukan : {putih}{len(accounts)}')
            print(line)
        for i, a in enumerate(accounts):
            log(f'{putih}[INFO   ] Akun ke-{i+1}')
            log(f'{kuning}[PROSES ] Mengambil data...')
            time.sleep(2)

            # New Client object
            client = Client(a)

            # Get user mining
            mining = client.get_user_mining()['userMining']
            log(f'{biru}[INFO   ] Username : {kuning}{censor_text(client.username)}')
            log(f'{biru}[INFO   ] Total token : {kuning}{mining['gotAmount']:,.3f}')
            log(f'{biru}[INFO   ] Token belum diclaim : {kuning}{mining['miningAmount']:,.3f}')
            burn_in = datetime.fromtimestamp(int(mining['dttmClaimDeadline'])/1000) - datetime.now()
            log(f'{merah}[WARNING] Token akan diburn dalam {str(format_timedelta(burn_in))}')
            time.sleep(2)

            # Task Executing
            tasks = client.task_executing()['tasks']['daily'][0]
            log(f'{kuning}[PROSES ] Memeriksa tugas login harian ...')
            time.sleep(2)
            if int(tasks['doneAmount']) < 1:
                log(f'{biru}[INFO   ] Tugas login harian belum selesai')

                # Daily Task
                daily_task = client.daily_boost()
                day = int(tasks['currentDay'])
                log(f'{biru}[INFO   ] Daily login ke {day}')
                log(f'{biru}[INFO   ] Total reward : {kuning}{tasks['rewardList'][day-1]}')
                log(f'{biru}[INFO   ] Tugas login harian sudah selesai')
            else:
                log(f'{biru}[INFO   ] Tugas login harian sudah selesai')

            # Claim mining
            log(f'{kuning}[PROSES ] Mengclaim token...')
            claim = client.claim_mining()['userMining']
            log(f'{biru}[INFO   ] Jumlah token yang diclaim : {kuning}{float(claim['gotAmount']-mining['gotAmount']):,.3f}')
            log(f'{biru}[INFO   ] Mining akun {censor_text(client.username)} selesai')
            log(f'{kuning}[PROSES ] Memeriksa akun lainnya ...')
            print(line)
            time.sleep(2)

        log(f'{biru}[INFO   ] Semua akun selesai diproses')
    except Exception as e:
        log(f'{merah}[ERROR  ] Unch, terjadi kesalahan!')
        log(f'{merah}{e.args[0]}')

def run():
    interval = claim_interval * 60  # xx minutes in seconds
    while True:
        main()
        countdown(interval)

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        sys.exit()
