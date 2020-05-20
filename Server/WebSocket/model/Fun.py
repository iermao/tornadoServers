import time
import datetime


def get_delta_days(t1, t2):
    dt2 = datetime.datetime.fromtimestamp(t2)
    dt2 = dt2.replace(hour=0, minute=0, second=0, microsecond=0)
    dt1 = datetime.datetime.fromtimestamp(t1)
    dt1 = dt1.replace(hour=0, minute=0, second=0, microsecond=0)
    return (dt2 - dt1).days
