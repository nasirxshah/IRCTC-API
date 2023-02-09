from dataclasses import dataclass, field


@dataclass(slots=True)
class WebTokenModel:
    username: str = field(init=False)
    password: str = field(init=False)
    captcha: str = field(init=False)
    uid: str = field(init=False)
    
    grant_type: str = "password"
    otpLogin: bool = False
    nlpIdentifier: str = ""
    nlpAnswer: str = ""
    nlpToken: str = ""
    lso: str = ""
    encodedPwd: bool = True
