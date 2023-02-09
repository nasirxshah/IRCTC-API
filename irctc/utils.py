import datetime as dt


def base36(n: int) -> str:
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    r = ""
    if n == 0:
        return "0"
    while n > 0:
        r = digits[n % 36] + r
        n = n // 36
    return r


def getTimestamp() -> int:
    return round(dt.datetime.now().timestamp() * 1000)
