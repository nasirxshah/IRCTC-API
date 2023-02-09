from dataclasses import dataclass, field
import requests
from urllib.parse import urljoin
from threading import Lock


@dataclass(slots=True)
class State:
    csrftoken: str = field(init=False)
    bearertoken: str = field(init=False)
    uid: str = field(init=False)


class RequestHandler:
    BASE_URI = "https://www.irctc.co.in"
    _routes = {
        "train.avlenq": "/eticketing/protected/mapps1/altAvlEnq/TC",
        "booking.fareenq": "/eticketing/protected/mapps1/avlFarenquiry/{trainNumber}/{journeyDate}/{fromStnCode}/{toStnCode}/{classCode}/{quotaCode}/N",
        "booking.boardingenq": "/eticketing/protected/mapps1/boardingStationEnq",
        "booking.lapfareenq": "/eticketing/protected/mapps1/allLapAvlFareEnq/Y",
        "booking.otp.resend": "/eticketing/protected/mapps1/resendOTP/BOOKING",
        "booking.otp.confirm": "/eticketing/protected/mapps1/captchaverify/{txnid}/BOOKINGWS/{otp}",
        "booking.captcha.confirm": "/eticketing/protected/mapps1/nlpcaptchaverify/{txnid}/BOOKINGWS/{nlpanswer}",
        "booking.captcha.exception.confirm": "/eticketing/protected/mapps1/nlpcaptchaverify/{txnid}/BOOKINGWS/{nlpAnswer}",
        "payment.init": "eticketing/protected/mapps1/bookingInitPayment/{txnid}",
        "payment.ewallet.confirm": "eticketing/protected/mapps1/verifyPayment/{txnid}",
        "payment.ewallet.otp.resend": "/eticketing/protected/mapps1/resendPaymentOtp/{txnid}",
        "payment.redirect": "/eticketing/PaymentRedirect"
    }

    __slots__ = ['state', 'reqSession', "lock"]

    def __init__(self, bearerToken, csrfToken, uid) -> None:
        self.reqSession = requests.Session()
        self.state = State()
        self.state.bearertoken = bearerToken
        self.state.csrftoken = csrfToken
        self.state.uid = uid
        self.lock = Lock()

    def url_from_route(self, route: str, urlargs: dict | None):
        if urlargs:
            return urljoin(self.BASE_URI, self._routes[route]).format(**urlargs)
        return urljoin(self.BASE_URI, self._routes[route])

    def request(self, route: str, urlargs: dict | None = None, json: dict | None = None, data: dict | None = None):
        headers = {
            "Authorization": f"Bearer {self.state.bearertoken}",
            "spa-csrf-token": self.state.csrftoken,
            "greq": self.state.uid,
            "bmirak": "webbm",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        url = self.url_from_route(route, urlargs)

        resp = self.reqSession.post(url, json=json, data=data, headers=headers)
        if resp.status_code == 200:
            self.state.csrftoken = resp.headers['csrf-token']
            return resp.json()

        if resp.json().get("error") == "invalid_token":
            raise InvalidAccessTokenError()

        if resp.headers.get('csrf-token') == "MISMATCH":
            raise MismatchedCsrfTokenError()
        raise requests.ConnectionError()


class InvalidAccessTokenError(Exception):
    pass


class MismatchedCsrfTokenError(Exception):
    pass
