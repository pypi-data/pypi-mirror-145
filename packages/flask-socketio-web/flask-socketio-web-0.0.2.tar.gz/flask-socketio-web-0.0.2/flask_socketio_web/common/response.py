import datetime
import decimal
import json
from enum import Enum


class State(Enum):
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


def success(data=None, state=State.SUCCESS.value, msg="ok"):
    return {"state": state, "data": json.dumps(data, cls=__JsonEncoder, default=str), "msg": msg}


def error(msg="error", state=State.ERROR.value, data=None):
    return {"state": state, "data": json.dumps(data, cls=__JsonEncoder, default=str), "msg": msg}


def warn(state=State.WARNING.value, data=None, msg="warn"):
    return {"state": state, "data": json.dumps(data, cls=__JsonEncoder, default=str), "msg": msg}


class __JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        super().default(o)
