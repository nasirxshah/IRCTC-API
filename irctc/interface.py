import base64
from io import BytesIO

from PIL import Image

from irctc.api import BookingAPI
from irctc.login.api import InvalidCaptchaError, LoginAPI
from irctc.ocr import OCR
import pickle
import logging


logger = logging.getLogger("irctc")


class IRCTC:
    def __init__(self, username: str) -> None:
        self.username = username

    def loadSession(self, path):
        with open(path, 'rb') as f:
            state = pickle.load(f)

        self.bookingApi = BookingAPI(
            state.bearertoken, state.csrftoken, state.uid)
        logger.debug(f"'{path}' previous session loaded")

    def dumpSession(self, path):
        if self.bookingApi:
            with open(path, "wb") as f:
                pickle.dump(self.bookingApi.handler.state, f)

        logger.debug(f"'{path}' session dumped")

    def login(self, password: str):
        rcontent = LoginAPI.getLoginCaptcha()
        captchaQuestion = rcontent['captchaQuestion']
        uid = rcontent['status']
        logger.debug(f"retrieved login captcha {captchaQuestion}")

        image = Image.open(BytesIO(base64.b64decode(captchaQuestion)))
        ocr = OCR(image)
        captcha = ocr.getText()
        logger.debug(f"ocr output - {captcha}")

        rcontent = LoginAPI.getWebToken(self.username, password, uid, captcha)
        bearerToken = rcontent.get('access_token')

        if bearerToken is None:
            raise InvalidCaptchaError()
        logger.debug(f'webtoken generated {rcontent}')

        rcontent = LoginAPI.validateUser(bearerToken, uid)
        self.bookingApi = BookingAPI(
            rcontent['access_token'], rcontent['csrf_token'], rcontent['uid'])

    def addJourney(self, srcStn, destStn, jrnyDate, quotaCode, classCode, trainNumber, mobile):
        self.srcStn = srcStn
        self.destStn = destStn
        self.jrnyDate = jrnyDate
        self.quotaCode = quotaCode
        self.classCode = classCode
        self.trainNumber = trainNumber
        self.mobile = mobile
        self.passengers = []

    def addPassenger(self, name, age, gender):
        if self.passengers:
            passenger = [name, age, gender]
            self.passengers.append(passenger)

    def bookTicket(self):
        self.bookingApi.getAvailableSeats(self.srcStn, self.destStn, self.jrnyDate,
                                          self.trainNumber, self.quotaCode, self.classCode)
        logger.debug("seat availablity enquiry done")
        self.bookingApi.getBoardingStations(self.srcStn, self.destStn, self.jrnyDate,
                                            self.trainNumber, self.quotaCode, self.classCode, 1)
        logger.debug("boarding station enquiry done")
        rcontent = self.bookingApi.getLapFare(self.srcStn, self.destStn, self.jrnyDate, self.trainNumber,
                                              self.quotaCode, self.classCode, "2", self.username, self.mobile, self.passengers)
        logger.debug("lap fare enquiry done")

        return rcontent

    def pay(self):
        pass
