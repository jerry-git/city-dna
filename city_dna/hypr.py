import requests
import os
import datetime


class HyprClient:
    def __init__(self, apikey=None):
        self._apikey = apikey or os.environ['HYPR_API_KEY']
        self._url = 'https://api.hypr.cl'

    def stations(self):
        """
        {'list': [{'address': 'Munkkisaarenlaituri',
           'alias': None,
           'city': 'Helsinki',
           'country': 'Finland',
           'description': 'Hernesaari LHC',
           'group': 'hernesaari',
           'latitude': 60.14951,
           'longitude': 24.92138,
           'postalcode': '00150',
           'serial': '0000000006dd41f6'},]

        """
        url = f'{self._url}/station/'
        headers = self._headers(command="list")
        return requests.post(url, headers=headers)

    def raw(self, start, end):
        """
        'raw':
        [
          {'distance': 17.4,
          'hash': 'fec758ad55ed547d0b77fd7b2c0fd24d59637b514fec3935f101c0ef',
          'latitude': 60.16448,
          'longitude': 24.97323,
          'serial': '0000000053c6c2be',
          'time': '2019-07-15T00:01:00Z'},
          ],
        'status': 'Success'}
        """
        start, end = self._format_dt(start), self._format_dt(end)
        url = f'{self._url}/raw/'
        headers = self._headers(time_start=start, time_stop=end)
        return requests.post(url, headers=headers)

    def _headers(self, **headers):
        return {**headers, **{'x-api-key': self._apikey}}

    def _format_dt(self, dt):
        return f'{dt.isoformat()}z'

if __name__ == '__main__':
    client = HyprClient()
    # resp = client.stations()
    start = datetime.datetime(2019, 7, 15)
    end = start + datetime.timedelta(minutes=1) # 1 minute --> 3412
    # resp = client.raw(start, end)
    breakpoint()






