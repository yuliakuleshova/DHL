""" Converting date and time"""

import pytz
import time
from datetime import datetime, timezone, timedelta


def convert_to_unixtime(datatime: str):
    """
    :param datatime: input string with data and time
    :return: unix timestamp
    """
    mnth = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Sep': 9}
    dt = datatime.split(" ")
    tm = dt[4].split(":")
    tz1 = pytz.timezone('Europe/Moscow')
    tz2 = pytz.timezone('UTC')
    new_dt = datetime(int(dt[3]), int(mnth[dt[2]]), int(dt[1]), int(tm[0]), int(tm[1]), int(tm[2]))
    dt = tz1.localize(new_dt)
    print(dt, dt.astimezone(tz2))
    return time.mktime(dt.astimezone(tz2).timetuple())

#dt.astimezone(tz2)

dt = "Sat, 30 Sep 2023 07:39:52 +0300"

print(convert_to_unixtime(dt))

#Two ways to get user's time zone:

tz_string = datetime.now().astimezone().tzname()
print(tz_string)

tz_string2 = datetime.now().astimezone().tzinfo
print(tz_string2)

# print(dt)
# mnth = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Sep': 9}
# tm = dt[4].split(":")
# print(dt[3], mnth[dt[2]], dt[1], tm[0], tm[1], tm[2])
#
# new_dt = datetime(int(dt[3]), int(mnth[dt[2]]), int(dt[1]), int(tm[0]), int(tm[1]), int(tm[2]))
# # unix_timestamp = time.mktime(new_dt.timetuple())
# # utc_timestamp = time.mktime(new_dt.utctimetuple())
# # print(unix_timestamp)
# # print(utc_timestamp)
#
# naive = datetime.now()
# print("Naive DateTime:", naive)
# UTC = datetime.now(timezone.utc)
# print("UTC DateTime", UTC)
# #msk_dateTime = datetime.now(timezone(timedelta(hours=+3), 'MCK'))
# tz = list(dt[5])
# print(tz)
# tz1 = ''.join(tz[0:3])
# print(tz1)
# msk_dateTime = datetime.now(timezone(timedelta(hours=int(tz1)), 'MCK'))
# print("In MSK::", msk_dateTime)