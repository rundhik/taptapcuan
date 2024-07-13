## https://github.com/rundhik/taptapcuan
## taptapcuan/diamore/diamore.py

import sys
import os

# Add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers import *

# Configuration
json_file = 'diamore.json'
cfg = config(json_file)
game = 'Diamore'
claim_interval = int(cfg['interval'])

class Header():
    '''Header http client'''
    def __init__(self):
        self.header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en,en-US;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'diamore-propd.smart-ui.pro',
        'Origin': 'https://app.diamore.co',
        'Referer': 'https://app.diamore.co/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'X-Requested-With': 'org.telegram.messenger',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Android WebView";v="126"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

class Client(Header):
    '''Client method'''
    def __init__(self, config: dict):
        super().__init__()
        self.telegramRawData    = config['telegramRawData']
        self.userAgent          = config['User-Agent']
        self.tapLow          = config['tapLow']
        self.tapHigh          = config['tapHigh']
        self.user_id            = self._get_userinfo()['user']['id']
        self.username           = self._get_userinfo()['user']['username']

    def _set_headers(self, extra_headers=None):
        self.header['Host'] = 'api.massan.club'
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
                log(f'{merah}[ERROR  ] {response.status_code}:{response.reason}')
                return response.json()
        except (Timeout, ConnectionError, JSONDecodeError, InvalidHeader, InvalidJSONError, MissingSchema) as e:
            log(f'{merah}[ERROR  ] Terjadi Kesalahan!')
            log(f'{merah}{e.args[0]}')

    def _get_userinfo(self):
        query = {k: json.loads(urllib.parse.unquote(v[0])) if k == 'user' else v[0] for k, v in urllib.parse.parse_qs(self.telegramRawData).items()}
        return query

    def user(self):
        url = 'https://diamore-propd.smart-ui.pro/user'
        h = {
            'Authorization': 'Token '+str(self.telegramRawData)
        }
        m = 'Get user'
        return self._make_request('GET', url, h, success_message=m)

    def visit(self):
        url = 'https://diamore-propd.smart-ui.pro/user/visit'
        h = {
            'Authorization': 'Token '+str(self.telegramRawData),
            'Content-Length': '0'
        }
        m = 'Get visit'
        return self._make_request('POST', url, h, success_message=m)

    def claim_daily(self):
        url = 'https://diamore-propd.smart-ui.pro/user/claim-daily'
        h = {
            'Authorization': 'Token '+str(self.telegramRawData),
        }
        m = 'Get claim daily'
        return self._make_request('POST', url, h, success_message=m)

    def referrals(self):
        url = 'https://diamore-propd.smart-ui.pro/referral/recruits/'
        h = {
            'Authorization': 'Token '+str(self.telegramRawData)
        }
        m = 'Get reqruits'
        return self._make_request('GET', url, h, success_message=m)

    def claim_referral(self):
        url = 'https://diamore-propd.smart-ui.pro/referral/claim'
        h = {
            'Authorization': 'Token '+str(self.telegramRawData),
        }
        m = 'Get claim referral'
        return self._make_request('POST', url, h, success_message=m)

    def sync_clicks(self):
        num = str(random.randrange(self.tapLow, self.tapHigh))
        data = {'tapBonuses': num}
        data = json.dumps(data)
        url = 'https://diamore-propd.smart-ui.pro/user/syncClicks'
        h = {
            'Authorization': 'Token '+str(self.telegramRawData),
            'Content-Type': 'application/json'
        }
        m = 'Post sync'
        return self._make_request('POST', url, h, data=data, success_message=m), num


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
                c = Client(a)

                # Get info akun
                u = c.user()
                log(f'{biru}[INFO   ] Username : {kuning}{censor_text(u["username"])}')
                log(f'{biru}[INFO   ] Balance : {kuning}{u["balance"]}')
                v = c.visit()

                # Daily bonus
                log(f'{kuning}[PROSES ] Memeriksa bonus harian...')
                time.sleep(2)
                daily_bonus = int(u["dailyBonusAvailable"])
                if daily_bonus > 0:
                    log(f'{kuning}[PROSES ] Mengambil bonus harian...')
                    time.sleep(1)
                    d = c.claim_daily()
                    if d["message"] == "ok":
                        log(f'{biru}[INFO   ] Mendapat bonus harian: {kuning}{daily_bonus}')
                    elif d["message"] == "Daily bonus not available":
                        log(f'{kuning}[INFO   ] Bonus harian sudah diambil')
                    else:
                        log(f'{kuning}[WARNING] {s["message"]}')
                else:
                    log(f'{biru}[INFO   ] Bonus harian belum ada')
                time.sleep(1)

                # Referal claim
                log(f'{kuning}[PROSES ] Memeriksa bonus referral...')
                time.sleep(2)
                ref = c.referrals()
                ref_bonus = int(ref["totalAvailableBonuses"])
                if ref_bonus > 0:
                    log(f'{kuning}[PROSES ] Mengambil bonus referral...')
                    r = c.claim_referral()
                    if r["message"] == "Bonuses claimed":
                        log(f'{biru}[INFO   ] Mendapat bonus referral: {kuning}{ref_bonus}')
                    else:
                        log(f'{kuning}[WARNING] {r["message"]}')
                else:
                    log(f'{biru}[INFO   ] Bonus referral belum ada')

                # Tap-tap
                log(f'{kuning}[PROSES ] Memeriksa permainan tap-tap...')
                time.sleep(2)
                s, tap = c.sync_clicks()
                if s["message"] == 'Bonuses incremented':
                    log(f'{kuning}[PROSES ] Sedang fap-fap, eh tap-tap ;) ...')
                    time.sleep(10)
                    log(f'{hijau}[SUKSES ] Permainan selesai')
                    log(f'{biru}[INFO   ] Tap-tap bonus : {kuning}{tap}')
                elif s["message"] == 'Clicks are not yet available':
                    log(f'{kuning}[WARNING] Belum waktunya tap-tap, udut dulu gan!')
                else:
                    log(f'{kuning}[WARNING] {s["message"]}')

                # Get update info akun
                u = c.user()
                log(f'{biru}[INFO   ] Update balance : {kuning}{u["balance"]}')
                log(f'{biru}[INFO   ] Mining akun {censor_text(u["username"])} selesai')
                time.sleep(1)
                log(f'{kuning}[PROSES ] Memeriksa akun lainnya...')
                time.sleep(3)
                print(line)

        log(f'{biru}[INFO   ] Semua akun selesai diproses')
        time.sleep(10)
        welcome_message(game, claim_interval)
        log(f'{kuning}[INFO   ] Menunggu waktu claim berikutnya')

    except Exception as e:
        log(f'{merah}[ERROR  ] Gawat, ono sing error lur!')
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
