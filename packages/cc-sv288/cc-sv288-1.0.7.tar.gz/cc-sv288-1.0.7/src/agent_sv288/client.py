import hashlib
from collections import defaultdict
from datetime import datetime, timedelta
from functools import cached_property

from api_helper import BaseClient, login_required
from bs4 import BeautifulSoup

from . import settings, exceptions


class Sv288Client(BaseClient):

    @property
    def default_domain(self):
        return settings.SV288_AGENT_DOMAIN

    @property
    def index_url(self):
        return self._url('index.jsp')

    @property
    def login_url(self):
        return self._url('auth/agent/login')

    @property
    def profile_url(self):
        return self._url('page/agent/myProfile.jsp')

    @staticmethod
    def get_session_key(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find('input', {'id': 'sessionKey'}).get('value')

    @property
    def session_key(self):
        r = self.get(self.index_url, params={'lang': 'en', '_': int(datetime.now().timestamp())})
        return self.get_session_key(r.text)

    @staticmethod
    def hash_method(txt):
        return hashlib.sha1(txt.encode('utf-8')).hexdigest()

    def get_login_data(self, hash_key=None):

        if hash_key is None:
            hash_key = self.session_key

        return {
            'userID': self.username.lower(),
            'password': self.hash_method(self.hash_method(self.password) + hash_key),
            'timeZone': -420
        }

    def login(self):
        login_data = self.get_login_data()
        r = self.post(self.login_url, login_data)

        json_data = r.json()
        if json_data.get('status').startswith('5') or json_data.get('status').startswith('4'):
            raise exceptions.AuthenticationError(json_data.get('message'))

        self.is_authenticated = True

    @staticmethod
    def get_rank_name(html):
        soup = BeautifulSoup(html, 'html.parser')
        info = soup.find('div', {'class': 'idInfo'})
        rank = info.find('li', {'class': 'status'}).text
        real_name = soup.find('span', {'class': 'user_id_txt'}).text.strip('\n\t\r')

        if 'sub' in real_name:
            real_name = real_name.split('sub')[0]

        return real_name, rank

    @cached_property
    @login_required
    def profile(self):
        r = self.get(self.profile_url)
        return self.get_rank_name(r.text)

    @property
    def root(self):
        return self.profile[0]

    @property
    def categories_config(self):
        return {
            'cam': {
                'platform': 'SV388',
                'location': 'CAM',
            },
            'phi': {
                'platform': 'SV388',
                'location': 'PHI',
            },
            'thai': {
                'platform': 'SV388',
                'location': 'TH',
            },
            'casino': {
                'platform': settings.SV288_CASINO_CATEGORIES,
                'location': ''
            }
        }

    @staticmethod
    def format_date(date_time):
        return date_time.strftime('%d-%m-%Y 12:00:00')

    @property
    def win_lose_setting_url(self):
        return self._url('page/agent/report/winLossDetailSetting.jsp')

    @property
    def win_lose_url(self):
        return self._url('service/agent/transaction/winloss')

    @staticmethod
    def get_report(username, values):
        return {
            'username': username.replace('CF_', '').lower(),
            'turnover': sum(value.get('turnover', 0) for value in values),
            'commission': sum(value.get('grossComm', 0) for value in values),
            'member_commission': sum(value.get('comm6', 0) for value in values),
            'win_lose': sum(value.get('playerWinLoss', 0) for value in values),
        }

    @staticmethod
    def get_reports(json_data):
        data = json_data.get('USD')

        if not data:
            return []

        for username, reports in data.items():
            username = username.replace('CF_', '').lower()

            collector = defaultdict(int)

            for report in reports:
                for k, v in report.items():
                    if isinstance(v, (float, int)):
                        collector[k] += v

            item = dict(collector,
                        username=username,
                        commission=collector.get('grossComm'),
                        win_lose=collector.get('playerWinLoss'),
                        )

            yield item

    @login_required
    def win_lose(self, from_date, to_date):
        _start = self.str2time(from_date)
        _end = self.str2time(to_date) + timedelta(days=1)

        data = {
            'startDate': self.format_date(_start),
            'endDate': self.format_date(_end),
            'userID': '',
            'webSiteType': 0,
            # 'platform': platforms,
            # 'location': location,
        }

        for category, config in self.categories_config.items():
            _data = dict(data, **config)

            headers = {
                'Cache-Control': 'no-cache',
                'Referer': self.win_lose_setting_url,
                'X-Requested-With': 'XMLHttpRequest'
            }

            r = self.post(self.win_lose_url, _data, headers=headers)

            for i in self.get_reports(r.json()):
                yield dict(i, category=category)
