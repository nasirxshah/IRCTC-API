import base64
from dataclasses import asdict
from urllib.parse import urljoin

import requests

from irctc.login.model import WebTokenModel
from irctc.utils import getTimestamp


class RequestHandler:
    BASE_URL = "https://www.irctc.co.in"
    _routes = {
        "login.captcha": "eticketing/protected/mapps1/loginCaptcha",
        "login.webtoken": "authprovider/webtoken",
        "login.validate.user": "eticketing/protected/mapps1/validateUser"
    }
    __slots__ = ['reqSession']

    def __init__(self) -> None:
        self.reqSession: requests.Session = requests.Session()

    def url_from_route(self, route: str):
        return urljoin(self.BASE_URL, self._routes[route])

    def request(self, route, data: dict | None = None, json: dict | None = None, params: dict | None = None, headers: dict | None = None):
        url = self.url_from_route(route)

        resp = self.reqSession.post(
            url, json=json, data=data, headers=headers) if json or data else self.reqSession.get(url, params=params, headers=headers)
        if resp.status_code == 200:
            return resp

        raise requests.ConnectionError()


class LoginAPI:
    __slots__ = []
    handler = RequestHandler()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

    @classmethod
    def getLoginCaptcha(cls):
        headers = {
            "greq": str(getTimestamp()),
            "bmirak": "webbm",
            "User-Agent": cls.user_agent
        }
        resp = cls.handler.request("login.captcha", headers=headers)
        return resp.json()

    @classmethod
    def getWebToken(cls, username: str, password: str, uid: str, captcha: str):
        headers = {
            "bmirak": "webbm",
            "User-Agent": cls.user_agent
        }
        model = WebTokenModel()
        model.username = username
        model.password = base64.b64encode(password.encode()).decode()
        model.uid = uid
        model.captcha = captcha

        resp = cls.handler.request(
            "login.webtoken", data=asdict(model), headers=headers)
        return resp.json()

    @classmethod
    def validateUser(cls, bearerToken, uid):
        headers = {
            "Authorization": f"Bearer {bearerToken}",
            "spa-csrf-token": str(getTimestamp()),
            "greq": uid,
            "bmirak": "webbm",
            "User-Agent": cls.user_agent
        }
        resp = cls.handler.request("login.validate.user", headers=headers)

        return {
            "access_token": bearerToken,
            "uid": uid,
            "csrf_token": resp.headers['csrf-token']
        }


class InvalidCaptchaError(Exception):
    pass
