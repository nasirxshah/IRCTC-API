from irctc.models import *
from irctc.engine.request import RequestHandler
from dataclasses import asdict
from irctc.utils import base36, getTimestamp


class BookingAPI:
    __slots__ = ['handler']

    def __init__(self, bearerToken, csrfToken, uid) -> None:
        self.handler = RequestHandler(bearerToken, csrfToken, uid)

    def getAvailableTrain(self, srcStn, destStn, jrnyDate, quotaCode) -> dict:
        model = AvailableEnquiryModel()
        model.srcStn = srcStn
        model.destStn = destStn
        model.jrnyDate = jrnyDate
        model.quotaCode = quotaCode

        return self.handler.request("train.avlenq", json=asdict(model))

    def getAvailableSeats(self, srcStn, destStn, jrnyDate, trainNumber, quotaCode, classCode) -> dict:
        model = FareEnquiryModel()
        model.fromStnCode = srcStn
        model.toStnCode = destStn
        model.journeyDate = jrnyDate
        model.trainNumber = trainNumber
        model.quotaCode = quotaCode
        model.classCode = classCode

        args = {
            "trainNumber": trainNumber,
            "journeyDate": jrnyDate,
            "fromStnCode": srcStn,
            "toStnCode": destStn,
            "classCode": classCode,
            "quotaCode": quotaCode
        }

        return self.handler.request("booking.fareenq", urlargs=args, json=asdict(model))

    def getBoardingStations(self, srcStn, destStn, jrnyDate, trainNumber, quotaCode, classCode, paymentType) -> dict:
        model = BoardingEnquiryModel()
        model.paymentType = paymentType
        dto = AltDTO()
        dto.srcStn = srcStn
        dto.destStn = destStn
        dto.jrnyDate = jrnyDate
        dto.trainNo = trainNumber
        dto.quotaCode = quotaCode
        dto.jrnyClass = classCode
        model.alternateAvlInputDTO.append(dto)

        return self.handler.request("booking.boardingenq", json=asdict(model))

    def getLapFare(self, srcStn, destStn, jrnyDate, trainNumber, quotaCode, classCode, paymentType, username, mobile, passengers: list[list]) -> dict:
        model = LapFareEnquiryModel()
        model.boardingStation = srcStn
        model.reservationUptoStation = destStn
        model.paymentType = paymentType
        model.wsUserLogin = username
        model.mobileNumber = mobile
        model.clientTransactionId = base36(getTimestamp())
        dto = LapDTO()
        dto.trainNo = trainNumber
        dto.fromStation = srcStn
        dto.toStation = destStn
        dto.quota = quotaCode
        dto.journeyClass = classCode
        dto.journeyDate = jrnyDate

        for id, passenger in enumerate(passengers, start=1):
            psgrmodel = PassengerModel()
            psgrmodel.passengerName = passenger[0]
            psgrmodel.passengerAge = passenger[1]
            psgrmodel.passengerGender = passenger[2]
            psgrmodel.passengerSerialNumber = id
            dto.passengerList.append(psgrmodel)

        model.lapAvlRequestDTO.append(dto)

        return self.handler.request("booking.lapfareenq", json=asdict(model))
