import rich
from rich import print
from typing import Optional
from requests import Request, get
from .gredients import *
from .objects import Pages, Device, Report, ThingsMatrixResponse, Template
from datetime import datetime, timedelta, timezone


def testGETCompany():
    import http.client
    conn = http.client.HTTPSConnection("hpdemo.thingsmatrix.io")

    payload = ''
    headers = {
        'accept':
        '*/*',
        'Authorization':
        'ApiKey eyJ0eXAiOiJBUElLRVkifQ.QzAwMDAwMi5Db21tVERDLmE1NzljMTBlNWIwZmE1NzY'
    }
    companyName = "HP"

    conn.request("GET", f"/api/v2/inventory/companies/{companyName}", payload,
                 headers)

    res = conn.getresponse()

    data = res.read()

    print(data.decode("utf-8"))


class ThingsMatrix:

    def __init__(self, api_key=API_KEY, base_url=BASE_URL) -> None:
        self.get = get
        self.__headers = {
            'accept': '*/*',
            'Authorization': f'ApiKey {api_key}'
        }
        self.__requests = None
        self.__reqponse = None

    #region Device
    def get_devices(self,
                    group: str = None,
                    modelId: str = None,
                    offset: int = None,
                    page: int = 1,
                    pageNumber: int = None,
                    pageSize: int = None,
                    paged: bool = None,
                    searchTerm: str = None,
                    size: int = 15,
                    sort: str = None,
                    sort_sorted: bool = None,
                    sort_unsorted: bool = None,
                    status: int = None,
                    tags: str = None,
                    unpaged: bool = None,
                    **kwargs):
        ...
        _locals = locals()
        del _locals['self']
        del _locals['kwargs']
        del _locals['sort_sorted']
        del _locals['sort_unsorted']

        for k, v in _locals.items():
            if v:
                kwargs[k] = v

        if sort_sorted:
            kwargs['sort.sorted'] = sort_sorted
        if sort_unsorted:
            kwargs['sort.unsorted'] = sort_unsorted
        devices = None
        response = self.get(f'{BASE_URL}/devices',
                            headers=self.__headers,
                            params=kwargs)
        if response.ok and response.status_code == 200:
            devices = Pages(response).collect_contents(Device)
        else:
            print(response.json())
        return response, devices

    def get_device(self, sn):
        response = ThingsMatrixResponse(
            self.get(f'{BASE_URL}/devices/{sn}', headers=self.__headers))
        if response.hasData:
            return Device(response.data)
        raise BaseException(response.msg)

    #endregion

    #region Groups
    def get_groups(self,
                   model_id: str = None,
                   offset: int = None,
                   page: int = None,
                   **kwargs):

        _locals = locals()
        del _locals['self']
        del _locals['kwargs']
        for k, v in _locals.items():
            if v:
                kwargs[k] = v

        response = self.get(f'{BASE_URL}/groups',
                            headers=self.__headers,
                            params=kwargs)
        if response.ok:
            print(response.json())
            return response
        else:
            print(response.json())

        ...

    #endregion

    #region Log Data
    def get_devices_reports(self, sn, startTime=None, endTime=None, **kwargs):
        #input imei,startTime,endTime
        # try startTime and endTime
        # "yyyy-mm-dd HH:mm:ss"
        ...
        _locals = locals()
        del _locals['self']
        del _locals['kwargs']
        for k, v in _locals.items():
            if v:
                kwargs[k] = v

        if startTime:
            kwargs['startTime'] = self.__convert_to_utc(startTime)
        if endTime:
            kwargs['endTime'] = self.__convert_to_utc(endTime)

        response = self.get(f'{BASE_URL}/data/reports',
                            headers=self.__headers,
                            params=kwargs)
        reports = []
        if response.ok:
            response, reports = Pages(response).collect_contents(
                Report, kwargs)
        else:
            print(response.json())
        return response, reports

    def __convert_to_utc(self, dateString: str) -> str:
        # [NTF] get system to utc delta and convert
        deltanow = datetime.now() - datetime.utcnow()
        data_time = datetime.strptime(dateString, "%Y-%m-%d %H:%M:%S")
        utc_time = data_time - deltanow
        return utc_time.strftime("%Y-%m-%d %H:%M:%S")

    def check_reports(self, **kwarg):
        #latitude and longtitude != null
        #radioud >1
        ...

    def get_devices_events(self):
        ...

    #endregion

    #region Models
    def get_models(self):
        response = self.get(f'{BASE_URL}/models', headers=self.__headers)

    #endregion

    #region Template Config
    def get_template(self, id=None, name=None, **kwargs):
        template = None
        _locals = locals()
        del _locals['self']
        del _locals['kwargs']
        for k, v in _locals.items():
            if v:
                kwargs[k] = v
        if id:
            response = ThingsMatrixResponse(
                self.get(f'{BASE_URL}/configs/{id}', headers=self.__headers))
            if response.hasData:
                template = Template(response.data)
        elif name:
            response = ThingsMatrixResponse(
                self.get(f'{BASE_URL}/configs/name/{name}',
                         headers=self.__headers))
            if response.hasData:
                template = Template(response.data)
        else:
            ...
        return template

    #endregion

    #region
    def get_location(self):
        ...
        location = self.get()

    #endregion

    def request_get_sender(self, url, params, collect):
        ...
        self.request = Request(url=url, params=params, headers=self.__headers)

    #TODO Get Model, Group, heartbeat's setting, Location Mode (Optional)

    def test_requests(self):
        response = self.get(f'{BASE_URL}/inventory/companies/HP')
