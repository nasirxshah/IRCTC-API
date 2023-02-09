from dataclasses import dataclass, field

# -------------------------------------------------------


@dataclass(slots=True)
class AvailableEnquiryModel:
    srcStn: str = field(init=False)
    destStn: str = field(init=False)
    jrnyDate: str = field(init=False)
    quotaCode: str = field(init=False)

    jrnyClass: str = ""
    concessionBooking: bool = False
    currentBooking: str = 'false'
    flexiFlag: bool = False
    handicapFlag: bool = False
    ticketType: str = "E"
    loyaltyRedemptionBooking: bool = False
    ftBooking: bool = False

# ---------------------------------------------------------


@dataclass(slots=True)
class FareEnquiryModel:
    quotaCode: str = field(init=False)
    trainNumber: str = field(init=False)
    fromStnCode: str = field(init=False)
    toStnCode: str = field(init=False)
    journeyDate: str = field(init=False)
    classCode: str = field(init=False)

    paymentFlag: str = "N"
    concessionBooking: bool = False
    ftBooking: bool = False
    loyaltyRedemptionBooking: bool = False
    ticketType: str = "E"
    moreThanOneDay: bool = True
    isLogedinReq: bool = True

# -------------------------------------------------------------


@dataclass(slots=True)
class AltDTO:
    trainNo: str = field(init=False)
    destStn: str = field(init=False)
    srcStn: str = field(init=False)
    jrnyDate: str = field(init=False)
    quotaCode: str = field(init=False)
    jrnyClass: str = field(init=False)


@dataclass(slots=True)
class BoardingEnquiryModel:
    paymentType: int = field(init=False)
    alternateAvlInputDTO: list[AltDTO] = field(default_factory=list)

    reservationMode: str = "WS_TA_B2C"
    clusterFlag: str = "N"
    onwardFlag: str = "N"
    cod: str = "false"
    autoUpgradationSelected: bool = False
    gnToCkOpted: bool = False
    twoPhaseAuthRequired: bool = False
    captureAddress: int = 0
    passBooking: bool = False
    journalistBooking: bool = False


# --------------------------------------------------------------
@dataclass(slots=True)
class PassengerModel:
    passengerName: str = field(init=False)
    passengerAge: int = field(init=False)
    passengerGender: str = field(init=False)
    passengerSerialNumber: int = field(init=False)

    passengerBerthChoice: str = ""
    passengerFoodChoice: None = None
    passengerBedrollChoice: None = None
    passengerNationality: str = "IN"
    passengerCardTypeMaster: None = None
    passengerCardNumberMaster: None = None
    psgnConcType: None = None
    psgnConcCardId: None = None
    psgnConcDOB: None = None
    psgnConcCardExpiryDate: None = None
    psgnConcDOBP: None = None
    softMemberId: None = None
    softMemberFlag: None = None
    psgnConcCardExpiryDateP: None = None
    passengerVerified: bool = False
    masterPsgnId: None = None
    mpMemberFlag: None = None
    passengerForceNumber: None = None
    passConcessionType: str = "0"
    passUPN: None = None
    passBookingCode: None = None
    childBerthFlag: bool = True
    passengerCardType: str = "NULL_IDCARD"
    passengerIcardFlag: bool = False
    passengerCardNumber: None = None


@dataclass(slots=True)
class LapDTO:
    trainNo: str = field(init=False)
    journeyDate: str = field(init=False)
    fromStation: str = field(init=False)
    toStation: str = field(init=False)
    journeyClass: str = field(init=False)
    quota: str = field(init=False)

    passengerList: list[PassengerModel] = field(default_factory=list)

    coachId: None = None
    reservationChoice: str = "99"
    ignoreChoiceIfWl: bool = True
    travelInsuranceOpted: bool = False
    warrentType: int = 0
    coachPreferred: bool = False
    autoUpgradation: bool = False
    bookOnlyIfCnf: bool = False
    addMealInput: None = None
    concessionBooking: bool = False
    ssQuotaSplitCoach: str = "N"


def getGst():
    return {
        "gstIn": "",
        "error": None
    }


@dataclass(slots=True)
class LapFareEnquiryModel:
    mobileNumber: str = field(init=False)
    reservationUptoStation: str = field(init=False)
    boardingStation: str = field(init=False)
    clientTransactionId: str = field(init=False)
    wsUserLogin: str = field(init=False)
    paymentType: str = field(init=False)
    lapAvlRequestDTO: list[LapDTO] = field(default_factory=list)

    reservationMode: str = "WS_TA_B2C"
    clusterFlag: str = "N"
    onwardFlag: str = "N"
    cod: str = "false"
    autoUpgradationSelected: bool = False
    gnToCkOpted: bool = False
    twoPhaseAuthRequired: bool = False
    captureAddress: int = 0
    moreThanOneDay: bool = False
    ticketType: str = "E"
    mainJourneyTxnId: None = None
    mainJourneyPnr: str = ""
    captcha: str = ""
    generalistChildConfirm: bool = False
    ftBooking: bool = False
    loyaltyRedemptionBooking: bool = False
    nosbBooking: bool = False
    warrentType: int = 0
    ftTnCAgree: bool = False
    bookingChoice: int = 1
    bookingConfirmChoice: int = 1
    bookOnlyIfCnf: bool = False
    returnJourney: None = None
    connectingJourney: bool = False
    gstDetails: dict = field(default_factory=getGst)


if __name__ == "__main__":
    from dataclasses import asdict
    import json
    model = AvailableEnquiryModel()
    print(json.dumps(asdict(model), indent=4))
