import requests
import datetime


class YaSchedule:

    base_url = 'https://api.rasp.yandex.net/v3.0/'

    def __init__(self, token: str, lang='ru_RU') -> None:
        """
        :param token: str
        :param lang: str lang codes info - https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
        """
        self.__token = token
        self.__lang = lang

    def __get_payload(self, **kwargs) -> dict:
        """
        Returns payload dict for requests
        :param kwargs:
        :return:
        """
        payload = {'apikey': self.__token,
                   'lang': self.__lang}
        for key, value in kwargs.items():
            if value is not None:
                key = key.replace('_', '', 1) if key.find('_', 0, 1) == 0 else key
                payload[key] = value
        return payload

    def __get_response(self, api_method_url: str, payload: dict) -> dict:
        request_url = f'{self.base_url}{api_method_url}/'
        response = requests.get(request_url, payload)
        return response.json()

    def get_all_stations(self, **kwargs) -> dict:
        """
        Returns all available stations of api
        API_INFO: https://yandex.ru/dev/rasp/doc/reference/stations-list.html
        :param kwargs: u can redefine any api_method values
        :return:
        """
        api_method_url = "stations_list"
        payload = self.__get_payload(**kwargs)
        return self.__get_response(api_method_url, payload)

    def get_schedule(self, from_station: str, to_station: str,
                     date: datetime.date = None, **kwargs) -> dict:
        """
        Get all flights from <city, station> to <city, station>.
        API_INFO: https://yandex.ru/dev/rasp/doc/reference/schedule-point-point.html
        :param from_station: station codes in yandex_code notations.
        :param to_station: station codes in yandex_code notations.
        :param date:
        :param kwargs: u can redefine any api_method values. For example, transport_type=<'train','plane'>.
        transport_type = plane by default.
        :return: dict of data
        """
        api_method_url = "search"
        payload = self.__get_payload(
            _from=from_station,
            _to=to_station,
            _date=date,
            **kwargs
        )
        return self.__get_response(api_method_url, payload)
