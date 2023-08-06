import itertools
import logging
import random
import string
import time
from datetime import datetime
from functools import cached_property
from urllib.parse import urlparse, urlencode

from api_helper import BaseClient, login_required
from bs4 import BeautifulSoup
from requests.cookies import cookiejar_from_dict

from . import settings, exceptions
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class IbetClient(BaseClient):
    session_domain = None

    @property
    def session_uri(self):
        return urlparse(self.session_domain)

    @property
    def default_domain(self):
        return settings.IBET_AGENT_DOMAIN

    def session_url(self, path=''):
        return '{origin.scheme}://{origin.netloc}/{path}'.format(
            path=path.lstrip('/'),
            origin=self.session_uri
        )

    @property
    def profile_url(self):
        return self.session_url('site-main/Dashboard/Index2')

    @property
    def win_lose_url(self):
        return self.session_url('/site-reports/winlossdetail/member')

    @property
    def root(self):
        return self.profile[0]

    @staticmethod
    def random_string(stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    CAPTCHA_RESULT = """{
      "success": true,
      "challenge_ts": "%s",
      "hostname": "www.wabi88.com",
      "score": 0.9,
      "action": "login"
    }"""

    DETECAS_ANALYSIS = '{"startTime":%s,"version":"2.0.4","exceptions":[],"executions":[],"storages":[],"devices":[],"enable":true}'

    @staticmethod
    def encrypt3(data, key):
        _key = ('a5s8d2e9c172' + key).encode("utf8")
        cipher = AES.new(_key, AES.MODE_CBC, iv=_key)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return b64encode(ct_bytes).decode('utf-8')

    def login_form_data(self, captcha='9243'):
        return {
            'code': captcha,
            'hidLanguage': 'en-US',
            'txtUserName': self.username,
            'txtPassWord': self.encrypt3(self.password, captcha),
            # 'deviceId': '0e5141b579654055963f99e906197651',
            # '__RequestVerificationToken': token,
            'browserSize': '803x868',
            'detecas-analysis': self.DETECAS_ANALYSIS % (round(time.time()) * 1000),
            '__tk': '25af24e5101e1e442e83c7f1f20f0cce51c9276f518a',
            'captcha_result': self.CAPTCHA_RESULT % datetime.now().strftime('%Y-%m-%d %H:%M:%SZ'),
            '__RequestVerificationToken': '0hEUhQhmysM7HfwJ_8lHnHKapgGnBm51PY2EPAGi_KVA8Uyw4GEBTQHK543M1LbnDeOiA_ozQu8FU9jHF5uo_N7Kt8o1'
        }

    @staticmethod
    def get_error(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find('div', id='errmsg').text

    @staticmethod
    def login_error(r, **kwargs):
        if r.status_code != 200:
            return

        if 'errmsg' in r.text:
            error = IbetClient.get_error(r.text)
            if error == 'Login error! Session expired.':
                raise Exception(error)
            raise exceptions.AuthenticationError(error)

    @staticmethod
    def first_login(r, **kwargs):
        if r.status_code != 200:
            return

        if 'ChangeSecurityCodeFirstLogin' in r.url:
            raise exceptions.AuthenticationError('ChangeSecurityCodeFirstLogin')

        if 'ChangeSecurityCodeByForcing' in r.url:
            raise exceptions.AuthenticationError('Need to set new security code')

        if 'Nickname/Index' in r.url:
            raise exceptions.AuthenticationError('Please set nickname')

    @property
    def skip_password_url(self):
        return self.session_url('site-main/Password/SkipForceChangePassword')

    @staticmethod
    def get_input(html, **kwargs):
        soup = BeautifulSoup(html, 'html.parser')
        _input = soup.find('input', attrs=kwargs)

        return _input.get('value')

    @staticmethod
    def get_verity_token(html):
        return IbetClient.get_input(html, name='__RequestVerificationToken')

    def login(self):
        self.random_ip()
        cookies = {
            'ASP.NET_SessionId': self.random_string(24),
            '__RequestVerificationToken': '5uR3HBdCqqU1eIPqn0-zu8uwaYZuW4zd054C2Xn9_fFtrnywOSV0Km1kJQe9cyjjodB_Y2T0n54PTp-OqPNm4eNaZjg1',
        }

        self.cookies = cookiejar_from_dict(cookies)

        r = self.post(self._url(), data=self.login_form_data(), headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }, hooks={
            'response': [self.login_error, self.first_login]
        })

        self.session_domain = r.url

        if 'RobotCaptcha/Index' in r.url:
            # FIXME
            raise exceptions.AuthenticationError('Need manual login.')

        if 'Password/ForceChangePassword' in r.url:
            verity_token = self.get_verity_token(r.text)
            self.post(self.skip_password_url, data={
                '__RequestVerificationToken': verity_token
            })

        self.is_authenticated = True

    @staticmethod
    def get_name_and_rank(html):
        soup = BeautifulSoup(html, 'html.parser')
        objs = soup.find(id='balance').find('div', {'class': 'container'}).find('div', {'class': 'row'}).find_all('div')
        rank, name = [i.get_text().lower() for i in objs]
        return name, rank

    @cached_property
    @login_required
    def profile(self):
        r = self.get(self.profile_url)
        return self.get_name_and_rank(r.text)

    PRODUCTS = {
        'sportbook': '1,5,42',
        'lotto': '3,23,28,63,8',
        'casino': '50,40,38,24,69,21,47,39,45,52,51,59,57,65,22,6,34,36,32,55,60,61,62,67,68',
    }

    ALL_PRODUCTS = {
        'all': '1,3,23,28,63,8,50,40,38,5,24,42,69,21,47,39,45,52,51,59,57,65,22,6,34,36,32,55,60,61,62,67,68'
    }

    @property
    def date_time_pattern(self):
        return '%m/%d/%Y'

    @staticmethod
    def get_report(html):
        soup = BeautifulSoup(html, 'html.parser')
        try:
            rows = soup.find('tbody').find_all('tr')
        except AttributeError as e:
            logging.error(html)
            raise e

        # base = soup.find('ul', {'class': 'breadcrumb'}).find_all('li')[-1].get_text().translate(
        #     str.maketrans("", "", "\n\r ")).lower()

        for row in rows:
            try:
                cols = row.find_all('td')

                username_link = cols[0].find('a')

                username = username_link.get_text().translate(str.maketrans("", "", "\n\r ")).lower()
                number_data = list(map(lambda x: IbetClient.format_float(x.get_text()), cols))

                yield {
                    'url': username_link.get('href'),
                    'username': username,
                    'bet_count': number_data[1],
                    'turnover': number_data[2],
                    'net_turnover': number_data[3],
                    'commission': number_data[4],
                    'win_lose': number_data[5],
                    'member_win_lose': number_data[5],
                    'member_commission': number_data[6],
                    'member_total': number_data[7],
                }
            except AttributeError:
                pass

    @login_required
    def win_lose(self, from_date, to_date, products=None, deep=False):
        products = products or self.PRODUCTS

        for category, product_ids in products.items():
            qs = {
                'IsFilterVisible': 'false',
                'IsStackMode': 'false',
                'UserSelectedProductIds': str(product_ids),
                'FromDate': self.format_date(from_date),
                'ToDate': self.format_date(to_date),
            }

            queue = iter([('?' + urlencode(qs), 0)])

            while next_item := next(queue, False):
                qs, level = next_item
                r = self.get(self.win_lose_url + qs)

                reports = self.get_report(r.text)
                next_queue = []
                for item in reports:
                    url = item.pop('url')

                    if deep:
                        yield dict(item, category=category, deep=level+1)
                    else:
                        yield dict(item, category=category)

                    if deep and 'site-betlists' not in url:
                        next_queue.append((url, level+1))

                if len(next_queue) > 0:
                    queue = itertools.chain(next_queue, queue)

    @login_required
    def gen_bet_list_url(self, from_date, to_date):
        qs = {
            'IsFilterVisible': 'false',
            'IsStackMode': 'false',
            'UserSelectedProductIds': '1,5,42',
            'FromDate': self.format_date(from_date),
            'ToDate': self.format_date(to_date),
        }

        queue = iter(['?' + urlencode(qs)])

        while next_url := next(queue, False):
            r = self.get(self.win_lose_url + next_url)

            if 'Too many requests' in r.text:
                logging.info('Too many requests. Sleep 10s')
                time.sleep(10)
                queue = itertools.chain([next_url], queue)
                continue

            reports = self.get_report(r.text)
            next_queue = []
            for item in reports:
                url = item.pop('url')

                if 'site-betlists' not in url:
                    next_queue.append(url)
                else:
                    yield url, item.get('username')

            if len(next_queue) > 0:
                queue = itertools.chain(next_queue, queue)

    # noinspection PyBroadException
    @staticmethod
    def get_tickets(html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('div', attrs={'class': 'bl_title'}).contents[0].get_text()
        *_, username = title.split('-')
        username = username.strip().lower()
        rows = soup.find('tbody').find_all('tr')
        for row in rows[:-1]:
            try:
                cols = row.find_all('td')

                # unpack cols
                _, trans_time_col, choice_col, odds_col, stake_col, win_col, status_col, *_ = cols

                # trans_time_col
                bet_at_orig = trans_time_col.find('div').get_text()
                bet_at = datetime.strptime(bet_at_orig, '%m/%d/%Y %I:%M:%S %p').isoformat()
                ref_id = trans_time_col.contents[0].replace('Ref No: ', '').strip()

                # choice_col
                selection_col = choice_col.find('div', recursive=False)
                bet_on_span = selection_col.find('span', recursive=False)

                is_live = len(bet_on_span.contents) >= 3

                bet_on = bet_on_span.contents[0].lower()
                handicap = bet_on_span.contents[1].get_text().strip().lower()
                score = bet_on_span.contents[2].get_text().strip(' []') if is_live else ''
                bet_type = selection_col.find('div', {'class': 'bettype'}).get_text().strip().lower()

                home_team, *_, away_team = selection_col.find('div', {'class': 'match'}).find_all('span')
                league = selection_col.find('span', {'class': 'leagueName'}).get_text().replace('\xa0', '')

                home_team = home_team.get_text().lower()
                away_team = away_team.get_text().lower()
                event_date = selection_col.find('div', {'class': 'event-date'}).get_text()
                issue_date = datetime.strptime(event_date, '%m/%d/%Y %I:%M %p').date().isoformat()
                sport = selection_col.find('span', {'class': 'sport'}).get_text().lower()

                # odds col
                odds, odds_type = [i.get_text() for i in odds_col.find_all('span')]
                odds = IbetClient.format_float(odds)

                # stake
                stake = IbetClient.format_float(stake_col.find('div').get_text())

                # win col
                win_lose, commission = [IbetClient.format_float(i.get_text()) for i in win_col.find_all('span')]
                # status col
                status = status_col.find('div', {'class': 'status'}).get_text()
                ip = status_col.find('div', {'class': 'iplink'}).get_text()

                # print(selection_col.contents)
                yield dict(
                    username=username,
                    bookmaker='ibet',
                    uuid='ibet-{}'.format(ref_id),
                    match_uuid='__'.join(['ibet', home_team, away_team, issue_date]),
                    ref_id=ref_id,
                    sport=sport,
                    bet_at=bet_at,
                    bet_on=bet_on,
                    handicap=handicap,
                    bet_type=bet_type,
                    score=score,
                    is_live=is_live,
                    home_team=home_team,
                    away_team=away_team,
                    league=league,
                    origin_odds=odds,
                    odds_type=odds_type,
                    stake=stake,
                    status=status,
                    win_lose=win_lose,
                    commission=commission,
                    ip=ip,
                    issue_date=issue_date
                )
            except Exception:
                pass

    @login_required
    def tickets(self, from_date, to_date):
        pool = self.gen_bet_list_url(from_date, to_date)
        while next_item := next(pool, None):
            uri, username = next_item
            r = self.get(self.session_url(uri))

            if 'Too many requests' in r.text:
                logging.info('Too many requests. Sleep 10s')
                time.sleep(10)
                pool = itertools.chain([next_item], pool)
                continue

            count = 0
            for i in self.get_tickets(r.text):
                count += 1
                yield i

            logging.info('member {} ticket {}'.format(username, count))

    @property
    def outstanding_url(self):
        return self.session_url('/site-reports/outstanding/masternew')

    @staticmethod
    def row2text(row):
        tds = row.find_all('td')
        return [td.get_text().translate(str.maketrans("", "", "\n ,")) for td in tds]

    @staticmethod
    def outstanding_parser(html):
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find('tbody')
        if not tbody:
            return

        rows = tbody.find_all('tr')

        for row in rows[:-1]:
            cols = row.find_all('td')
            username_link = cols[0].find('a').get('href')
            username = cols[0].get_text().translate(str.maketrans("", "", "\n ,")).lower()
            yield {
                'username': username,
                'url': username_link,
                'outstanding': IbetClient.format_float(cols[1].get_text())
            }

    @login_required
    def outstanding(self, products=None, deep=False):
        products = products or self.PRODUCTS

        for category, product_ids in products.items():
            pool = iter([('?UserSelectedProductIds={}'.format(product_ids), 0)])

            while next_item := next(pool, False):
                qs, level = next_item
                r = self.get(self.outstanding_url + qs)

                if 'Too many requests' in r.text:
                    logging.info('Too many requests. Sleep 10s')
                    time.sleep(10)
                    # logging.info('Too many requests. relogin!')
                    # self.cookies.clear()
                    # self.login()
                    pool = itertools.chain([next_item], pool)
                    continue

                next_pool = []
                for item in self.outstanding_parser(r.text):
                    url = item.pop('url')
                    if deep:
                        yield dict(item, category=category, deep=level + 1)
                    else:
                        yield dict(item, category=category)

                    if deep and 'site-betlists' not in url:
                        next_pool.append((url, level + 1))

                if len(next_pool) > 0:
                    pool = itertools.chain(next_pool, pool)



